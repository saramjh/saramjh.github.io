require 'date'
require 'fileutils'
require 'yaml'

slug, title = ARGV
abort 'Usage: ruby scripts/new_post.rb ascii-slug "글 제목"' unless slug && title
abort 'Slug must use lowercase letters, numbers and hyphens.' unless slug.match?(/\A[a-z0-9]+(?:-[a-z0-9]+)*\z/)
root = File.expand_path('..', __dir__)
directory = File.join(root, '_posts', slug)
abort "Already exists: #{directory}" if File.exist?(directory)
date = Time.now.getlocal('+09:00').strftime('%Y-%m-%d')
FileUtils.mkdir_p(directory)
metadata = { 'title' => title, 'date' => date, 'permalink' => "/#{slug}/", 'layout' => 'default', 'lang' => 'ko', 'tags' => [], 'description' => '' }
path = File.join(directory, "#{date}-#{slug}.md")
File.write(path, metadata.to_yaml + "---\n\n# #{title}\n\n")
puts path
