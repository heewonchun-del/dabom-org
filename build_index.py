# -*- coding: utf-8 -*-
"""Build dabom-org/index.html: 9 languages + browser language detection."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"d:\dev\dabom-org")
EXTRA = json.loads((ROOT / "i18n_extra.json").read_text(encoding="utf-8"))
MT_TARGETS = json.loads((ROOT / "mt_targets.json").read_text(encoding="utf-8"))
OLD = (ROOT / "index.html").read_text(encoding="utf-8")
ICON_HREF = re.search(r'href="(data:image/png;base64,[^"]+)"', OLD).group(1)
ICON_IMG = re.search(
    r'<img src="(data:image/png;base64,[^"]+)" alt="" class="header-icon"', OLD
).group(1)
DOWNLOAD_DABOM = (
    "https://github.com/heewonchun-del/dabom-org/releases/download/"
    "dabom-v3.1.4/Dabom_Setup_Full.exe"
)
DOWNLOAD_OLLAMA = (
    "https://github.com/heewonchun-del/dabom-org/releases/download/"
    "dabom-v3.1.4/OllamaSetup.exe"
)
DOWNLOAD_MATHEON = (
    "https://github.com/heewonchun-del/dabom-org/releases/download/"
    "matheon-v4.1.5/Matheon_Setup_Full.exe"
)
DOWNLOAD_DANOL = (
    "https://github.com/heewonchun-del/dabom-org/releases/download/"
    "danol-v1.3.3/danol_setup_full.zip"
)

LANG_META = [
    ("ar", "العربية"),
    ("de", "Deutsch"),
    ("en", "English"),
    ("es", "Español"),
    ("fr", "Français"),
    ("ja", "日本語"),
    ("ko", "한국어"),
    ("ru", "Русский"),
    ("zh", "中文"),
]
CODES = [c for c, _ in LANG_META]

BASE_PATH = ROOT / "i18n_base.json"


def ul(items: list[str]) -> str:
    return "<ul>\n" + "\n".join(f"            <li>{x}</li>" for x in items) + "\n        </ul>"


def block(lang: str, t: dict) -> str:
    return f"""
    <div data-lang="{lang}" lang="{lang}">
        <h2>{t['about_h2']}</h2>
        <p class="lead">{t['about_lead']}</p>
        <p>{t['about_p1']}</p>
        <p>{t['about_p2']}</p>
    </div>"""


def dabom_block(lang: str, t: dict) -> str:
    return f"""
    <div data-lang="{lang}" lang="{lang}">
        <h2>{t['dabom_h2']}</h2>
        <p class="lead">{t['dabom_lead']}</p>
        <p>{t['dabom_intro']}</p>
        <h3>{t['dabom_one_h3']}</h3>
        <p>{t['dabom_one_p']}</p>
        <h3>{t['dabom_new_h3']}</h3>
        {ul(t['dabom_new_items'])}
        <h3>{t['dabom_adv_h3']}</h3>
        <p>{t['dabom_adv_p']}</p>
        <h3>{t['dabom_feat_h3']}</h3>
        {ul(t['dabom_feat_items'])}
        <h3>{t['dabom_ai_h3']}</h3>
        <p>{t['dabom_ai_p']}</p>
        <h3>{t['dabom_lang_h3']}</h3>
        <p>{t['dabom_lang_p']}</p>
        <h3>{t['dabom_how_h3']}</h3>
        {ul(t['dabom_how_items'])}
        <p><a href="#download-dabom">{t['goto_dl_dabom']}</a></p>
    </div>"""


def matheon_block(lang: str, t: dict) -> str:
    return f"""
    <div data-lang="{lang}" lang="{lang}">
        <h2>{t['matheon_h2']}</h2>
        <p class="lead">{t['matheon_lead']}</p>
        <p>{t['matheon_intro']}</p>
        <h3>{t['matheon_why_h3']}</h3>
        <p>{t['matheon_why_p']}</p>
        <h3>{t['matheon_feat_h3']}</h3>
        {ul(t['matheon_feat_items'])}
        <h3>{t['matheon_ai_h3']}</h3>
        <p>{t['matheon_ai_p']}</p>
        <h3>{t['matheon_lang_h3']}</h3>
        <p>{t['matheon_lang_p']}</p>
        <h3>{t['matheon_how_h3']}</h3>
        {ul(t['matheon_how_items'])}
        <p><a href="#download-matheon">{t['goto_dl_matheon']}</a></p>
    </div>"""


def danol_block(lang: str, t: dict) -> str:
    return f"""
    <div data-lang="{lang}" lang="{lang}">
        <h2>{t['danol_h2']}</h2>
        <p>{t['danol_intro']}</p>
        <h3>{t['games_h3']}</h3>
        <p>{t['games_lead']}</p>
        <h4>{t['g1']}</h4>
        {ul(t['g1_items'])}
        <h4>{t['g2']}</h4>
        {ul(t['g2_items'])}
        <h4>{t['g3']}</h4>
        {ul(t['g3_items'])}
        <h4>{t['g4']}</h4>
        {ul(t['g4_items'])}
        <h4>{t['g5']}</h4>
        {ul(t['g5_items'])}
        <p>{t['ai_note']}</p>
        <h3>{t['lang_h3']}</h3>
        <p>{t['lang_p']}</p>
        <h3>{t['how_h3']}</h3>
        {ul(t['how_items'])}
        <p><a href="#download-danol">{t['goto_dl_danol']}</a></p>
    </div>"""


def dl_block(lang: str, t: dict) -> str:
    return f"""
    <div data-lang="{lang}" lang="{lang}">
        <h2>{t['dl_h2']}</h2>
        <p>{t['dl_lead']}</p>
        <h3 id="download-dabom">{t['dl_dabom_h3']}</h3>
        <p>{t['dl_dabom_lead']}</p>
        <p><a class="button" href="{DOWNLOAD_DABOM}">{t['dl_dabom_btn']}</a></p>
        <p><a class="button" href="{DOWNLOAD_OLLAMA}">{t['dl_ollama_btn']}</a></p>
        <h4>{t['dl_dabom_file_h3']}</h4>
        {ul(t['dl_dabom_file_items'])}
        <h4>{t['dl_dabom_need_h3']}</h4>
        {ul(t['dl_dabom_need_items'])}
        <div class="note">
            <p>{t['dl_dabom_warn']}</p>
        </div>
        <h3 id="download-matheon">{t['dl_matheon_h3']}</h3>
        <p>{t['dl_matheon_lead']}</p>
        <p><a class="button" href="{DOWNLOAD_MATHEON}">{t['dl_matheon_btn']}</a></p>
        <p><a class="button" href="{DOWNLOAD_OLLAMA}">{t['dl_ollama_btn']}</a></p>
        <h4>{t['dl_matheon_file_h3']}</h4>
        {ul(t['dl_matheon_file_items'])}
        <h4>{t['dl_matheon_need_h3']}</h4>
        {ul(t['dl_matheon_need_items'])}
        <div class="note">
            <p>{t['dl_matheon_warn']}</p>
        </div>
        <h3 id="download-danol">{t['dl_danol_h3']}</h3>
        <p>{t['dl_danol_lead']}</p>
        <p><a class="button" href="{DOWNLOAD_DANOL}">{t['dl_danol_btn']}</a></p>
        <h4>{t['dl_danol_file_h3']}</h4>
        {ul(t['dl_danol_file_items'])}
        <h4>{t['dl_danol_need_h3']}</h4>
        {ul(t['dl_danol_need_items'])}
        <div class="note">
            <p>{t['dl_danol_warn']}</p>
        </div>
    </div>"""


def a11y_block(lang: str, t: dict) -> str:
    return f"""
    <div data-lang="{lang}" lang="{lang}">
        <h2>{t['a11y_h2']}</h2>
        <p>{t['a11y_lead']}</p>
        <h3>{t['a11y_h3']}</h3>
        {ul(t['a11y_items'])}
        <p>{t['a11y_end']}</p>
    </div>"""


def contact_block(lang: str, t: dict) -> str:
    return f"""
    <div data-lang="{lang}" lang="{lang}">
        <h2>{t['contact_h2']}</h2>
        <p>{t['contact_p']}</p>
        <p><a href="mailto:support@dabom.org">support@dabom.org</a></p>
    </div>"""


def span_all(key: str, T: dict) -> str:
    return "\n".join(
        f'        <span data-lang="{c}">{T[c][key]}</span>' for c in CODES
    )


def main() -> None:
    # Prefer i18n_base.json if present; else require it
    if not BASE_PATH.exists():
        raise SystemExit("missing i18n_base.json — write en/ko/de first")
    base = json.loads(BASE_PATH.read_text(encoding="utf-8"))
    T = {**base, **EXTRA}
    for c in CODES:
        if c not in T:
            raise SystemExit(f"missing language {c}")

    css_lang = "\n".join(
        f'html[lang="{c}"] [data-lang="{c}"] {{ display: block; }}\n'
        f'html[lang="{c}"] span[data-lang="{c}"] {{ display: inline; }}\n'
        f'html[lang="{c}"] nav li[data-lang="{c}"] {{ display: inline-block; }}\n'
        f'html[lang="{c}"] label[data-lang="{c}"] {{ display: inline; }}'
        for c in CODES
    )
    hreflang = "\n".join(
        f'<link rel="alternate" hreflang="{c}" href="https://dabom.org/?lang={c}">'
        for c in CODES
    )
    og_alt = "\n".join(
        f'<meta property="og:locale:alternate" content="{c}">' for c in CODES if c != "en"
    )
    options = "\n".join(
        f'            <option value="{c}" lang="{c}">{name}</option>' for c, name in LANG_META
    )
    skip = "\n".join(f'    <span data-lang="{c}">{T[c]["skip"]}</span>' for c in CODES)
    labels = "\n".join(
        f'    <label id="lang-label-{c}" class="lang-label" data-lang="{c}" for="lang-select">{T[c]["lang_label"]}</label>'
        for c in CODES
    )
    nav_items = []
    for c in CODES:
        t = T[c]
        nav_items.append(
            f"""        <li data-lang="{c}"><a href="#about">{t['nav_about']}</a></li>
        <li data-lang="{c}"><a href="#dabom">{t['nav_dabom']}</a></li>
        <li data-lang="{c}"><a href="#matheon">{t['nav_matheon']}</a></li>
        <li data-lang="{c}"><a href="#danol">{t['nav_danol']}</a></li>
        <li data-lang="{c}"><a href="#download">{t['nav_download']}</a></li>
        <li data-lang="{c}"><a href="#translate">{t['nav_translate']}</a></li>
        <li data-lang="{c}"><a href="#accessibility">{t['nav_a11y']}</a></li>
        <li data-lang="{c}"><a href="#contact">{t['nav_contact']}</a></li>"""
        )
    prompt_titles = "\n".join(
        f'        <span data-lang="{c}" id="prompt-title-{c}">{T[c]["prompt_h2"]}</span>'
        for c in CODES
    )
    prompt_ps = "\n".join(
        f'        <p data-lang="{c}">{T[c]["prompt_p"]}</p>' for c in CODES
    )
    prompt_btns = "\n".join(
        f'        <button type="button" class="button" data-lang="{c}" id="prompt-dismiss" hidden>{T[c]["prompt_dismiss"]}</button>'
        for c in CODES
    )
    # one dismiss button text updated by JS is simpler:
    prompt_dismiss_map = {c: T[c]["prompt_dismiss"] for c in CODES}
    titles_map = {c: T[c]["title"] for c in CODES}
    live_map = {c: name for c, name in LANG_META}
    nav_label_map = {c: T[c]["nav_label"] for c in CODES}

    taglines = "\n".join(
        f'    <p class="tagline" data-lang="{c}">{T[c]["tagline"]}</p>' for c in CODES
    )
    bylines = "\n".join(
        f'        <span data-lang="{c}">{T[c]["byline"]}</span>' for c in CODES
    )
    brands = "\n".join(
        f'        <span data-lang="{c}">{T[c]["brand"]}</span>' for c in CODES
    )
    footer_by = "\n".join(
        f'        <span data-lang="{c}">{T[c]["footer_by"]}</span>' for c in CODES
    )

    about = "\n".join(block(c, T[c]) for c in CODES)
    # fix about section - block() wrongly used about fields only — rewrite
    about = "\n".join(
        f"""    <div data-lang="{c}" lang="{c}">
        <h2>{T[c]['about_h2']}</h2>
        <p class="lead">{T[c]['about_lead']}</p>
        <p>{T[c]['about_p1']}</p>
        <p>{T[c]['about_p2']}</p>
    </div>"""
        for c in CODES
    )
    dabom = "\n".join(dabom_block(c, T[c]) for c in CODES)
    matheon = "\n".join(matheon_block(c, T[c]) for c in CODES)
    danol = "\n".join(danol_block(c, T[c]) for c in CODES)
    download = "\n".join(dl_block(c, T[c]) for c in CODES)
    a11y = "\n".join(a11y_block(c, T[c]) for c in CODES)
    contact = "\n".join(contact_block(c, T[c]) for c in CODES)

    mt_options = "\n".join(
        f'            <option value="{code}">{label}</option>' for code, label in MT_TARGETS
    )
    mt_headings = "\n".join(
        f'        <div data-lang="{c}" lang="{c}">\n'
        f'            <h2>{T[c]["mt_h2"]}</h2>\n'
        f'            <p class="lead">{T[c]["mt_lead"]}</p>\n'
        f"        </div>"
        for c in CODES
    )
    mt_labels = "\n".join(
        f'            <label data-lang="{c}" id="mt-label-{c}" for="mt-lang">{T[c]["mt_label"]}</label>'
        for c in CODES
    )
    mt_notes = "\n".join(
        f'        <p class="note" data-lang="{c}" lang="{c}">{T[c]["mt_note"]}</p>'
        for c in CODES
    )
    mt_submit_map = {c: T[c]["mt_submit"] for c in CODES}

    translate_section = f"""
<section id="translate">
{mt_headings}
    <form id="mt-form">
        <p class="mt-controls">
{mt_labels}
            <select id="mt-lang" required>
                <option value="">—</option>
{mt_options}
            </select>
        </p>
        <p>
            <button type="submit" class="button" id="mt-submit">{T['en']['mt_submit']}</button>
        </p>
    </form>
{mt_notes}
</section>
"""

    html = f"""<!DOCTYPE html>
<html lang="en" id="html-root">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{T['en']['title']}</title>
<meta name="description" content="{T['en']['desc']}">
<link rel="canonical" href="https://dabom.org/">
{hreflang}
<link rel="alternate" hreflang="x-default" href="https://dabom.org/">
<meta property="og:title" content="Dabom | AI daily-life assistant — Dabom.org">
<meta property="og:description" content="{T['en']['og_desc']}">
<meta property="og:url" content="https://dabom.org/">
<meta property="og:type" content="website">
<meta property="og:locale" content="en">
{og_alt}
<link rel="icon" type="image/png" href="{ICON_HREF}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Dabom",
  "alternateName": "다봄",
  "applicationCategory": "AccessibilityApplication",
  "operatingSystem": "Windows 10 or later, 64-bit",
  "softwareVersion": "3.1",
  "inLanguage": {json.dumps(CODES, ensure_ascii=False)},
  "description": "An AI-based Windows daily-life assistant for people who are blind or have low vision.",
  "downloadUrl": "{DOWNLOAD_DABOM}",
  "url": "https://dabom.org/",
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "The Dabom Project",
    "url": "https://dabom.org/"
  }}
}}
</script>
<script>
(function () {{
  var SUPPORTED = {json.dumps(CODES)};
  function mapTag(tag) {{
    if (!tag) return null;
    tag = String(tag).toLowerCase().replace(/_/g, "-");
    var primary = tag.split("-")[0];
    if (primary === "zh") return "zh";
    if (SUPPORTED.indexOf(primary) >= 0) return primary;
    return null;
  }}
  function detect() {{
    try {{
      var q = new URLSearchParams(location.search).get("lang");
      if (q && SUPPORTED.indexOf(q) >= 0) return {{ lang: q, reason: "url" }};
      var saved = localStorage.getItem("dabom-lang");
      if (saved && SUPPORTED.indexOf(saved) >= 0) return {{ lang: saved, reason: "saved" }};
      var list = navigator.languages && navigator.languages.length
        ? navigator.languages
        : [navigator.language || navigator.userLanguage || ""];
      for (var i = 0; i < list.length; i++) {{
        var m = mapTag(list[i]);
        if (m) return {{ lang: m, reason: "browser" }};
      }}
    }} catch (e) {{}}
    return {{ lang: "en", reason: "fallback" }};
  }}
  var d = detect();
  document.documentElement.lang = d.lang;
  document.documentElement.setAttribute("data-lang-reason", d.reason);
  if (d.lang === "ar") document.documentElement.dir = "rtl";
  else document.documentElement.dir = "ltr";
}})();
</script>
<style>
:root {{
    --primary: #1a2a4a;
    --accent: #1d4ed8;
    --accent-dark: #1e3a8a;
    --text: #111827;
    --muted: #374151;
    --border: #d1d5db;
    --focus: #b45309;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    font-family: Arial, Helvetica, sans-serif;
    line-height: 1.75;
    background: #fff;
    color: var(--text);
}}
a {{ color: #1e40af; }}
a:focus, button:focus, select:focus {{
    outline: 3px solid var(--focus);
    outline-offset: 3px;
}}
.skip-link {{
    position: absolute;
    top: -48px;
    left: 10px;
    background: #000;
    color: #fff;
    padding: 8px 12px;
    z-index: 100;
}}
.skip-link:focus {{ top: 10px; }}
html[dir="rtl"] .skip-link {{ left: auto; right: 10px; }}
.visually-hidden {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}}
header {{
    background: #1a2a4a;
    color: #fff;
    padding: 48px 20px 40px;
    text-align: center;
}}
.header-icon {{
    width: 96px;
    height: 96px;
    margin: 0 auto 16px;
    display: block;
}}
header h1 {{
    font-size: 2.4em;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
}}
header .tagline {{
    font-size: 1.15em;
    color: #e5e7eb;
    max-width: 40em;
    margin: 0 auto 12px;
}}
.project-identity {{
    font-size: 0.95em;
    color: #e5e7eb;
}}
.project-identity a {{ color: #fff; }}
.lang-bar {{
    background: #111827;
    padding: 10px 20px;
    text-align: right;
}}
html[dir="rtl"] .lang-bar {{ text-align: left; }}
.lang-bar label.lang-label {{
    color: #f9fafb;
    margin-right: 10px;
    font-size: 1em;
}}
html[dir="rtl"] .lang-bar label.lang-label {{ margin-right: 0; margin-left: 10px; }}
.lang-bar label {{
    color: #f9fafb;
    margin-right: 10px;
    font-size: 1em;
}}
html[dir="rtl"] .lang-bar label {{ margin-right: 0; margin-left: 10px; }}
.lang-bar select {{
    font-size: 1em;
    padding: 6px 10px;
    border-radius: 4px;
    border: 1px solid #d1d5db;
    background: #fff;
    color: #111;
    max-width: 100%;
}}
#lang-prompt {{
    background: #fff7ed;
    border: 2px solid #c2410c;
    padding: 18px 20px;
    margin: 0;
}}
#lang-prompt[hidden] {{ display: none !important; }}
#lang-prompt h2 {{
    font-size: 1.25em;
    color: #9a3412;
    border: 0;
    margin: 0 0 10px;
    padding: 0;
}}
#lang-prompt .button {{ margin-top: 12px; }}
nav {{
    background: #1e3a5f;
    padding: 8px 20px;
    position: sticky;
    top: 0;
    z-index: 50;
}}
nav ul {{
    list-style: none;
    text-align: center;
}}
nav li {{ display: inline-block; }}
nav a {{
    color: #f8fafc;
    display: inline-block;
    margin: 6px 10px;
    text-decoration: underline;
    font-weight: bold;
}}
nav a:hover, nav a:focus {{ color: #fff; }}
main {{
    max-width: 960px;
    margin: auto;
    padding: 36px 20px 48px;
}}
section {{ margin-bottom: 56px; }}
h2 {{
    font-size: 1.7em;
    border-bottom: 2px solid var(--border);
    padding-bottom: 8px;
    margin-bottom: 16px;
    color: var(--primary);
}}
h3 {{
    font-size: 1.15em;
    margin-top: 22px;
    margin-bottom: 8px;
    color: #1e3a5f;
}}
h4 {{
    font-size: 1.05em;
    margin-top: 18px;
    margin-bottom: 8px;
    color: #1e3a5f;
}}
p {{ margin-bottom: 14px; }}
ul {{ padding-left: 1.4em; margin-bottom: 14px; }}
html[dir="rtl"] ul {{ padding-left: 0; padding-right: 1.4em; }}
li {{ margin-bottom: 6px; }}
.lead {{ font-size: 1.12em; }}
.note {{
    background: #f3f4f6;
    border: 1px solid var(--border);
    padding: 16px 18px;
    margin: 18px 0;
}}
.button {{
    display: inline-block;
    padding: 14px 22px;
    background: var(--accent);
    color: #fff;
    text-decoration: none;
    border: 0;
    border-radius: 6px;
    font-weight: bold;
    cursor: pointer;
    font-size: 1em;
}}
.button:hover, .button:focus {{ background: var(--accent-dark); color: #fff; }}
.mt-controls select {{
    font-size: 1em;
    padding: 8px 10px;
    max-width: 100%;
    min-width: 16em;
    margin-top: 8px;
}}
.mt-controls label {{
    margin-right: 10px;
}}
html[dir="rtl"] .mt-controls label {{ margin-right: 0; margin-left: 10px; }}
footer {{
    background: #111827;
    color: #e5e7eb;
    text-align: center;
    padding: 28px 20px;
    font-size: 0.95em;
}}
footer a {{ color: #bfdbfe; }}
[data-lang] {{ display: none; }}
{css_lang}
@media (max-width: 640px) {{
    header h1 {{ font-size: 2em; }}
    .button {{ display: block; text-align: center; width: 100%; margin: 0.75rem 0; }}
    .lang-bar {{ text-align: center; }}
    html[dir="rtl"] .lang-bar {{ text-align: center; }}
}}
</style>
</head>
<body>

<a href="#main-content" class="skip-link">
{skip}
</a>

<div class="lang-bar">
{labels}
    <select id="lang-select" aria-labelledby="lang-label-en">
{options}
    </select>
</div>
<div id="lang-status" class="visually-hidden" aria-live="polite"></div>

<div id="lang-prompt" hidden role="region" aria-labelledby="lang-prompt-heading">
    <h2 id="lang-prompt-heading">{T['en']['prompt_h2']}</h2>
{prompt_ps}
    <p>
        <label for="lang-select-prompt" class="visually-hidden">{T['en']['lang_label']}</label>
        <select id="lang-select-prompt" aria-label="{T['en']['lang_label']}">
{options}
        </select>
    </p>
    <button type="button" class="button" id="prompt-dismiss">{T['en']['prompt_dismiss']}</button>
</div>

<header>
    <img src="{ICON_IMG}" alt="" class="header-icon" width="96" height="96">
    <p class="project-identity">
{brands}
    </p>
    <h1>Dabom</h1>
{taglines}
    <p class="project-identity">
{bylines}
        <a href="https://dabom.org/">dabom.org</a>
    </p>
</header>

<nav id="main-nav" aria-label="Main">
    <ul>
{chr(10).join(nav_items)}
    </ul>
</nav>

<main id="main-content">

<section id="about">
{about}
</section>

<section id="dabom">
{dabom}
</section>

<section id="matheon">
{matheon}
</section>

<section id="danol">
{danol}
</section>

<section id="download">
{download}
</section>

{translate_section}

<section id="accessibility">
{a11y}
</section>

<section id="contact">
{contact}
</section>

</main>

<footer>
    <p>The Dabom Project</p>
    <p>
{footer_by}
    </p>
    <p><a href="mailto:support@dabom.org">support@dabom.org</a></p>
    <p>© 2026 Dabom.org</p>
</footer>

<script>
var SUPPORTED = {json.dumps(CODES)};
var titles = {json.dumps(titles_map, ensure_ascii=False)};
var liveText = {json.dumps(live_map, ensure_ascii=False)};
var navLabels = {json.dumps(nav_label_map, ensure_ascii=False)};
var promptTitles = {json.dumps({c: T[c]["prompt_h2"] for c in CODES}, ensure_ascii=False)};
var promptDismiss = {json.dumps(prompt_dismiss_map, ensure_ascii=False)};
var metaDesc = {json.dumps({c: T[c]["desc"] for c in CODES}, ensure_ascii=False)};
var mtSubmit = {json.dumps(mt_submit_map, ensure_ascii=False)};

function setLang(lang, announce, fromPrompt) {{
    if (SUPPORTED.indexOf(lang) < 0) lang = "en";
    document.documentElement.lang = lang;
    document.documentElement.dir = (lang === "ar") ? "rtl" : "ltr";
    document.title = titles[lang] || titles.en;

    var meta = document.querySelector('meta[name="description"]');
    if (meta) meta.setAttribute("content", metaDesc[lang] || metaDesc.en);

    var sel = document.getElementById("lang-select");
    if (sel) sel.value = lang;
    var sel2 = document.getElementById("lang-select-prompt");
    if (sel2) sel2.value = lang;

    // Point aria-labelledby at the visible language label
    if (sel) sel.setAttribute("aria-labelledby", "lang-label-" + lang);

    var mtLang = document.getElementById("mt-lang");
    if (mtLang) mtLang.setAttribute("aria-labelledby", "mt-label-" + lang);
    var mtBtn = document.getElementById("mt-submit");
    if (mtBtn) mtBtn.textContent = mtSubmit[lang] || mtSubmit.en;

    var nav = document.getElementById("main-nav");
    if (nav) nav.setAttribute("aria-label", navLabels[lang] || "Main");

    var ph = document.getElementById("lang-prompt-heading");
    if (ph) ph.textContent = promptTitles[lang] || promptTitles.en;
    var pd = document.getElementById("prompt-dismiss");
    if (pd) pd.textContent = promptDismiss[lang] || promptDismiss.en;

    try {{ localStorage.setItem("dabom-lang", lang); }} catch (e) {{}}

    try {{
        var url = new URL(location.href);
        url.searchParams.set("lang", lang);
        history.replaceState(null, "", url.pathname + url.search + url.hash);
    }} catch (e) {{}}

    if (fromPrompt) {{
        var prompt = document.getElementById("lang-prompt");
        if (prompt) prompt.hidden = true;
    }}

    if (announce) {{
        var status = document.getElementById("lang-status");
        status.textContent = "";
        window.setTimeout(function () {{ status.textContent = liveText[lang] || lang; }}, 50);
    }}
}}

document.getElementById("lang-select").addEventListener("change", function (e) {{
    setLang(e.target.value, true, true);
}});
document.getElementById("lang-select-prompt").addEventListener("change", function (e) {{
    setLang(e.target.value, true, true);
}});
document.getElementById("prompt-dismiss").addEventListener("click", function () {{
    setLang("en", true, true);
}});

document.getElementById("mt-form").addEventListener("submit", function (e) {{
    e.preventDefault();
    var tl = document.getElementById("mt-lang").value;
    if (!tl) {{
        document.getElementById("mt-lang").focus();
        return;
    }}
    // Translate the English edition for more stable machine output.
    var source = "https://dabom.org/?lang=en";
    var dest =
        "https://translate.google.com/translate?sl=en&tl=" +
        encodeURIComponent(tl) +
        "&u=" +
        encodeURIComponent(source);
    var status = document.getElementById("lang-status");
    status.textContent = "";
    window.setTimeout(function () {{
        status.textContent = (mtSubmit[document.documentElement.lang] || mtSubmit.en);
        window.setTimeout(function () {{ location.href = dest; }}, 200);
    }}, 30);
}});

(function init() {{
    var lang = document.documentElement.lang || "en";
    var reason = document.documentElement.getAttribute("data-lang-reason") || "";
    setLang(lang, false, false);
    if (reason === "fallback") {{
        var prompt = document.getElementById("lang-prompt");
        if (prompt) {{
            prompt.hidden = false;
            // Keep English content visible; prompt asks user to pick.
        }}
    }}
}})();
</script>

</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8", newline="\n")
    print("wrote", ROOT / "index.html", "bytes", len(html.encode("utf-8")))


if __name__ == "__main__":
    main()
