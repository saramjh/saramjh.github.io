# frozen_string_literal: true
require 'nokogiri'
require 'pathname'

root = Pathname.new(ARGV.fetch(0, '_site')).expand_path
portfolio = root.join('portfolio')
abort 'Portfolio index missing' unless portfolio.join('index.html').file?
files = portfolio.glob('**/index.html')
abort "Portfolio case-study coverage missing (#{files.size})" unless files.size >= 7

errors = []
files.each do |path|
  doc = Nokogiri::HTML(path.read)
  errors << "#{path}: loaded AdSense" if doc.at_css('script[src*="pagead2.googlesyndication.com"], meta[name="google-adsense-account"], ins.adsbygoogle')
  errors << "#{path}: unexpected privacy-choices link" if doc.at_css('#privacy-choices')
  errors << "#{path}: missing independent portfolio style" unless doc.at_css('link[href="/assets/css/portfolio.css"]')
  errors << "#{path}: expected one H1" unless doc.css('main h1').size == 1
end

# Milestone *blog posts* remain monetized. Only the /portfolio/ namespace is ad-free.
%w[koreaves-published-contributions-en koreaves-external-resources-ko].each do |slug|
  path = root.join(slug, 'index.html')
  doc = Nokogiri::HTML(path.read)
  errors << "#{path}: blog advertising unexpectedly disabled" unless doc.at_css('script[src*="pagead2.googlesyndication.com"], meta[name="google-adsense-account"]')
end

unless errors.empty?
  warn errors.join("\n")
  exit 1
end
puts "Portfolio contract passed: #{files.size} ad-free pages; regular milestone article ads retained."
