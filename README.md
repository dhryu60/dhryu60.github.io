# 송정 기술 블로그 운영 가이드

## 블로그 글 작성 프롬프트

아래 프롬프트를 Gemini Gem 또는 AI 글쓰기 도구에 입력한다.

```text
GitHub Pages Jekyll 블로그용 Markdown으로 작성해줘.
반드시 맨 위에 YAML front matter를 포함해줘.

---
title: "..."
date: 2026-06-19
tags: [...]
categories: [...]
description: "..."
---

본문에는 참고자료에서 확인 가능한 내용만 쓰고,
추측은 "추정된다", "가능성이 있다"처럼 표현해줘.

수식은 KaTeX/LaTeX 문법으로 작성해줘.
문장 안의 짧은 수식은 $...$로 쓰고,
독립된 수식은 $$...$$ 블록으로 작성해줘.
수식을 코드블록 안에 넣지 마.
