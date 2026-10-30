# Koridor

Média bilingue (FR/EN) qui suit, projet par projet, les infrastructures et l'énergie en
Afrique. Le contenu est produit chaque semaine par une équipe de huit agents IA. Rien
n'est publié sans la validation du rédacteur en chef.

## Le cycle de la semaine

1. **Lundi, tôt le matin** : une tâche planifiée lance le chef d'orchestre
   (`agents/00-orchestrateur.md`).
2. Les agents travaillent dans l'ordre : Veilleur, Vérificateur, Documentaliste,
   Rédacteur, Traducteur, Éditeur, Rapporteur, Publieur.
3. Le Publieur ouvre une **pull request** contenant les données mises à jour, le Brief et
   le rapport de la semaine. Vous recevez un message avec le lien.
4. **Vous relisez** le rapport (2 minutes), puis la pull request :
   - si tout est bon, vous la fusionnez et le site se met à jour tout seul en 2 minutes ;
   - si vous voulez une correction, vous laissez un commentaire et elle est faite avant la
     fusion.
5. Le pôle communication (`agents/com/`) prend ensuite le relais : il prépare les
   posts de la semaine en brouillons dans Typefully, que vous programmez vous-même.
   Stratégie complète : `editorial/communication.md`.

## L'équipe

| Agent | Fiche | Rôle |
|---|---|---|
| Chef d'orchestre | `agents/00-orchestrateur.md` | Lance les agents dans l'ordre et arrête le cycle en cas d'erreur |
| Veilleur | `agents/01-veilleur.md` | Repère les faits nouveaux dans les sources surveillées |
| Vérificateur | `agents/02-verificateur.md` | Confirme, met en attente ou écarte chaque fait |
| Documentaliste | `agents/03-documentaliste.md` | Met à jour la base projets |
| Rédacteur | `agents/04-redacteur.md` | Écrit les fiches et le Brief en français |
| Traducteur | `agents/05-traducteur.md` | Produit la version anglaise |
| Éditeur | `agents/06-editeur.md` | Relit, vérifie les chiffres, contrôle le rendu |
| Publieur | `agents/07-publieur.md` | Construit le site et ouvre la pull request |
| Rapporteur | `agents/08-rapporteur.md` | Rédige le compte rendu de la semaine |

## Le pôle communication

| Agent | Fiche | Rôle |
|---|---|---|
| Directeur de la communication | `agents/com/00-directeur-com.md` | Lance le cycle communication et vous envoie le récapitulatif |
| Stratège | `agents/com/01-stratege.md` | Plan de la semaine : quoi dire, où, quand |
| Plume sociale | `agents/com/02-plume.md` | Textes FR/EN pour LinkedIn, X, WhatsApp, e-mail |
| Studio visuel | `agents/com/03-studio.md` | Carrousel PDF et visuels aux couleurs Koridor |
| Diffuseur | `agents/com/04-diffuseur.md` | Brouillons Typefully non programmés, liens marqués |
| Vigie et engagement | `agents/com/05-vigie.md` | Posts du secteur à commenter, réponses aux commentaires |
| Référenceur | `agents/com/06-referenceur.md` | Contrôle SEO et aperçus de partage du site |
| Relais et partenariats | `agents/com/07-relais.md` | Chaque mois, dix relais à approcher avec un message préparé |
| Analyste | `agents/com/08-analyste.md` | Ce qui a marché, chiffres à l'appui |

Aucun agent ne publie, ne commente ni n'envoie de message : vous gardez la main.

## Les skills

Les agents appliquent six fiches de méthode rangées dans `.claude/skills/` : vérification
des faits, archivage des sources, corrections, écriture sans tics, chiffres et données,
newsletter e-mail. Ce sont des adaptations en français de skills de la collection
claude-skills-journalism (Joe Amditis, licence MIT). Chaque fiche d'agent dit lesquelles
lire. Détail, origine et ce qui n'a pas été repris : `.claude/skills/README.md`.

## Organisation du dépôt

```
.claude/skills/ méthodes partagées par les agents (vérification, archivage, écriture…)
agents/       consignes de chaque agent
editorial/    charte éditoriale, règles des sources (sources.md) et registre lisible (registre.md)
data/         base projets (projects.json), registre des sources (sources.json), Briefs, format des données
site/         générateur du site, styles, configuration
scripts/      contrôle des données, plan et fusion de la collecte, registre lisible
reports/      un rapport par semaine
.github/      contrôle des pull requests et publication sur GitHub Pages
```

## Commandes

```
python3 scripts/validate.py   # contrôle les données et le registre des sources
python3 scripts/registre_md.py # régénère editorial/registre.md après une modification du registre
python3 site/build.py         # génère le site dans dist/ (avec aperçus de partage et sitemap.xml)
python3 scripts/og_image.py --fonts DOSSIER  # régénère les images de partage (voir le script)
python3 scripts/archiver.py --demo --out /tmp/archives  # teste l'archivage des sources sans réseau
```

## Archivage des sources

Chaque lundi vers 3 h 40, et après chaque fusion qui modifie `data/projects.json`, le
workflow « Archivage des sources » (`.github/workflows/archives.yml`) lance
`scripts/archiver.py`. Il vérifie que chaque source citée répond encore et en garde une
copie datée dans la Wayback Machine. L'état est rangé sur la branche `archives-sources` ;
le Rapporteur en reprend le résumé dans le rapport de la semaine (sources devenues
injoignables, sources sans copie). Rien à configurer : le workflow n'a besoin d'aucune
clé.

## Mesure d'audience

Le site utilise **Umami Cloud**, sans cookie ni donnée personnelle : pas de bandeau de
consentement à afficher. Il compte les visites et pages vues, et `site/audience.js` ajoute
les clics utiles à la rédaction : sources officielles ouvertes depuis les fiches, module
qui envoie vers une fiche, filtres, carte, recherches (dont celles sans résultat), lecture
complète d'une fiche, clics vers le Brief, changement de langue.

Chaque lundi vers 4 h, le workflow « Bilan d'audience » (`.github/workflows/audience.yml`)
interroge Umami avec `scripts/audience.py` et range le bilan de la semaine sur la branche
`stats-audience`. Le Rapporteur le reprend dans le rapport de la pull request. Pour tester la
mise en forme sans compte : `python3 scripts/audience.py --demo --out /tmp/audience`.

## Réglages (`site/config.json`)

- `show_unverified` : affiche les fiches « à confirmer » avec une étiquette. À passer à
  `false` quand la base confirmée sera assez riche.
- `analytics.website_id` : l'identifiant du site dans Umami Cloud. Tant qu'il est vide,
  aucun traceur n'est ajouté au site. La clé d'accès aux chiffres, elle, n'est jamais dans
  le dépôt : elle est rangée dans le secret GitHub `UMAMI_API_KEY`. Sur le plan gratuit,
  qui ne donne pas de clé, on range à la place le lien de partage du tableau de bord dans
  le secret `UMAMI_SHARE_URL`.
- `newsletter_signup_url` : l'adresse du formulaire d'inscription du service d'envoi
  (Buttondown, Brevo…). Tant qu'elle est vide, le site annonce une ouverture prochaine.

## Mise en ligne (une seule fois)

Dans le dépôt GitHub : Settings → Pages → Source : **GitHub Actions**.

## Les sources

Koridor s'appuie d'abord sur les émetteurs officiels : banques multilatérales, bailleurs,
institutions régionales, États, régulateurs et sociétés publiques. Le registre
(`data/sources.json`, lisible dans `editorial/registre.md`) recense 155 sources, avec leur
site, leur compte X et leur page LinkedIn officiels, relevés sur leur propre site. Chaque
semaine, le Veilleur collecte ces trois canaux avec Apify ; le budget maximal est d'environ
1 $ par semaine (1,40 $ la semaine où s'ajoutent les sources mensuelles).

Pour ajouter une source, demandez-le simplement : elle sera vérifiée (lien constaté sur le
site officiel) puis proposée dans une pull request.
