const search = document.querySelector('#search');
const cards = [...document.querySelectorAll('.topic-card')];
function filterTopics() {
  const terms = search.value.normalize('NFC').toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  let count = 0;
  for (const card of cards) {
    const text = (card.dataset.search + ' ' + card.textContent).normalize('NFC').toLocaleLowerCase();
    card.hidden = !terms.every(term => text.includes(term));
    if (!card.hidden) count++;
  }
  document.querySelector('#empty').hidden = count !== 0;
  document.querySelector('#result-count').textContent = `${count}개의 주제가 있습니다.`;
}
search.addEventListener('input', filterTopics);
document.querySelector('#reset-search').addEventListener('click', () => { search.value = ''; filterTopics(); search.focus(); });
filterTopics();
