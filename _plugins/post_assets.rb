# Keep source assets beside their post. Publish them beside the rendered HTML,
# and optionally at an explicitly recorded legacy URL for old external links.
module Blog
  class PostAsset < Jekyll::StaticFile
    def initialize(site, source, url)
      super(site, site.source, '', File.basename(source))
      @asset_source = source
      @asset_url = url
    end

    def path
      @asset_source
    end

    def destination(dest)
      File.join(dest, @asset_url.delete_prefix('/'))
    end

    def url
      @asset_url
    end
  end

  class PostAssets < Jekyll::Generator
    priority :low

    def generate(site)
      occupied = (site.pages + site.posts.docs + site.static_files).to_h do |item|
        [File.expand_path(item.destination(site.dest)), item.path]
      end
      site.posts.docs.group_by { |post| File.dirname(post.path) }.each do |directory, posts|
        next if directory == File.join(site.source, '_posts')
        if posts.size != 1
          raise Jekyll::Errors::FatalException, "Keep one post per folder: #{directory}"
        end
        post = posts.first
        unless post.url.end_with?('/')
          raise Jekyll::Errors::FatalException, "Post permalink must end with /: #{post.path}"
        end
        bases = [post.url, post.data['legacy_asset_url']].compact.uniq
        bases.each do |base|
          unless base.start_with?('/') && base.end_with?('/') && !base.split('/').include?('..')
            raise Jekyll::Errors::FatalException, "Invalid asset URL: #{base}"
          end
        end
        Dir.glob(File.join(directory, '**', '*')).sort.each do |source|
          next unless File.file?(source)
          next if source == post.path
          next if source.delete_prefix(directory + '/').split('/').any? { |part| part.start_with?('.', '_') }
          next if %w[.md .markdown].include?(File.extname(source).downcase)
          relative = source.delete_prefix(directory + '/')
          bases.each do |base|
            asset = PostAsset.new(site, source, base + relative)
            target = File.expand_path(asset.destination(site.dest))
            if occupied.key?(target)
              raise Jekyll::Errors::FatalException, "Asset output collision: #{target}"
            end
            occupied[target] = source
            site.static_files << asset
          end
        end
      end
    end
  end
end
