#!/usr/bin/env python3
"""Turn Mor's grammar guide (.docx) into data/grammar/index.json.

The guide is converted as it is: headings, paragraphs, bold / italic /
underline, lists and tables (with merged and coloured cells).  It is split
into sections at each heading, so the app can open one topic at a time.

    python3 tools/build_grammar.py "Pali Grammar Summary.docx"
"""
import html, json, os, re, sys, unicodedata, zipfile
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# only very clear typos are corrected (reported to Mor)
FIXES = [("pahanāya", "pahānāya"), ("gatssa", "gatassa"), ("abijānāti", "abhijānāti"),
         ("bhkkhu", "bhikkhu"), ("whould", "would"), ("speach", "speech"), ("׳", "’")]
FIXED = []

# coloured cells: keep the colour, with a matching dark-mode shade (see app.css)
FILLS = {"FFF2CC": "c-yel", "DEEAF6": "c-blu", "D9E2F3": "c-blu2", "FBE4E6": "c-pnk"}


def on(el, tag):
    x = el.find(tag)
    if x is None:
        return False
    v = x.get(W + "val")
    return v not in ("0", "false", "none")


def fix(t):
    t = unicodedata.normalize("NFC", t)
    for a, b in FIXES:
        if a in t:
            FIXED.append((a, b))
            t = t.replace(a, b)
    return t


def runs_html(p):
    """Inline content of a paragraph."""
    out = []

    def walk(node):
        for ch in node:
            tag = ch.tag
            if tag == W + "r":
                rpr = ch.find(W + "rPr")
                b = i = u = False
                if rpr is not None:
                    b, i = on(rpr, W + "b"), on(rpr, W + "i")
                    ue = rpr.find(W + "u")
                    u = ue is not None and ue.get(W + "val") != "none"
                for x in ch:
                    if x.tag == W + "t":
                        out.append((x.text or "", b, i, u))
                    elif x.tag == W + "tab":
                        out.append((" ", False, False, False))
                    elif x.tag in (W + "br", W + "cr"):
                        out.append(("\n", False, False, False))
            elif tag in (W + "hyperlink", W + "smartTag", W + "ins", W + "fldSimple", W + "sdtContent"):
                walk(ch)
            elif tag == W + "sdt":
                c = ch.find(W + "sdtContent")
                if c is not None:
                    walk(c)
    walk(p)
    # merge neighbours with the same formatting, then build html
    merged = []
    for t, b, i, u in out:
        if merged and merged[-1][1:] == (b, i, u) and t != "\n" and merged[-1][0] != "\n":
            merged[-1] = (merged[-1][0] + t, b, i, u)
        else:
            merged.append((t, b, i, u))
    s = ""
    for t, b, i, u in merged:
        if t == "\n":
            s += "<br>"
            continue
        h = html.escape(fix(t), quote=False)
        if not t.strip():
            s += h
            continue
        lead = re.match(r"^\s*", h).group(0)
        trail = re.search(r"\s*$", h).group(0)
        core = h.strip()
        if u: core = f"<u>{core}</u>"
        if i: core = f"<i>{core}</i>"
        if b: core = f"<b>{core}</b>"
        s += lead + core + trail
    s = re.sub(r"(<br>\s*)+$", "", s.strip())
    s = re.sub(r"^(\s*<br>)+", "", s)
    s = s.replace("</b><b>", "").replace("</i><i>", "")
    return s.strip()


def text_of(p):
    return "".join(t.text or "" for t in p.iter(W + "t")).strip()


class Numbering:
    def __init__(self, z):
        self.fmt = {}
        try:
            root = ET.fromstring(z.read("word/numbering.xml"))
        except KeyError:
            return
        absf = {}
        for a in root.findall(W + "abstractNum"):
            lv = {}
            for l in a.findall(W + "lvl"):
                f = l.find(W + "numFmt")
                lv[l.get(W + "ilvl")] = f.get(W + "val") if f is not None else "bullet"
            absf[a.get(W + "abstractNumId")] = lv
        for n in root.findall(W + "num"):
            a = n.find(W + "abstractNumId").get(W + "val")
            self.fmt[n.get(W + "numId")] = absf.get(a, {})

    def kind(self, numId, ilvl):
        f = self.fmt.get(numId, {}).get(ilvl or "0", "bullet")
        return "ol" if f in ("decimal", "lowerLetter", "upperLetter", "lowerRoman", "upperRoman") else "ul"


TOC_LEVEL = {}   # bookmark name -> heading level, read from the table of contents
PROMOTE = {}     # id(paragraph) -> level, for headings found through TOC bookmarks


def read_toc(body):
    for p in body.iter(W + "p"):
        ppr = p.find(W + "pPr")
        st = ppr.find(W + "pStyle") if ppr is not None else None
        m = re.match(r"TOC(\d)", st.get(W + "val")) if st is not None else None
        if not m:
            continue
        for h in p.iter(W + "hyperlink"):
            a = h.get(W + "anchor")
            if a:
                TOC_LEVEL[a] = int(m.group(1))
    # a bookmark sits in the heading paragraph itself or in an empty one just before it
    carry = None
    for p in body.findall(W + "p"):
        names = [b.get(W + "name") for b in p.iter(W + "bookmarkStart")]
        lv = next((TOC_LEVEL[n] for n in names if n in TOC_LEVEL), None) or carry
        if lv is None:
            continue
        if text_of(p):
            PROMOTE[id(p)] = lv
            carry = None
        else:
            carry = lv


def para_info(p, num):
    ppr = p.find(W + "pPr")
    style, level, lst, jc = "", None, None, ""
    if ppr is not None:
        s = ppr.find(W + "pStyle")
        style = s.get(W + "val") if s is not None else ""
        o = ppr.find(W + "outlineLvl")
        if o is not None:
            level = int(o.get(W + "val")) + 1
        np_ = ppr.find(W + "numPr")
        if np_ is not None and np_.find(W + "numId") is not None and np_.find(W + "numId").get(W + "val") != "0":
            il = np_.find(W + "ilvl")
            lst = num.kind(np_.find(W + "numId").get(W + "val"), il.get(W + "val") if il is not None else "0")
        j = ppr.find(W + "jc")
        jc = j.get(W + "val") if j is not None else ""
    m = re.match(r"Heading(\d)", style)
    if m:
        level = int(m.group(1))
    if id(p) in PROMOTE:
        level, lst = PROMOTE[id(p)], None
    return style, level, lst, jc


CUR = {"title": ""}


def table_html(tbl, num):
    rows = tbl.findall(W + "tr")
    grid = []  # each row: list of cells dict
    for tr in rows:
        cells, col = [], 0
        for tc in tr.findall(W + "tc"):
            pr = tc.find(W + "tcPr")
            span, vm, fill = 1, None, None
            if pr is not None:
                g = pr.find(W + "gridSpan")
                if g is not None:
                    span = int(g.get(W + "val"))
                v = pr.find(W + "vMerge")
                if v is not None:
                    vm = v.get(W + "val") or "continue"
                sh = pr.find(W + "shd")
                if sh is not None:
                    f = (sh.get(W + "fill") or "").upper()
                    if f in FILLS:
                        fill = FILLS[f]
            cells.append({"col": col, "span": span, "vm": vm, "fill": fill, "html": blocks_html(list(tc), num), "rowspan": 1})
            col += span
        grid.append(cells)
    # resolve vertical merges
    for ri, cells in enumerate(grid):
        for c in cells:
            if c["vm"] == "continue":
                for rj in range(ri - 1, -1, -1):
                    up = next((x for x in grid[rj] if x["col"] == c["col"] and not x.get("gone")), None)
                    if up is not None:
                        up["rowspan"] += 1
                        c["gone"] = True
                        break
    # drop columns that are empty in every row (layout leftovers)
    ncol = max((c["col"] + c["span"] for r in grid for c in r), default=0)
    used = [False] * ncol
    for r in grid:
        for c in r:
            if not c.get("gone") and re.sub(r"<[^>]+>|\s|&nbsp;", "", c["html"]):
                for k in range(c["col"], c["col"] + c["span"]):
                    used[k] = True
    cls = ' class="t-practice"' if CUR["title"].startswith("Practicing") and sum(used) == 1 else ""
    out = [f'<div class="tbl"><table{cls}>']
    for r in grid:
        tds = []
        for c in r:
            if c.get("gone"):
                continue
            span = sum(1 for k in range(c["col"], c["col"] + c["span"]) if used[k])
            if span == 0:
                continue
            attrs = ""
            if span > 1: attrs += f' colspan="{span}"'
            if c["rowspan"] > 1: attrs += f' rowspan="{c["rowspan"]}"'
            if c["fill"]: attrs += f' class="{c["fill"]}"'
            tds.append(f"<td{attrs}>{c['html']}</td>")
        if tds:
            out.append("<tr>" + "".join(tds) + "</tr>")
    out.append("</table></div>")
    return "".join(out)


def is_rule(h):
    """A list line that names a rule: it opens with a bold phrase of several words,
    followed by nothing, a note in brackets, or a new line."""
    m = re.match(r"<b>([^<]+)</b>(.*)$", h.strip(), re.S)
    if not m or len(m.group(1).split()) < 3:
        return False
    rest = m.group(2).strip()
    return rest == "" or rest.startswith(("(", "<br>", ":"))


def list_html(kind, items):
    """Where a list mixes rules (bold) and examples, only the rules get a bullet;
    the examples sit under their rule without one."""
    if items and is_rule(items[0]) and any(not is_rule(x) for x in items):
        out = []
        for h in items:
            if is_rule(h):
                if out:
                    out.append("</li>")
                out.append(f'<li class="rule">{h}')
            else:
                out.append(f'<div class="ex">{h}</div>')
        out.append("</li>")
        return f'<{kind} class="rules">' + "".join(out) + f"</{kind}>"
    return f"<{kind}>" + "".join(f"<li>{h}</li>" for h in items) + f"</{kind}>"


def blocks_html(nodes, num, top=False, sink=None):
    """Paragraphs, lists and tables.  At top level, headings go to `sink`."""
    out, lst = [], None
    want_h1 = False

    items = []

    def close():
        nonlocal lst
        if lst:
            out.append(list_html(lst, items))
            items.clear()
            lst = None
    for n in nodes:
        if n.tag == W + "p":
            style, level, kind, jc = para_info(n, num)
            if style.startswith("TOC") or style == "Title":
                continue
            h = runs_html(n)
            if top and level is None and h == "<b><u>Nouns</u></b>":
                level, h = 1, "Nouns"
            if top and level is None and want_h1 and h:
                want_h1 = False
                if re.fullmatch(r"<b><u>[^<]{1,40}</u></b>", h):
                    level, h = 1, re.sub(r"<[^>]+>", "", h)
            if top and level in (1, 2):
                close()
                if text_of(n):
                    sink(level, h, out)
                    out = []
                else:
                    want_h1 = level == 1
                continue
            if kind:
                if lst != kind:
                    close()
                    lst = kind
                items.append(h)
                continue
            close()
            if not h:
                continue
            cls = ' class="ctr"' if jc == "center" else ""
            out.append(f"<p{cls}>{h}</p>")
        elif n.tag == W + "tbl":
            close()
            out.append(table_html(n, num))
        elif n.tag == W + "sdt":
            # the table of contents lives in a content control: skip it
            continue
    close()
    if top:
        sink(None, None, out)
        return ""
    return "".join(out)


def slug(t):
    t = unicodedata.normalize("NFD", re.sub(r"<[^>]+>", "", t).lower())
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


# short ids for the topics the app links to from word labels
IDS = {
    "introduction": "introduction", "pali-phonetics": "phonetics",
    "verb-conjugation-present-tense-indicative": "present", "verbs": "verbs",
    "the-case-system-noun-inflection": "cases", "practicing-the-cases": "practicing-cases",
    "sandhi": "sandhi", "pronouns": "pronouns",
    "personal-pronouns-aham-tvam-i-you": "personal-pronouns",
    "demonstrative-pronouns-ima-this-these": "demonstrative-pronouns",
    "relative-pronouns-ya-which-that-which-one-who": "relative-pronouns",
    "interrogative-pronouns-ka-who-what-which": "interrogative-pronouns",
    "adjectives-vant-i-i-ka": "adjectives", "compounds": "compounds",
    "the-optative-eyya-e": "optative", "the-absolutive-tva-ya": "absolutive",
    "the-imperative-tu": "imperative", "the-infinitive-tum": "infinitive",
    "the-past-tense-aorist": "aorist", "the-future-tense-issa": "future",
    "participles": "participles", "the-past-participle-ta-na": "past-participle",
    "the-present-participle-anta-mana": "present-participle",
    "the-future-passive-participle-or-ptp-tabba-aniya-eyya": "future-passive-participle",
    "adverbs-am-ena": "adverbs", "nouns": "nouns",
}


def main(path):
    z = zipfile.ZipFile(path)
    num = Numbering(z)
    body = ET.fromstring(z.read("word/document.xml")).find(W + "body")
    read_toc(body)
    sections, chapter = [], {"t": ""}
    pending = {"level": None, "title": None}

    def sink(level, h, content):
        # content belongs to the heading seen before; then start the new one
        if pending["title"] is not None:
            body_html = "".join(content).strip()
            pending["title"] = re.sub(r"\s*<br>\s*", " ", pending["title"])
            title_text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", pending["title"]))).strip()
            if body_html:
                sid = IDS.get(slug(title_text), slug(title_text))
                sections.append({"id": sid, "title": title_text, "titleHtml": pending["title"],
                                 "chapter": chapter["t"] if pending["level"] == 2 else title_text,
                                 "html": body_html})
            elif pending["level"] == 2:
                pass
        if level == 1:
            chapter["t"] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<br>|<[^>]+>", " ", h))).strip()
        pending["level"], pending["title"] = level, h
        CUR["title"] = re.sub(r"<[^>]+>", "", h or "")
    blocks_html(list(body), num, top=True, sink=sink)
    ids = [s["id"] for s in sections]
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, dup
    PARADIGMS = {  # key: (form that identifies the table, DPD patterns it stands for)
        "buddha": ("buddhena", ["a masc", "a masc pl"]),
        "sila": ("sīlena", ["a nt", "a nt east", "kamma nt"]),
        "saddha": ("saddhāya", ["ā fem"]),
        "sati": ("satiyā", ["i fem", "jāti fem"]),
        "bhikkhu": ("bhikkhunā", ["u masc"]),
        "sattha": ("satthārā", ["ar masc", "ar2 masc"]),
        "anicca": ("aniccena", ["a adj", "a ordin"]),
        "silava": ("sīlavatā", ["ant adj"]),
        "atapi": ("ātāpinā", ["ī adj"]),
        "gata": ("gatena", ["a pp"]),
        "gacchanta": ("gacchantena", ["anta prp"]),
        "gantabba": ("gantabbaṃ", ["a ptp"]),
        "personal": ("mayhaṃ", ["ahaṃ pron", "tvaṃ pron"]),
        "third": ("tissā", ["ta pron"]),
        "ima": ("iminā", ["ima pron"]),
        "ya": ("yāsaṃ", ["ya pron"]),
        "ka": ("kissa", ["ka pron"]),
    }
    paradigms = {}
    for sec in sections:
        for m in re.finditer(r'((?:<p[^>]*>(?:(?!</p>).)*</p>\s*)?)(<div class="tbl"><table[^>]*>.*?</table></div>)', sec["html"]):
            plain = re.sub(r"</?(td|p|tr)[^>]*>|<br>", " ", m.group(2))
            plain = re.sub(r"<[^>]+>", "", plain)
            for key, (form, pats) in PARADIGMS.items():
                if re.search(r"(?<!\w)" + form + r"(?!\w)", plain):
                    assert key not in paradigms, key
                    lead = re.sub(r"<[^>]+>", "", m.group(1)).strip()
                    lead = re.sub(r"'\s*(\S+?)\s*'", r"‘\1’", lead)
                    if key == "buddha":
                        lead = "Masculine nouns ending in ‘a’: buddha"
                    elif key == "third":
                        lead = "Third Person (he / she / it)"
                    elif len(lead) > 70:
                        lead = ""
                    paradigms[key] = {"section": sec["id"], "title": lead or sec["title"], "patterns": pats,
                                      "html": m.group(2)}
                    if key == "gantabba":   # "the rest of the declension is like that of anicca / gata"
                        paradigms[key]["rest"] = "anicca"
    missing = set(PARADIGMS) - set(paradigms)
    assert not missing, missing
    # the case chart's definitions, to show next to any table
    cases = next(s for s in sections if s["id"] == "cases")
    case_def = {}
    for row in re.findall(r"<tr>(.*?)</tr>", cases["html"]):
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", row)]
        cells = [html.unescape(c) for c in cells]
        name = next((c for c in cells[:2] if c in ("Nominative", "Accusative", "Instrumental", "Dative", "Ablative", "Genitive", "Locative", "Vocative")), None)
        if name:
            k = cells.index(name)
            d = re.sub(r"<td[^>]*>|</td>|<p[^>]*>", "", re.findall(r"<td[^>]*>.*?</td>", row)[k + 3])
            case_def[name.lower()] = re.sub(r"\s*(</p>|<br>)\s*", " ", d).strip()
    cases["html"] = cases["html"].replace("<table>", '<table class="t-cases">', 1)
    out = {"title": "Pāḷi Grammar Summary", "author": "Mor Ifrah",
           "paradigms": paradigms, "caseDefs": case_def,
           "intro": "A simplified grammar guide to accompany the Pāḷi texts we read.",
           "sections": sections}
    dest = os.path.join(ROOT, "data", "grammar", "index.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    for s in sections:
        print(f"{s['id']:28} {s['chapter'][:24]:24} | {s['title'][:60]}  ({len(s['html'])} chars)")
    print("typo fixes:", sorted(set(FIXED)))


if __name__ == "__main__":
    main(sys.argv[1])
