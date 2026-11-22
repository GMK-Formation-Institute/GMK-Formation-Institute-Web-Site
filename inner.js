// filtres
document.querySelectorAll('.filters').forEach(f=>f.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
f.querySelector('.on')?.classList.remove('on');b.classList.add('on');const c=b.dataset.f;
f.parentElement.querySelectorAll('[data-cat]').forEach(it=>{it.classList.toggle('hide',c!=='all'&&!it.dataset.cat.split(' ').includes(c));it.classList.add('in')})}));
// onglets spécialisations
const tabs=document.querySelector('.tabs2');
if(tabs){const show=k=>{tabs.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x.dataset.tab===k));document.querySelectorAll('.panel').forEach(p=>{p.classList.toggle('on',p.id===k);if(p.id===k)p.querySelectorAll('.rv').forEach(r=>r.classList.add('in'))})};
tabs.addEventListener('click',e=>{const b=e.target.closest('button');if(b){show(b.dataset.tab);history.replaceState(null,'','#'+b.dataset.tab)}});
if(location.hash&&document.getElementById(location.hash.slice(1)))show(location.hash.slice(1));}
// visionneuse
const lbx=document.createElement('div');lbx.className='lbx';lbx.innerHTML='<b>×</b><img alt="">';document.body.appendChild(lbx);
lbx.onclick=()=>lbx.classList.remove('on');document.addEventListener('keydown',e=>e.key==='Escape'&&lbx.classList.remove('on'));
document.querySelectorAll('[data-lb]').forEach(a=>a.onclick=e=>{e.preventDefault();lbx.querySelector('img').src=a.getAttribute('href');lbx.classList.add('on')});
