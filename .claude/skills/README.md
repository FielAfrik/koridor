# Skills de Koridor

Un skill est une fiche de méthode qu'un agent lit avant une tâche précise. Claude Code
charge automatiquement les skills de ce dossier quand il travaille dans le dépôt ; les
fiches des agents (`agents/`) indiquent en plus lesquels lire, pour que les sous-agents
lancés par le chef d'orchestre les appliquent aussi.

| Skill | Ce qu'il apporte | Agents qui l'utilisent |
|---|---|---|
| `verification-faits` | Découper un candidat en affirmations, méthode SIFT, contrôles par type de document, divergences, piste de vérification | Vérificateur, Éditeur |
| `archivage-sources` | Copie Wayback datée de chaque source citée, contrôle des liens morts, conduite à tenir quand une source disparaît | Vérificateur, Éditeur, Rapporteur, chef d'orchestre |
| `corrections` | Correction visible et datée sur la fiche, Brief déjà paru, posts déjà publiés, journal des corrections | Documentaliste, Éditeur, Rapporteur, Diffuseur |
| `ecriture-koridor` | Tics d'écriture à supprimer en français et en anglais, relecture en deux passes | Rédacteur, Traducteur, Éditeur, Plume sociale |
| `chiffres-et-donnees` | Unités, devises, totaux, comparaisons, graphiques, données ouvertes, chiffres d'audience | Rédacteur, Éditeur, Studio visuel, Analyste, Rapporteur |
| `newsletter-email` | Choix du service, délivrabilité, RGPD, format e-mail du Brief | Publieur, Diffuseur, Analyste |

## Origine et licence

Ces six skills sont des adaptations en français de skills de la collection
claude-skills-journalism de Joe Amditis (https://github.com/jamditis/claude-skills-journalism,
version du 29 octobre 2026, commit a1e2709), publiée sous licence MIT. Le texte de la
licence est dans `LICENCE-claude-skills-journalism.txt`.

| Skill Koridor | Skill d'origine |
|---|---|
| `verification-faits` | `journalism-core/fact-check-workflow`, `journalism-core/source-verification` |
| `archivage-sources` | `research-toolkit/web-archiving` |
| `corrections` | `journalism-core/fact-check-workflow` (partie corrections) |
| `ecriture-koridor` | `journalism-core/ai-writing-detox` |
| `chiffres-et-donnees` | `journalism-core/data-journalism` |
| `newsletter-email` | `journalism-core/newsletter-publishing` |

Les originaux sont écrits pour des rédactions américaines (style AP, droit américain).
Ils ont été réécrits pour les règles de `editorial/charte.md` et `editorial/sources.md`,
qui l'emportent en cas de désaccord.

## Ce qui n'a pas été repris, et pourquoi

- `page-monitoring` : Koridor détecte déjà les nouvelles publications des sites
  officiels avec Apify et `data/veille/pages-vues.json`. Les outils du skill (Distill,
  UptimeRobot, Twarc) ne sont pas utilisés ici. Le contrôle des liens morts est fait par
  `scripts/archiver.py`.
- `newsroom-style` et les hooks `ap-style-check` et `ai-slop-detector` : écrits pour
  l'anglais et le style AP, ils signaleraient de fausses erreurs sur des textes en
  français. `ecriture-koridor` les remplace.
- Le hook `archive-reminder` : l'archivage est automatique (workflow « Archivage des
  sources »), un rappel ne sert à rien.
- `foia-requests`, `brazil-records-requests`, `interview-prep`, `crisis-communications`,
  les boîtes à outils vidéo, sécurité et développement : hors du travail de Koridor.

Pour mettre à jour un skill depuis la collection d'origine, comparer la nouvelle version
avec celle du commit a1e2709 et reporter les changements utiles à la main : ne jamais
écraser l'adaptation par l'original.
