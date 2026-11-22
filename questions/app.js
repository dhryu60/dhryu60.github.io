const search=document.querySelector('#search');
if(search){
  const theme=document.querySelector('#theme-filter');
  const kind=document.querySelector('#kind-filter');
  const cards=[...document.querySelectorAll('#results .card')];
  const params=new URLSearchParams(location.search);
  if([...theme.options].some(o=>o.value===params.get('theme')))theme.value=params.get('theme');
  search.value=params.get('q')||'';
  function filter(){
    const q=search.value.toLocaleLowerCase().trim();let count=0;
    for(const card of cards){const match=(!theme.value||card.dataset.theme===theme.value)&&(!kind?.value||card.dataset.kind===kind.value)&&(!q||card.dataset.search.toLocaleLowerCase().includes(q)||card.textContent.toLocaleLowerCase().includes(q));card.hidden=!match;if(match)count++;}
    document.querySelector('#result-count').textContent=`${count}편의 글`;
    document.querySelector('#empty').hidden=count!==0;
  }
  search.addEventListener('input',filter);theme.addEventListener('change',filter);kind?.addEventListener('change',filter);filter();
}
