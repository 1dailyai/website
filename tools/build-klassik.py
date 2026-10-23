#!/usr/bin/env python3
"""Baut die Design-Variante «Klassik» in den Ordner /klassik/.

Die bestehenden Seiten im Hauptordner bleiben unverändert. Das Script übernimmt
deren Inhalt (Hauptteil), ersetzt Kopf- und Fusszeile durch die klassische
Navigation, lädt zusätzlich assets/css/klassik.css und ergänzt Sprungmarken.
Startseite und Grundsätze-Seite kommen aus tools/klassik/*.html.

Aufruf (im Hauptordner der Website):  python3 tools/build-klassik.py
Nach jeder Textänderung an den bestehenden Seiten einfach erneut ausführen.
"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "klassik")
SRC = os.path.join(ROOT, "tools", "klassik")
CSS_V = "1"

# Seitenzuordnung DE <-> EN
PAGES = [  # (key, de, en, group)
    ("index", "index.html", "index.html", None),
    ("principles", "grundsaetze.html", "principles.html", "g1"),
    ("gold", "goldmarkt.html", "gold-market.html", "g2"),
    ("method", "methode.html", "method.html", "g3"),
    ("ir", "investor-relations.html", "investor-relations.html", "g4"),
    ("about", "ueber-uns.html", "about.html", "g5"),
    ("vision", "vision.html", "vision.html", "g5"),
    ("contact", "kontakt.html", "contact.html", "g5"),
    ("privacy", "datenschutz.html", "privacy.html", None),
]
NEW_PAGES = {"index", "principles"}  # handgeschrieben in tools/klassik/

NAV = {
 "de": [
  ("g1", "Grundsätze", "grundsaetze.html", "Wie wir arbeiten und wofür wir stehen: Regeln, Risiko und Transparenz.", [
    ("Unser Ansatz", "grundsaetze.html#ansatz"),
    ("Systematisch statt spekulativ", "grundsaetze.html#systematisch"),
    ("Kapitalschutz zuerst", "grundsaetze.html#kapitalschutz"),
    ("Technologie im Dienst des Menschen", "grundsaetze.html#technologie"),
    ("Prozess vor Ergebnis", "grundsaetze.html#prozess"),
    ("Transparenz", "grundsaetze.html#transparenz"),
    ("Langfristigkeit", "grundsaetze.html#langfristig"),
    ("Schweizer Aktiengesellschaft", "grundsaetze.html#aufstellung")]),
  ("g2", "Goldmarkt", "goldmarkt.html", "Wie der Goldmarkt funktioniert, wo Gold gehandelt wird und was den Preis bewegt.", [
    ("Rohstoff und Währung", "goldmarkt.html#natur"),
    ("Gold in Zahlen", "goldmarkt.html#zahlen"),
    ("Preisentwicklung", "goldmarkt.html#preis"),
    ("Börsenplätze der Welt", "goldmarkt.html#boersenplaetze"),
    ("Handelszeiten", "goldmarkt.html#handelszeiten"),
    ("Preistreiber", "goldmarkt.html#preistreiber"),
    ("XAUUSD und CFD-Handel", "goldmarkt.html#xauusd"),
    ("Warum Gold", "goldmarkt.html#warum-gold")]),
  ("g3", "Methode", "methode.html", "Die 1daily-Methode: das Regelwerk, nach dem wir handeln.", [
    ("Das Kern-Setup", "methode.html#kern-setup"),
    ("Grundhaltung", "methode.html#grundhaltung"),
    ("Die fünf Komponenten", "methode.html#komponenten"),
    ("Ausführung", "methode.html#ausfuehrung"),
    ("Wirtschaftsnews", "methode.html#news"),
    ("KI, Mensch und System", "methode.html#rollen"),
    ("Wissensbasis als PDF", "methode.html#pdf")]),
  ("g4", "Investoren", "investor-relations.html", "Seed-Runde, Investment Story und der aktuelle Stand der 1daily AG.", [
    ("Investment Story", "investor-relations.html#story"),
    ("Track Record", "index.html#track"),
    ("Stand heute", "investor-relations.html#stand"),
    ("Meilensteine", "investor-relations.html#meilensteine"),
    ("Seed-Runde", "investor-relations.html#seed"),
    ("Interesse anmelden", "investor-relations.html#form")]),
  ("g5", "Unternehmen", "ueber-uns.html", "Eine Schweizer Aktiengesellschaft mit Sitz in Steffisburg, Kanton Bern.", [
    ("Über 1daily", "ueber-uns.html"),
    ("So arbeiten wir", "ueber-uns.html#arbeitsweise"),
    ("Gründer", "ueber-uns.html#gruender"),
    ("Vision und Philosophie", "vision.html"),
    ("Kontakt", "kontakt.html"),
    ("Impressum", "kontakt.html#impressum")]),
 ],
 "en": [
  ("g1", "Principles", "principles.html", "How we work and what we stand for: rules, risk and transparency.", [
    ("Our approach", "principles.html#approach"),
    ("Systematic, not speculative", "principles.html#systematic"),
    ("Capital protection first", "principles.html#capital-protection"),
    ("Technology serving people", "principles.html#technology"),
    ("Process over outcome", "principles.html#process"),
    ("Transparency", "principles.html#transparency"),
    ("Long-term thinking", "principles.html#long-term"),
    ("A Swiss stock corporation", "principles.html#structure")]),
  ("g2", "Gold market", "gold-market.html", "How the gold market works, where gold is traded and what moves the price.", [
    ("Commodity and currency", "gold-market.html#nature"),
    ("Gold in numbers", "gold-market.html#numbers"),
    ("Price history", "gold-market.html#price"),
    ("Trading venues", "gold-market.html#venues"),
    ("Trading hours", "gold-market.html#hours"),
    ("Price drivers", "gold-market.html#drivers"),
    ("XAUUSD and CFD trading", "gold-market.html#xauusd"),
    ("Why gold", "gold-market.html#why-gold")]),
  ("g3", "Method", "method.html", "The 1daily Method: the rulebook we trade by.", [
    ("The core setup", "method.html#kern-setup"),
    ("Mindset", "method.html#mindset"),
    ("The five components", "method.html#komponenten"),
    ("Execution", "method.html#execution"),
    ("Economic news", "method.html#news"),
    ("AI, people and system", "method.html#roles"),
    ("Knowledge base (PDF)", "method.html#pdf")]),
  ("g4", "Investors", "investor-relations.html", "Seed round, investment story and where 1daily AG stands today.", [
    ("Investment story", "investor-relations.html#story"),
    ("Track record", "index.html#track"),
    ("Where we stand", "investor-relations.html#status"),
    ("Milestones", "investor-relations.html#milestones"),
    ("Seed round", "investor-relations.html#seed"),
    ("Register your interest", "investor-relations.html#form")]),
  ("g5", "Company", "about.html", "A Swiss stock corporation based in Steffisburg, Canton of Bern.", [
    ("About 1daily", "about.html"),
    ("How we work", "about.html#how-we-work"),
    ("Founder", "about.html#founder"),
    ("Vision and philosophy", "vision.html"),
    ("Contact", "contact.html"),
    ("Legal notice", "contact.html#impressum")]),
 ],
}

SECTION_IDS = {
 "de": {"Die duale Natur": "natur", "Gold in Zahlen": "zahlen", "Preisentwicklung": "preis",
        "Handelszeiten": "handelszeiten", "Preistreiber": "preistreiber", "XAUUSD im Detail": "xauusd",
        "So handelt 1daily": "so-handelt-1daily", "Warum Gold": "warum-gold", "Grundhaltung": "grundhaltung",
        "Ausführung": "ausfuehrung", "Drei Rollen": "rollen", "Stand heute": "stand", "Meilensteine": "meilensteine",
        "Seed-Runde": "seed", "So arbeiten wir": "arbeitsweise", "Gründer &amp; Verwaltungsrat": "gruender",
        "Das Unternehmen": "unternehmen", "Unser Markt": "markt", "Unsere Grundsätze": "grundsaetze",
        "Der Gründer": "gruender", "Für Investoren": "fuer-investoren"},
 "en": {"A dual nature": "nature", "Gold in numbers": "numbers", "Price history": "price", "Trading hours": "hours",
        "Price drivers": "drivers", "XAUUSD in detail": "xauusd", "How 1daily trades": "how-1daily-trades",
        "Why gold": "why-gold", "Mindset": "mindset", "Execution": "execution", "Three roles": "roles",
        "Where we stand": "status", "Milestones": "milestones", "Seed round": "seed", "How we work": "how-we-work",
        "Founder &amp; Board Member": "founder", "The company": "company", "Our market": "market",
        "Our principles": "principles", "The founder": "founder", "For investors": "for-investors"},
}

T = {
 "de": {"skip": "Zum Inhalt springen", "home": "1daily AG, zur Startseite", "nav": "Hauptnavigation",
        "bar": "1daily AG · Schweizer Aktiengesellschaft · Steffisburg BE", "contact": "Kontakt", "contact_href": "kontakt.html",
        "cta": "Investor werden", "menu_open": "Menü öffnen", "menu_close": "Menü schliessen", "menu": "Menü",
        "mnav": "Mobile Navigation", "overview": "Übersicht", "lang": "Sprache",
        "legal": "Keine Anlageberatung. Keine Renditegarantie. Investitionen in Jungunternehmen und der Handel mit Finanzinstrumenten können zum Totalverlust führen. Die 1daily AG handelt ausschliesslich auf eigene Rechnung und erbringt keine bewilligungspflichtigen Finanzdienstleistungen.",
        "imprint": "Impressum", "imprint_href": "kontakt.html#impressum", "privacy": "Datenschutz", "privacy_href": "datenschutz.html",
        "switch": "Bisheriges Design ansehen", "foot": "Fusszeile", "addr": "Hardeggweg 2<br>3612 Steffisburg<br>Schweiz"},
 "en": {"skip": "Skip to content", "home": "1daily AG, home", "nav": "Main navigation",
        "bar": "1daily AG · Swiss stock corporation · Steffisburg, Switzerland", "contact": "Contact", "contact_href": "contact.html",
        "cta": "Become an investor", "menu_open": "Open menu", "menu_close": "Close menu", "menu": "Menu",
        "mnav": "Mobile navigation", "overview": "Overview", "lang": "Language",
        "legal": "No investment advice. No guaranteed returns. Investments in start-ups and trading in financial instruments can lead to a total loss. 1daily AG trades exclusively for its own account and does not provide licensed financial services.",
        "imprint": "Legal notice", "imprint_href": "contact.html#impressum", "privacy": "Privacy", "privacy_href": "privacy.html",
        "switch": "View previous design", "foot": "Footer", "addr": "Hardeggweg 2<br>3612 Steffisburg<br>Switzerland"},
}


def lang_links(lang, page):
    """Pfade zur DE- und EN-Version derselben Seite, relativ zur aktuellen Seite."""
    de, en = page[1], page[2]
    if lang == "de":
        return de, "en/" + en
    return "../" + de, en


def old_design_link(lang, page):
    key = page[0]
    if key in ("principles",):
        return "../index.html" if lang == "de" else "../../en/index.html"
    return ("../" + page[1]) if lang == "de" else ("../../en/" + page[2])


def header(lang, page, a):
    t = T[lang]
    de_href, en_href = lang_links(lang, page)
    cur = page[3]
    items = []
    for gid, label, href, intro, links in NAV[lang]:
        cur_attr = ' aria-current="page"' if gid == cur else ""
        lis = "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for l, h in links)
        items.append(
            f'<li class="kdd"><a class="kt" href="{href}"{cur_attr}>{label}</a>'
            f'<div class="kpanel"><div class="kpanel-in"><div class="kpanel-intro"><b>{label}</b><p>{intro}</p>'
            f'<a href="{href}">{t["overview"]} →</a></div><ul>{lis}</ul></div></div></li>')
    mm = []
    for gid, label, href, intro, links in NAV[lang]:
        inner = f'<a href="{href}">{t["overview"]}</a>' + "".join(f'<a href="{h}">{html.escape(l)}</a>' for l, h in links)
        mm.append(f'<details><summary>{label}</summary><div>{inner}</div></details>')
    de_cur = ' aria-current="true"' if lang == "de" else ""
    en_cur = ' aria-current="true"' if lang == "en" else ""
    return f'''<div class="kbar"><div class="wrap"><span>{t["bar"]}</span><div class="kbar-r"><a href="{t["contact_href"]}">{t["contact"]}</a><span class="klang" role="group" aria-label="{t["lang"]}"><a href="{de_href}" data-lang="de" hreflang="de" lang="de"{de_cur}>DE</a><a href="{en_href}" data-lang="en" hreflang="en" lang="en"{en_cur}>EN</a></span></div></div></div>
<header class="site-header"><div class="wrap">
<a class="wordmark" href="index.html" aria-label="{t["home"]}"><img class="logo" src="{a}img/logo-1daily.svg" alt="" width="78" height="30"></a>
<nav class="knav" aria-label="{t["nav"]}"><ul>{"".join(items)}</ul></nav>
<div class="hdr-right"><a class="btn btn-dark btn-sm" href="investor-relations.html#form">{t["cta"]}</a><button class="burger" type="button" data-menu="open" aria-label="{t["menu_open"]}" aria-expanded="false" aria-controls="mmenu"><svg width="26" height="26" viewBox="0 0 28 28" fill="none" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 8h20M4 14h20M4 20h20"/></svg></button></div>
</div></header>
<div class="mmenu" id="mmenu" role="dialog" aria-modal="true" aria-label="{t["menu"]}">
<div class="mmenu-top"><a class="wordmark" href="index.html" aria-label="{t["home"]}"><img class="logo" src="{a}img/logo-1daily.svg" alt="" width="78" height="30"></a><button class="burger close" style="display:inline-flex" type="button" data-menu="close" aria-label="{t["menu_close"]}"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>
<nav aria-label="{t["mnav"]}">{"".join(mm)}<a class="mm-plain" href="{t["contact_href"]}">{t["contact"]}</a></nav>
<div class="mmenu-bottom"><a class="btn btn-dark" href="investor-relations.html#form">{t["cta"]}</a>
<div class="lang" style="align-self:center" aria-label="{t["lang"]}"><a href="{de_href}" data-lang="de" hreflang="de" lang="de"{de_cur}>Deutsch</a><a href="{en_href}" data-lang="en" hreflang="en" lang="en"{en_cur}>English</a></div>
<small>{t["bar"]}</small></div>
</div>
'''


def footer(lang, page, a):
    t = T[lang]
    de_href, en_href = lang_links(lang, page)
    cols = []
    for gid, label, href, intro, links in NAV[lang]:
        lis = "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for l, h in links[:6])
        cols.append(f'<div><h4><a href="{href}">{label}</a></h4><ul>{lis}</ul></div>')
    return f'''<footer class="kfoot"><div class="wrap">
<div class="kfoot-grid"><div class="kfoot-brand"><a class="wordmark" href="index.html" aria-label="{t["home"]}"><img class="logo" src="{a}img/logo-1daily-white.svg" alt="" width="78" height="30"></a><address>1daily AG<br>{t["addr"]}<br>CHE-344.641.720</address></div>{"".join(cols)}</div>
<div class="kfoot-bottom"><p>{t["legal"]} © 2026 1daily AG</p>
<nav class="kfoot-links" aria-label="{t["foot"]}"><a href="{t["imprint_href"]}">{t["imprint"]}</a><a href="{t["privacy_href"]}">{t["privacy"]}</a><span class="klang"><a href="{de_href}" data-lang="de" hreflang="de" lang="de"{' aria-current="true"' if lang=="de" else ""}>DE</a><a href="{en_href}" data-lang="en" hreflang="en" lang="en"{' aria-current="true"' if lang=="en" else ""}>EN</a></span><a class="kswitch" href="{old_design_link(lang, page)}">{t["switch"]}</a></nav></div>
</div></footer>
'''


def add_section_ids(body, lang):
    table = SECTION_IDS[lang]
    parts = re.split(r"(?=<section\b)", body)
    out = []
    for p in parts:
        m = re.match(r"<section\b([^>]*)>", p)
        if m and " id=" not in m.group(1) and "page-hero" not in m.group(1):
            e = re.search(r'class="eyebrow[^"]*"[^>]*>([^<]+)<', p)
            if e and e.group(1).strip() in table:
                p = p.replace("<section", f'<section id="{table[e.group(1).strip()]}"', 1)
        out.append(p)
    return "".join(out)


def transform_head(head, lang, a):
    head = re.sub(r'<script>\(function\(\)\{var d=document\.documentElement,s=null;.*?</script>\n?', "", head, flags=re.S)
    head = re.sub(r'<link rel="stylesheet" href="[^"]*dark\.css[^"]*">\n?', "", head)
    head = re.sub(r'(<link rel="stylesheet" href="[^"]*style\.css[^"]*">)',
                  r'\1\n<link rel="stylesheet" href="' + a + 'css/klassik.css?v=' + CSS_V + '">', head)
    head = re.sub(r'<link rel="preload" href="[^"]*plus-jakarta-sans-latin-800-normal\.woff2"[^>]*>',
                  f'<link rel="preload" href="{a}fonts/source-serif-4-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>', head)
    head = head.replace('<meta name="theme-color" content="#FFFFFF">', '<meta name="theme-color" content="#13233A">')
    # Vorschau nicht indexieren, solange die bisherige Version Standard ist
    head = head.replace("<meta charset=\"utf-8\">", "<meta charset=\"utf-8\">\n<meta name=\"robots\" content=\"noindex, follow\">", 1)
    return head


def fix_paths(s, lang):
    if lang == "de":
        return re.sub(r'(?<=["\'(,\s])assets/', "../assets/", s)
    return s.replace("../assets/", "../../assets/")


def build_page(lang, page):
    key = page[0]
    fname = page[1] if lang == "de" else page[2]
    a = "../assets/" if lang == "de" else "../../assets/"
    if key in NEW_PAGES:
        src = open(os.path.join(SRC, f"{key}.{lang}.html"), encoding="utf-8").read()
    else:
        src = open(os.path.join(ROOT, fname if lang == "de" else "en/" + fname), encoding="utf-8").read()
        src = fix_paths(src, lang)
    head, rest = src.split("</head>", 1)
    head = transform_head(head, lang, a)
    i_main = rest.index('<main id="main">')
    i_end = rest.index("</main>") + len("</main>")
    main = add_section_ids(rest[i_main:i_end], lang)
    tail = rest[i_end:]
    tail = re.sub(r"<footer class=\"site-footer\">.*?</footer>\n?", "", tail, flags=re.S)
    tail = re.sub(r'<script src="[^"]*anim\.js[^"]*"></script>\n?', "", tail)
    body_open = f'<body class="klassik">\n<a class="skip" href="#main">{T[lang]["skip"]}</a>\n'
    out = head + "</head>\n" + body_open + header(lang, page, a) + main + "\n" + footer(lang, page, a) + tail.lstrip("\n")
    dest = os.path.join(OUT, fname if lang == "de" else "en/" + fname)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(out)
    return dest


if __name__ == "__main__":
    for lang in ("de", "en"):
        for p in PAGES:
            print("✓", os.path.relpath(build_page(lang, p), ROOT))
