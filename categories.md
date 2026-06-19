---
layout: default
title: 카테고리
---

<article class="article">
  <header class="article-header">
    <h1>카테고리</h1>
    <p>카테고리별로 정리한 글 목록입니다.</p>
  </header>

  <div class="archive-list">
    {% assign categories = site.categories | sort %}
    {% for category in categories %}
      <section id="{{ category[0] | slugify }}">
        <h2>{{ category[0] }}</h2>
        <ul class="link-list">
          {% for post in category[1] %}
            <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
          {% endfor %}
        </ul>
      </section>
    {% endfor %}
  </div>
</article>
