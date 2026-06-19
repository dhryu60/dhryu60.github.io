---
layout: default
title: 홈
---

# dhryu60의 기술 블로그에 오신 것을 환영합니다.

## 최신 게시글 목록

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a> — <i>{{ post.date | date: "%Y-%m-%d" }}</i>
    </li>
  {% endfor %}
</ul>
