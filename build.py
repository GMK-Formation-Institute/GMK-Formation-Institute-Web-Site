# Génère les pages intérieures du site v2 à partir du style de index.html
import re, pathlib, urllib.parse
R = pathlib.Path(__file__).parent
idx = (R / "index.html").read_text()
WA_N = "2250707589081"
def wa(m="Bonjour, je souhaite des informations sur IGMK Formation."): return f"https://wa.me/{WA_N}?text=" + urllib.parse.quote(m)
F = "img/formations/"

# --- liens de navigation de l'accueil ---
NAV = [("ecole.html","L'école"),("formations.html","Formations"),("stage.html","Le stage"),("diplomees.html","Diplômées"),("galerie.html","Galerie"),("actualites.html","Actualités"),("contact.html","Contact")]
def SUB(items): return '<div class="sub"><div class="subi">' + "".join(f'<a class="si" href="{h}"><span class="sim"><img class="ph" src="img/{im}" alt=""></span><b>{t}</b><small>{d}</small></a>' for h,t,d,im in items) + '</div></div>'
menu = ('<nav class="menu" id="menu">'
 + '<div class="dd"><a href="ecole.html">L\'école</a>' + SUB([("ecole.html","Notre méthode","80 % pratique, 20 % théorie","formations/32.jpg"),("diplomees.html","Diplômées","Où sont-elles aujourd'hui","formations/coiffure/18.jpg"),("galerie.html","Galerie","L'école en images","formations/maquillage/5.jpg")]) + '</div>'
 + '<div class="dd"><a href="formations.html">Formations</a>' + SUB([("esthetique.html","Esthétique","6 mois + 3 mois de stage","formations/esthetique/5.jpg"),("coiffure.html","Coiffure","6 mois + 3 mois de stage","formations/coiffure/4.jpg"),("specialisations.html","Spécialisations","Maquillage, onglerie, massage, déco","formations/onglerie/10.jpg")]) + '</div>'
 + '<a href="stage.html">Le stage</a><a href="actualites.html">Actualités</a><a href="contact.html">Contact</a></nav>')
PARENT = {"diplomees.html":"ecole.html","galerie.html":"ecole.html"}
idx = re.sub(r'<nav class="menu" id="menu">.*?</nav>', lambda m: menu, idx, flags=re.S)
idx = idx.replace('<a class="brand" href="#"', '<a class="brand" href="index.html"')
for a,b in [('href="#">Toutes les formations','href="formations.html">Toutes les formations'),('href="#" style="align-self:flex-start">Découvrir le stage','href="stage.html" style="align-self:flex-start">Découvrir le stage'),('href="#">Toutes les diplômées','href="diplomees.html">Toutes les diplômées')]:
    idx = idx.replace(a,b)
for h,t in [("esthetique.html","Esthétique"),("coiffure.html","Coiffure"),("specialisations.html#maquillage","Maquillage"),("specialisations.html#onglerie","Onglerie"),("specialisations.html#massage","Massage"),("specialisations.html#decoration","Décoration")]:
    idx = re.sub(rf'<a href="[^"]*" class="rv">(<span class="no">\d+</span><h3>{t}</h3>)', rf'<a href="{h}" class="rv">\1', idx)
FOOT_L = ('<div><h5>Formations</h5><ul><li><a href="esthetique.html">Esthétique</a></li><li><a href="coiffure.html">Coiffure</a></li><li><a href="specialisations.html#maquillage">Maquillage</a></li><li><a href="specialisations.html#onglerie">Onglerie</a></li><li><a href="specialisations.html#massage">Massage</a></li><li><a href="specialisations.html#decoration">Décoration</a></li></ul></div>'
          '<div><h5>L\'institut</h5><ul><li><a href="ecole.html">L\'école</a></li><li><a href="stage.html">Le stage</a></li><li><a href="diplomees.html">Diplômées</a></li><li><a href="galerie.html">Galerie</a></li><li><a href="actualites.html">Actualités</a></li><li><a href="contact.html">Contact</a></li></ul></div>')
idx = re.sub(r'<div><h5>Formations</h5>.*?</ul></div>\s*<div><h5>L\'institut</h5>.*?</ul></div>', FOOT_L, idx, flags=re.S)
if 'Toutes les actualités' not in idx:
    idx = idx.replace('<h2 class="rv">À la une <i>chez IGMK.</i></h2></div>', '<h2 class="rv">À la une <i>chez IGMK.</i></h2><a class="link rv" href="actualites.html" style="margin-top:22px">Toutes les actualités →</a></div>')
idx = re.sub(r'<a class="cta" href="[^"]*"( target="_blank")?>Prendre rendez-vous', '<a class="cta" href="inscription.html">Me pré-inscrire', idx)
idx = re.sub(r'(<a class="cta" href="inscription.html">Me pré-inscrire)', r'\1', idx)
(R / "index.html").write_text(idx)

# --- briques partagées extraites de l'accueil ---
head_html = idx.split("<body>")[0]
css_extra = (R / "inner.css").read_text()
header = re.search(r'<header class="nav".*?</header>', idx, re.S).group(0)
footer = re.search(r'<footer>.*?</footer>', idx, re.S).group(0)
wa_btn = re.search(r'<a class="wa".*?</a>', idx, re.S).group(0)
script = re.search(r'<script>(.*?)</script>', idx, re.S).group(1)
INNER_JS = (R / "inner.js").read_text()

def page(fn, title, desc, body, active=None, wa_msg=None):
    h = re.sub(r"<title>.*?</title>", f"<title>{title} — IGMK Formation</title>", head_html)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)
    h = h.replace("</style>", css_extra + "\n</style>")
    act = PARENT.get(active, active)
    hd = header.replace(f'<a href="{act}">', f'<a href="{act}" class="act">', 1) if act else header
    w = wa_btn.replace(f'https://wa.me/{WA_N}"', wa(wa_msg) + '"') if wa_msg else wa_btn
    (R / fn).write_text(f"{h}<body class=\"inner\">\n{hd}\n{body}\n{"" if fn=="inscription.html" else final()}\n{footer}\n{w}\n<script>{script}\n{INNER_JS}</script>\n</body>\n</html>\n")

def hero(img, kicker, l1, l2, lead, tags=(), btn=""):
    t = "".join(f"<span>{x}</span>" for x in tags)
    return f'''<section class="phero"><div class="txt"><div class="crumb"><a href="index.html">Accueil</a> / {kicker}</div><div class="kicker">{kicker}</div>
<h1><span><em>{l1}</em></span><span><em><i>{l2}</i></em></span></h1><p class="lead">{lead}</p>{f'<div class="tags">{t}</div>' if t else ''}{f'<div class="row">{btn}</div>' if btn else ''}</div>
<div class="media"><img class="ph" src="{img}" alt=""></div></section>'''

def H(k, a, b, lead="", center=False, dark=False):
    return f'<div class="shead{" c" if center else ""}"><div><div class="kicker rv">{k}</div><h2 class="rv">{a}<br><i>{b}</i></h2></div>{f"<p class=\"lead rv\">{lead}</p>" if lead else ""}</div>'

def final(t1="Votre métier", t2="commence ici.", msg=None):
    return f'''<section class="final"><img class="ph" src="{F}esthetique/1.jpg" alt=""><div class="c"><div class="kicker">Rentrée de janvier 2027 · Places limitées</div>
<h2>{t1}<br><i>{t2}</i></h2><div class="row"><a class="btn solid" href="inscription.html">Me pré-inscrire</a><a class="btn" href="{wa(msg) if msg else wa()}" target="_blank">Échanger sur WhatsApp</a><a class="btn" href="tel:+2250707589081">07 07 58 90 81</a></div></div></section>'''

def mosaic(items, gid=""):
    return f'<div class="mos"{f" id={gid}" if gid else ""}>' + "".join(f'<a href="{F}{p}" data-lb data-cat="{c}" class="rv"><img class="ph" src="{F}{p}" alt="{cap}" loading="lazy"><span>{cap}</span></a>' for p,c,cap in items) + '</div>'

STAGE = f'''<section class="stage"><div class="im"><img class="ph" src="{F}coiffure/7.jpg" alt=""></div><div class="tx"><div class="kicker rv">Le stage obligatoire</div><h2 class="rv">Trois mois<br><i>sur le terrain.</i></h2>
<blockquote class="rv">« La maîtrise de nos apprenantes surprend souvent leurs maîtres de stage. »</blockquote><ul class="rv"><li>Instituts & salons partenaires <b>40+</b></li><li>Durée minimale <b>3 mois</b></li><li>Diplômées en activité à 6 mois <b>87 %</b></li></ul>
<a class="btn rv" href="stage.html" style="align-self:flex-start">Découvrir le stage</a></div></section>'''

def prices(hl="Esthétique"):
    out = '<div class="prices">'
    for t, d, li in [("Esthétique","Formation longue · 11 modules",["6 mois à l'école","3 mois de stage obligatoire","Fascicules & kit de démarrage","Certificat IGMK"]),("Coiffure","Formation longue · 6 modules",["6 mois à l'école","3 mois de stage obligatoire","Fascicules & kit de démarrage","Certificat IGMK"]),("Spécialisation","Maquillage · Onglerie · Massage · Déco",["2 semaines intensives","100 % atelier","Matériel fourni","Attestation IGMK"])]:
        out += f'<div class="pr rv{" hl" if t==hl else ""}"><div class="pk">{d}</div><h3>{t}</h3><div class="amt">XXX 000 <small>FCFA</small></div><div class="mo">ou paiement mensuel échelonné</div><ul>' + "".join(f"<li>{x}</li>" for x in li) + f'</ul><a class="btn{" solid" if t==hl else ""}" href="{wa("Bonjour, je souhaite connaître le tarif de la formation " + t + ".")}" target="_blank">Me renseigner</a></div>'
    return out + '</div>'

FAQ = '<div class="faq">' + "".join(f'<details class="rv"{" open" if i==0 else ""}><summary>{q}<i></i></summary><p>{a}</p></details>' for i,(q,a) in enumerate([
 ("Faut-il un niveau scolaire ou une expérience ?","Non. Nos formations sont ouvertes aux débutantes motivées. Tout s'apprend en atelier, pas à pas."),
 ("Le stage est-il vraiment obligatoire ?","Oui. Les 3 mois de stage en institut ou en salon partenaire font partie intégrante du cursus : c'est ce qui rend nos diplômées immédiatement opérationnelles."),
 ("Peut-on payer en plusieurs fois ?","Oui, le paiement peut être échelonné par mois. Écrivez-nous sur WhatsApp pour connaître les modalités."),
 ("Quels sont les horaires ?","Du lundi au vendredi, de 8h à 17h, à Yopougon – Millionnaire."),
 ("Reçoit-on un diplôme ?","Un certificat IGMK Formation est délivré à l'issue de la formation et du stage validé.")])) + '</div>'

# ------------------------- PAGES -------------------------
page("formations.html","Nos formations","Formations longues en esthétique et coiffure, spécialisations en maquillage, onglerie, massage et décoration à Abidjan.",
 hero(F+"esthetique/7.jpg","Formations","Six métiers,","un même niveau d'exigence.","Deux formations longues pour devenir professionnelle, quatre spécialisations pour se perfectionner. Toujours 80 % de pratique.",["6 mois + 3 mois de stage","Spécialisations 2 semaines","80 % pratique"])
 + '<section class="sec"><div class="w">' + H("Formations longues","Devenir professionnelle","en neuf mois.") + '<div class="big2">' + "".join(
   f'<a class="bc rv" href="{h}"><div class="im"><img class="ph" src="{F}{p}" alt=""></div><div class="bt"><span class="no">{n}</span><h3>{t}</h3><p>{d}</p><div class="meta">6 mois à l\'école · 3 mois de stage · {m}</div><span class="link">Découvrir le programme →</span></div></a>'
   for n,h,p,t,m,d in [("01","esthetique.html","esthetique/5.jpg","Esthétique","11 modules","Soins du visage et du corps, épilation, manucure, pédicure, massage, maquillage, cosmétique."),("02","coiffure.html","coiffure/4.jpg","Coiffure","6 modules","Coiffures africaines et modernes, tresses, nattes, tissage, perruques, lace frontal.")]) + '</div></div></section>'
 + '<section class="sec ivory"><div class="w">' + H("Spécialisations","Se perfectionner","en deux semaines.","Des modules courts et certifiants, pour les débutantes comme pour les professionnelles.") + '<div class="spe4">' + "".join(
   f'<a class="sc rv" href="specialisations.html#{k}"><div class="im"><img class="ph" src="{F}{p}" alt=""></div><span class="no">0{i+3}</span><h3>{t}</h3><p>{d}</p></a>'
   for i,(k,p,t,d) in enumerate([("maquillage","maquillage/57.jpg","Maquillage","Événementiel, mariée, contouring"),("onglerie","onglerie/10.jpg","Onglerie","Gel, résine, acrygel, nail art"),("massage","massage/3.jpg","Massage","Relaxant, amincissant, drainant"),("decoration","decoration/13.jpg","Décoration","Salles, stands, véhicules")])) + '</div></div></section>'
 + STAGE
 + '<section class="sec"><div class="w">' + H("Tarifs","Payez","à votre rythme.","Montants indicatifs, à confirmer auprès de l'école.") + prices() + '</div></section>', "formations.html")

def formation(fn, name, img, mods, gal, intro, skills, nb):
    msg = f"Bonjour, je souhaite des informations sur la formation {name}."
    page(fn, f"Formation {name}", f"Formation {name} à Abidjan : 6 mois à l'école + 3 mois de stage obligatoire. 80 % pratique.",
     hero(F+img,"Formation longue",name,"en neuf mois.",intro,["6 mois à l'école","+ 3 mois de stage","80 % pratique",f"{nb} modules"],f'<a class="btn solid" href="{wa(msg)}" target="_blank">Me renseigner</a><a class="link" href="#programme">Voir le programme →</a>')
     + f'''<section class="sec"><div class="w split"><div><div class="kicker rv">Pour qui ?</div><h2 class="rv">Aucune expérience<br><i>requise.</i></h2>
<p class="lead rv" style="margin-top:30px">Cette formation s'adresse à toute personne motivée par les métiers de la beauté, même débutante. À la sortie, vous exercez en institut ou à votre compte.</p>
<ul class="chk rv">''' + "".join(f"<li>{s}</li>" for s in skills) + f'''</ul></div><div class="pics rv"><figure><img class="ph" src="{F}{gal[0]}" alt=""></figure><figure><img class="ph" src="{F}{gal[1]}" alt=""></figure><figure><img class="ph" src="{F}{gal[2]}" alt=""></figure></div></div></section>'''
     + '<section class="sec dark" id="programme"><div class="w">' + H("Le programme",f"{nb} modules,","en atelier.") + '<div class="mods">' + "".join(
       f'<div class="md rv"><div class="im"><img class="ph" src="{F}{p}" alt="" loading="lazy"></div><span class="no">{i+1:02d}</span><h4>{t}</h4></div>' for i,(t,p) in enumerate(mods)) + '</div></div></section>'
     + '<section class="sec"><div class="w"><div class="facts">' + "".join(f'<div class="rv"><b>{a}</b><span>{b}</span></div>' for a,b in [("6","Mois à l'école"),("3","Mois de stage<br>obligatoire"),("80<sup>%</sup>","Du temps<br>en atelier"),(str(nb),"Modules<br>certifiants")]) + '</div></div></section>'
     + '<section class="sec ivory"><div class="w">' + H("Réalisations","Fait par","nos apprenantes.") + mosaic([(g,name.lower(),"Réalisation d'élève") for g in gal]) + '</div></section>'
     + STAGE
     + '<section class="sec"><div class="w">' + H("Tarif","Payez","à votre rythme.") + prices(name) + '</div></section>'
     + '<section class="sec ivory"><div class="w split">' + '<div>' + H("Questions","Vos questions,","nos réponses.") + '</div>' + FAQ + '</div></section>', "formations.html", msg)

formation("esthetique.html","Esthétique","esthetique/5.jpg",
 [("Soins du visage","esthetique/1.jpg"),("Soins du corps","massage/5.jpg"),("Épilation","esthetique/4.jpg"),("Manucure","onglerie/5.jpg"),("Pédicure","onglerie/10.jpg"),("Massage","massage/7.jpg"),("Maquillage","maquillage/6.jpg"),("Cosmétique","esthetique/8.jpg"),("Dermatologie esthétique","esthetique/16.jpg"),("Biologie esthétique","esthetique/2.jpg"),("Insertion professionnelle","esthetique/6.jpg")],
 ["esthetique/3.jpg","esthetique/7.jpg","esthetique/8.jpg","esthetique/1.jpg","esthetique/16.jpg","esthetique/6.jpg","esthetique/2.jpg"],
 "Les soins du visage, du corps, des mains et des pieds, maîtrisés en 6 mois d'ateliers puis appliqués pendant 3 mois en institut.",
 ["Réaliser des soins du visage et du corps","Pratiquer l'épilation, la manucure et la pédicure","Conseiller la clientèle et vendre des produits"], 11)

formation("coiffure.html","Coiffure","coiffure/4.jpg",
 [("Coiffures africaines","coiffure/3.jpg"),("Coiffures modernes","coiffure/6.jpg"),("Tresses & nattes","coiffure/2.jpg"),("Tissage, perruques, lace","coiffure/7.jpg"),("Traitement des cheveux","coiffure/15.jpg"),("Insertion professionnelle","coiffure/18.jpg")],
 ["coiffure/1.jpg","coiffure/2.jpg","coiffure/3.jpg","coiffure/6.jpg","coiffure/7.jpg","coiffure/15.jpg","coiffure/18.jpg"],
 "Coiffures africaines et modernes, tresses, tissage, perruques et soins du cheveu : 6 mois d'ateliers puis 3 mois de stage en salon.",
 ["Réaliser tresses, nattes, tissages et perruques","Traiter et soigner tous types de cheveux","Gérer une clientèle en salon"], 6)

SPE = [("maquillage","Maquillage","maquillage/4.jpg",["maquillage/1.jpg","maquillage/3.jpg","maquillage/5.jpg","maquillage/8.jpg"],"Morphologie du visage, maniement des pinceaux, harmonie des couleurs, épilation des sourcils.",["L'harmonie des couleurs","La mise en valeur du visage","La correction des défauts","Le maquillage événementiel","Contouring, baking…"]),
("onglerie","Onglerie","onglerie/10.jpg",["onglerie/1.jpg","onglerie/3.jpg","onglerie/4.jpg","onglerie/5.jpg"],"Spécialisez-vous en prothésie ongulaire et lancez votre activité.",["Manucure et pédicure","Pose de capsules et de vernis","Gel, résine, acrygel, chablon","Nail art","Façonnage des ongles"]),
("massage","Massage","massage/3.jpg",["massage/1.jpg","massage/2.jpg","massage/4.jpg","massage/5.jpg"],"Massages manuels du visage, du cou et du décolleté, connaissance des muscles et communication avec la cliente.",["Bien-être et relaxation","Soins amincissants","Soins raffermissants","Soins énergisants et drainants","Soins du dos et du buste"]),
("decoration","Décoration","decoration/13.jpg",["decoration/12.jpg","decoration/14.jpg","decoration/15.jpg","decoration/16.jpg"],"Une façon simple d'apporter une touche d'originalité à vos événements.",["Décoration de salles","Décoration de voitures","Décoration de stands","Origami"])]
page("specialisations.html","Spécialisations","Spécialisations de 2 semaines : maquillage, onglerie, massage, décoration.",
 hero(F+"maquillage/57.jpg","Spécialisations","Se spécialiser","en deux semaines.","Des modules courts et certifiants pour se perfectionner ou se lancer dans un nouveau métier.",["2 semaines","100 % atelier","Certifiant"])
 + '<section class="sec"><div class="w"><div class="tabs2">' + "".join(f'<button data-tab="{k}"{" class=on" if i==0 else ""}><span>0{i+1}</span>{t}</button>' for i,(k,t,*_) in enumerate(SPE)) + '</div>' + "".join(
   f'<div class="panel{" on" if i==0 else ""}" id="{k}"><div class="split"><div><div class="kicker">Spécialisation · 2 semaines</div><h2>Formation<br><i>{t}.</i></h2><p class="lead" style="margin-top:28px">{d}</p><ul class="chk">' + "".join(f"<li>{x}</li>" for x in li) + f'</ul><a class="btn solid" style="margin-top:36px" href="{wa(f"Bonjour, je souhaite des informations sur la spécialisation {t}.")}" target="_blank">Me renseigner</a></div><div class="pics"><figure><img class="ph" src="{F}{img}" alt=""></figure><figure><img class="ph" src="{F}{g[0]}" alt=""></figure><figure><img class="ph" src="{F}{g[1]}" alt=""></figure></div></div>' + mosaic([(x,k,t) for x in g]) + '</div>'
   for i,(k,t,img,g,d,li) in enumerate(SPE)) + '</div></section>'
 + '<section class="sec ivory"><div class="w">' + H("Tarifs","Payez","à votre rythme.") + prices("Spécialisation") + '</div></section>', "formations.html")

page("stage.html","Le stage obligatoire","Stage obligatoire de 3 mois en institut de beauté ou salon de coiffure partenaire.",
 hero(F+"coiffure/15.jpg","Le stage","Trois mois","sur le terrain.","Le stage relie la formation à l'emploi. Il prolonge les 6 mois à l'école par une vraie immersion en institut ou en salon partenaire.",["Obligatoire","Minimum 3 mois","40+ partenaires"])
 + '<section class="manif"><div class="w"><div class="kicker rv">Pourquoi obligatoire</div><br><br><p class="big rv">Un geste appris en atelier <img class="ph" src="img/formations/coiffure/6.jpg" alt=""> ne devient un <i>métier</i> qu\'au contact de vraies clientes <img class="ph" src="img/formations/esthetique/3.jpg" alt=""> dans un vrai salon. C\'est pourquoi <i>chaque</i> diplômée IGMK y passe.</p></div></section>'
 + '<section class="journey"><div class="w"><div class="head"><div><div class="kicker rv">Les bénéfices</div><h2 class="rv" style="margin-top:24px">Apprendre<br><i>en situation réelle.</i></h2></div></div><div class="steps">' + "".join(
   f'<div class="st rv{" hl" if hl else ""}"><div class="im"><img class="ph" src="{F}{p}" alt=""></div><div class="n">{n}</div><h3>{t}</h3><p>{d}</p></div>' for n,p,t,d,hl in [("01","coiffure/18.jpg","Consolider le geste","Les gestes appris à l'école deviennent des automatismes face aux vraies clientes.",0),("02","maquillage/7.jpg","Gagner en confiance","S'organiser, gérer la pression, gagner en maturité professionnelle.",0),("03","coiffure/7.jpg","Accéder à l'emploi","Beaucoup de nos élèves sont embauchées par leur institut de stage.",0)]) + '</div></div></section>'
 + '<section class="sec"><div class="w">' + H("Le déroulé","Le parcours","du stage.") + '<div class="tl">' + "".join(f'<div class="rv"><b>{a}</b><h4>{t}</h4><p>{d}</p></div>' for a,t,d in [("Mois 6","Choix de l'institut","Nous vous orientons vers le partenaire adapté à votre profil et à votre quartier."),("Semaine 1","Accueil & observation","Découverte de l'équipe, de la clientèle et des protocoles du salon."),("Mois 1 à 3","Pratique encadrée","Vous réalisez des prestations sous le regard d'un maître de stage."),("Fin","Évaluation & certificat","Bilan avec l'école et le maître de stage, puis remise du certificat.")]) + '</div></div></section>'
 + '<section class="testi"><div class="w"><div class="kicker rv" style="justify-content:center">Paroles de maître de stage</div><q class="rv">« Les stagiaires d\'IGMK arrivent <i>opérationnelles</i>. Elles ont déjà les bons gestes et la bonne attitude. »</q><div class="who rv"><div><b>Gérante d\'institut</b><span>Cocody · Partenaire depuis 2016</span></div></div></div></section>'
 + '<section class="sec"><div class="w">' + H("Partenaires","Ils accueillent","nos stagiaires.","Plus de 40 instituts et salons partenaires dans tout Abidjan.") + '<div class="logos">' + "".join('<div class="rv">Logo partenaire</div>' for _ in range(8)) + '</div></div></section>'
 + '<div class="strip">' + "".join(f'<div><img class="ph" src="{F}{p}" alt=""></div>' for p in ["coiffure/7.jpg","maquillage/8.jpg","onglerie/4.jpg","esthetique/16.jpg","massage/8.jpg","maquillage/9.jpg"]) + '</div>', "stage.html")

AL = [("coiffure/18.jpg","Aïcha K.","2019","Fondatrice du salon Aïcha Hair, Yopougon. Trois employées.","Coiffure","coiffure compte"),("esthetique/8.jpg","Mariam T.","2022","Esthéticienne au Spa Riviera, embauchée après son stage.","Esthétique","esthetique institut"),("onglerie/10.jpg","Grâce A.","2023","Prothésiste ongulaire à domicile, 1 200 abonnées TikTok.","Onglerie","onglerie compte"),("maquillage/57.jpg","Fatou D.","2021","Maquilleuse mariages & shootings à Abidjan.","Maquillage","maquillage compte"),
      ("esthetique/3.jpg","Awa B.","2020","Responsable d'un institut à Cocody Angré.","Esthétique","esthetique institut"),("coiffure/2.jpg","Nadège S.","2018","Coiffeuse en salon, spécialiste lace frontal.","Coiffure","coiffure institut"),("onglerie/3.jpg","Prisca Y.","2024","A ouvert son bar à ongles à Marcory.","Onglerie","onglerie compte"),("maquillage/3.jpg","Ruth O.","2022","Maquilleuse pour une agence de mannequins.","Maquillage","maquillage institut")]
page("diplomees.html","Nos diplômées","Où sont aujourd'hui les diplômées d'IGMK Formation ?",
 hero(F+"coiffure/18.jpg","Diplômées","Nos diplômées","font le métier.","Plus de 500 professionnelles formées depuis 2012. Elles exercent en institut, en salon ou à leur compte, à Abidjan et dans tout le pays.",["500+ diplômées","87 % en activité à 6 mois"])
 + '<section class="alum"><div class="w"><div class="filters">' + "".join(f'<button data-f="{k}"{" class=on" if k=="all" else ""}>{t}</button>' for k,t in [("all","Toutes"),("esthetique","Esthétique"),("coiffure","Coiffure"),("onglerie","Onglerie"),("maquillage","Maquillage"),("compte","À leur compte"),("institut","En institut")]) + '</div><div class="track grid" id="alumni">' + "".join(
   f'<div class="ac rv" data-cat="{c}"><div class="im"><img src="{F}{p}" alt=""><span class="yr">PROMO {y}</span></div><h4>{n}</h4><p>{d}</p><small>{m}</small></div>' for p,n,y,d,m,c in AL) + '</div></div></section>'
 + '<section class="testi"><div class="w"><div class="kicker rv" style="justify-content:center">Témoignage</div><q class="rv">« Dès mon premier jour de stage, je savais travailler. Aujourd\'hui, j\'ai <i>mon propre salon</i> et trois employées. »</q><div class="who rv"><img src="img/feedback/001.jpg" alt=""><div><b>Aïcha K.</b><span>Coiffure · Promo 2019</span></div></div></div></section>'
 + '<section class="stage"><div class="im"><img class="ph" src="'+F+'esthetique/6.jpg" alt=""></div><div class="tx"><div class="kicker rv">Salons & instituts</div><h2 class="rv">Vous recrutez ?<br><i>Parlons-en.</i></h2><p class="lead rv" style="color:#d9cbd6;margin-bottom:40px">Proposez un stage ou un emploi à nos diplômées : nous vous mettons en relation avec les profils adaptés.</p><a class="btn solid rv" style="align-self:flex-start" href="' + wa("Bonjour, je suis un salon et je souhaite proposer un stage ou un emploi.") + '" target="_blank">Proposer une offre</a></div></section>', "diplomees.html")

page("ecole.html","L'école","Présentation de l'Institut GMK Formation, école de beauté à Abidjan depuis 2012.",
 hero(F+"bg3.jpg","L'école","Former l'excellence","depuis 2012.","L'Institut GMK Formation modernise et professionnalise les métiers de l'esthétique et de la coiffure en Côte d'Ivoire.",["Depuis 2012","500+ diplômées","Yopougon – Millionnaire"])
 + '<section class="sec"><div class="w split"><div><div class="kicker rv">Notre histoire</div><h2 class="rv">Une formation courte,<br><i>pratique et efficace.</i></h2><p class="lead rv" style="margin-top:30px">À la création de l\'école, nous avons misé sur une formation courte qui répond à la fois aux attentes des apprenantes et aux exigences modernes du métier. Aujourd\'hui, nos anciennes élèves exercent à Abidjan et dans tout le pays.</p></div><div class="pics rv"><figure><img class="ph" src="img/about/001.jpg" alt=""></figure><figure><img class="ph" src="img/about/111.jpg" alt=""></figure><figure><img class="ph" src="'+F+'29.jpg" alt=""></figure></div></div></section>'
 + '<section class="method"><div class="w g"><div class="stick"><div class="kicker rv">Pédagogie</div><h2 class="rv">80 % pratique,<br><i>20 % théorie.</i></h2><p class="lead rv">Chaque notion vue en cours est immédiatement appliquée en atelier, sur modèle, avec du matériel professionnel.</p><div class="ratio rv"><div class="r"><b>80%</b><span>Atelier & modèles</span></div><div class="r"><b>20%</b><span>Théorie & fascicules</span></div></div></div>'
 + '<div class="vals">' + "".join(f'<div class="rv"><img class="ph" src="{F}{p}" alt=""><span class="no">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n,p,t,d in [("01","maquillage/25.jpg","Suivi personnalisé","Chaque apprenante est accompagnée individuellement par ses formateurs."),("02","32.jpg","Évaluations régulières","Des contrôles pratiques et théoriques tout au long du cursus."),("03","33.jpg","Fascicules de cours","Des supports clairs, conçus par nos formateurs.")]) + '</div></div></section>'
 + '<div class="strip">' + "".join(f'<div><img class="ph" src="{p}" alt=""></div>' for p in [F+"coiffure/4.jpg",F+"esthetique/7.jpg","img/appareil.jpg",F+"massage/1.jpg",F+"onglerie/1.jpg",F+"maquillage/9.jpg"]) + '</div>'
 + '<section class="sec dark"><div class="w">' + H("Corps enseignant","Des professionnels","du métier.","Esthéticiennes, coiffeurs, cosméticiens, médecins, pharmaciens, maquilleurs, masseurs et décorateurs.") + '<div class="track">' + "".join(
   f'<div class="ac rv"><div class="im"><img src="img/{p}" alt="" style="object-position:top"></div><h4>Nom Prénom</h4><small>{r}</small></div>' for p,r in [("instructor/002.jpg","Esthétique"),("instructor/010.jpg","Coiffure"),("instructor/decoration1.jpg","Décoration"),("about/KOUAKOU.jpg","Maquillage")]) + '</div></div></section>'
 + re.search(r'<section class="lead-s">.*?</section>', idx, re.S).group(0), "ecole.html")

GAL = []
for cat, imgs in [("esthetique",["1","3","5","7","8","16"]),("coiffure",["1","2","3","4","6","15"]),("maquillage",["1","3","4","5","57","9"]),("onglerie",["1","2","3","4","5","10"]),("massage",["1","2","3","4","5","8"]),("decoration",["12","13","14","15","16"])]:
    GAL += [(f"{cat}/{i}.jpg", cat, cat.capitalize().replace("Esthetique","Esthétique").replace("Decoration","Décoration")) for i in imgs]
import random; random.Random(4).shuffle(GAL)
page("galerie.html","Galerie","Photos des ateliers, réalisations des élèves et stages IGMK Formation.",
 hero(F+"maquillage/5.jpg","Galerie","La beauté","en images.","Ateliers, réalisations des élèves, stages et vie de l'école.")
 + '<section class="sec"><div class="w"><div class="filters">' + "".join(f'<button data-f="{k}"{" class=on" if k=="all" else ""}>{t}</button>' for k,t in [("all","Tout"),("esthetique","Esthétique"),("coiffure","Coiffure"),("maquillage","Maquillage"),("onglerie","Onglerie"),("massage","Massage"),("decoration","Décoration")]) + '</div>' + mosaic(GAL, "gal") + '</div></section>', "galerie.html")

page("contact.html","Contact","Contactez IGMK Formation à Yopougon – Millionnaire, Abidjan.",
 hero(F+"esthetique/6.jpg","Contact","Venez nous","rencontrer.","Nos équipes vous accueillent du lundi au vendredi, de 8h à 17h, à Yopougon – Millionnaire.",(),f'<a class="btn solid" href="{wa()}" target="_blank">Écrire sur WhatsApp</a>')
 + '''<section class="sec"><div class="w split"><div class="cinfo">
<div class="rv"><span class="kicker">Adresse</span><p>Yopougon – Millionnaire, Abidjan<br>28 BP 242 Abidjan 28</p></div>
<div class="rv"><span class="kicker">Téléphones</span><p><a href="tel:+2250707589081">07 07 58 90 81</a><br><a href="tel:+2250102939221">01 02 93 92 21</a><br><a href="tel:+2252522019710">25 22 01 97 10</a></p></div>
<div class="rv"><span class="kicker">E-mail</span><p><a href="mailto:info@igmk-formation.net">info@igmk-formation.net</a></p></div>
<div class="rv"><span class="kicker">Horaires</span><p>Lundi – Vendredi · 8h – 17h<br>Samedi & dimanche · fermé</p></div></div>
<iframe class="gmap rv" loading="lazy" title="Plan d'accès" src="https://www.google.com/maps?q=Yopougon+Millionnaire+Abidjan&output=embed"></iframe></div></section>''', "contact.html")

def CD(d,l): return f'<div class="ncd" data-end="{d}"><small>{l}</small><div><span><b data-u="d">00</b>jours</span><span><b data-u="h">00</b>heures</span><span><b data-u="m">00</b>min</span><span><b data-u="s">00</b>sec</span></div></div>'
NEWS = [ # (catégorie, filtre, date affichée, image, titre, texte, lien, fin du compte à rebours, libellé)
 ("Rentrée","rentree","1 nov. 2026","esthetique/1.jpg","Rentrée de <i>janvier 2027</i> : inscriptions ouvertes","Les inscriptions sont ouvertes pour les formations Esthétique et Coiffure. Places limitées à 20 apprenantes par salle.","formations.html","2027-01-12T08:00:00","Début des cours dans"),
 ("Promotion","promo","15 nov. 2026","onglerie/10.jpg","−15 % sur les <i>spécialisations</i>","Onglerie, maquillage, massage, décoration : remise sur toute inscription avant le 15 décembre.","specialisations.html","2026-12-15T23:59:59","Fin de l'offre dans"),
 ("Événement","event","10 nov. 2026","maquillage/57.jpg","Journée <i>portes ouvertes</i>","Visitez nos ateliers, rencontrez les formateurs et assistez à des démonstrations en direct.","contact.html","2026-12-06T09:00:00","Ouverture des portes dans"),
 ("Stage","stage","2 nov. 2026","coiffure/7.jpg","Début des stages, <i>promo 2026</i>","Nos apprenantes rejoignent plus de 40 instituts et salons partenaires pour trois mois de terrain.","stage.html","",""),
 ("Vie de l'école","vie","20 oct. 2026","massage/4.jpg","Un nouvel espace <i>massage & spa</i>","Une salle entièrement rééquipée pour les modules massage et soins du corps.","ecole.html","",""),
 ("Diplômées","vie","5 oct. 2026","coiffure/18.jpg","Cérémonie de remise des <i>certificats</i>","48 nouvelles professionnelles diplômées, en présence des familles et des partenaires.","diplomees.html","",""),
 ("Stage","stage","18 sept. 2026","esthetique/6.jpg","Trois nouveaux <i>instituts partenaires</i>","Cocody, Marcory et Bingerville rejoignent notre réseau de stage.","stage.html","",""),
]
f0 = NEWS[0]
page("actualites.html","Actualités","Rentrées, promotions, stages et événements de l'école IGMK Formation à Abidjan.",
 hero(F+"maquillage/25.jpg","Actualités","La vie","de l'école.","Rentrées, promotions, débuts de stage, événements : tout ce qui se passe chez IGMK.")
 + f'''<section class="sec"><div class="w"><div class="kicker rv" style="margin-bottom:34px">À la une</div><div class="nbox rv" style="height:auto"><article class="nit on" style="position:relative"><div class="im"><img class="ph" src="{F}{f0[3]}" alt=""></div><div class="tx" style="padding:clamp(34px,5vw,70px)"><span class="ntag">{f0[0]}</span><h3>{f0[4]}</h3><p>{f0[5]}</p>{CD(f0[7],f0[8])}<div class="when"><span>Publié le {f0[2]}</span><a href="{f0[6]}">En savoir plus →</a></div></div></article></div></div></section>'''
 + '<section class="sec ivory"><div class="w"><div class="filters">' + "".join(f'<button data-f="{k}"{" class=on" if k=="all" else ""}>{t}</button>' for k,t in [("all","Tout"),("rentree","Rentrée"),("promo","Promotions"),("stage","Stages"),("event","Événements"),("vie","Vie de l'école")]) + '</div><div class="ngrid">' + "".join(
   f'<a class="nc rv" data-cat="{k}" href="{h}"><div class="im"><img class="ph" src="{F}{im}" alt="" loading="lazy"><span class="ntag">{c}</span></div><div class="nb"><small>{d}</small><h3>{t}</h3><p>{x}</p>{CD(e,l) if e else ""}<span class="link">Lire →</span></div></a>' for c,k,d,im,t,x,h,e,l in NEWS[1:]) + '</div></div></section>', "actualites.html")

# ---------------- PRÉ-INSCRIPTION ----------------
FORMS = [("esthetique","Esthétique","6 mois + 3 mois de stage","esthetique/5.jpg","Formation longue"),
         ("coiffure","Coiffure","6 mois + 3 mois de stage","coiffure/4.jpg","Formation longue"),
         ("maquillage","Maquillage","2 semaines","maquillage/57.jpg","Spécialisation"),
         ("onglerie","Onglerie","2 semaines","onglerie/10.jpg","Spécialisation"),
         ("massage","Massage","2 semaines","esthetique/6.jpg","Spécialisation"),
         ("decoration","Décoration","2 semaines","maquillage/5.jpg","Spécialisation")]
COMMUNES = ["Yopougon","Abobo","Adjamé","Attécoubé","Cocody","Koumassi","Marcory","Plateau","Port-Bouët","Treichville","Bingerville","Songon","Anyama","Hors d'Abidjan"]
def CH(name, opts, multi=False): return f'<div class="chips" data-name="{name}">' + "".join(f'<label><input type="{"checkbox" if multi else "radio"}" name="{name}" value="{o}"><span>{o}</span></label>' for o in opts) + '</div>'
fcards = "".join(f'<label class="fcard"><input type="radio" name="formation" value="{k}" data-t="{t}" data-d="{d}" data-im="{F}{im}"><span class="fi"><img class="ph" src="{F}{im}" alt="" loading="lazy"></span><span class="ft"><small>{c}</small><b>{t}</b><em>{d}</em></span><i class="ok"></i></label>' for k,t,d,im,c in FORMS)
INS = f'''<section class="ins-top"><div class="w"><div class="crumb"><a href="index.html">Accueil</a> / Pré-inscription</div>
<h1>Réservez votre <i>place.</i></h1><p class="lead">2 minutes, sans paiement. Nous vous rappelons sous 24 h pour finaliser votre inscription.</p>
<ol class="steps"><li class="on"><b>1</b>Formation</li><li><b>2</b>Vos informations</li><li><b>3</b>Confirmation</li></ol></div></section>
<section class="ins"><div class="w ins-g">
<form class="ins-f" id="insf" novalidate>
<fieldset class="stp on" data-s="1"><legend>Quelle formation vous intéresse ?</legend><div class="fcards">{fcards}</div><p class="err" data-for="formation">Choisissez une formation.</p>
<h4>À quelle rentrée ?</h4>{CH("rentree",["Janvier 2027","Avril 2027","Je ne sais pas encore"])}<p class="err" data-for="rentree">Choisissez une rentrée.</p>
<div class="fnav"><span></span><button type="button" class="btn solid nx">Continuer →</button></div></fieldset>

<fieldset class="stp" data-s="2"><legend>Parlez-nous de vous</legend>
<div class="g2"><div class="f"><label for="nom">Nom</label><input id="nom" name="nom" autocomplete="family-name" placeholder="Ex. Konan" required></div>
<div class="f"><label for="prenom">Prénoms</label><input id="prenom" name="prenom" autocomplete="given-name" placeholder="Ex. Aya Marie" required></div></div>
<div class="f"><label for="tel">Numéro WhatsApp</label><div class="tel"><span>+225</span><input id="tel" name="tel" inputmode="numeric" autocomplete="tel-national" placeholder="07 07 00 00 00" required></div><small class="hint">10 chiffres. C'est sur ce numéro que nous vous recontactons.</small></div>
<div class="g2"><div class="f"><label for="commune">Commune</label><select id="commune" name="commune" required><option value="">Choisir…</option>{"".join(f"<option>{c}</option>" for c in COMMUNES)}</select></div>
<div class="f"><label for="age">Âge</label><select id="age" name="age"><option value="">Choisir…</option><option>Moins de 18 ans</option><option>18 – 25 ans</option><option>26 – 35 ans</option><option>Plus de 35 ans</option></select></div></div>
<h4>Votre expérience</h4>{CH("niveau",["Débutante","J'ai quelques bases","Je travaille déjà dans la beauté"])}
<h4>Comment nous avez-vous connus ? <small>(facultatif)</small></h4>{CH("source",["Facebook","TikTok","Instagram","Une ancienne élève","Bouche à oreille","Autre"])}
<div class="fnav"><button type="button" class="lnk pv">← Retour</button><button type="button" class="btn solid nx">Continuer →</button></div></fieldset>

<fieldset class="stp" data-s="3"><legend>Vérifiez et envoyez</legend>
<dl class="rec" id="rec"></dl>
<h4>Comment préférez-vous être recontacté(e) ?</h4>{CH("contact",["WhatsApp","Appel téléphonique"])}
<h4>À quel moment ?</h4>{CH("moment",["Matin (8 h – 12 h)","Après-midi (12 h – 17 h)","Peu importe"])}
<label class="cons"><input type="checkbox" id="cons"><span>J'accepte d'être recontacté(e) par IGMK Formation au sujet de ma demande. Mes données ne sont pas partagées.</span></label><p class="err" data-for="cons">Merci de cocher cette case.</p>
<div class="fnav"><button type="button" class="lnk pv">← Modifier</button><button type="submit" class="btn solid">Envoyer ma pré-inscription</button></div></fieldset>

<div class="done" id="done" hidden><div class="ck">✓</div><div class="kicker">Pré-inscription envoyée</div><h2>Merci <i id="dn">Aya</i> !</h2>
<p>Votre demande <b id="dref">PRE-2611-0058</b> est bien enregistrée. Une conseillère vous contacte <b id="dwhen">sous 24 h</b>.</p>
<ol class="nxt"><li><b>Nous vous appelons</b><span>Pour répondre à vos questions et fixer une visite.</span></li>
<li><b>Visite & dossier</b><span>Apportez une pièce d'identité, 2 photos d'identité et les frais d'inscription.</span></li>
<li><b>Rentrée</b><span id="drent">Début des cours le 12 janvier 2027 à Yopougon – Millionnaire.</span></li></ol>
<div class="row"><a class="btn solid" id="dwa" href="#" target="_blank">Suivre sur WhatsApp</a><a class="lnk" href="index.html">Retour à l'accueil</a></div></div>
</form>

<aside class="ins-a"><div class="card"><div class="kicker">Votre choix</div><div class="sel" id="sel"><div class="ph0">Aucune formation choisie</div></div>
<div class="cdx"><small>Rentrée de janvier dans</small><b id="cdd">—</b></div>
<ul class="why"><li>Aucun paiement à cette étape</li><li>20 apprenantes maximum par salle</li><li>Paiement échelonné possible</li><li>Stage en institut partenaire garanti</li></ul>
<a class="hlp" href="{wa("Bonjour, j'ai une question avant de me pré-inscrire.")}" target="_blank">Une question ? <b>Écrivez-nous sur WhatsApp</b></a></div></aside>
</div></section>
<script>(()=>{{
const f=document.getElementById('insf'),S=[...f.querySelectorAll('.stp')],tops=[...document.querySelectorAll('.steps li')],K='igmk-preinsc';let cur=1;
const v=n=>{{const e=f.querySelector('[name="'+n+'"]:checked');return e?e.value:(f.elements[n]&&f.elements[n].value||'')}};
const save=()=>{{const d={{}};[...new FormData(f)].forEach(([k,x])=>d[k]=x);try{{localStorage.setItem(K,JSON.stringify(d))}}catch(e){{}}}};
try{{const d=JSON.parse(localStorage.getItem(K)||'{{}}');Object.entries(d).forEach(([k,x])=>{{const r=f.querySelector('[name="'+k+'"][value="'+CSS.escape(x)+'"]');if(r)r.checked=true;else if(f.elements[k]&&f.elements[k].tagName)f.elements[k].value=x}})}}catch(e){{}}
const q=new URLSearchParams(location.search).get('f');if(q){{const r=f.querySelector('[name=formation][value="'+q+'"]');if(r)r.checked=true}}
const tel=f.elements.tel;tel.addEventListener('input',()=>{{const d=tel.value.replace(/\\D/g,'').slice(0,10);tel.value=d.replace(/(\\d{{2}})(?=\\d)/g,'$1 ')}});
const sel=()=>{{const r=f.querySelector('[name=formation]:checked');document.getElementById('sel').innerHTML=r?'<img src="'+r.dataset.im+'" alt=""><div><b>'+r.dataset.t+'</b><small>'+r.dataset.d+'</small>'+(v('rentree')?'<em>Rentrée : '+v('rentree')+'</em>':'')+'</div>':'<div class="ph0">Aucune formation choisie</div>'}};
f.addEventListener('change',()=>{{sel();save();f.querySelectorAll('.err.on').forEach(e=>{{const n=e.dataset.for;if(n==='cons'?f.querySelector('#cons').checked:v(n))e.classList.remove('on')}})}});f.addEventListener('input',e=>{{save();const x=e.target.closest('.f');if(x)x.classList.remove('bad')}});f.addEventListener('change',e=>{{const x=e.target.closest('.f');if(x)x.classList.remove('bad')}});sel();
const err=(n,b)=>{{const e=f.querySelector('.err[data-for="'+n+'"]');if(e)e.classList.toggle('on',b);return b}};
const bad=(el,b)=>{{el.closest('.f').classList.toggle('bad',b);return b}};
const ok=s=>{{let k=true;if(s===1){{if(err('formation',!v('formation')))k=false;if(err('rentree',!v('rentree')))k=false}}
 if(s===2){{if(bad(f.elements.nom,!f.elements.nom.value.trim()))k=false;if(bad(f.elements.prenom,!f.elements.prenom.value.trim()))k=false;if(bad(tel,tel.value.replace(/\\D/g,'').length!==10))k=false;if(bad(f.elements.commune,!f.elements.commune.value))k=false}}
 if(s===3&&err('cons',!f.querySelector('#cons').checked))k=false;return k}};
const go=n=>{{cur=n;S.forEach(x=>x.classList.toggle('on',+x.dataset.s===n));tops.forEach((l,i)=>{{l.classList.toggle('on',i+1===n);l.classList.toggle('ok',i+1<n)}});
 if(n===3){{const r=f.querySelector('[name=formation]:checked');document.getElementById('rec').innerHTML=[['Formation',r.dataset.t+' · '+r.dataset.d,1],['Rentrée',v('rentree'),1],['Nom',f.elements.prenom.value+' '+f.elements.nom.value.toUpperCase(),2],['WhatsApp','+225 '+tel.value,2],['Commune',v('commune'),2],['Expérience',v('niveau')||'—',2]].map(([a,b,s])=>'<div><dt>'+a+'</dt><dd>'+b+'</dd><button type="button" data-go="'+s+'">Modifier</button></div>').join('')}}
 document.querySelector('.ins-top').scrollIntoView({{behavior:'smooth'}})}};
f.addEventListener('click',e=>{{if(e.target.closest('.nx')&&ok(cur))go(cur+1);if(e.target.closest('.pv'))go(cur-1);const g=e.target.closest('[data-go]');if(g)go(+g.dataset.go)}});
f.addEventListener('submit',e=>{{e.preventDefault();if(!ok(3))return;const ref='PRE-2611-'+String(58+Math.floor(Math.random()*40)).padStart(4,'0');
 S.forEach(x=>x.classList.remove('on'));tops.forEach(l=>{{l.classList.remove('on');l.classList.add('ok')}});const d=document.getElementById('done');d.hidden=false;
 document.getElementById('dn').textContent=f.elements.prenom.value.split(' ')[0];document.getElementById('dref').textContent=ref;
 const m=v('moment');document.getElementById('dwhen').textContent=(v('contact')==='Appel téléphonique'?'par téléphone':'sur WhatsApp')+' sous 24 h'+(m&&m!=='Peu importe'?', '+m.split(' (')[0].toLowerCase():'');
 const rt=v('rentree');document.getElementById('drent').textContent=rt==='Avril 2027'?'Début des cours en avril 2027 à Yopougon – Millionnaire.':rt==='Janvier 2027'?'Début des cours le 12 janvier 2027 à Yopougon – Millionnaire.':'Nous vous conseillerons sur la date la plus adaptée.';
 document.getElementById('dwa').href='https://wa.me/{WA_N}?text='+encodeURIComponent('Bonjour, je viens de me pré-inscrire sur le site (dossier '+ref+').');
 try{{localStorage.removeItem(K)}}catch(e){{}};document.querySelector('.ins-top').scrollIntoView({{behavior:'smooth'}})}});
const end=new Date('2027-01-12T08:00:00');const t=()=>{{const s=Math.max(0,end-new Date()),j=Math.floor(s/864e5);document.getElementById('cdd').textContent=j+' jours'}};t();
}})()</script>'''
page("inscription.html","Pré-inscription en ligne","Pré-inscrivez-vous en 2 minutes aux formations IGMK : esthétique, coiffure, maquillage, onglerie. Sans paiement, rappel sous 24 h.", INS)

print("Pages v2 générées.")

# --- mode édition (démo locale uniquement : IGMK_EDIT=1 python3 build.py) ---
import os
EDIT = os.environ.get("IGMK_EDIT") == "1"
for f in R.glob("*.html"):
    t = f.read_text()
    if EDIT and 'src="editor.js"' not in t:
        f.write_text(t.replace("</body>", '<script src="editor.js"></script>\n</body>', 1))
    elif not EDIT and 'src="editor.js"' in t:
        f.write_text(t.replace('<script src="editor.js"></script>\n', ''))
