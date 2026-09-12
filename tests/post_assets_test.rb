require 'jekyll'
require 'tmpdir'
require 'fileutils'
require_relative '../_plugins/post_assets'

def assert(value, message)
  raise message unless value
end

Dir.mktmpdir('blog-assets-test') do |root|
  source = File.join(root, 'source')
  destination = File.join(root, 'output')
  folder = File.join(source, '_posts', 'example')
  FileUtils.mkdir_p(File.join(folder, 'nested'))
  post = File.join(folder, '2024-01-01-example.md')
  File.write(post, "---\ntitle: Example\npermalink: /renamed/\nlegacy_asset_url: /posts/original/\n---\n![Example](nested/image%20one.png)\n")
  File.binwrite(File.join(folder, 'nested', 'image one.png'), 'image bytes')
  File.write(File.join(folder, '.private'), 'must not publish')
  config = Jekyll.configuration('source' => source, 'destination' => destination, 'quiet' => true)
  site = Jekyll::Site.new(config)
  site.process
  %w[renamed posts/original].each do |prefix|
    assert(File.binread(File.join(destination, prefix, 'nested', 'image one.png')) == 'image bytes', 'Asset bytes changed')
    assert(!File.exist?(File.join(destination, prefix, '.private')), 'Hidden file published')
  end
  assert(File.read(File.join(destination, 'renamed', 'index.html')).include?('nested/image%20one.png'), 'Relative image reference changed')
  File.write(File.join(folder, 'index.html'), 'collision')
  begin
    Jekyll::Site.new(config).process
    raise 'Output collision was not rejected'
  rescue Jekyll::Errors::FatalException => error
    assert(error.message.include?('collision'), 'Unexpected build failure')
  end
end
puts 'Post assets: relative URLs, nested paths, spaces, legacy aliases, hidden files and collisions passed.'
