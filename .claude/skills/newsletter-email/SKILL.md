---
name: newsletter-email
description: Choisir le service d'envoi, préparer et contrôler l'envoi par e-mail du Brief du lundi (délivrabilité, désinscription, RGPD, liens marqués). À utiliser par le Publieur et le Diffuseur, et pour la décision du service d'e-mail (Brevo, Buttondown ou Substack).
---

# Newsletter e-mail

Adapté de `newsletter-publishing` (collection claude-skills-journalism de Joe Amditis,
licence MIT, voir `../README.md`), ramené au Brief du lundi et au droit européen (le
rédacteur en chef est en France ; une partie des lecteurs aussi).

Tant que `newsletter_signup_url` est vide dans `site/config.json`, ce skill sert à
préparer la décision du § 9 de `editorial/communication.md`. Ensuite il sert chaque
lundi.

## Choisir le service

Critères à vérifier sur le site de chaque service le jour du choix (les offres
changent) :
- formulaire d'inscription intégrable au site statique, avec double confirmation ;
- envoi depuis un domaine Koridor (SPF, DKIM, DMARC gérés par le service une fois le
  domaine vérifié) ;
- désinscription en un clic gérée par le service ;
- import et export de la liste en CSV, pour ne pas dépendre du service ;
- envoi programmé, statistiques d'ouverture et de clic, marqueurs UTM conservés ;
- hébergement des données et contrat de sous-traitance RGPD ;
- prix à 150, 1 000 et 5 000 abonnés.

Le choix revient au rédacteur en chef. Le skill ne fait que préparer la comparaison.

## Avant le premier envoi (une fois)

1. Domaine propre (§ 9.4 de la stratégie) : sans domaine, l'envoi part depuis le domaine
   du service et passe plus souvent en spam.
2. Enregistrements DNS donnés par le service : SPF, DKIM (clé d'au moins 1 024 bits),
   DMARC au moins `p=none`, puis `p=quarantine` quand les envois sont stables.
3. Adresse d'expédition sur le domaine (`brief@…`) et adresse de réponse lue par le
   rédacteur en chef.
4. Envoi de test vers une adresse Gmail et une adresse Outlook : le message arrive en
   boîte de réception, pas en spam.

## Exigences des grandes messageries

Gmail et Yahoo depuis février 2024, Outlook depuis mai 2025 :
- SPF et DKIM valides, l'un des deux aligné sur le domaine de l'adresse d'expédition ;
- DMARC publié ;
- désinscription en un clic (en-têtes `List-Unsubscribe` et
  `List-Unsubscribe-Post`, norme RFC 8058), traitée sous deux jours, plus un lien
  visible dans le message ;
- taux de plaintes pour spam sous 0,3 % (Google vise 0,1 %), à suivre dans Google
  Postmaster Tools quand le volume le permet.

Le seuil « gros expéditeur » de Gmail est de 5 000 messages par jour : Koridor en est
loin, mais les services appliquent ces règles à tous. Depuis novembre 2025, Gmail
rejette les messages non conformes au lieu de les retarder.

## RGPD

- Consentement explicite : case non précochée, texte qui dit ce qu'on reçoit (« Le Brief
  du lundi, un e-mail par semaine »).
- Double confirmation (lien de validation envoyé par e-mail) : elle prouve le
  consentement et protège la liste.
- Lien vers la politique de confidentialité au formulaire et dans chaque envoi.
- Désinscription sans connexion, export et suppression des données sur demande.
- Jamais de liste achetée, jamais d'import de contacts LinkedIn ou WhatsApp sans leur
  accord (règle 6 de la stratégie).

## Le Brief au format e-mail

- Objet : 60 caractères au plus, le fait principal (gabarit de la Plume sociale).
- Texte d'aperçu (préheader) : la deuxième information de la semaine.
- Ordre : Les projets qui ont bougé (une ligne et un lien par projet), Le deal, Le
  décryptage (chapô et lien vers la page du Brief), Échéances si la rubrique existe.
- Liens complets, sans raccourcisseur, chacun avec `utm_source=email`,
  `utm_medium=newsletter`, `utm_campaign=brief-AAAA-MM-JJ`.
- Version texte brut jointe, images avec texte alternatif, poids sous 100 ko.
- Pied : adresse d'expédition, lien de désinscription, lien vers la politique de
  confidentialité.

## Chaque lundi (Publieur, après la fusion seulement)

1. Construire l'e-mail depuis `data/briefs/AAAA-MM-JJ.json` de `main`, jamais depuis la
   branche de veille non fusionnée.
2. Vérifier chaque chiffre contre la fiche du site (skill `chiffres-et-donnees`) et le
   texte avec le skill `ecriture-koridor`.
3. Contrôler les liens (aucun 404) et les marqueurs UTM.
4. Créer l'envoi en brouillon programmé pour 7 h (heure de Paris), ou en simple
   brouillon si le rédacteur en chef préfère valider : aucun agent n'envoie sans son
   accord (règle 1 de la stratégie).

## Suivi (Analyste)

Chaque semaine : envoyés, délivrés, ouvertures, clics, désinscriptions, plaintes.
Repères de la presse spécialisée cités par la source d'origine : ouverture de 40 % ou
plus, clic de 4 % ou plus, désinscription sous 0,5 % par envoi. Ces repères sont
américains et indicatifs ; la base de comparaison de Koridor est son propre historique.
Les taux d'ouverture sont faussés par la protection de la vie privée d'Apple Mail : le
clic est le chiffre le plus fiable.
