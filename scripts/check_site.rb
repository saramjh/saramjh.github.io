require 'nokogiri'
require 'uri'
require 'pathname'
require 'yaml'
require 'date'
require 'digest'

root = Pathname.new(ARGV.fetch(0, '_site')).expand_path
abort "Build directory missing: #{root}" unless root.directory?
errors = []
count = 0

home = root.join('index.html')
if home.file?
  home_doc = Nokogiri::HTML(home.read)
  stylesheet = home_doc.at_css('link[rel="stylesheet"][href*="/assets/css/style.css"]')
  errors << 'Primary stylesheet link missing' unless stylesheet
  errors << 'Primary stylesheet uses a build-time cache-busting query' if stylesheet&.[]('href').to_s.include?('?')
else
  errors << 'index.html missing'
end

robots = root.join('robots.txt')
if robots.file?
  robots_text = robots.read
  expected_sitemaps = %w[
    https://saramjh.github.io/sitemap.xml
    https://saramjh.github.io/space_atlas_student/sitemap.xml
    https://saramjh.github.io/richChecker/sitemap.xml
    https://saramjh.github.io/richChecker-us/sitemap.xml
    https://saramjh.github.io/scratchLottery/sitemap.xml
  ]
  expected_sitemaps.each do |url|
    errors << "robots.txt missing sitemap: #{url}" unless robots_text.include?("Sitemap: #{url}")
  end
else
  errors << 'robots.txt missing'
end

%w[AGENTS.md CLAUDE.md].each do |local_only|
  errors << "Local-only artifact leaked into build: #{local_only}" if root.join(local_only).exist?
end
%w[.context .serena].each do |local_only|
  errors << "Local-only directory leaked into build: #{local_only}" if root.join(local_only).exist?
end

root.glob('**/*.html').each do |file|
  page_url = '/' + file.relative_path_from(root).to_s
  doc = Nokogiri::HTML(file.read)
  doc.css('a[href]').each do |node|
    href = node['href'].to_s
    if href.start_with?('/http://', '/https://')
      errors << "#{page_url}: malformed absolute link #{href}"
    end
  end
  ids = Hash.new(0)
  doc.css('[id]').each do |node|
    id = node['id'].to_s
    ids[id] += 1 unless id.empty?
  end
  ids.each do |id, occurrences|
    errors << "#{page_url}: duplicate id #{id} (#{occurrences} occurrences)" if occurrences > 1
  end
  doc.css('img[src], meta[property="og:image"], meta[name="twitter:image"]').each do |node|
    src = node['src'] || node['content']
    next if src.nil? || src.empty? || src.start_with?('data:')
    begin
      url = URI.join("https://saramjh.github.io#{page_url}", src.gsub(' ', '%20'))
      next unless url.host == 'saramjh.github.io'
      count += 1
      path = root.join(URI::DEFAULT_PARSER.unescape(url.path).delete_prefix('/')).cleanpath
      errors << "#{page_url}: missing image #{src}" unless path.to_s.start_with?(root.to_s + '/') && path.file?
    rescue URI::InvalidURIError
      errors << "#{page_url}: invalid image URL #{src}"
    end
  end
  doc.css('img[srcset], source[srcset]').each do |node|
    node['srcset'].to_s.split(',').each do |candidate|
      src = candidate.strip.split(/\s+/, 2).first
      next if src.nil? || src.empty? || src.start_with?('data:')
      begin
        url = URI.join("https://saramjh.github.io#{page_url}", src.gsub(' ', '%20'))
        next unless url.host == 'saramjh.github.io'
        count += 1
        path = root.join(URI::DEFAULT_PARSER.unescape(url.path).delete_prefix('/')).cleanpath
        errors << "#{page_url}: missing srcset image #{src}" unless path.to_s.start_with?(root.to_s + '/') && path.file?
      rescue URI::InvalidURIError
        errors << "#{page_url}: invalid srcset image URL #{src}"
      end
    end
  end
end
sitemap = root.join('sitemap.xml')
errors << 'sitemap.xml missing' unless sitemap.file?
if sitemap.file?
  xml = Nokogiri::XML(sitemap.read)
  errors.concat(xml.errors.map(&:message))
  locations = xml.xpath('//*[local-name()="loc"]').map(&:text)
  source_root = Pathname.new(File.expand_path('..', __dir__))
  source_root.glob('_posts/**/*.md').each do |post|
    metadata = YAML.safe_load(post.read.split(/^---[ \t]*$/, 3)[1], permitted_classes: [Date, Time])
    next if metadata['published'] == false || Date.parse(metadata['date'].to_s) > Time.now.getlocal('+09:00').to_date
    permalink = metadata.fetch('permalink')
    sitemap_url = "https://saramjh.github.io#{permalink}"
    if metadata['sitemap'] == false
      errors << "Excluded post leaked into sitemap: #{permalink}" if locations.include?(sitemap_url)
    else
      errors << "Missing post in sitemap: #{permalink}" unless locations.include?(sitemap_url)
    end

    redirect_target = metadata['redirect_to']
    if redirect_target
      output = permalink.end_with?('/') ? root.join(permalink.delete_prefix('/'), 'index.html') : root.join(permalink.delete_prefix('/'))
      if output.file?
        redirect_doc = Nokogiri::HTML(output.read)
        canonical = redirect_doc.at_css('link[rel="canonical"]')&.[]('href')
        robots = redirect_doc.at_css('meta[name="robots"]')&.[]('content').to_s.downcase
        refresh = redirect_doc.at_css('meta[http-equiv="refresh"]')&.[]('content').to_s
        errors << "Redirect canonical mismatch: #{permalink}" unless canonical == redirect_target
        errors << "Redirect must be noindex: #{permalink}" unless robots.include?('noindex')
        errors << "Redirect refresh target mismatch: #{permalink}" unless refresh.include?(redirect_target)
      else
        errors << "Redirect output missing: #{permalink}"
      end
    end

    legacy = metadata['legacy_asset_url']
    next unless legacy
    post.dirname.glob('**/*').select(&:file?).each do |asset|
      next if asset == post || %w[.md .markdown].include?(asset.extname.downcase)
      relative = asset.relative_path_from(post.dirname).to_s
      next if relative.split('/').any? { |part| part.start_with?('.', '_') }
      output = root.join(legacy.delete_prefix('/'), relative)
      unless output.file? && Digest::SHA256.file(asset).hexdigest == Digest::SHA256.file(output).hexdigest
        errors << "Missing or changed legacy asset: #{legacy}#{relative}"
      end
    end
  end
end
abort errors.join("\n") unless errors.empty?
puts "Checked #{count} local image references; sitemap coverage and legacy asset contents verified."
