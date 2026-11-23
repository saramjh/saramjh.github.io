#!/usr/bin/env bash
# Use this repository's pinned Ruby without altering the user's shell or RVM.
set -euo pipefail
repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
pinned="$(tr -d '[:space:]' < "$repo/.ruby-version")"
candidates=()
if [[ -n "${BLOG_RUBY_BIN:-}" ]]; then
  candidates=("$BLOG_RUBY_BIN")
else
  candidates=("/opt/homebrew/opt/ruby/bin/ruby" "/usr/local/opt/ruby/bin/ruby")
  if command -v ruby >/dev/null 2>&1; then candidates+=("$(command -v ruby)"); fi
fi
selected=""
for candidate in "${candidates[@]}"; do
  [[ -x "$candidate" ]] || continue
  version="$("$candidate" -e 'print RUBY_VERSION' 2>/dev/null || true)"
  if [[ "$version" == "$pinned" ]]; then selected="$candidate"; break; fi
done
if [[ -z "$selected" ]]; then
  printf 'Required Ruby %s unavailable; no installation attempted.
' "$pinned" >&2
  exit 2
fi
ruby_dir="$(cd "$(dirname "$selected")" && pwd -P)"
bundler="$ruby_dir/bundle"
if [[ ! -x "$bundler" ]]; then echo 'Bundler missing beside Ruby' >&2; exit 3; fi
export PATH="$ruby_dir:$PATH"
export BUNDLE_GEMFILE="$repo/Gemfile"
export BUNDLE_PATH="${BLOG_BUNDLE_PATH:-${XDG_CACHE_HOME:-$HOME/.cache}/saramjh-jekyll/ruby-$pinned}"
export JEKYLL_ENV=production
cd "$repo"
case "${1:-build}" in
  doctor) "$selected" --version; "$bundler" --version; "$bundler" check ;;
  install) "$bundler" install --jobs 2 --retry 1 ;;
  build)
    if ! "$bundler" check; then
      echo 'Missing scoped gems; run scripts/build-blog-local.sh install' >&2; exit 4
    fi
    if [[ -n "${BLOG_BUILD_DEST:-}" ]]; then
      destination="$BLOG_BUILD_DEST"
      if [[ "$destination" != /* || -e "$destination" ]]; then
        echo 'BLOG_BUILD_DEST must be an unused absolute path' >&2; exit 5
      fi
    else
      temp_base="${TMPDIR:-/tmp}"
      temp_base="${temp_base%/}"
      destination="$(mktemp -d "$temp_base/saramjh-jekyll-build.XXXXXX")"
    fi
    if [[ "$destination" == "$repo" || "$destination" == "$repo/"* ]]; then
      echo 'Build destination cannot be inside repo' >&2; exit 6
    fi
    "$bundler" exec jekyll build --destination "$destination"
    test -s "$destination/index.html"
    printf 'BLOG_BUILD_SUCCESS destination=%s ruby=%s
' "$destination" "$pinned"
    ;;
  *) echo 'Usage: scripts/build-blog-local.sh {doctor|install|build}' >&2; exit 64 ;;
esac
