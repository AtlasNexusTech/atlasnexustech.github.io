window.dashboardData = {
  focus: {
    title: "Démonstration de pilotage opérationnel",
    copy: "Données synthétiques destinées à illustrer une organisation de projets, sans information client ni activité interne réelle."
  },
  lanes: [
    {
      title: "Projet démonstratif — livraison web",
      detail: "Exemple synthétique : contrôle qualité terminé et publication prête à être vérifiée.",
      status: "ship",
      label: "Green",
      tags: ["Web", "QA", "Livraison"],
      priority: 1
    },
    {
      title: "Tableau de suivi démonstratif",
      detail: "Exemple synthétique de cockpit destiné à centraliser les statuts et prochaines étapes.",
      status: "ship",
      label: "Ship",
      tags: ["GitHub Pages", "Static", "Ops"],
      priority: 2
    },
    {
      title: "Offres à qualifier",
      detail: "Exemple synthétique de priorisation commerciale avant validation.",
      status: "watch",
      label: "Watch",
      tags: ["AtlasNexus", "Offers", "€"],
      priority: 3
    },
    {
      title: "Opportunités à examiner",
      detail: "Exemple synthétique : vérifier les données et les risques avant toute décision.",
      status: "watch",
      label: "Qualify",
      tags: ["Données", "Risques", "Décision"],
      priority: 4
    }
  ],
  deals: [
    { city: "Exemple A", price: "—", note: "Opportunité synthétique", risk: "Vérifier les données sources" },
    { city: "Exemple B", price: "—", note: "Opportunité synthétique", risk: "Qualifier les hypothèses" },
    { city: "Exemple C", price: "—", note: "Opportunité synthétique", risk: "Documenter la décision" }
  ],
  timeline: [
    { title: "Préparer", body: "Rassembler les éléments nécessaires à une livraison démonstrative.", owner: "Équipe" },
    { title: "Vérifier", body: "Contrôler le rendu et consigner les résultats sans donnée confidentielle.", owner: "Équipe" },
    { title: "Itérer", body: "Améliorer le livrable à partir des contrôles réalisés.", owner: "Équipe" }
  ]
};
