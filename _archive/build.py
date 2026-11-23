from pathlib import Path
import argparse
import html
import json
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description='Build the archive from its topic list.')
parser.add_argument('--topics', type=Path, default=ROOT / 'topics.json')
parser.add_argument('--output', type=Path, default=ROOT.parent)
args = parser.parse_args()
OUT = args.output.resolve()
raw_topics = json.loads(args.topics.read_text(encoding='utf-8'))
if not isinstance(raw_topics, list) or not raw_topics:
    raise ValueError('주제 목록에는 하나 이상의 항목이 필요합니다.')
ids = set()
topics = []
for item in raw_topics:
    for field in ('id', 'han', 'title', 'category', 'color', 'intro', 'desc', 'tags'):
        if not isinstance(item.get(field), str) or not item[field].strip():
            raise ValueError(f'필수 문자열 누락: {field}')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', item['id']) or item['id'] in ids:
        raise ValueError('id는 중복 없는 영문 소문자·숫자·하이픈이어야 합니다.')
    ids.add(item['id'])
    if item['color'] not in ('green', 'rust', 'ochre', 'blue'):
        raise ValueError('color는 green, rust, ochre, blue 중 하나여야 합니다.')
    if not isinstance(item.get('links'), list):
        raise ValueError('links는 목록이어야 합니다.')
    links = []
    for link in item['links']:
        if not isinstance(link, list) or len(link) != 3 or not all(isinstance(v, str) and v.strip() for v in link):
            raise ValueError('자료 링크는 [제목, 설명, 주소] 형식이어야 합니다.')
        title, desc, url = link
        parsed = urlsplit(url)
        if not ((url.startswith('/') and not url.startswith('//')) or (parsed.scheme == 'https' and parsed.netloc)) or any(c.isspace() for c in url) or chr(92) in url:
            raise ValueError(f'지원하지 않는 링크: {url}')
        links.append((html.escape(title), html.escape(desc), url))
    topic = {key: html.escape(value, quote=True) for key, value in item.items() if key != 'links'}
    topic['links'] = links
    topics.append(topic)
OUT.mkdir(parents=True, exist_ok=True)

def header():
    return '''<a class="skip" href="#main">본문으로 이동</a><header class="mast"><a class="brand" href="/index.html"><span class="seal" aria-hidden="true">獨<br>樂</span><span>독락당<small>디지털 아카이브</small></span></a><nav aria-label="주 메뉴"><a href="/index.html#topics">주제별 탐색</a><a href="/index.html#reading">읽기의 시작</a><a href="/index.html#about">독락당 소개</a></nav><a class="header-search" href="/index.html#search-area" aria-label="주제 검색"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/></svg></a></header>''' + '<nav class="topic-nav" aria-label="아카이브 주제">' + ''.join(f'<a href="/topics/{t["id"]}.html">{t["title"]}</a>' for t in topics) + '</nav>'

def footer():
    return '''<footer><a class="footer-brand" href="/index.html">獨樂堂 <span>독락당 디지털 아카이브</span></a><p>읽고, 사유하고, 다시 만나는 곳.</p><a href="/blog/">기술 블로그</a><span class="footnote">고전 · 인문학 · 과학</span></footer>'''

def document(title, content, script=False):
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} · 독락당 디지털 아카이브</title><meta name="description" content="고전과 인문학, 과학을 함께 읽는 독락당. {', '.join(t['title'] for t in topics)} 등을 주제별로 탐색하세요."><meta name="theme-color" content="#f5f2e9"><link rel="icon" href="/seal.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css">{'<script src="/app.js" defer></script>' if script else ''}</head><body>{header()}{content}{footer()}</body></html>'''

cards = ''.join(f'''<a class="topic-card {t['color']}" href="/topics/{t['id']}.html" data-search="{t['tags']} {t['title']}"><div class="card-art" aria-hidden="true"><span class="big-han">{t['han']}</span><span class="art-line"></span><span class="vertical">獨樂堂藏</span></div><div class="card-body"><span class="eyebrow">{t['category']}</span><h3>{t['title']}</h3><p>{t['intro']}</p><span class="card-bottom">주제 펼쳐보기 <span>열기</span></span></div></a>''' for t in topics)
home = '''<main id="main"><section class="hero"><div class="hero-copy"><p class="eyebrow"><span class="tiny-line"></span> DOKRAKDANG DIGITAL ARCHIVE</p><h1>오래된 지혜,<br>새로운 <em>사유의 자리.</em></h1><p class="hero-desc">한 권의 고전에서 오늘의 질문까지.<br>시대와 분야를 건너, 읽고 생각하는 즐거움을 나눕니다.</p><a class="primary" href="#topics">아카이브 둘러보기</a><span class="hero-note">당신의 질문이 머무는 곳에서 시작하세요.</span></div><div class="hero-art" aria-label="고전과 사유를 상징하는 책과 원형 창의 일러스트" role="img"><div class="moon"></div><div class="arch-lines"></div><div class="vertical-poem">읽는 즐거움<br>생각하는 깊이</div><div class="book book-back"><span>思惟</span></div><div class="book book-front"><span>獨樂堂</span><i></i><i></i><i></i><i></i></div><div class="shelf"></div><span class="art-caption">책을 펼치면, 사유의 풍경이 열립니다.</span></div></section><section id="topics" class="topics section"><div class="section-head"><div><p class="eyebrow">EXPLORE THE ARCHIVE</p><h2>어떤 주제와 만나볼까요?</h2></div><p>지금 마음이 향하는 서가를 골라보세요.</p></div><div id="search-area" class="search-row"><span>주제별 서가 <b>__TOPIC_COUNT__</b></span><label class="search-box"><span class="sr-only">주제와 키워드 검색</span><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/></svg><input id="search" type="search" placeholder="주제나 키워드로 찾아보기" autocomplete="off"></label></div><p id="result-count" class="sr-only" role="status" aria-live="polite"></p><div class="topic-grid">''' + cards + '''</div><div id="empty" class="empty" hidden><h3>일치하는 주제가 없습니다.</h3><p>‘논어’, ‘두보’, ‘진화’, ‘환대’ 같은 키워드로 찾아보세요.</p><button id="reset-search" class="primary">전체 주제 보기</button></div></section><section id="reading" class="reading section"><div class="section-head"><div><p class="eyebrow">A PLACE TO BEGIN</p><h2>첫 장을 여는 세 가지 길</h2></div><p>무엇부터 읽을지 고민된다면.</p></div><div class="reading-grid"><a href="/classics/confucius-comparison.html"><span class="eyebrow">비교하며 읽기</span><h3>같은 공자,<br>다른 시대의 해석</h3><p>교육과 정치 참여를 둘러싼<br>주석과 해석을 나란히 읽습니다.</p><span class="read-link">공자 해석 비교</span></a><a href="/classics/dusi-reading.html#works"><span class="eyebrow">천천히 음미하기</span><h3>두보의 가을을<br>우리말로 만나다</h3><p>「추흥」의 원문과 언해,<br>현대어 풀이를 함께 펼칩니다.</p><span class="read-link">두시언해 작품 읽기</span></a><a href="/questions/question-1.html"><span class="eyebrow">오늘의 삶에 묻기</span><h3>아무 말 없이 곁에<br>있는 것도 위로일까?</h3><p>욥과 친구들의 침묵에서<br>함께 머무는 일의 의미를 읽습니다.</p><span class="read-link">첫 번째 질문 읽기</span></a></div></section><section id="about" class="about section"><div class="about-mark" aria-hidden="true">獨<br>樂<br>堂</div><div><p class="eyebrow">ABOUT DOKRAKDANG</p><h2>읽는 즐거움이 쌓여,<br>하나의 서재가 됩니다.</h2><p>독락당 디지털 아카이브는 고전과 인문학, 과학의 여러 갈래를<br class="desktop"> 한자리에서 읽고 탐색하는 디지털 서재입니다.</p><p>원문을 살피고, 해석을 비교하고, 오늘의 질문으로 이어갑니다.<br class="desktop"> 익숙한 한 문장도 다시 펼치면 새로운 생각의 시작이 됩니다.</p></div><div class="about-side"><span>이곳의 읽기</span><p>원문과 풀이를 함께</p><p>서로 다른 해석을 나란히</p><p>출처와 맥락을 가까이</p></div></section></main>'''
(OUT / 'index.html').write_text(document('첫 화면', home.replace('__TOPIC_COUNT__', str(len(topics))), True), encoding='utf-8')
(OUT / 'topics').mkdir(exist_ok=True)
for t in topics:
    links = ''.join(f'<a class="resource" href="{html.escape(url, quote=True)}"><div><h3>{title}</h3><p>{desc}</p></div><span>읽기</span></a>' for title, desc, url in t['links'])
    if not links:
        links = '<p class="preparing">자료를 준비하고 있습니다. 곧 이 서가에서 만나보세요.</p>'
    others = ''.join(f'<a href="/topics/{o["id"]}.html">{o["title"]}</a>' for o in topics if o != t)
    content = f'''<main id="main" class="topic-page {t['color']}"><nav class="breadcrumb" aria-label="현재 위치"><a href="/index.html">독락당</a><span>/</span><a href="/index.html#topics">주제별 탐색</a><span>/</span><span aria-current="page">{t['title']}</span></nav><section class="topic-intro"><div><p class="eyebrow">{t['category']}</p><h1>{t['title']}</h1><p class="topic-lead">{t['intro']}</p><p>{t['desc']}</p></div><span class="topic-han" aria-hidden="true">{t['han']}</span></section><section class="resources"><h2>이 서가에서 읽을 수 있는 것</h2>{links}</section><section class="other-topics"><h2>다른 서가도 만나보세요</h2><div>{others}</div></section></main>'''
    (OUT / 'topics' / (t['id'] + '.html')).write_text(document(t['title'], content), encoding='utf-8')
print(f'Built archive and {len(topics)} topic pages in {OUT}.')
