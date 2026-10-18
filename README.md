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
5. Le Publieur prépare aussi trois brouillons de posts LinkedIn.

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

## Organisation du dépôt

```
agents/       consignes de chaque agent
editorial/    charte éditoriale et liste des sources (rangs A, B, C)
data/         base projets (projects.json), Briefs, format des données
site/         générateur du site, styles, configuration
scripts/      contrôle des données
reports/      un rapport par semaine
.github/      contrôle des pull requests et publication sur GitHub Pages
```

## Commandes

```
python3 scripts/validate.py   # contrôle les données
python3 site/build.py         # génère le site dans dist/
```

## Réglages (`site/config.json`)

- `show_unverified` : affiche les fiches « à confirmer » avec une étiquette. À passer à
  `false` quand la base confirmée sera assez riche.
- `newsletter_signup_url` : l'adresse du formulaire d'inscription du service d'envoi
  (Buttondown, Brevo…). Tant qu'elle est vide, le site annonce une ouverture prochaine.

## Mise en ligne (une seule fois)

Dans le dépôt GitHub : Settings → Pages → Source : **GitHub Actions**.
