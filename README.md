# Atlas Nexus — Immersive Beta

Application expérimentale indépendante publiée exclusivement sur `https://beta.atlasnexus.tech`.

## Isolation

- **Production** : `AtlasNexusTech/atlasnexustech.github.io` → `atlasnexus.tech`
- **Bêta** : `AtlasNexusTech/beta-atlasnexus` → `beta.atlasnexus.tech`
- Aucun fichier du site principal n’est importé au runtime.
- Le CTA renvoie volontairement vers le formulaire du site principal.

## Stack et build

React, TypeScript, Vite, Three.js, React Three Fiber et Drei.

```bash
npm ci
npm run test
npm run build
npm run preview
```

Le build statique est produit dans `dist/`. Le workflow `.github/workflows/pages.yml` publie uniquement ce répertoire avec GitHub Pages.

## DNS / GitHub Pages

Configuration attendue :

- Type : `CNAME`
- Nom : `beta`
- Cible : `atlasnexustech.github.io`
- TTL : `Auto` (ou 300 secondes pendant la mise en place)
- Le domaine personnalisé GitHub Pages du dépôt doit être `beta.atlasnexus.tech`.
- `public/CNAME` garantit que le build contient uniquement ce domaine.

Avec Cloudflare, commencer en **DNS only** pendant la validation TLS GitHub Pages. Le proxy peut être réactivé ensuite si nécessaire, sans règle Worker ni redirection vers le domaine principal.

## Déploiement

Un push sur `main` déclenche : `npm ci` → tests → build → publication de `dist/`.

Déploiement manuel :

```bash
gh workflow run pages.yml --repo AtlasNexusTech/beta-atlasnexus
```

## Rollback

Le rollback ne touche jamais `atlasnexus.tech` :

```bash
git revert <commit-beta>
git push origin main
```

Le workflow republie automatiquement la version précédente. En urgence, désactiver GitHub Pages sur le dépôt bêta ou retirer uniquement le CNAME DNS `beta`; ne pas modifier les entrées de l’apex.

## Promotion future

La promotion se fera par un changement explicite dans le dépôt de production après validation. La bêta ne partage ni build, ni workflow, ni dépendance runtime avec la homepage actuelle.
