#!/usr/bin/env python3
"""Security regression checks for the static Atlas Nexus site."""
from pathlib import Path
from urllib.parse import urlparse
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SCRIPT_HOSTS = {
    "assets.calendly.com",
    "cdn.jsdelivr.net",
    "gc.zgo.at",
    "s3.tradingview.com",
}
errors = []
html_files = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]

for path in html_files:
    text = path.read_text(encoding="utf-8", errors="ignore")
    rel = path.relative_to(ROOT)
    if "<head" not in text.lower():
        continue
    if 'http-equiv="Content-Security-Policy"' not in text:
        errors.append(f"{rel}: missing Content-Security-Policy meta")
    if not re.search(r'<meta\s+name=["\']referrer["\']', text, re.I):
        errors.append(f"{rel}: missing referrer policy")

    for match in re.finditer(r"<a\b[^>]*>", text, re.I):
        tag = match.group(0)
        if re.search(r'target=["\']_blank["\']', tag, re.I):
            rel_attr = re.search(r'rel=["\']([^"\']*)["\']', tag, re.I)
            values = set(rel_attr.group(1).lower().split()) if rel_attr else set()
            if not {"noopener", "noreferrer"}.issubset(values):
                errors.append(f"{rel}: unsafe target=_blank")

    for src in re.findall(r'<script\b[^>]*\bsrc=["\']([^"\']+)', text, re.I):
        normalized = "https:" + src if src.startswith("//") else src
        if normalized.startswith(("http://", "https://")):
            host = urlparse(normalized).hostname or ""
            if host not in ALLOWED_SCRIPT_HOSTS:
                errors.append(f"{rel}: unapproved external script host {host}")

    for tag in re.findall(r'<script\b[^>]*\bsrc=["\']https://cdn\.jsdelivr\.net[^>]*>', text, re.I):
        if "integrity=" not in tag or "crossorigin=" not in tag:
            errors.append(f"{rel}: jsDelivr script without SRI/crossorigin")

    if re.search(r'<form\b[^>]*action=["\']https://formsubmit\.co/', text, re.I):
        if re.search(r'name=["\']_captcha["\'][^>]*value=["\']false["\']', text, re.I):
            errors.append(f"{rel}: FormSubmit CAPTCHA disabled")
        if not re.search(r'name=["\']_honey["\']', text, re.I):
            errors.append(f"{rel}: FormSubmit honeypot missing")

tracking = (ROOT / "js" / "tracking.js").read_text(encoding="utf-8")
if "origin.indexOf('calendly.com')" in tracking:
    errors.append("js/tracking.js: permissive Calendly origin check")
if "originHost !== 'calendly.com'" not in tracking:
    errors.append("js/tracking.js: exact Calendly origin check missing")

desk = (ROOT / "atlas-desk" / "client" / "index.html").read_text(encoding="utf-8")
for required in (
    "const TRUSTED_SIGNAL='wss://signal.atlasnexus.tech/ws'",
    "return TRUSTED_SIGNAL",
    "list.replaceChildren()",
    "_savedPassword=null",
):
    if required not in desk:
        errors.append(f"atlas-desk/client/index.html: missing hardening contract {required}")
if "list.innerHTML+=" in desk:
    errors.append("atlas-desk/client/index.html: remote filename DOM injection regression")

for relative in ("verify/index.html", "verify/en/index.html"):
    page = (ROOT / relative).read_text(encoding="utf-8")
    if "ethers.umd.min.js" not in page or "integrity=\"sha384-" not in page:
        errors.append(f"{relative}: ethers SRI missing")
    if re.search(r"status\.innerHTML\s*=\s*['\"]❌\s*['\"]\s*\+", page):
        errors.append(f"{relative}: untrusted wallet error rendered as HTML")

for workflow in (ROOT / ".github" / "workflows").glob("*.yml"):
    text = workflow.read_text(encoding="utf-8")
    for use in re.findall(r"uses:\s*([^\s]+)", text):
        ref = use.rsplit("@", 1)[-1]
        if not re.fullmatch(r"[0-9a-f]{40}", ref):
            errors.append(f"{workflow.relative_to(ROOT)}: action not pinned to immutable SHA: {use}")

if errors:
    print("SECURITY_CHECK_FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print(f"SECURITY_CHECK_OK ({len(html_files)} HTML pages)")
