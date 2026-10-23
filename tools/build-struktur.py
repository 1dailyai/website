#!/usr/bin/env python3
"""Setzt die neue Inhaltsstruktur (Navigation mit Untermenüs, Fusszeile mit
Sitemap, Sprungmarken) in den Seiten der Hauptfassung um – im bisherigen Design.

Die Menüstruktur ist dieselbe wie in der Klassik-Fassung (tools/build-klassik.py,
Liste NAV). Änderungen an Menüpunkten deshalb dort vornehmen und danach beide
Scripts ausführen:

    python3 tools/build-struktur.py
    python3 tools/build-klassik.py

Das Script ersetzt nur Kopfzeile, mobiles Menü und Fusszeile und ergänzt fehlende
Abschnitts-IDs. Der Inhalt zwischen <main> und </main> bleibt unangetastet.
"""
import os, re, html, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("bk", os.path.join(ROOT, "tools", "build-klassik.py"))
bk = importlib.util.module_from_spec(spec); spec.loader.exec_module(bk)

T = {
 "de": {"home": "1daily AG, zur Startseite", "nav": "Hauptnavigation", "cta": "Investor werden",
        "theme": "Farbschema wechseln", "menu_open": "Menü öffnen", "menu_close": "Menü schliessen", "menu": "Menü",
        "mnav": "Mobile Navigation", "overview": "Übersicht", "contact": "Kontakt", "contact_href": "kontakt.html",
        "lang": "Sprache", "lang_pick": "Sprache wählen", "scheme": "Farbschema", "light": "Hell", "dark": "Dunkel",
        "foot": "Fusszeile", "imprint": "Impressum", "imprint_href": "kontakt.html#impressum",
        "privacy": "Datenschutz", "privacy_href": "datenschutz.html", "place": "1daily AG · Steffisburg, Schweiz",
        "addr": "1daily AG<br>Hardeggweg 2<br>3612 Steffisburg<br>Schweiz",
        "legal": "Keine Anlageberatung. Keine Renditegarantie. Investitionen in Jungunternehmen und der Handel mit Finanzinstrumenten können zum Totalverlust führen. © 2026 1daily AG · Hardeggweg 2, 3612 Steffisburg, Schweiz · CHE-344.641.720"},
 "en": {"home": "1daily AG, home", "nav": "Main navigation", "cta": "Become an investor",
        "theme": "Switch colour scheme", "menu_open": "Open menu", "menu_close": "Close menu", "menu": "Menu",
        "mnav": "Mobile navigation", "overview": "Overview", "contact": "Contact", "contact_href": "contact.html",
        "lang": "Language", "lang_pick": "Choose language", "scheme": "Colour scheme", "light": "Light", "dark": "Dark",
        "foot": "Footer", "imprint": "Legal notice", "imprint_href": "contact.html#impressum",
        "privacy": "Privacy", "privacy_href": "privacy.html", "place": "1daily AG · Steffisburg, Switzerland",
        "addr": "1daily AG<br>Hardeggweg 2<br>3612 Steffisburg<br>Switzerland",
        "legal": "No investment advice. No guaranteed returns. Investments in start-ups and trading in financial instruments can lead to a total loss. © 2026 1daily AG · Hardeggweg 2, 3612 Steffisburg, Switzerland · CHE-344.641.720"},
}

ARROW = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8A6219" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
MOON = '<svg class="ic-moon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 14.2A8.5 8.5 0 0 1 9.8 3.5a8.5 8.5 0 1 0 10.7 10.7z"/></svg>'
SUN = '<svg class="ic-sun" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M4.6 4.6l1.6 1.6M17.8 17.8l1.6 1.6M2.5 12h2.2M19.3 12h2.2M4.6 19.4l1.6-1.6M17.8 6.2l1.6-1.6"/></svg>'
BURGER = '<svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><defs><linearGradient id="bgold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8A6624"/><stop offset=".55" stop-color="#D9B862"/><stop offset="1" stop-color="#B8892E"/></linearGradient></defs><path stroke="url(#bgold)" d="M4 8h20M10 14h14M16 20h8"/></svg>'


def logos(a):
    return (f'<img class="logo logo-l" src="{a}img/logo-1daily.svg" alt="" width="78" height="30">'
            f'<img class="logo logo-d" src="{a}img/logo-1daily-white.svg" alt="" width="78" height="30">')


def lang_links(lang, de, en):
    if lang == "de":
        return de, ("en/" + en if en else "en/index.html")
    return "../" + de, en


def header(lang, de, en, group, a):
    t = T[lang]
    de_h, en_h = lang_links(lang, de, en)
    dds = []
    for gid, label, href, intro, links in bk.NAV[lang]:
        cur = ' aria-current="page"' if gid == group else ""
        lis = "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for l, h in links)
        dds.append(f'<div class="dd"><a class="nl" href="{href}"{cur}>{label}</a><div class="ddp"><div class="ddp-in">'
                   f'<div class="ddp-intro"><b>{label}</b><p>{intro}</p><a class="link-arrow" href="{href}">{t["overview"]} →</a></div>'
                   f'<ul>{lis}</ul></div></div></div>')
    mm = []
    for gid, label, href, intro, links in bk.NAV[lang]:
        inner = f'<a href="{href}">{t["overview"]}</a>' + "".join(f'<a href="{h}">{html.escape(l)}</a>' for l, h in links)
        mm.append(f'<details><summary>{label}</summary><div>{inner}</div></details>')
    dc = ' aria-current="true"' if lang == "de" else ""
    ec = ' aria-current="true"' if lang == "en" else ""
    return f'''<header class="site-header"><div class="wrap">
<a class="wordmark" href="index.html" aria-label="{t["home"]}">{logos(a)}</a>
<div class="hdr-right"><nav class="nav nav-dd" aria-label="{t["nav"]}">{"".join(dds)}<a class="btn btn-dark btn-sm" href="investor-relations.html#form">{t["cta"]}</a></nav>
<button class="theme-toggle" type="button" data-theme-toggle aria-label="{t["theme"]}" title="{t["theme"]}">{MOON}{SUN}</button><button class="burger" type="button" data-menu="open" aria-label="{t["menu_open"]}" aria-expanded="false" aria-controls="mmenu">{BURGER}</button></div>
</div></header>
<div class="mmenu" id="mmenu" role="dialog" aria-modal="true" aria-label="{t["menu"]}">
<div class="mmenu-top"><a class="wordmark" href="index.html" aria-label="{t["home"]}">{logos(a)}</a><button class="burger close" style="display:inline-flex" type="button" data-menu="close" aria-label="{t["menu_close"]}"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0F0F0F" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>
<nav class="mm-dd" aria-label="{t["mnav"]}">{"".join(mm)}<a href="{t["contact_href"]}">{t["contact"]}{ARROW}</a></nav>
<div class="mmenu-bottom"><a class="btn btn-gold" href="investor-relations.html#form">{t["cta"]}</a>
<div class="lang" style="align-self:center" aria-label="{t["lang"]}"><a href="{de_h}" data-lang="de" hreflang="de" lang="de"{dc}>Deutsch</a><a href="{en_h}" data-lang="en" hreflang="en" lang="en"{ec}>English</a></div>
<small>{t["place"]}</small></div>
</div>
'''


def footer(lang, de, en, a):
    t = T[lang]
    de_h, en_h = lang_links(lang, de, en)
    cols = "".join(
        f'<div><h4><a href="{href}">{label}</a></h4><ul>' +
        "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for l, h in links[:6]) + '</ul></div>'
        for gid, label, href, intro, links in bk.NAV[lang])
    dc = ' aria-current="true"' if lang == "de" else ""
    ec = ' aria-current="true"' if lang == "en" else ""
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-cols"><div class="foot-brand"><a class="wordmark" href="index.html" aria-label="{t["home"]}">{logos(a)}</a><address>{t["addr"]}</address></div>{cols}</div>
<div class="foot-top"><nav class="foot-nav" aria-label="{t["foot"]}"><a href="{t["contact_href"]}">{t["contact"]}</a><a href="{t["imprint_href"]}">{t["imprint"]}</a><a href="{t["privacy_href"]}">{t["privacy"]}</a></nav>
<div class="foot-switch"><div class="lang" role="group" aria-label="{t["lang_pick"]}"><a href="{de_h}" data-lang="de" hreflang="de" lang="de"{dc}>DE</a><a href="{en_h}" data-lang="en" hreflang="en" lang="en"{ec}>EN</a></div><div class="lang theme-seg" role="group" aria-label="{t["scheme"]}"><button type="button" data-theme-set="light">{t["light"]}</button><button type="button" data-theme-set="dark">{t["dark"]}</button></div></div></div>
<p class="foot-legal">{t["legal"]}</p>
</div></footer>
'''


def rebuild(path, lang, de, en, group):
    s = open(path, encoding="utf-8").read()
    a = "assets/" if lang == "de" else "../assets/"
    i_h = s.index('<header class="site-header">')
    i_m = s.index('<main id="main">')
    s = s[:i_h] + header(lang, de, en, group, a) + s[i_m:]
    i_m = s.index('<main id="main">'); i_e = s.index("</main>") + len("</main>")
    s = s[:i_m] + bk.add_section_ids(s[i_m:i_e], lang) + s[i_e:]
    s = re.sub(r'<footer class="site-footer">.*?</footer>\n?', lambda m: footer(lang, de, en, a), s, flags=re.S)
    open(path, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    for key, de, en, group in bk.PAGES:
        rebuild(os.path.join(ROOT, de), "de", de, en, group); print("✓", de)
        rebuild(os.path.join(ROOT, "en", en), "en", de, en, group); print("✓ en/" + en)
    rebuild(os.path.join(ROOT, "404.html"), "de", "index.html", None, None); print("✓ 404.html")
