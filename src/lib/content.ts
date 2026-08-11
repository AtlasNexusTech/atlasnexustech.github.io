export interface UseCase {
  id: string
  label: string
  title: string
  description: string
  proof: string
}

export const USE_CASES: UseCase[] = [
  {
    id: 'automation',
    label: '01 / AUTOMATION',
    title: 'Automatiser les tâches qui débordent.',
    description: 'Mails, devis, relances et routines administratives deviennent des flux opérés par vos agents, sur votre infrastructure.',
    proof: 'Vous validez les points sensibles. Le reste circule sans ajouter un SaaS de plus.',
  },
  {
    id: 'reporting',
    label: '02 / REPORTING',
    title: 'Transformer l’activité en décisions lisibles.',
    description: 'Les agents collectent, structurent et préparent vos rapports pour que le bon signal arrive au bon moment.',
    proof: 'Des synthèses prêtes à relire, documentées et reliées à leurs sources.',
  },
  {
    id: 'agents',
    label: '03 / AGENTS MÉTIER',
    title: 'Déployer un système adapté à votre travail réel.',
    description: 'Chaque agent est configuré autour de vos outils, de vos règles et de vos étapes de validation.',
    proof: 'Pas de démonstration générique : une tâche réelle, installée et démontrée chez vous.',
  },
  {
    id: 'infrastructure',
    label: '04 / INFRASTRUCTURE',
    title: 'Garder les agents là où vous les maîtrisez.',
    description: 'Déploiement sur votre machine ou un VPS, avec code, documentation et formats ouverts.',
    proof: 'Votre infrastructure, vos données, votre capacité à reprendre la main.',
  },
  {
    id: 'orchestration',
    label: '05 / ORCHESTRATION',
    title: 'Faire coopérer plusieurs capacités sans perdre le contrôle.',
    description: 'Mémoire, outils et agents spécialisés sont orchestrés comme un système cohérent plutôt qu’une accumulation de bots.',
    proof: 'Les sorties convergent vers des validations humaines claires.',
  },
]

export const SCENES = [
  { id: 'top', label: 'INTRO', title: 'ATLAS NEXUS' },
  { id: 'approach', label: 'APPROACH', title: 'Une infrastructure, pas un SaaS.' },
  { id: 'method', label: 'METHOD', title: 'Déployer. Connecter. Valider. Opérer.' },
  { id: 'systems', label: 'SYSTEMS', title: 'Des capacités reliées à votre activité.' },
  { id: 'contact', label: 'ACT', title: 'Commencez par trente minutes utiles.' },
] as const

export const PRIMARY_CTA = {
  label: 'Réserver mon diagnostic gratuit de 30 min',
  href: 'https://atlasnexus.tech/#contact',
} as const
