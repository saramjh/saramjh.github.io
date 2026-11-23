require 'date'
require 'fileutils'
require 'json'
require 'open3'
require 'yaml'

args = ARGV.dup
source_url = nil
if args.first == '--achievement-source'
  source_url = args[1]
  abort 'Usage: ruby scripts/new_post.rb --achievement-source URL ascii-slug "글 제목"' if source_url.nil? || source_url.empty?
  args = args.drop(2)
end
slug, title = args
abort 'Usage: ruby scripts/new_post.rb [--achievement-source URL] ascii-slug "글 제목"' unless args.length == 2 && slug && title
abort 'Slug must use lowercase letters, numbers and hyphens.' unless slug.match?(/\A[a-z0-9]+(?:-[a-z0-9]+)*\z/)
root = File.expand_path('..', __dir__)
directory = File.join(root, '_posts', slug)
abort "Already exists: #{directory}" if File.exist?(directory)

if source_url
  script = File.join(__dir__, 'check_achievement_source_coverage.py')
  stdout, stderr, status = Open3.capture3(
    'python3', script, '--posts-root', File.join(root, '_posts'),
    '--recognitions-file', File.join(root, '_data', 'recognitions.yml'), '--source-url', source_url
  )
  case status.exitstatus
  when 3
    report = JSON.parse(stdout)
    matches = report.fetch('sources').flat_map do |source|
      source.fetch('matches').map { |match| match['permalink'] || match['postPath'] } +
        source.fetch('ledgerMatches').map { |record| "evidence:#{record['recordId']} (#{record['recordType']})" }
    end
    abort "Existing source coverage requires editorial review before another story: #{matches.uniq.join(', ')}"
  when 0
    warn 'No exact source URL in original posts or evidence ledger. Manual source, rights and editorial review is still required.'
  else
    abort "Source coverage check unavailable; no post created: #{stderr.strip[0, 180]}"
  end
end

date = Time.now.getlocal('+09:00').strftime('%Y-%m-%d')
FileUtils.mkdir_p(directory)
metadata = { 'title' => title, 'date' => date, 'permalink' => "/#{slug}/", 'layout' => 'default', 'lang' => 'ko', 'tags' => [], 'description' => '' }
path = File.join(directory, "#{date}-#{slug}.md")
File.write(path, metadata.to_yaml + "---\n\n# #{title}\n\n")
puts path
