// Aperçus de palettes : applique une palette à toutes les pages et affiche le sélecteur.
// La palette vient de ?palette=N, sinon du dernier choix (mémorisé dans le navigateur).
(function () {
  var P = {
    '3': { n: 'Rose poudré', ink: '#2A1622', ivory: '#FBF3F4', gold: '#A63D6B', goldl: '#F2B8C6', mute: '#6A5560', lav: '#F6E7E8', lead: '#5A4350', brand: '#A63D6B', ov: '#4a1f33c4' },
    '4': { n: 'Lavande et pêche', ink: '#241430', ivory: '#F6F1F9', gold: '#6B3A8E', goldl: '#E3A587', mute: '#5E5068', lav: '#EEE8F4', lead: '#4E3F5C', brand: '#B5603A', ov: '#3a1f4dc4' },
    '5': { n: 'Terracotta et sable', ink: '#2B1A14', ivory: '#F8F1E8', gold: '#A4512B', goldl: '#E8A07A', mute: '#6B5A50', lav: '#F3E9DD', lead: '#5C4A40', brand: '#6B7A4B', ov: '#3a2218c4' }
  };
  var K = 'igmk-palette', q = new URLSearchParams(location.search).get('palette'), cur = null;
  try { if (q !== null) localStorage.setItem(K, q); cur = q !== null ? q : localStorage.getItem(K); } catch (e) { cur = q; }
  if (!P[cur]) cur = 'a';
  var a = function (c, pct) { return 'color-mix(in srgb,' + c + ' ' + pct + '%,transparent)'; };
  function css(p) {
    var ink = 'var(--ink)', lav = 'var(--lav)';
    return ':root{--ink:' + p.ink + ';--ivory:' + p.ivory + ';--paper:#FFFFFF;--gold:' + p.gold + ';--gold-l:' + p.goldl + ';--plum:' + p.ink + ';--mute:' + p.mute + ';--line:' + a(p.ink, 12) + ';--lav:' + p.lav + ';--lead:' + p.lead + '}'
      // navigation
      + '.nav{color:var(--ink)}.nav:before{background:linear-gradient(' + a(p.lav, 94) + ',' + a(p.lav, 0) + ')}'
      + '.nav.s,.nav.mo{background:#fff!important;box-shadow:0 1px 0 ' + a(p.ink, 10) + '}'
      + '.brand small{color:' + p.brand + '}.menu a:hover{color:var(--gold)}.menu a.act{color:var(--gold)!important;border-color:var(--gold)!important}'
      + '.nav .cta{background:var(--gold);color:#fff;border-color:var(--gold)}.nav .cta:hover{background:var(--ink);border-color:var(--ink)}'
      + '.subi,.subi:before{background:#fff;border-color:' + a(p.ink, 10) + '}.subi{box-shadow:0 30px 60px -20px ' + a(p.ink, 24) + '}'
      + '.si b{color:var(--ink)}.si:hover b{color:var(--gold)}.si small{color:var(--mute)}.menu.open{background:var(--lav)}.menu.open .si b{color:var(--gold)}'
      // accueil
      + '.hero{background:var(--lav);color:var(--ink)}.hero .lead{color:var(--lead)}.hero .media:after{background:linear-gradient(90deg,' + lav + ' 0,' + a(p.lav, 0) + ' 30%)}'
      + '.btn:hover{background:var(--ink);color:#fff;border-color:var(--ink)}'
      + '.marq{background:var(--gold)!important;color:#fff;border:0}.marq span:nth-child(even){color:var(--gold-l)}'
      + '.method{background:var(--lav)}.journey{background:#fff;color:var(--ink)}.journey .head .lead{color:var(--mute)}.steps{background:' + a(p.ink, 10) + '}.st{background:#fff}.st p{color:var(--mute)}'
      + '.strip{background:#fff}.testi{background:var(--lav)}'
      + '.stage .kicker,.lead-s .kicker,.stage h2 i,.lead-s h2 i,.ld .q:before,.ltxt .q:before,.sign{color:var(--gold-l)}'
      + '.nbox{background:#fff;color:var(--ink);box-shadow:0 0 0 1px ' + a(p.ink, 10) + ',0 30px 60px -30px ' + a(p.ink, 20) + '}'
      + '.nit .tx{background:none}.nit p{color:var(--mute)}.nit h3 i,.nit .when{color:var(--gold)}.nit .when a{color:var(--ink)}'
      + '.ncd small{color:var(--mute)}.ncd span{border-color:' + a(p.gold, 20) + ';color:var(--gold)}.ncd b{color:var(--ink)}'
      + '.final:after{background:' + p.ov + '}footer h5{color:var(--gold-l)}.wa{background:var(--gold);border-color:var(--gold)}.wa svg{fill:#fff}'
      // pages intérieures
      + '.phero{background:var(--lav);color:var(--ink)}.phero .lead{color:var(--lead)}.crumb{color:var(--mute)}.crumb a:hover{color:var(--gold)}'
      + '.phero .media:after{background:linear-gradient(90deg,' + lav + ' 0,' + a(p.lav, 0) + ' 35%)}.phero .tags span{border-color:' + a(p.gold, 35) + ';color:var(--gold)}'
      + '.sec.dark .kicker,.sec.dark h2 i,.sec.dark h3 i{color:var(--gold-l)}'
      + '.ins-top{background:var(--lav);color:var(--ink)}.ins-top .lead{color:var(--lead)}.steps li{color:var(--mute)}.steps li:not(:last-child):after{background:' + a(p.ink, 20) + '}'
      + '.steps b{border-color:' + a(p.ink, 25) + '}.steps li.on{color:var(--ink)}.steps li.ok{color:var(--gold)}.steps li.ok b{border-color:var(--gold)}'
      + '.ins-a .kicker{color:var(--gold-l)}'
      + '@media (max-width:1000px){.hero .media:after,.phero .media:after{background:linear-gradient(0deg,' + lav + ' 0,' + a(p.lav, 0) + ' 50%)}.nav.mo{background:var(--lav)!important}}';
  }
  if (cur !== 'a') { var st = document.createElement('style'); st.textContent = css(P[cur]); document.head.appendChild(st); }
  // sélecteur
  var bar = document.createElement('div'); bar.className = 'pbar';
  var items = [['a', 'Actuelle']].concat(Object.keys(P).map(function (k) { return [k, k + ' · ' + P[k].n]; }));
  bar.innerHTML = '<a class="pb-h" href="index.html">Toutes les palettes</a>' + items.map(function (it) {
    return '<a href="?palette=' + it[0] + '"' + (it[0] === cur ? ' class="on"' : '') + '>' + it[1] + '</a>';
  }).join('');
  bar.querySelector('.pb-h').href = 'index.html'.replace('index.html', 'palettes.html');
  var s2 = document.createElement('style');
  s2.textContent = '.pbar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:300;display:flex;gap:4px;background:#111;padding:5px;border-radius:30px;box-shadow:0 10px 30px #0005;max-width:calc(100vw - 100px);overflow-x:auto;scrollbar-width:none}'
    + '.pbar::-webkit-scrollbar{display:none}.pbar a{color:#ddd;font:600 11px/1 Manrope,sans-serif;letter-spacing:.06em;padding:9px 12px;border-radius:20px;white-space:nowrap;text-transform:none;text-decoration:none}.pbar a.on{background:#fff;color:#111}.pbar .pb-h{color:#999}'
    + '@media(max-width:700px){.pbar{left:12px;transform:none;max-width:calc(100vw - 96px)}}';
  document.head.appendChild(s2);
  function mount() { document.body.appendChild(bar); var o = bar.querySelector('.on'); if (o) bar.scrollLeft = o.offsetLeft - (bar.clientWidth - o.offsetWidth) / 2; }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
})();
