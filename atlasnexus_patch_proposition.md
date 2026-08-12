# PROPOSITION DE PATCH — atlasnexus-site/index.html (non appliqué)
Vérifié le 11/08/2026 : le site a DÉJÀ GoatCounter (analytics actif sur atlasnexus.goatcounter.com).
Le vrai gap = preuve sociale + vente de la récurrence. Patchs proposés (à valider par Alexandre) :

## P1. Bloc Témoignages (à insérer après la section "why", avant "work")
Structure HTML (tailwind, à adapter au style du site) :
  <section id="testimonials" class="py-16 bg-surface">
    <div class="max-w-6xl mx-auto px-6">
      <h2 class="...">Ils m'ont fait confiance</h2>
      <div class="grid md:grid-cols-3 gap-6">
        <!-- 3 cartes: citation + nom + société + livrable -->
      </div>
    </div>
  </section>
⚠️ Utiliser UNIQUEMENT de vrais retours clients (demander par email aux 2-3 premiers clients des builds
   "refonte artisan/restaurant/santé/consultant" + UI design system). Ne jamais inventer de citations.

## P2. CTA récurrence dans l'offre A (déploiement 50€)
Actuellement : "déploiement sur votre infrastructure · clé en main 90€ · infogérance dès 15€/mois"
→ Ajouter sous le prix une ligne de valeur :
  "L'infogérance = votre agent mis à jour, surveillé et opérationnel en continu — 15€/mois,
   sans engagement. 10 clients = 150€/mois de revenu récurrent pour moi, zéro surprise pour vous."
→ Mettre un 2e bouton "Voir l'offre infogérance" à côté de "Demander un déploiement".

## P3. Preuve chiffrée dans le hero
Sous "Déploiement d'agent IA · 50€" : badge "X agents déployés · 100% livrés avec documentation"
(chiffre réel à tenir à jour — commence par 1-2 builds documentés).

## P4. Suivi de conversion (léger)
GoatCounter est déjà là → ajouter un événement de clic sur les boutons CTA :
  <script>document.querySelectorAll('a[href*="order-form"], a[href^="mailto"]')
    .forEach(a => a.addEventListener('click', () => goatcounter.count({event: true, path: 'cta:' + a.href})))</script>
→ permet de mesurer quelles offres génèrent des demandes.

## Ordre d'exécution recommandé
1. P2 (texte seul, 10 min, impact immédiat sur le panier moyen)
2. P4 (analytics CTA, 15 min, mesure avant/après)
3. P1 (après avoir collecté 2-3 vrais retours, 1-2 h)
4. P3 (quand le compteur de builds est > 2)
