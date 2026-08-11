window.dashboardData = {
  focus: {
    title: "GitHub → publication → preuve live",
    copy: "Pousser proprement, vérifier le rendu, puis garder une URL partageable pour les prochaines itérations."
  },
  lanes: [
    {
      title: "AI2Work — build Render",
      detail: "Source main vérifiée localement; build Next.js OK. À surveiller côté Render après chaque nouveau push.",
      status: "ship",
      label: "Green",
      tags: ["Next.js", "Render", "Wallet UI"],
      priority: 1
    },
    {
      title: "Atlas Control Room",
      detail: "Dashboard statique amélioré, prêt à versionner et publier comme cockpit opérationnel Atlas.",
      status: "ship",
      label: "Ship",
      tags: ["GitHub Pages", "Static", "Ops"],
      priority: 2
    },
    {
      title: "Offres monétisables",
      detail: "Pages Web, IA agentique et Motion UI à garder orientées livrable client simple, vendable et vérifiable.",
      status: "watch",
      label: "Watch",
      tags: ["AtlasNexus", "Offers", "€"],
      priority: 3
    },
    {
      title: "Deals achat-revente",
      detail: "Shortlist active avec liens directs uniquement; qualifier les risques avant projection de marge.",
      status: "watch",
      label: "Qualify",
      tags: ["LBC", "DPE", "Marge"],
      priority: 4
    }
  ],
  deals: [
    { city: "Thiais", price: "119k€", note: "2 pièces · 35 m² · DPE D", risk: "Vérifier charges + PV AG" },
    { city: "Valenton", price: "110k€", note: "2 pièces · 26,28 m² · DPE E", risk: "Négociation DPE / travaux" },
    { city: "Chennevières", price: "100k€", note: "Studio · 21,77 m² · DPE E", risk: "Liquidité + coût rénovation" }
  ],
  timeline: [
    { title: "Publier", body: "Pousser le dashboard sur GitHub Pages avec un commit scoped et vérifier l’URL live avec cache-buster.", owner: "Bolt" },
    { title: "Prouver", body: "Conserver une version locale accessible sur localhost et une version publique partageable pour validation rapide.", owner: "Atlas" },
    { title: "Itérer", body: "Ajouter ensuite les vrais flux utiles : builds, liens Render/GitHub, opportunités et tâches du jour.", owner: "Alexandre" }
  ]
};
