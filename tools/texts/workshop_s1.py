"""Texts from Mor's Pāḷi Workshop booklet (V3, 25.7.26), section 1 "sīla, dāna & saddhā",
taken over from the Pāḷi Workshop Reader with their word analyses (meanings from DPD).
They go to the library's "More texts" tab.  build_library.py calls build_prebuilt(api)."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "_workshop_booklet.json"), encoding="utf-8"))
SECTION = 1
PUNCT = re.compile(r"^([“”\"‘’,.;:!?—…\s\[\]()]*)(.*?)([“”\"‘’,.;:!?—…\s\[\]()]*)$")
NO_PARSE = re.compile(r"indeclinable|two words joined|absolutive|infinitive|adverb|term of address|^numeral|idiom|prefix", re.I)
GENDER_POS = {"masculine noun": {"masc"}, "feminine noun": {"fem"}, "neuter noun": {"nt"},
              "adjective": {"adj", "pp", "prp", "ptp", "ordin"}, "pronoun": {"pron"}, "past participle": {"pp", "adj"},
              "present participle": {"prp", "adj"}}


def convert_word(key, e, api):
    w = {"form": key, "lemma": e["lemma"], "label": e["g"], "ctx": e["ctx"], "q": e.get("q") or e["lemma"]}
    for a, b in (("dpd", "dpd"), ("lit", "lit"), ("con", "construction"), ("note", "note"), ("more", "more")):
        if e.get(a):
            w[b] = e[a]
    if e.get("parts"):
        w["parts"] = [{"form": p["w"], "label": p["g"], "meaning": p["m"]} for p in e["parts"]]
    sandhi = e["g"].startswith("two words joined")
    w["heads"] = [] if sandhi or not e.get("dpd") else [{"lemma": e["lemma"], "meaning": e["dpd"]}]
    w["parse"] = not sandhi and not NO_PARSE.search(e["g"])
    # the word's declension type, from DPD, for the case tables
    kind = next((pos for k, pos in GENDER_POS.items() if e["g"].startswith(k)), None)
    d = api["find"](e["lemma"], kind)
    if d:
        w["pos"] = d["pos"]
        w.update(api["declension"](e["g"], e["g"], d))
    return w


def build_prebuilt(api):
    sec = next(s for s in DATA["SECTIONS"] if s["n"] == SECTION)
    out = []
    for s in sec["suttas"]:
        D = dict(DATA["E"]); D.update(s.get("words") or {})
        words, paras = {}, []
        for b in s["boxes"]:
            toks = []
            for li, line in enumerate(b["pali"]):
                if li:
                    toks.append(["\n"])
                for ti, tok in enumerate(line.split(" ")):
                    if ti:
                        toks.append([" "])
                    m = PUNCT.match(tok)
                    core = m.group(2); key = core.lower()
                    if not core or key not in D:
                        toks.append([tok]); continue
                    if m.group(1): toks.append([m.group(1)])
                    toks.append([api["pali_case"](core), key])
                    if m.group(3): toks.append([m.group(3)])
                    if key not in words:
                        words[key] = convert_word(key, D[key], api)
            p = {"t": toks, "en": "\n".join(b["en"]), "lines": True}
            if b.get("ref"): p["ref"] = b["ref"]
            paras.append(p)
        title = s["title"] if s["title"][:1].islower() else s["title"]
        out.append({
            "id": "ws1-" + s["id"], "title": title, "titleEn": s.get("en") or "",
            "ref": (s.get("ref") or "").replace(" - ", " · "),
            "source": f"Pāḷi Workshop booklet · page {s['page']}",
            "credit": "Pāḷi text and English translation as in Mor’s Pāḷi Workshop booklet.",
            "section": "extra", "collection": "workshop", "group": f"{sec['n']} · {sec['title']}", "groupSub": sec.get("sub", ""),
            "paras": paras, "words": words,
        })
    return out
