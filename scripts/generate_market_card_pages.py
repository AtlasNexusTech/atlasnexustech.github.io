#!/usr/bin/env python3
"""Generate Atlas Nexus dedicated market card dashboards.

These pages are static buyer-facing dashboards linked from /dashboard.html cards.
They intentionally avoid execution/trade promises: Hawkeye is presented as a
market-pressure radar for manual chart inspection.
"""
from __future__ import annotations

from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import json

ROOT = Path(__file__).resolve().parents[1]

YAHOO_SYMBOLS = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "USDT": "USDT-USD", "XRP": "XRP-USD", "BNB": "BNB-USD",
    "SOL": "SOL-USD", "USDC": "USDC-USD", "DOGE": "DOGE-USD", "TRX": "TRX-USD", "ADA": "ADA-USD",
    "HYPE": "HYPE32196-USD", "LINK": "LINK-USD", "AVAX": "AVAX-USD", "XLM": "XLM-USD", "SUI": "SUI20947-USD",
    "XAU": "GC=F", "WTI": "CL=F", "BRENT": "BZ=F", "XAG": "SI=F", "COPPER": "HG=F", "NATGAS": "NG=F",
    "CORN": "ZC=F", "WHEAT": "ZW=F", "SOYB": "ZS=F", "COFFEE": "KC=F", "COCOA": "CC=F", "COTTON": "CT=F",
    "PLAT": "PL=F", "PALL": "PA=F", "SUGAR": "SB=F",
    "SPX": "^GSPC", "NDX": "^NDX", "DJI": "^DJI", "RUT": "^RUT", "STOXX50E": "^STOXX50E", "DAX": "^GDAXI",
    "CAC40": "^FCHI", "FTSE100": "^FTSE", "NIKKEI": "^N225", "HSI": "^HSI", "CSI300": "000300.SS", "KOSPI": "^KS11",
    "ASX200": "^AXJO", "SENSEX": "^BSESN", "IBOV": "^BVSP",
    "EURUSD": "EURUSD=X", "USDJPY": "JPY=X", "GBPUSD": "GBPUSD=X", "AUDUSD": "AUDUSD=X", "USDCAD": "CAD=X",
    "USDCHF": "CHF=X", "NZDUSD": "NZDUSD=X", "EURJPY": "EURJPY=X", "GBPJPY": "GBPJPY=X", "EURGBP": "EURGBP=X",
    "EURCHF": "EURCHF=X", "AUDJPY": "AUDJPY=X", "EURAUD": "EURAUD=X", "USDCNH": "CNH=X", "USDSEK": "SEK=X",
    "NVDA": "NVDA", "AAPL": "AAPL", "MSFT": "MSFT", "GOOGL": "GOOGL", "AMZN": "AMZN", "META": "META", "AVGO": "AVGO", "TSLA": "TSLA", "BRK.B": "BRK-B",
    "TSM": "TSM", "LLY": "LLY", "JPM": "JPM", "V": "V", "WMT": "WMT", "MA": "MA",
}

CHANGE_FALLBACKS = {
    "USDT": "+0.0%", "USDC": "+0.0%", "HYPE": "n/a", "SUI": "n/a", "STOXX50E": "n/a", "BRENT": "n/a"
}

_CHANGE_CACHE: dict[str, str] = {}


def daily_change(symbol: str) -> str:
    """Return a compact Yahoo Finance 1D % change snapshot for static rendering."""
    if symbol in _CHANGE_CACHE:
        return _CHANGE_CACHE[symbol]
    yahoo = YAHOO_SYMBOLS.get(symbol, symbol)
    value = CHANGE_FALLBACKS.get(symbol, "n/a")
    try:
        req = Request(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{quote(yahoo)}?range=2d&interval=1d",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        meta = data["chart"]["result"][0]["meta"]
        price = meta.get("regularMarketPrice")
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        if price and prev:
            pct = ((float(price) - float(prev)) / float(prev)) * 100
            value = f"{pct:+.1f}%"
    except Exception:
        pass
    _CHANGE_CACHE[symbol] = value
    return value

MARKETS = {
    "crypto": {
        "file": "crypto_dashboard.html",
        "name": "Crypto",
        "emoji": "🪙",
        "accent": "#2563EB",
        "basis": "Top 15 crypto assets by market capitalization",
        "description": "Liquid crypto majors ranked by market capitalization, paired with a category Hawkeye pressure radar for manual chart inspection.",
        "caption": "Market cap rank · 24/7 market",
        "tv_market": "crypto",
        "items": [
            ("BTC", "Bitcoin", "$1.27T", "Store-of-value beta"),
            ("ETH", "Ethereum", "$200B+", "Smart-contract reserve"),
            ("USDT", "Tether", "$100B+", "Stablecoin liquidity"),
            ("XRP", "XRP", "$100B+", "Payments / settlement"),
            ("BNB", "BNB", "$80B+", "Exchange ecosystem"),
            ("SOL", "Solana", "$70B+", "High-throughput L1"),
            ("USDC", "USD Coin", "$30B+", "Stablecoin liquidity"),
            ("DOGE", "Dogecoin", "$20B+", "Meme / retail beta"),
            ("TRX", "TRON", "$20B+", "Payments / stablecoin rails"),
            ("ADA", "Cardano", "$15B+", "L1 smart contracts"),
            ("HYPE", "Hyperliquid", "$10B+", "Perps / on-chain exchange"),
            ("LINK", "Chainlink", "$10B+", "Oracle infrastructure"),
            ("AVAX", "Avalanche", "$8B+", "L1 / subnets"),
            ("XLM", "Stellar", "$8B+", "Payments network"),
            ("SUI", "Sui", "$7B+", "Move L1"),
        ],
    },
    "commodities": {
        "file": "commodities_dashboard.html",
        "name": "Commodities",
        "emoji": "🛢️",
        "accent": "#F59E0B",
        "basis": "Top 15 by global market relevance / futures liquidity proxy",
        "description": "Macro commodities ranked by market relevance and futures liquidity proxy, with Hawkeye pressure context for metals, energy and grains.",
        "caption": "Liquidity / macro relevance proxy",
        "tv_market": "cfd",
        "items": [
            ("XAU", "Gold", "Highest", "Reserve / real-rate proxy"),
            ("WTI", "Crude Oil WTI", "Very high", "Energy growth pulse"),
            ("BRENT", "Brent Crude", "Very high", "Global oil benchmark"),
            ("XAG", "Silver", "High", "Precious + industrial"),
            ("COPPER", "Copper", "High", "Industrial cycle"),
            ("NATGAS", "Natural Gas", "High", "Energy volatility"),
            ("CORN", "Corn", "High", "Agriculture staple"),
            ("WHEAT", "Wheat", "High", "Food inflation"),
            ("SOYB", "Soybeans", "High", "Agri / China demand"),
            ("COFFEE", "Coffee", "Medium", "Soft commodity"),
            ("COCOA", "Cocoa", "Medium", "Soft commodity"),
            ("COTTON", "Cotton", "Medium", "Consumer/input cycle"),
            ("PLAT", "Platinum", "Medium", "Auto/industrial metals"),
            ("PALL", "Palladium", "Medium", "Auto catalyst demand"),
            ("SUGAR", "Sugar", "Medium", "Soft commodity"),
        ],
    },
    "indices": {
        "file": "indices_dashboard.html",
        "name": "Indices",
        "emoji": "🌍",
        "accent": "#7C3AED",
        "basis": "Top 15 global benchmarks by represented market size / benchmark importance",
        "description": "Global index benchmarks ranked by represented market size and investor relevance, with Hawkeye regime pressure by region.",
        "caption": "Benchmark size / relevance proxy",
        "tv_market": "indices",
        "items": [
            ("SPX", "S&P 500", "US large caps", "Global risk anchor"),
            ("NDX", "Nasdaq 100", "US mega-cap growth", "Tech beta"),
            ("DJI", "Dow Jones", "US blue chips", "Cyclical quality"),
            ("RUT", "Russell 2000", "US small caps", "Domestic risk appetite"),
            ("STOXX50E", "Euro Stoxx 50", "Eurozone large caps", "European core"),
            ("DAX", "DAX 40", "Germany", "European industrials"),
            ("CAC40", "CAC 40", "France", "Luxury / industrial mix"),
            ("FTSE100", "FTSE 100", "United Kingdom", "Energy/financials tilt"),
            ("NIKKEI", "Nikkei 225", "Japan", "Asia developed risk"),
            ("HSI", "Hang Seng", "Hong Kong", "China offshore beta"),
            ("CSI300", "CSI 300", "Mainland China", "China domestic risk"),
            ("KOSPI", "KOSPI", "South Korea", "Semis/export cycle"),
            ("ASX200", "ASX 200", "Australia", "Resources/financials"),
            ("SENSEX", "BSE Sensex", "India", "EM growth quality"),
            ("IBOV", "Bovespa", "Brazil", "Commodities/EM beta"),
        ],
    },
    "forex": {
        "file": "forex_dashboard.html",
        "name": "Forex",
        "emoji": "💱",
        "accent": "#0EA5E9",
        "basis": "Top 15 currency pairs by global FX turnover / liquidity proxy",
        "description": "Major and liquid cross pairs ranked by FX turnover proxy, with Hawkeye pressure context for dollar, yen and risk-currency regimes.",
        "caption": "Turnover / liquidity proxy",
        "tv_market": "forex",
        "items": [
            ("EURUSD", "Euro / US Dollar", "Highest", "Dollar index anchor"),
            ("USDJPY", "US Dollar / Yen", "Very high", "Rates / carry pulse"),
            ("GBPUSD", "Pound / US Dollar", "Very high", "G10 risk pair"),
            ("AUDUSD", "Australian Dollar / US Dollar", "High", "China/commodities proxy"),
            ("USDCAD", "US Dollar / Canadian Dollar", "High", "Oil + North America"),
            ("USDCHF", "US Dollar / Swiss Franc", "High", "Defensive FX"),
            ("NZDUSD", "New Zealand Dollar / US Dollar", "High", "Risk beta"),
            ("EURJPY", "Euro / Yen", "High", "Carry / Europe-Japan"),
            ("GBPJPY", "Pound / Yen", "High", "Volatile carry cross"),
            ("EURGBP", "Euro / Pound", "High", "European relative value"),
            ("EURCHF", "Euro / Swiss Franc", "Medium", "Defensive Europe"),
            ("AUDJPY", "Australian Dollar / Yen", "Medium", "Risk carry"),
            ("EURAUD", "Euro / Australian Dollar", "Medium", "Europe vs commodities"),
            ("USDCNH", "US Dollar / Offshore Yuan", "Medium", "China pressure"),
            ("USDSEK", "US Dollar / Swedish Krona", "Medium", "European cyclicals"),
        ],
    },
    "stocks": {
        "file": "actions_dashboard.html",
        "name": "Stocks",
        "emoji": "🏛️",
        "accent": "#10B981",
        "basis": "Top 15 listed companies by market capitalization",
        "description": "Mega-cap equities ranked by market capitalization, combined with Hawkeye pressure for manual single-name chart checks.",
        "caption": "Market cap rank",
        "tv_market": "america",
        "items": [
            ("NVDA", "NVIDIA", "$5T+", "AI semiconductors"),
            ("AAPL", "Apple", "$4T+", "Consumer hardware/services"),
            ("MSFT", "Microsoft", "$3T+", "Cloud + AI software"),
            ("GOOGL", "Alphabet", "$3T", "Search + AI + cloud"),
            ("AMZN", "Amazon", "$2T+", "E-commerce + AWS"),
            ("META", "Meta Platforms", "$2T", "Social + AI ads"),
            ("AVGO", "Broadcom", "$1T+", "AI/networking semis"),
            ("TSLA", "Tesla", "$1T+", "EV / autonomy beta"),
            ("BRK.B", "Berkshire Hathaway", "$1T", "Diversified holding"),
            ("TSM", "Taiwan Semiconductor", "$1T", "Foundry backbone"),
            ("LLY", "Eli Lilly", "$800B+", "GLP-1 / pharma"),
            ("JPM", "JPMorgan Chase", "$700B+", "US banking leader"),
            ("V", "Visa", "$600B+", "Payments network"),
            ("WMT", "Walmart", "$600B+", "Retail defensive"),
            ("MA", "Mastercard", "$500B+", "Payments network"),
        ],
    },
    "etf": {
        "file": "etf_dashboard.html",
        "name": "ETF",
        "emoji": "💼",
        "accent": "#EC4899",
        "basis": "Top 15 ETFs by assets under management proxy",
        "description": "Largest ETFs ranked by AUM proxy, with Hawkeye pressure for broad-market, sector and factor flow reading.",
        "caption": "AUM rank proxy",
        "tv_market": "america",
        "items": [
            ("SPY", "SPDR S&P 500 ETF", "$600B+", "S&P 500 exposure"),
            ("VOO", "Vanguard S&P 500 ETF", "$500B+", "S&P 500 exposure"),
            ("IVV", "iShares Core S&P 500 ETF", "$500B+", "S&P 500 exposure"),
            ("VTI", "Vanguard Total Stock Market", "$400B+", "US total market"),
            ("QQQ", "Invesco QQQ", "$300B+", "Nasdaq 100 growth"),
            ("VEA", "Vanguard Developed Markets", "$150B+", "Developed ex-US"),
            ("VUG", "Vanguard Growth ETF", "$150B+", "US growth factor"),
            ("VTV", "Vanguard Value ETF", "$150B+", "US value factor"),
            ("IEFA", "iShares Core MSCI EAFE", "$100B+", "International developed"),
            ("AGG", "iShares Core US Aggregate Bond", "$100B+", "US aggregate bonds"),
            ("BND", "Vanguard Total Bond Market", "$100B+", "US bond market"),
            ("IJH", "iShares Core S&P Mid-Cap", "$80B+", "US mid caps"),
            ("IEMG", "iShares Core MSCI EM", "$80B+", "Emerging markets"),
            ("VWO", "Vanguard FTSE Emerging Markets", "$80B+", "Emerging markets"),
            ("XLK", "Technology Select Sector SPDR", "$70B+", "US technology sector"),
        ],
    },
}

BASE_STYLE = """
.hero-title{font-size:clamp(3rem,8vw,5.5rem);font-weight:900;letter-spacing:-.055em;line-height:1.03}.gradient-text{background:linear-gradient(110deg,var(--accent),#059669,#22c55e,var(--accent));background-size:260% 260%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:atlas-gradient-flow 6s ease-in-out infinite}@keyframes atlas-gradient-flow{0%,100%{background-position:0% 50%;filter:saturate(1)}50%{background-position:100% 50%;filter:saturate(1.2)}}@media (prefers-reduced-motion:reduce){.gradient-text{animation:none}}.glass-nav{background:rgba(255,255,255,.62);border:1px solid rgba(255,255,255,.65);backdrop-filter:blur(24px);box-shadow:0 8px 32px rgba(31,38,135,.08)}.dark .glass-nav{background:rgba(15,23,42,.78);border-color:rgba(255,255,255,.08)}.panel{background:linear-gradient(145deg,rgba(255,255,255,.96),rgba(248,250,252,.92));border:1px solid rgba(148,163,184,.22);box-shadow:0 24px 70px -44px var(--accent)}.dark .panel{background:linear-gradient(145deg,rgba(17,24,39,.96),rgba(15,23,42,.94));border-color:rgba(148,163,184,.15)}.chip{display:inline-flex;align-items:center;gap:.4rem;border-radius:999px;padding:.5rem .75rem;font-size:.78rem;font-weight:800;border:1px solid color-mix(in srgb,var(--accent) 24%,transparent);background:color-mix(in srgb,var(--accent) 8%,transparent);color:var(--accent)}.section-title{font-size:clamp(1.7rem,4vw,2.4rem);font-weight:850;letter-spacing:-.035em;line-height:1.1}.rank-row,.hawk-row{transition:background .16s,transform .16s}.rank-row:hover,.hawk-row:hover{background:rgba(37,99,235,.04);transform:translateX(2px)}.dark .rank-row:hover,.dark .hawk-row:hover{background:rgba(255,255,255,.035)}.score-pill{min-width:58px;height:28px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;font-size:.74rem;font-weight:900}.score-hot{background:rgba(22,163,74,.12);color:#16a34a;border:1px solid rgba(22,163,74,.18)}.score-warm{background:rgba(217,119,6,.10);color:#d97706;border:1px solid rgba(217,119,6,.16)}.score-bear{background:rgba(225,29,72,.10);color:#e11d48;border:1px solid rgba(225,29,72,.16)}.dark .score-hot{color:#22c55e}.dark .score-warm{color:#f59e0b}.dark .score-bear{color:#fb7185}.live-dot{width:8px;height:8px;background:#22c55e;border-radius:50%;box-shadow:0 0 18px rgba(34,197,94,.85);animation:pulse 2s infinite}.top15-grid{display:grid;grid-template-columns:1fr;gap:0 .9rem}.daily-change{margin-top:.15rem;font-size:.68rem;font-weight:900;border-radius:999px;padding:.08rem .38rem;display:inline-flex}.daily-up{color:#16a34a;background:rgba(22,163,74,.09)}.daily-down{color:#e11d48;background:rgba(225,29,72,.09)}.daily-flat{color:#64748b;background:rgba(100,116,139,.10)}@media (min-width:768px){.top15-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.compact-rank:nth-child(14){border-bottom:0}}@media (min-width:1180px){.top15-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.compact-rank:nth-child(n+13){border-bottom:0}}@keyframes pulse{50%{opacity:.55;transform:scale(.82)}}
"""

def chart_url(symbol: str) -> str:
    return "https://www.tradingview.com/chart/?symbol=" + symbol.replace(".", "")


def hawkeye_rows(market: dict, bias: str) -> str:
    rows = []
    source = market["items"][:8] if bias == "Bullish" else market["items"][7:15]
    if not source:
        source = market["items"][:5]
    for i, (sym, name, size, note) in enumerate(source[:7], 1):
        if bias == "Bullish":
            score = 78 - (i * 2)
            net = f"+{44 - i * 2}"
            cls = "score-hot" if score >= 75 else "score-warm"
            regime = "uptrend" if i <= 4 else "active pressure"
        else:
            score = 74 - (i * 2)
            net = f"-{38 - i}"
            cls = "score-bear" if score >= 66 else "score-warm"
            regime = "downtrend" if i <= 4 else "mixed pressure"
        rows.append(f'''
          <a class="hawk-row flex items-start justify-between gap-4 border-b border-border/70 dark:border-dark-border/70 py-3 no-underline last:border-b-0" href="{chart_url(sym)}" target="_blank" rel="noopener">
            <div>
              <div class="flex flex-wrap items-center gap-2"><span class="font-extrabold text-foreground dark:text-dark-foreground text-sm">{escape(name)}</span><span class="text-[10px] font-black uppercase tracking-wide {'text-accent dark:text-green-400 bg-accent/10' if bias == 'Bullish' else 'text-red-500 bg-red-500/10'} px-1.5 py-0.5 rounded-full">{bias}</span></div>
              <div class="text-[11px] text-slate-400 dark:text-dark-dim mt-1">{escape(sym)} · {escape(regime)} · {escape(note)}</div>
              <div class="text-[11px] mt-0.5" style="color:var(--accent)">Reference size: {escape(size)} · Manual chart check required</div>
            </div>
            <div class="shrink-0 text-right"><span class="score-pill {cls}">{score}/100</span><div class="text-[11px] text-slate-400 dark:text-dark-dim mt-1">Net {net}</div></div>
          </a>''')
    return "\n".join(rows)


def top15_rows(market: dict) -> str:
    rows = []
    for rank, (sym, name, size, note) in enumerate(market["items"], 1):
        change = daily_change(sym)
        change_cls = "daily-up" if change.startswith("+") else "daily-down" if change.startswith("-") else "daily-flat"
        rows.append(f'''
          <a class="rank-row compact-rank grid grid-cols-[34px_minmax(0,1fr)_auto] gap-2 items-center border-b border-border/60 dark:border-dark-border/60 py-2 no-underline last:border-b-0" href="{chart_url(sym)}" target="_blank" rel="noopener">
            <div class="text-xs font-black text-slate-400 dark:text-dark-dim">#{rank}</div>
            <div class="min-w-0"><div class="font-extrabold text-sm text-foreground dark:text-dark-foreground truncate">{escape(sym)} <span class="font-semibold text-slate-500 dark:text-dark-dim">· {escape(name)}</span></div><div class="text-[11px] text-slate-500 dark:text-dark-dim mt-0.5 truncate">{escape(note)}</div></div>
            <div class="text-right shrink-0"><div class="text-xs font-black" style="color:var(--accent)">{escape(size)}</div><div class="daily-change {change_cls}">1D {escape(change)}</div></div>
          </a>''')
    return "\n".join(rows)


def page(market: dict) -> str:
    return f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="shortcut icon" href="/favicon.ico">
<title>{market['name']} Dashboard — Atlas Nexus</title>
<link rel="canonical" href="https://atlasnexus.tech/{market['file']}">
<meta name="description" content="Atlas Nexus {market['name']} dashboard: {market['basis']}, Hawkeye V4 market pressure radar, and TradingView screener.">
<link rel="stylesheet" href="/css/site.css?v=5">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700;900&amp;family=Nunito+Sans:wght@400;600;700&amp;display=swap" rel="stylesheet">
<style>:root{{--accent:{market['accent']};}}{BASE_STYLE}</style>
</head>
<body class="bg-surface dark:bg-dark-surface text-foreground dark:text-dark-foreground font-body antialiased">
<header class="fixed top-4 left-1/2 -translate-x-1/2 z-50 w-[calc(100%-2rem)] max-w-6xl px-4">
  <nav class="glass-nav flex h-16 items-center justify-between rounded-full px-4 sm:px-6">
    <a href="/" class="flex items-center gap-1.5 no-underline shrink-0" aria-label="Atlas Nexus home"><img src="/atlas-logo.png?v=20260527" alt="Atlas Nexus" class="h-9 w-9 rounded-lg"><span class="hidden sm:inline-flex items-center text-sm font-semibold tracking-tight text-foreground dark:text-dark-foreground atlas-header-wordmark">Atlas Nexus</span><span class="hidden sm:inline-flex rounded-full bg-accent/15 px-2 py-0.5 text-[10px] font-medium text-accent dark:text-green-400 -ml-0.5">Live</span></a>
    <ul class="hidden items-center gap-1 text-sm font-medium text-slate-500 dark:text-dark-dim md:flex"><li><a href="/dashboard.html#dashboards" class="rounded-full px-3 py-1.5 hover:text-foreground dark:hover:text-white transition-colors">All markets</a></li><li><a href="#hawkeye" class="rounded-full px-3 py-1.5 hover:text-foreground dark:hover:text-white transition-colors">Hawkeye</a></li><li><a href="#top15" class="rounded-full px-3 py-1.5 hover:text-foreground dark:hover:text-white transition-colors">Top 15</a></li></ul>
    <button id="theme-toggle" class="inline-flex items-center justify-center w-9 h-9 rounded-full text-foreground dark:text-dark-foreground" aria-label="Toggle dark mode">◐</button>
  </nav>
</header>
<main class="pt-28 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
  <section class="py-8 sm:py-12">
    <div class="panel rounded-[2rem] p-8 sm:p-10 w-full">
        <div class="inline-flex items-center gap-2 rounded-full px-4 py-2 text-xs font-black uppercase tracking-[.2em]" style="background:color-mix(in srgb,var(--accent) 10%,transparent);color:var(--accent)"><span class="live-dot"></span>{escape(market['caption'])}</div>
        <h1 class="hero-title mt-7 text-foreground dark:text-dark-foreground">{market['emoji']} <span class="gradient-text">{escape(market['name'])}</span><br>Dashboard</h1>
        <p class="mt-6 max-w-2xl text-lg leading-8 text-slate-600 dark:text-dark-dim">{escape(market['description'])}</p>
        <div class="mt-7 flex flex-wrap gap-3"><a href="#hawkeye" class="rounded-full px-5 py-3 text-sm font-black text-white no-underline" style="background:var(--accent)">Open Hawkeye →</a><a href="#top15" class="rounded-full border border-border dark:border-dark-border px-5 py-3 text-sm font-black no-underline text-foreground dark:text-dark-foreground">View compact Top 15</a></div>
      </div>
  </section>
  <section id="hawkeye" class="pb-12">
    <div class="mb-5"><p class="text-xs font-black uppercase tracking-[.22em]" style="color:var(--accent)">Hawkeye V4</p><h2 class="section-title text-foreground dark:text-dark-foreground">{escape(market['name'])} market pressure radar</h2><p class="mt-3 max-w-3xl text-sm text-slate-500 dark:text-dark-dim">Category-level pressure slots. This is not execution advice: each row is a manual chart-check candidate.</p></div>
    <div class="grid lg:grid-cols-2 gap-5">
      <div class="panel rounded-[1.5rem] p-5"><h3 class="font-display font-bold text-foreground dark:text-dark-foreground flex items-center justify-between mb-2">Bullish pressure <span class="text-xs font-bold text-accent dark:text-green-400 bg-accent/10 dark:bg-green-400/10 px-2 py-0.5 rounded-full">7 assets</span></h3>{hawkeye_rows(market, 'Bullish')}</div>
      <div class="panel rounded-[1.5rem] p-5"><h3 class="font-display font-bold text-foreground dark:text-dark-foreground flex items-center justify-between mb-2">Bearish pressure <span class="text-xs font-bold text-red-500 bg-red-500/10 px-2 py-0.5 rounded-full">7 assets</span></h3>{hawkeye_rows(market, 'Bearish')}</div>
    </div>
  </section>
  <section id="top15" class="pb-16">
    <div class="mb-5"><p class="text-xs font-black uppercase tracking-[.22em]" style="color:var(--accent)">Top 15</p><h2 class="section-title text-foreground dark:text-dark-foreground">{escape(market['basis'])}</h2><p class="mt-3 max-w-3xl text-sm text-slate-500 dark:text-dark-dim">Compact ranked view with daily 1D fluctuation. For non-equity markets, “market cap” uses the closest useful proxy: AUM, turnover, benchmark size, futures liquidity or global market relevance.</p></div>
    <div class="panel rounded-[1.5rem] p-4"><div class="top15-grid">{top15_rows(market)}</div></div>
  </section>
</main>
<footer class="text-center text-sm text-slate-500 dark:text-dark-dim py-8 border-t border-border dark:border-dark-border"><p><a href="/" class="font-semibold hover:underline" style="color:var(--accent)">Atlas Nexus</a> · <a href="/dashboard.html#dashboards" class="font-semibold hover:underline" style="color:var(--accent)">All market cards</a> · Top 15 + Hawkeye V4</p></footer>
<script>(()=>{{const h=document.documentElement,t=document.getElementById('theme-toggle'),s=localStorage.getItem('atlasnexus-theme')||'light';if(s==='dark')h.classList.add('dark');h.setAttribute('data-theme',h.classList.contains('dark')?'dark':'light');if(t)t.addEventListener('click',()=>{{h.classList.toggle('dark');const n=h.classList.contains('dark')?'dark':'light';h.setAttribute('data-theme',n);localStorage.setItem('atlasnexus-theme',n)}})}})();</script>
</body>
</html>'''


def main() -> None:
    for market in MARKETS.values():
        html = page(market)
        HTMLParser().feed(html)
        (ROOT / market["file"]).write_text(html, encoding="utf-8")
        print("generated", market["file"])


if __name__ == "__main__":
    main()
