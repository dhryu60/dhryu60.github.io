---
layout: default
title: 홈
---

<h1 class="sr-only">송정의 기술 블로그에 오신 것을 환영합니다.</h1>

<div class="home-grid">
  <main class="post-list" aria-label="최신 게시글">
    {% for post in site.posts %}
      <article class="post-card">
        <div class="post-meta">
          <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y. %m. %d." }}</time>
          {% if post.author %}
            <span>{{ post.author }}</span>
          {% endif %}
        </div>
        <h2 class="post-title">
          <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        </h2>
        {% if post.description %}
          <p class="post-description">{{ post.description }}</p>
        {% else %}
          <p class="post-description">{{ post.excerpt | strip_html | truncate: 180 }}</p>
        {% endif %}
      </article>
    {% endfor %}
  </main>

  <aside class="sidebar" aria-label="블로그 탐색">
    {% if site.tags.size > 0 %}
      <section class="sidebar-section">
        <h2>태그</h2>
        <ul class="link-list">
          {% assign tags = site.tags | sort %}
          {% for tag in tags %}
            {% assign tag_slug = tag[0] | slugify %}
            <li>
              <a href="{{ '/tags/' | relative_url }}#{{ tag_slug }}">{{ tag[0] }} <span>({{ tag[1].size }})</span></a>
            </li>
          {% endfor %}
        </ul>
      </section>
    {% endif %}

    {% if site.categories.size > 0 %}
      <section class="sidebar-section">
        <h2>카테고리</h2>
        <ul class="link-list">
          {% assign categories = site.categories | sort %}
          {% for category in categories %}
            {% assign category_slug = category[0] | slugify %}
            <li>
              <a href="{{ '/categories/' | relative_url }}#{{ category_slug }}">{{ category[0] }} <span>({{ category[1].size }})</span></a>
            </li>
          {% endfor %}
        </ul>
      </section>
    {% endif %}

    <section class="sidebar-section">
      <h2>다시보기</h2>
      <ul class="link-list">
        <li><a href="{{ '/' | relative_url }}">전체 글</a></li>
        <li><a href="{{ site.github.repository_url | default: 'https://github.com/dhryu60/dhryu60.github.io' }}">GitHub 저장소</a></li>
        <li><a href="https://github.com/dhryu60/dhryu60.github.io/wiki">Wiki</a></li>
      </ul>
    </section>
  </aside>
</div>
