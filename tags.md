---
layout: default
title: 태그
---

<article class="article">
  <header class="article-header">
    <h1>태그</h1>
    <p>태그별로 정리한 글 목록입니다.</p>
  </header>

  <div class="archive-list">
    {% assign tags = site.tags | sort %}
    {% for tag in tags %}
      <section id="{{ tag[0] | slugify }}">
        <h2>{{ tag[0] }}</h2>
        <ul class="link-list">
          {% for post in tag[1] %}
            <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
          {% endfor %}
        </ul>
      </section>
    {% endfor %}
  </div>
</article>
