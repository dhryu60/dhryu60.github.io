---
title: "GitHub Pages로 기술 블로그 만들기"
date: 2026-06-19
tags: [github-pages, jekyll, github-actions, technical-blog, markdown]
description: "GitHub Pages와 Jekyll을 이용해 기술 블로그를 만들고, GitHub Issue와 Actions를 활용해 글을 발행하는 기본 구조를 정리합니다."
---

# GitHub Pages로 기술 블로그 만들기

GitHub Pages는 GitHub 저장소에 있는 파일을 웹사이트로 공개해주는 기능이다. 기술 블로그를 만들 때는 Markdown으로 글을 작성하고, GitHub Pages가 이를 HTML 웹페이지로 변환해 공개하는 방식으로 운영할 수 있다.

이 글에서는 GitHub Pages, Jekyll, Markdown, GitHub Issue, GitHub Actions가 각각 어떤 역할을 하는지 정리한다.

## 기본 구조

GitHub Pages 기반 기술 블로그는 보통 다음과 같은 파일 구조를 가진다.

```text
저장소
├─ _config.yml
├─ index.md
├─ _posts/
│  └─ 2026-06-19-example-post.md
└─ .github/
   └─ workflows/
      └─ publish-post.yml
```

각 파일과 폴더의 역할은 다음과 같다.

`_config.yml`은 사이트 설정 파일이다. 사이트 제목, 테마, URL 구조 같은 정보를 설정한다.

`index.md`는 블로그의 첫 화면이다. 최신 글 목록을 보여주거나 블로그 소개를 작성할 수 있다.

`_posts` 폴더는 블로그 글이 저장되는 곳이다. Jekyll은 이 폴더 안의 Markdown 파일을 블로그 게시글로 인식한다.

`.github/workflows` 폴더는 GitHub Actions 자동화 설정을 저장하는 곳이다. 이곳에 workflow 파일을 두면 특정 조건에서 자동 작업을 실행할 수 있다.

## GitHub Pages와 Jekyll

GitHub Pages는 저장소에 있는 파일을 웹사이트로 공개한다. 이때 Jekyll을 사용하면 Markdown 파일을 HTML 페이지로 변환할 수 있다.

예를 들어 `_posts` 폴더에 다음과 같은 파일이 있으면 Jekyll은 이를 블로그 글로 처리한다.

```text
_posts/2026-06-19-github-pages-blog.md
```

파일 이름은 보통 다음 형식을 따른다.

```text
YYYY-MM-DD-title.md
```

날짜는 글의 발행일로 사용되고, 제목 부분은 URL을 만드는 데 사용될 수 있다.

## YAML Front Matter

Jekyll 블로그 글의 맨 위에는 YAML front matter를 넣는다. 이것은 글의 제목, 날짜, 태그, 설명 같은 정보를 담는 머리말이다.

예시는 다음과 같다.

```yaml
---
title: "GitHub Pages로 기술 블로그 만들기"
date: 2026-06-19
tags: [github-pages, jekyll, blog]
description: "GitHub Pages와 Jekyll로 기술 블로그를 만드는 방법을 정리합니다."
---
```

YAML front matter는 반드시 `---`로 시작하고 `---`로 끝나야 한다. 이 부분에 문법 오류가 있으면 GitHub Pages 빌드가 실패할 수 있다.

예를 들어 다음과 같은 형태는 문제가 될 수 있다.

```yaml
description: "설명 문장입니다.".
```

마지막 점이 따옴표 밖에 있기 때문이다. 올바른 형태는 다음과 같다.

```yaml
description: "설명 문장입니다."
```

## GitHub Issue를 글 작성 창처럼 사용하기

GitHub Issue는 원래 버그, 할 일, 아이디어를 기록하는 기능이다. 하지만 GitHub Actions와 함께 사용하면 블로그 글 작성 창처럼 활용할 수 있다.

흐름은 다음과 같다.

```text
GitHub Issue 작성
→ publish 라벨 붙이기
→ GitHub Actions 실행
→ _posts 폴더에 Markdown 파일 생성
→ GitHub Pages에서 공개
```

즉 Issue의 제목은 블로그 글 제목으로 사용하고, Issue의 본문은 글 내용으로 사용할 수 있다.

이 방식은 GitHub 웹 화면에서 글을 작성하고, `publish` 라벨을 붙이는 것만으로 블로그 글을 발행할 수 있다는 장점이 있다.

## GitHub Actions의 역할

GitHub Actions는 GitHub 저장소 안에서 자동 작업을 실행하는 기능이다.

기술 블로그에서는 다음과 같은 작업을 자동화할 수 있다.

```text
Issue가 생성되거나 수정됨
→ publish 라벨이 있는지 확인
→ Issue 제목과 본문을 가져옴
→ _posts 폴더에 Markdown 파일 생성
→ 변경 사항을 커밋하고 푸시
```

이렇게 하면 사용자가 직접 `_posts` 폴더에 파일을 만들지 않아도 블로그 글을 발행할 수 있다.

다만 자동화가 안정적으로 작동하려면 workflow에 적절한 권한이 필요하다.

```yaml
permissions:
  contents: write
```

이 설정은 GitHub Actions가 저장소에 새 글 파일을 커밋하고 푸시할 수 있도록 한다.

## Gemini Gem을 활용한 글 작성

Gemini Gem은 블로그 글 초안을 작성하는 도구로 활용할 수 있다. 사용자가 주제와 참고자료를 제공하면, Gem이 GitHub Pages Jekyll 블로그용 Markdown을 작성하도록 만들 수 있다.

안전한 운영 방식은 다음과 같다.

```text
Gemini Gem이 글 작성
→ 사용자가 내용 확인
→ GitHub Issue에 붙여넣기
→ publish 라벨 붙이기
→ 자동 공개
```

이 방식은 완전 자동 발행보다 안전하다. 기술 블로그에서는 사실관계, 제품명, 날짜, 수치, 출처가 중요하기 때문에 사람이 한 번 검수하는 단계가 필요하다.

Gemini Gem에는 다음과 같은 지시를 줄 수 있다.

```text
GitHub Pages Jekyll 블로그용 Markdown으로 작성해줘.
반드시 맨 위에 YAML front matter를 포함해줘.

---
title: "..."
date: 2026-06-19
tags: [...]
description: "..."
---

본문에는 참고자료에서 확인 가능한 내용만 쓰고,
추측은 "추정된다", "가능성이 있다"처럼 표현해줘.
```

이렇게 하면 Gem이 Jekyll에서 읽을 수 있는 형식으로 글을 작성할 가능성이 높아진다.

## 안전한 발행 흐름

가장 안전한 흐름은 다음과 같다.

```text
1. 주제와 참고자료 준비
2. Gemini Gem으로 초안 작성
3. 사람이 내용과 YAML front matter 확인
4. GitHub Issue 생성
5. 본문에 Markdown 붙여넣기
6. publish 라벨 추가
7. GitHub Actions가 _posts에 글 생성
8. GitHub Pages에서 공개
```

이 구조는 자동화의 편리함과 사람 검수의 안정성을 함께 가져갈 수 있다.

완전 자동화도 가능하지만, 검수 없이 공개하면 잘못된 정보가 블로그에 올라갈 가능성이 있다. 따라서 기술 블로그 초기 운영 단계에서는 사람이 최종 확인한 뒤 발행하는 방식이 적절하다.

## 정리

GitHub Pages 기술 블로그의 핵심은 간단하다.

```text
Markdown으로 글 작성
→ Jekyll이 HTML로 변환
→ GitHub Pages가 웹사이트로 공개
```

여기에 GitHub Issue와 GitHub Actions를 더하면 글 작성과 발행 과정을 자동화할 수 있다.

Gemini Gem은 글 초안을 만드는 데 사용하고, GitHub Issue는 발행 요청 창처럼 사용하며, GitHub Actions는 Issue를 실제 블로그 글 파일로 변환하는 역할을 맡는다.

이 구조를 사용하면 별도의 서버를 운영하지 않고도 GitHub 저장소만으로 기술 블로그를 운영할 수 있다.
