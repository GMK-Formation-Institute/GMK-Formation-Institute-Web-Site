# Site public — IGMK Formation

Site vitrine de l'Institut GMK Formation (Abidjan) : école de coiffure et d'esthétique.

Site statique (HTML, CSS, JavaScript), sans dépendance à installer.

## Pages

| Page | Fichier |
|---|---|
| Accueil | `index.html` |
| L'école, diplômées, galerie | `ecole.html`, `diplomees.html`, `galerie.html` |
| Formations | `formations.html`, `esthetique.html`, `coiffure.html`, `specialisations.html` |
| Le stage | `stage.html` |
| Actualités | `actualites.html` |
| Pré-inscription en ligne | `inscription.html` |
| Contact | `contact.html` |

## Voir le site en local

```bash
python3 -m http.server 8000
```

Puis ouvrir http://localhost:8000.

## Modifier le site

`index.html` sert de modèle : l'en-tête, le menu, le pied de page et les styles des pages intérieures en sont extraits.
Le contenu des pages intérieures est dans `build.py`. Après une modification :

```bash
python3 build.py
```

Styles et scripts propres aux pages intérieures : `inner.css`, `inner.js`.

## À compléter avant la mise en ligne

- Confirmer le numéro WhatsApp utilisé dans les boutons (`WA_N` dans `build.py`).
- Remplacer les tarifs « XXX 000 FCFA » par les vrais montants.
- Le formulaire de pré-inscription est une maquette : l'envoi est simulé tant que l'espace de gestion n'est pas en place.
