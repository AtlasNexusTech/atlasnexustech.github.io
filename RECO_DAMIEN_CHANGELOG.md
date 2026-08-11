# AtlasNexus v2 — Refonte selon les recos de Damien (2026-08-11)

**Prévisualisation locale : http://localhost:8125/** (copie de travail `~/atlasnexus-site-v2/`, prod intacte)
Relance du serveur : `cd ~/atlasnexus-site-v2 && python3 -m http.server 8125 --bind 0.0.0.0`

## Mapping reco → changement

| Reco Damien | Appliqué |
|---|---|
| **Promesse A** (l'équipe fantôme, 48 h) | H1 : « L'équipe que vous n'avez pas les moyens d'embaucher, installée chez vous en 48 heures. » |
| Hero complet proposé | Sous-titre mails/devis/relances/rapports + « Y compris le dimanche, sans vous » + ligne de réassurance « Livré en 48 h. Code sur GitHub. Vous ne payez pas si l'agent ne tourne pas. » |
| Prix retiré du CTA principal | CTA primaire = « Réserver mon diagnostic 30 min — gratuit » (→ #contact), secondaire = « Voir un agent tourner en vrai (2 min) » (→ /ia-agentique/). Plus aucun « 50€ » dans le hero ni le CTA mobile |
| **Bloc Avant/Après** | Section dédiée sous le hero, tableau 2 colonnes (5 lignes exactes de Damien), responsive avec labels empilés sur mobile |
| **Une échelle, une porte** | Offres A/B/C remplacées par Étape 0 (premier agent 48 h, 50€/90€ repositionné « victoire rapide »), Étape 1 (Système Solo, 900–1 800€), Étape 2 (« Votre équipe reste en vie », 90–190€/mois) |
| Coaching & web hors de la home | Reléguées à une ligne discrète sous les offres + liens footer (/training/, /demos-web/) |
| **Renversement du risque** | Section Garantie dédiée : 48 h sinon rien payé + 30 jours / 5 h par semaine sinon je continue gratuitement + conditions (accès, onboarding, CGV) |
| « Pourquoi » côté client | Réécrit : « Vous restez propriétaire. Tout tourne chez vous. » — 6 cartes bénéfices (propriété, victoire 48 h, validation humaine, formation, données locales, interlocuteur direct) |
| Réalisations → résultats | Intro reformulée « Voyez par vous-même » + « références clients sur demande ». **Pas de chiffres inventés** (Damien : aller chercher les vrais chiffres d'abord — à faire avec 3 derniers clients avant d'ajouter des métriques) |
| Rareté honnête | « Je prends 4 déploiements par mois pour garantir le délai de 48 h. » (fin de section Méthode) |
| CTA formulaire 5 champs → 2 | Email + « Décrivez votre semaine type » uniquement (formsubmit.co conservé) |
| Labs hors de la home | Section Products/Labs supprimée (+ script carousel), remplacée par « Comment c'est construit » (4 cartes de réassurance technique sans jargon) ; lien Labs discret en footer et dans la carte R&D |
| Title/meta SEO | « Atlas Nexus — Vos agents IA font tourner votre activité. Vous récupérez vos week-ends. » (title, description, OG, Twitter, JSON-LD) |
| Zéro jargon dans le parcours de vente | Vérifié : aucun LLM/RAG/ERC-8004/x402/MCP/Celo dans la home (la carte « UI Design System » a été reformulée) |

## Modifs techniques
- `index.html` seul modifié (56 335 → ~45 600 chars). CSS/JS du design system intacts.
- Styles additionnels inline `<style>` : `.ba-table` (avant/après), `.guarantee-card`, override `.hero-title` (promesse longue → clamp 2.1–3.55rem).
- Script carousel Labs supprimé ; script reveal/IntersectionObserver conservé (réinjecté).
- Testé Playwright 1440px + 390px : 0 erreur JS console.

## ⚠️ Avant tout déploiement en prod
1. Les tests pytest du repo prod (28/28) attendent l'ancienne structure (`offer-price` = ["50","40"], anciens marqueurs) → **mettre à jour les tests en même temps**.
2. La garantie « 5 h/semaine sinon gratuit » doit être alignée dans les **CGV** (point 4 de Damien).
3. Version EN (`/en/`) non traduite — à faire si la v2 est validée.
4. Chiffres de résultats clients à collecter avant d'enrichir « Réalisations » (Damien insiste : un avant/après vend, un artefact non).


---

# Amélioration UI/UX drastique + image de marque (2026-08-11, itération 2)

## Image hero
- `hero-orb` (sphère CSS floue) **remplacée par `assets/atlasnexusfond.jpg`** (logo 3D verre + vagues de particules, copié du bureau Windows).
- Intégration : ancrée à droite, masque dégradé vers la gauche + voile de lisibilité côté texte, dérive lente (26 s, désactivée si `prefers-reduced-motion`), préchargée (`<link rel=preload>`).
- **Dark mode** : opacité 38 % + overlay bleu nuit — rendu premium vérifié.
- Mobile : image atténuée (50 %/22 % dark) décalée à droite, voile renforcé.

## Nouvelle couche `css/v2.css` (12 Ko, remplace le <style> inline)
- **Nav** : CTA « Contact » → « Diagnostic 30 min ».
- **Hero** : puces de réassurance avec ✓ verts (48 h · GitHub · pas payé si ça ne tourne pas).
- **Avant/Après** : icônes ✗ rouges / ✓ verts par ligne, reveal en cascade, hover bleuté, ombre portée, labels empilés sur mobile.
- **Offres** : pastilles d'étape numérotées (0/1/2), checklists ✓ par carte, CTA pleine largeur (primaire dégradé / ghost), **Étape 1 « Recommandé — le vrai levier » mise en avant** (bordure bleue, scale 1.03, badge).
- **Garantie** : carte premium à bordure dégradée + sceau vert « Garantie écrite » + 2 volets (48 h gratuit / 5 h par semaine sinon je continue).
- **Méthode** : ligne de timeline reliant les 3 étapes (desktop).
- **Comment c'est construit** : icônes dans des tuiles dégradées.
- **Contact** : badge live « 4 déploiements par mois — créneaux ouverts » (point pulsant), focus states avec halo bleu, bouton avec flèche.
- **Footer** : restructuré 3 colonnes (marque+tagline / Naviguer / Aller plus loin) + baseline légale.
- Global : scroll-margin ancres, ::selection bleu, soulignements animés sur liens inline, focus-visible.

## Vérifications
- Playwright desktop 1440px (light + dark) + mobile 390px : **0 erreur JS console**.
- Poids ajouté : image 49 Ko + CSS 12 Ko.


---

# Redesign du tableau Avant/Après (itération 3)

L'ancien tableau 2 colonnes est remplacé par un **flux de transformation** :
- **Paires alignées** sur une grille `1fr / flèche / 1fr` : chaque problème (carte grise en pointillés, ✗ rouge en pastille) est relié par une **flèche bleue dégradée** à son état résolu (carte blanche élevée, bordure et ombre vertes, ✓ vert en pastille).
- **En-têtes chips** : « Aujourd'hui » (neutre, icône horloge) vs « Dans 30 jours, avec vos agents » (vert dégradé, icône étoile).
- **Micro-interactions** : hover d'une paire → la carte « après » se soulève et la flèche grossit.
- **Bannière de résultat** en dégradé bleu marine : « Résultat : vos soirées et vos week-ends de retour. » + CTA pilule blanche « Voir comment on y va » → #offers (pont direct vers l'échelle d'offres).
- **Mobile** : chaque paire devient une carte conteneur empilée (avant ↓ après), flèche pivotée à 90°.
- **Dark mode** complet (cartes ardoise, verts adaptés).
- Reveal en cascade conservé. 0 erreur JS (Playwright light/dark/mobile).


---

# Corrections bugs visuels + retours utilisateur (itération 4)

1. **Header « Atlas Nexus »** : marque passée en Rubik 800 (tracking serré, hover bleu) — taille desktop 1.15rem, mobile ≤640px réduite à .8rem pour ne plus tronquer (vérifié à 390px).
2. **Image hero (jpeg trop grande)** : hauteur 118% → 94%, largeur max 56%, ancrée bas-droite, double masque dégradé (horizontal + vertical haut), dérive ralentie (30 s, scale 1.03).
3. **Méthode (gros bug visuel)** : suppression de la ligne de timeline qui traversait les titres Brief/Build/Livraison ; la phrase de rareté devient un **panneau pilule centré** avec point pulsant vert (« Je prends 4 déploiements par mois… »).
4. **Offre « vrai levier » revue** : Étape 1 = **« Accompagnement + écosystème multi-agentique » à 150€** (au lieu de Système Solo 900–1 800€). Checks : audit, écosystème multi-agents connecté aux outils, accompagnement personnalisé, documentation+formation.
5. **Section Labs restaurée à l'identique** (design d'origine « Prototypes, open source et R&D », id #labs) entre « Comment c'est construit » et Contact, avec son **carousel animé** (script réinjecté, contrôles pause/flèches, SVG defs Solana déjà présents). La carte R&D de « Comment c'est construit » pointe désormais l'ancre #labs.
6. **Bug préexistant corrigé** : chips de la carte « Vérification d'identité agentique » illisibles en dark (classes Tailwind `dark:` non compilées dans le build) → normalisation des chips #labs en dark via v2.css.

Vérifications Playwright : desktop light/dark + mobile 390px, 0 erreur JS console.


---

# Itération 5 : typographie, tirets, effet particules

1. **Zéro tiret cadratin** : les 18 occurrences remplacées contextuellement (deux-points, virgules, points médians « · », reformulations : « Réserver mon diagnostic gratuit de 30 min », « Recommandé · le vrai levier », title/meta « Atlas Nexus : Vos agents IA… »).
2. **Header « Atlas Nexus »** : Rubik 800 (trop gras) → **Nunito Sans 700** (la police de texte du site), 1.05rem desktop / .82rem mobile, tracking léger, hover bleu conservé. Vérifié non tronqué à 390px.
3. **Effet particules connectées restauré** : le canvas antigravity (55 particules, connexions, attraction souris, glow curseur) était enseveli sous l'image + voile → remonté au-dessus (`#antigravity-canvas{z-index:2}`) et visibilité boostée (alpha connexions 0.07→0.11, near-mouse 0.12→0.22, épaisseur 0.5-1.4px, glow 0.09). L'effet « constellation qui suit la souris » de l'ancien accueil est de retour, par-dessus l'image de marque, en light et dark.

Playwright light/dark/mobile : 0 erreur JS.


---

# Itération 6 : wording temps libre + espacement puces hero

1. **Wording** : « soirées / week-ends » remplacé partout par « engagement quotidien / temps libre » (0 occurrence restante) :
   - Title/OG/Twitter : « …Moins d'engagement quotidien, plus de temps libre. »
   - Bannière résultat : « Résultat : moins d'engagement quotidien, plus de temps libre. »
   - Footer : « …pendant que vous retrouvez du temps libre. »
   - Placeholder formulaire : « Ex : les mails, les devis et les relances débordent sur mon temps personnel… »
2. **Espacement puces de réassurance** (« Livré en 48 h · Code sur GitHub, à vous · … ») : gap vertical .55→.85rem, marge haute 1.9rem, **marge basse 1.5rem**, + padding bas de hero 4.5rem sur mobile pour dégager le CTA sticky.


---

# Itération 7 : refonte drastique de la section Réalisations

**Avant** : 3 petites cartes texte avec une pastille ou une icône, aucune preuve visuelle.
**Après** : un **bento portfolio** de 6 projets avec captures réelles.

- **Captures automatisées** : screenshots Playwright 1280x800 de chaque projet, bandeaux « démo » et filigrane « DÉMO CONFIDENTIELLE » masqués à la capture (injection CSS `body::after{display:none}`), export JPEG q74-76 dans `assets/shots/` (43-99 Ko chacun). La capture AZ Bois est clippée à 1280x700 pour supprimer la bande blanche sous le hero.
- **Grille bento** : carte vedette (Refontes web artisans) sur 2 colonnes x 2 lignes en grid interne `auto 1fr auto` (l'image remplit toute la hauteur, zéro espace mort), 5 cartes secondaires. Responsive : 2 colonnes sur tablette, 1 colonne sur mobile.
- **Cadre navigateur** sur chaque carte : 3 pastilles + pilule d'URL (demos-web · atlasnexus.tech, markets-dashboard, framer-motion-ui, ia-receptionniste, datatoolkit, atlas-desk) : lecture immédiate « ce sont de vrais sites en ligne ».
- **Badge catégorie** en bas à gauche de la capture (Refonte web, Dashboard temps réel, React · animations, Agent IA, Outil navigateur, Open source) avec pastille de couleur par univers.
- **Interactions** : lift de la carte au survol, zoom lent de la capture (scale 1.045), flèche qui passe en pastille bleue dégradée et pivote à -45°.
- **Pied de section** : note « livré documenté, code sur GitHub quand le client le souhaite » + CTA « Toutes les démos web ».
- Dark mode complet, 0 erreur JS, vérifié desktop 1440px et mobile 390px.
