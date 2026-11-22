const controls = document.querySelector('.topic-controls');
const buttons = [...controls.querySelectorAll('button[data-topic]')];
const topics = [...document.querySelectorAll('.topic')];
const status = document.getElementById('comparison-status');

function showTopic(topic) {
  const selected = ['education', 'politics', 'all'].includes(topic) ? topic : 'education';
  for (const panel of topics) panel.hidden = selected !== 'all' && panel.id !== selected;
  for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.topic === selected));
  status.textContent = selected === 'all' ? '교육과 정치 참여, 두 주제의 다섯 관점을 모두 표시합니다.' : `${selected === 'education' ? '교육' : '정치 참여'}에 관한 한·위, 송대, 청대, 조선 실학, 크릴의 다섯 관점을 표시합니다.`;
}

controls.hidden = false;
showTopic(location.hash.slice(1));
for (const button of buttons) button.addEventListener('click', () => {
  history.replaceState(null, '', `#${button.dataset.topic}`);
  showTopic(button.dataset.topic);
});
window.addEventListener('hashchange', () => {
  const topic = location.hash.slice(1);
  if (['education', 'politics', 'all'].includes(topic)) showTopic(topic);
});
