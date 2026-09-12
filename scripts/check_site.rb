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
root.glob('**/*.html').each do |file|
  page_url = '/' + file.relative_path_from(root).to_s
  doc = Nokogiri::HTML(file.read)
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
    errors << "Missing post in sitemap: #{permalink}" unless locations.include?("https://saramjh.github.io#{permalink}")
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
