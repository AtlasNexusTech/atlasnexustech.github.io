"""Génère sitemap.xml complet pour atlasnexus.tech.
Scanne les pages réelles (index.html), ajoute hreflang FR/EN quand les paires existent.
"""
import subprocess, re, json
from pathlib import Path

BASE = Path(__file__).parent
DOMAIN = "https://atlasnexus.tech"

# pages réelles (dossiers avec index.html)
pages = subprocess.run(['find', '.', '-name', 'index.html', '-not', '-path', '*/node_modules/*'],
                       capture_output=True, text=True, cwd=BASE).stdout.split()
pages = [p.replace('./', '').replace('/index.html', '') for p in pages]
pages = [p for p in pages if p != '']

# Exclure les pages noindex : jamais noindex + sitemap (signal SEO contradictoire).
# Une page est noindex si son index.html contient name="robots" content="...noindex..."
def is_noindex(p):
    if p == 'index.html':
        return False
    try:
        html = (BASE / p / 'index.html').read_text(encoding='utf-8')
    except Exception:
        return False
    return bool(re.search(r'name="robots"\s+content="[^"]*noindex', html, re.I))

pages = [p for p in pages if not is_noindex(p)]


# Construire les URLs : root = /, sinon /<page>/
urls = set()
for p in pages:
    if p == 'index.html':
        urls.add('/')
    else:
        urls.add('/' + p + '/')

# paires FR/EN : /x/ ↔ /en/x/ ou /x/en/
def lang_pair(u):
    """Retourne (fr, en) si la page a un équivalent EN, sinon None."""
    if u == '/':
        return ('/', '/en/')
    path = u.strip('/')
    # cas /en/x/ (déjà EN) — son FR est /x/
    if path.startswith('en/'):
        fr = '/' + path[3:] + '/'
        return (fr, u) if fr in urls else None
    # cas /x/en/ (EN dans sous-dossier) — son FR est /x/
    if path.endswith('/en'):
        fr = '/' + path[:-3] + '/'
        return (fr, u) if fr in urls else None
    # page FR — chercher /en/x/ ou /x/en/
    en1 = '/en/' + path + '/'
    en2 = '/' + path + '/en/'
    if en1 in urls:
        return (u, en1)
    if en2 in urls:
        return (u, en2)
    return None

# Priorités par type de page
def priority(u):
    if u == '/' or u == '/en/':
        return '1.0'
    path = u.strip('/').rstrip('/')
    if path in ('ia-agentique', 'en/ia-agentique', 'developpement-web-donnees', 'en/developpement-web-donnees',
                'training', 'en/training'):
        return '0.9'
    if 'en' in path.split('/') or path.endswith('en'):
        return '0.8'
    return '0.7'

def changefreq(u):
    if u == '/' or u == '/en/':
        return 'weekly'
    if 'demo' in u or 'artisan' in u or 'refonte' in u:
        return 'monthly'
    return 'monthly'

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
lines.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')

# Trier : root d'abord, puis alphabétique
sorted_urls = sorted(urls, key=lambda u: (u != '/', u))

for u in sorted_urls:
    pair = lang_pair(u)
    if pair:
        fr, en = pair
        # n'écrire que la version FR (avec les 2 hreflang) pour éviter les doublons
        if u != fr:
            continue
        line = f'  <url><loc>{DOMAIN}{fr}</loc>'
        line += f'<xhtml:link rel="alternate" hreflang="fr" href="{DOMAIN}{fr}"/>'
        line += f'<xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}{en}"/>'
        line += f'<xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}{fr}"/>'
        line += f'<changefreq>{changefreq(fr)}</changefreq><priority>{priority(fr)}</priority></url>'
        lines.append(line)
    else:
        line = f'  <url><loc>{DOMAIN}{u}</loc>'
        line += f'<changefreq>{changefreq(u)}</changefreq><priority>{priority(u)}</priority></url>'
        lines.append(line)

# pages spéciales hors repo (dédupliquées — verify/ peut déjà être scanné)
import re as _re
_existing = set(_re.findall(r'<loc>(https://atlasnexus\.tech/[^<]*)</loc>', '\n'.join(lines)))
if 'https://atlasnexus.tech/alexandre-lasly/' not in _existing:
    lines.append('  <url><loc>https://atlasnexus.tech/alexandre-lasly/</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>')
if 'https://atlasnexus.tech/verify/' not in _existing:
    lines.append('  <url><loc>https://atlasnexus.tech/verify/</loc><changefreq>monthly</changefreq><priority>0.3</priority></url>')

lines.append('</urlset>')
content = '\n'.join(lines) + '\n'
(BASE / 'sitemap.xml').write_text(content, encoding='utf-8')
print(f'Sitemap généré : {sum(1 for l in lines if "<url>" in l)} URLs')

# validation XML rapide
import xml.etree.ElementTree as ET
ET.fromstring(content)
print('✅ XML valide')
