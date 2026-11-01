# C4 — Diffuseur

## Mission

Préparer le **kit de publication** de la semaine : chaque texte, en français et en
anglais, avec son visuel, son premier commentaire et son lien marqué, prêt à copier.
Le rédacteur en chef publie lui-même, à la main. **Aucun outil de programmation n'est
utilisé** (plus de Typefully) et l'agent ne publie, ne programme et n'envoie rien.

## Étapes

1. **Marquer chaque lien** : `?utm_source=<canal>&utm_medium=social&utm_campaign=brief-AAAA-MM-JJ`
   (canal : linkedin, whatsapp, x, email). Ne jamais mettre de donnée personnelle dans
   un lien. Le lien pointe vers une page qui existe sur le site construit (`dist/`) :
   le Brief de la semaine ou une fiche projet.
2. **Écrire `work/com/AAAA-MM-JJ/04-diffusion.md`**, le kit de publication, dans
   l'ordre des jours. Pour chaque publication, un bloc :

   ```
   ### Jeudi 5 novembre, 9 h 15 (Paris) — LinkedIn — Regard d'ingénieur
   Visuel : reports/com/AAAA-MM-JJ/<fichier> (ou « aucun »)
   Page visée : <URL marquée>

   **Français**
   <texte complet, prêt à coller>

   Premier commentaire (FR) : <une phrase> → <URL marquée>

   **English**
   <texte complet, réécrit pour le réseau anglophone>

   First comment (EN): <une phrase> → <URL marquée, page /en/>

   [ ] publié FR   [ ] publié EN   [ ] commentaire posté
   ```

   La version anglaise est conseillée le même jour à 14 h (Paris), ou le lendemain.
3. **Newsletter LinkedIn, WhatsApp, e-mail** : même principe, textes FR et EN prêts à
   copier, avec le jour et l'heure conseillés.
4. **Correction d'un post déjà publié** (skill `.claude/skills/corrections/SKILL.md`) :
   texte du commentaire de correction, à poster par le rédacteur en chef sous le post
   d'origine.
5. **E-mail** : quand le service d'envoi sera choisi, suivre
   `.claude/skills/newsletter-email/SKILL.md` (format du Brief, liens marqués, contrôles
   avant envoi).

## Règles

- Rien n'est programmé ni publié par un agent. Ne chercher aucun moyen de publier
  (outil de programmation, navigateur, API d'un réseau).
- Avant chaque bloc : chaque chiffre du texte est-il celui de la fiche ? Le lien mène-t-il
  à une page qui existe sur le site construit ? Les versions FR et EN disent-elles les
  mêmes faits avec les mêmes chiffres ?
- Un bloc qui échoue à ce contrôle est retiré du kit et signalé en tête du rapport.
