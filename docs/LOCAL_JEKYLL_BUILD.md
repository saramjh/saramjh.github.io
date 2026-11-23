# Local Jekyll build on macOS

This repository pins Ruby 3.4.6. An RVM-enabled shell can report that its Ruby is missing even when Homebrew has the exact version. The repository script selects the installed Ruby and uses a separate Bundler path.

From the repository root, run these commands:

~~~sh
scripts/build-blog-local.sh doctor
scripts/build-blog-local.sh build
~~~

The first command verifies the Ruby and dependencies. The second generates a production site in a new temporary directory outside the repository and prints its path. Neither changes the global RVM or shell configuration.

When the scoped dependencies are missing, explicitly install the free RubyGems first:

~~~sh
scripts/build-blog-local.sh install
~~~

The default bundle location is ~/.cache/saramjh-jekyll/ruby-3.4.6. You can set BLOG_BUNDLE_PATH to reuse an existing bundle, and BLOG_BUILD_DEST to an unused absolute destination for inspection. This script does not publish; CI and public URL checks remain necessary.
