"""Render the curated Cosmos article's headings, paragraphs, lists and inline links."""
from pathlib import Path
import html
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent


def inline(text):
    # The source uses only bold and Markdown links; escape all other content.
    pattern = r'\[([^\]]+)\]\((https?://[^\s)]+)\)|\*\*([^*]+)\*\*'
    result, start = [], 0
    for match in re.finditer(pattern, text):
        result.append(html.escape(text[start:match.start()]))
        if match.group(1):
            result.append(f'<a href="{html.escape(match.group(2), quote=True)}">{html.escape(match.group(1))}</a>')
        else:
            result.append(f'<strong>{html.escape(match.group(3))}</strong>')
        start = match.end()
    result.append(html.escape(text[start:]))
    return ''.join(result)


def build_cosmos(out, document):
    source = ROOT.parent / 'classics' / 'cosmos.md'
    images = json.loads((ROOT / 'cosmos-images.json').read_text(encoding='utf-8'))
    for image in images:
        if not (ROOT.parent / 'assets' / 'cosmos' / f"{image['id']}.webp").is_file():
            raise ValueError(f"Missing image: {image['id']}")

    def figure(item, hero=False):
        name = item['id']
        loading = 'fetchpriority="high"' if hero else 'loading="lazy" decoding="async"'
        return f'''<figure class="cosmos-figure {'cosmos-cover' if hero else ''}" id="image-{name}">
<a href="/assets/cosmos/{name}.webp" aria-label="{html.escape(item['alt'], quote=True)} 원본 크기로 보기"><img src="/assets/cosmos/{name}.webp" width="{item['width']}" height="{item['height']}" alt="{html.escape(item['alt'], quote=True)}" {loading}></a>
<figcaption>{html.escape(item['caption'])}<span class="image-credit">{html.escape(item['credit'])} · <a href="{item['source']}">공식 원본</a> · <a href="{item['license_url']}">{html.escape(item['license'])}</a></span></figcaption></figure>'''

    parts = re.split(r'^## (.+)$', source.read_text(encoding='utf-8'), flags=re.M)

    def blocks(text):
        output = []
        for block in re.split(r'\n\s*\n', text.strip()):
            if not block:
                continue
            if all(line.startswith('- ') for line in block.splitlines()):
                output.append('<ul>' + ''.join(f'<li>{inline(line[2:])}</li>' for line in block.splitlines()) + '</ul>')
            else:
                cls = ' class="video-link"' if block.startswith('영상 해당 구간:') else ''
                output.append(f'<p{cls}>{inline(block)}</p>')
        return '\n'.join(output)

    introduction = re.sub(r'^# .+\n', '', parts[0], count=1)
    article = [f'<div class="cosmos-opening">{blocks(introduction)}</div>']
    toc = []
    for heading, body in zip(parts[1::2], parts[2::2]):
        number = re.match(r'^(\d+) ', heading)
        section_id = f'chapter-{number.group(1)}' if number else ('questions' if heading == '독락당에서 이어 갈 질문' else 'sources')
        toc.append(f'<li><a href="#{section_id}">{html.escape(heading)}</a></li>')
        related = ''.join(figure(item) for item in images if item.get('chapter') == section_id)
        article.append(f'<section id="{section_id}" class="cosmos-chapter"><h2>{html.escape(heading)}</h2>{blocks(body)}{related}</section>')

    image_note = '<p class="image-note">이미지는 각 기관의 관측 자료와 사진입니다. 웹 표시를 위해 크기를 조정하고 WebP로 변환했으며, 색과 구도는 변경하지 않았습니다. 각 이미지의 출처와 이용 조건은 캡션에서 확인할 수 있습니다.</p>'
    content = f'''<main id="main" class="cosmos-page">
<nav class="breadcrumb" aria-label="현재 위치"><a href="/index.html">독락당</a><span>/</span><a href="/topics/cosmos.html">코스모스</a><span>/</span><span aria-current="page">함께 읽기</span></nav>
<section class="cosmos-hero"><div class="cosmos-hero-copy"><p class="eyebrow">CARL SAGAN · COSMOS</p><h1>코스모스<span>우주 속 인간의 자리</span></h1><p class="cosmos-deck">별과 생명에서 문명의 기억까지.<br>13장의 사유를 오늘의 과학과 함께 읽습니다.</p><p class="cosmos-meta">1980년의 고전 · 이후의 발견 · 지구의 미래</p><div class="cosmos-actions"><a class="primary" href="#chapter-1">첫 장부터 읽기</a><a href="https://www.youtube.com/watch?v=qiZZZE4Ef1Q">해설 영상 보기</a></div></div>{figure(images[0], True)}</section>
<div class="cosmos-layout"><aside class="cosmos-toc"><details open id="cosmos-toc"><summary>이 글의 순서</summary><nav aria-label="코스모스 글 목차"><ol>{''.join(toc)}</ol></nav></details><a class="cosmos-download" href="/classics/cosmos.md" download>본문 파일 저장</a></aside>
<article class="cosmos-body" aria-label="코스모스의 핵심 사유와 현대 과학의 발견">{''.join(article)}{image_note}<a class="cosmos-return" href="/index.html#topics">다른 서가 둘러보기</a></article></div></main>
<script>document.getElementById('cosmos-toc').open = window.matchMedia('(min-width: 1001px)').matches;</script>'''
    page = document('코스모스의 핵심 사유와 현대 과학의 발견', content)
    page = page.replace('</head>', '<link rel="stylesheet" href="/classics/cosmos.css"></head>')
    page = page.replace('href="/topics/cosmos.html">코스모스</a>', 'href="/topics/cosmos.html" aria-current="page">코스모스</a>', 1)
    (out / 'classics').mkdir(exist_ok=True)
    (out / 'classics' / 'cosmos.html').write_text(page, encoding='utf-8')
    if out.resolve() != ROOT.parent.resolve():
        shutil.copy2(source, out / 'classics' / 'cosmos.md')
    print('Built Cosmos reading page with 13 chapters and 7 credited images.')
