# Exemple public — extracteur de données publiques

Cet exemple démontre la **structure et la reproductibilité** du livrable annoncé. Il utilise uniquement dix pages HTML locales et des données synthétiques (`SYN-001` à `SYN-010`). Les URL en `.invalid` ne désignent aucun site réel.

## Contenu

- `source-pages/` : 10 pages HTML synthétiques homogènes ;
- `extracteur_demo.py` : script Python 3 sans dépendance externe ;
- `exemple-extraction.csv` : 10 lignes × 8 champs ;
- `exemple-extraction.json` : les mêmes 10 enregistrements structurés ;
- `journal-execution.txt` : compte rendu d’exécution ;
- `exemple-extracteur-donnees-publiques.zip` : archive complète.

## Exécution

```bash
python3 extracteur_demo.py
```

Sortie attendue :

```text
OK: 10 pages, 8 champs, 0 erreur
```

## Limites de démonstration

Cet exemple local ne valide ni la légalité, ni les droits, ni les conditions d’utilisation, ni `robots.txt`, ni la stabilité d’une source réelle. Une source réelle doit rester publique, autorisée, sans connexion, CAPTCHA, contrôle d’accès ou données sensibles. Aucun fichier confidentiel n’est nécessaire pour la qualification initiale.
