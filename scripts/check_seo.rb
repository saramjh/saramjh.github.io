require 'json'
require 'nokogiri'
require 'pathname'
require 'yaml'
require 'date'
require 'cgi'

site_root = Pathname.new(ARGV.fetch(0, '_site')).expand_path
source_root = Pathname.new(File.expand_path('..', __dir__))
abort "Build directory missing: #{site_root}" unless site_root.directory?

errors = []
posts = {}
strict_heading_since = Date.new(2026, 10, 1)

source_root.glob('_posts/**/*.md').sort.each do |post|
  parts = post.read.split(/^---[ 	]*$/, 3)
  metadata = YAML.safe_load(parts[1].to_s, permitted_classes: [Date, Time], aliases: true) || {}
  permalink = metadata['permalink']
  next unless permalink

  posts[permalink] = metadata
  next if metadata['published'] == false

  errors << "#{post}: explicit lang is required" if metadata['lang'].to_s.strip.empty?

  if metadata.key?('faq') && metadata['faq_schema'] != true
    errors << "#{post}: faq metadata is unused unless faq_schema is true"
  end

  if metadata.key?('tags')
    tags = metadata['tags']
    errors << "#{post}: tags must be a YAML array" unless tags.is_a?(Array)
    if tags.is_a?(Array)
      tags.each do |tag|
        value = tag.to_s
        errors << "#{post}: malformed tag #{value.inspect}" if value.strip.empty? || value != value.strip || value.end_with?(',')
      end
    end
  end
end

posts.each do |permalink, metadata|
  next if metadata['published'] == false

  if (alternate = metadata['alternate_url'])
    target = posts[alternate]
    if target.nil?
      errors << "#{permalink}: alternate target missing: #{alternate}"
    elsif target['alternate_url'] != permalink
      errors << "#{permalink}: alternate target is not reciprocal: #{alternate}"
    end
  end

  output = permalink.end_with?('/') ?
    site_root.join(permalink.delete_prefix('/'), 'index.html') :
    site_root.join(permalink.delete_prefix('/'))

  unless output.file?
    errors << "#{permalink}: rendered page missing"
    next
  end

  doc = Nokogiri::HTML(output.read)

  if metadata['redirect_to']
    next
  end

  expected_canonical = "https://saramjh.github.io#{permalink}"
  canonical = doc.at_css('link[rel="canonical"]')&.[]('href')
  errors << "#{permalink}: canonical mismatch: #{canonical.inspect}" unless canonical == expected_canonical

  description = doc.at_css('meta[name="description"]')&.[]('content').to_s.strip
  errors << "#{permalink}: meta description missing" if description.empty?

  og_image = doc.at_css('meta[property="og:image"]')&.[]('content').to_s.strip
  errors << "#{permalink}: og:image missing" if og_image.empty?

  og_site_name = doc.at_css('meta[property="og:site_name"]')&.[]('content').to_s
  errors << "#{permalink}: og:site_name must equal DevTestudinidae" unless og_site_name == 'DevTestudinidae'

  robots = doc.at_css('meta[name="robots"]')&.[]('content').to_s.downcase
  errors << "#{permalink}: max-image-preview:large missing" unless robots.include?('max-image-preview:large')

  author_link = doc.at_css('link[rel="author"]')&.[]('href')
  errors << "#{permalink}: rel=author must point to /about/" unless author_link == 'https://saramjh.github.io/about/'

  html_lang = doc.at_css('html')&.[]('lang').to_s.split('-').first
  source_lang = metadata['lang'].to_s.split('-').first
  errors << "#{permalink}: rendered lang #{html_lang.inspect} != source #{source_lang.inspect}" unless html_lang == source_lang

  source_tags = Array(metadata['tags'])
  semantic_candidates = posts.select do |target_url, target|
    next false if target_url == permalink || target['published'] == false || target['redirect_to']
    target_lang = target['lang'].to_s.split('-').first
    target_lang == source_lang && !(source_tags & Array(target['tags'])).empty?
  end

  related = doc.css('.related-posts a[href]')
  errors << "#{permalink}: related section missing despite semantic matches" if !semantic_candidates.empty? && related.empty?
  errors << "#{permalink}: unrelated section rendered without semantic matches" if semantic_candidates.empty? && doc.at_css('.related-posts')

  related.each do |link|
    target_url = link['href'].to_s
    target = posts[target_url]
    if target.nil?
      errors << "#{permalink}: related link target is not a published post: #{target_url}"
      next
    end
    target_lang = target['lang'].to_s.split('-').first
    errors << "#{permalink}: related link language mismatch: #{target_url}" unless target_lang == source_lang
    errors << "#{permalink}: related link has no shared tag: #{target_url}" if (source_tags & Array(target['tags'])).empty?
  end

  errors << "#{permalink}: more than 4 related links rendered" if related.length > 4

  headings = doc.css('main h1, main h2, main h3, main h4, main h5, main h6')
  h1_count = headings.count { |heading| heading.name == 'h1' }
  errors << "#{permalink}: expected exactly one H1, found #{h1_count}" unless h1_count == 1

  published_on = Date.parse(metadata['date'].to_s)
  if published_on >= strict_heading_since
    levels = headings.map { |heading| heading.name.delete_prefix('h').to_i }
    levels.each_cons(2) do |current, following|
      if following > current + 1
        errors << "#{permalink}: heading level jumps from H#{current} to H#{following}"
        break
      end
    end
  end

  json_ld = doc.css('script[type="application/ld+json"]').map do |node|
    begin
      JSON.parse(node.text)
    rescue JSON::ParserError => e
      errors << "#{permalink}: invalid JSON-LD: #{e.message}"
      nil
    end
  end.compact

  types = json_ld.flat_map do |obj|
    type = obj['@type']
    type.is_a?(Array) ? type : [type]
  end.compact

  errors << "#{permalink}: BlogPosting JSON-LD missing" unless types.include?('BlogPosting')

  faq_present = types.include?('FAQPage')
  faq_expected = metadata['faq_schema'] == true
  if faq_present != faq_expected
    errors << "#{permalink}: FAQPage schema presence #{faq_present} != faq_schema #{faq_expected}"
  end

  if (blog = json_ld.find { |obj| Array(obj['@type']).include?('BlogPosting') })
    author = blog['author'] || {}
    errors << "#{permalink}: BlogPosting author must link to /about/" unless author['url'] == 'https://saramjh.github.io/about/'
    same_as = Array(author['sameAs'])
    errors << "#{permalink}: BlogPosting author sameAs missing GitHub" unless same_as.include?('https://github.com/saramjh')
  end
end

home = Nokogiri::HTML(site_root.join('index.html').read)
errors << 'Homepage must contain exactly one H1' unless home.css('h1').length == 1
errors << 'Tags page must be linked from primary navigation' unless home.at_css('nav a[href="/tags/"]')

theme_control = home.at_css('#mode')
errors << 'Theme control must be a button' unless theme_control&.name == 'button'
errors << 'Theme control requires an accessible label' if theme_control&.[]('aria-label').to_s.strip.empty?

menu_control = home.at_css('#menu-trigger')
errors << 'Mobile menu control requires an accessible label' if menu_control&.[]('aria-label').to_s.strip.empty?
errors << 'Mobile menu control must reference its navigation target' unless menu_control&.[]('aria-controls') == 'primary-navigation'
errors << 'Mobile navigation target missing' unless home.at_css('#primary-navigation')

tags_file = site_root.join('tags', 'index.html')
if tags_file.file?
  tags_doc = Nokogiri::HTML(tags_file.read)
  tag_ids = tags_doc.css('main h2[id]').map { |node| node['id'].to_s }
  errors << 'Tags page contains duplicate tag IDs' unless tag_ids.uniq.length == tag_ids.length
  tag_ids.each do |id|
    errors << "Tags page has unsafe whitespace in tag ID #{id.inspect}" if id.match?(/[[:space:]]/)
  end

  tags_doc.css('.archive-tags a.tag-item[href^="#"]').each do |link|
    href = link['href'].to_s
    next if href == '#'
    errors << "Tags page has whitespace in tag href #{href.inspect}" if href.match?(/[[:space:]]/)
    fragment = CGI.unescape(href.delete_prefix('#'))
    errors << "Tags page fragment has no matching section: #{href}" unless tag_ids.include?(fragment)
  end
end

{
  'About page' => site_root.join('about', 'index.html'),
  'Archive page' => site_root.join('archive', 'index.html'),
  'Tags page' => site_root.join('tags', 'index.html')
}.each do |label, file|
  if file.file?
    page_doc = Nokogiri::HTML(file.read)
    errors << "#{label} must contain exactly one H1" unless page_doc.css('h1').length == 1
  else
    errors << "#{label} output missing"
  end
end

error_file = site_root.join('404.html')
if error_file.file?
  error_doc = Nokogiri::HTML(error_file.read)
  error_robots = error_doc.at_css('meta[name="robots"]')&.[]('content').to_s.downcase
  errors << '404 page must contain exactly one H1' unless error_doc.css('h1').length == 1
  errors << '404 page must be noindex' unless error_robots.include?('noindex')
  errors << '404 page must not load AdSense' if error_doc.at_css('script[src*="pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]') || error_doc.at_css('meta[name="google-adsense-account"]')

  privacy_path = site_root.join('privacy', 'index.html')
  unless File.exist?(privacy_path)
    errors << 'privacy page is missing'
  else
    privacy_doc = Nokogiri::HTML(File.read(privacy_path))
    errors << 'privacy page must contain exactly one H1' unless privacy_doc.css('h1').length == 1
    errors << 'privacy page must not load AdSense' if privacy_doc.at_css('script[src*="pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]') || privacy_doc.at_css('meta[name="google-adsense-account"]')
    errors << 'privacy page must disclose Google AdSense' unless privacy_doc.text.include?('Google AdSense')
    errors << 'privacy page must disclose Google Analytics' unless privacy_doc.text.include?('Google Analytics')
    errors << 'privacy page must disclose Microsoft Clarity' unless privacy_doc.text.include?('Microsoft Clarity')
    errors << 'privacy page must disclose Disqus' unless privacy_doc.text.include?('Disqus')
  end
else
  errors << '404 page output missing'
end

about_file = site_root.join('about', 'index.html')
if about_file.file?
  about = Nokogiri::HTML(about_file.read)
  begin
    about_types = about.css('script[type="application/ld+json"]').map { |n| JSON.parse(n.text)['@type'] }
    errors << 'About page ProfilePage schema missing' unless about_types.include?('ProfilePage')
  rescue JSON::ParserError => e
    errors << "About page invalid JSON-LD: #{e.message}"
  end
else
  errors << 'About page output missing'
end

header_source = source_root.join('_includes', 'header.html').read
errors << 'Stale Jekyll Klise app metadata returned' if header_source.include?('Jekyll Klise')

abort errors.join("
") unless errors.empty?
puts "SEO contract passed for #{posts.count { |_url, metadata| metadata['published'] != false && !metadata['redirect_to'] }} rendered posts."
