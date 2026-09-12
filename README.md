# DevTestudinidae 블로그

Jekyll 블로그. 글과 첨부 파일은 `_posts/<slug>/` 한 폴더에서 관리합니다.
GitHub Actions가 빌드·검사 후 GitHub Pages에 배포합니다.

## 새 글 작성

```sh
ruby scripts/new_post.rb rich-checker-renewal "부자 관상 테스트를 새로 만들었습니다"
```

생성된 Markdown 파일 옆에 이미지를 넣고 파일명으로 참조합니다.

```text
_posts/rich-checker-renewal/
  2026-09-12-rich-checker-renewal.md
  screenshot.jpg
```

```markdown
![관상 테스트 화면](screenshot.jpg)
```

HTML도 `<img src="screenshot.jpg" alt="관상 테스트 화면">`처럼 사용합니다.
공백이 있는 파일명은 URL에서 `%20`으로 표기하세요. 새 파일은 영문 소문자와 하이픈을 권장합니다.
하위 폴더는 `images/screenshot.jpg`처럼 참조할 수 있습니다.
`description`은 검색 설명, `lang`은 글 언어입니다. 공유 대표 이미지를 지정하려면
`image: /rich-checker-renewal/screenshot.jpg`를 추가하세요.

한 폴더에는 글 하나만 두고, `permalink`는 `/slug/`처럼 `/`로 끝나게 합니다.
새 글마다 별도의 이미지 폴더 경로나 Liquid 코드를 설정할 필요가 없습니다.

## 로컬 실행

`.ruby-version`의 Ruby 3.4.6을 사용합니다. macOS 기본 Ruby 2.6은 사용하지 않습니다.

```sh
bundle install
bundle exec jekyll serve
```

Homebrew Ruby를 사용한다면 해당 Ruby의 `bin` 디렉터리를 PATH 앞에 추가하세요.

배포 전 검사:

```sh
JEKYLL_ENV=production bundle exec jekyll build --trace
bundle exec ruby scripts/check_site.rb
bundle exec ruby tests/post_assets_test.rb
```

검사는 생성된 HTML의 로컬 본문 이미지·공유 이미지, 사이트맵의 전체 글 포함 여부,
기존 이미지 URL의 파일 내용 보존 여부를 확인합니다.
외부 이미지 서버의 상태는 검사하지 않습니다.

## 빌드 구조

- `_plugins/post_assets.rb`: 글 옆 첨부 파일을 글 URL 아래에 복사합니다.
- 기존 글의 `legacy_asset_url`: 과거 `/posts/...` 이미지 URL도 함께 생성합니다.
  기존 링크 보존용이므로 삭제하거나 변경하지 마세요. 새 글에는 필요 없습니다.
- `_site/`: 자동 생성 결과. 수정하거나 Git에 추가하지 않습니다.
- `sitemap.xml`, `feed.xml`: 빌드 시 자동 생성. 루트에 수동 파일을 만들지 않습니다.
- `_config.yml`: 사이트 공통 설정.
- `_includes/adsense.html`: `google_adsense` 값이 있을 때만 AdSense 자동 광고 스크립트를 삽입합니다.
- `_includes/seo_schema.html`: 글에는 `BlogPosting`, 일반 페이지에는 `WebSite` JSON-LD를 삽입합니다.
- `.github/workflows/pages.yml`: PR에서 빌드·검사, main에서 검사 후 배포.

## 검색 노출 관리

새 글에는 `title`, `description`, `lang`, `tags`, `image`, `permalink`를 채우세요.
본문 첫 부분에는 글의 핵심 주제와 대상 검색어를 자연스럽게 포함하고, 관련된 기존 글이 있으면 서로 링크합니다.
검색엔진과 AI 검색은 기본 HTML, canonical, 사이트맵, 구조화 데이터를 함께 보므로 별도의 AI 전용 파일보다
글 품질과 메타데이터를 꾸준히 관리하는 편이 낫습니다.

기존 이미지 URL을 유지하기 위한 작은 로컬 플러그인으로 복사를 처리하므로
`jekyll-postfiles`나 `github-pages` gem은 필요하지 않습니다.
첨부 파일은 공개되므로 글 폴더에는 공개할 파일만 넣으세요.

## 최초 배포 전환

이 변경은 GitHub Pages 기본 빌드에서 사용자 정의 Actions 빌드로 전환합니다.
저장소 **Settings → Pages → Build and deployment → Source → GitHub Actions**로
변경하고 이 변경 사항을 main에 반영하세요. 기본 브랜치 빌드는 로컬 플러그인을 실행하지 않습니다.
Actions의 `Build and deploy blog` 실행 성공과 실제 글·이미지 URL을 확인합니다.
이후에는 글 폴더를 추가하고 main에 push하면 자동으로 검사 후 배포합니다.
