#!/usr/bin/env python3
"""Build data/library/*.json from the text specs in tools/texts/.

Needs the DPD index pickle made from the Digital Pali Dictionary sources
(dpd-db, db/backup_tsv): see tools/README.md.  Usage:
    python3 tools/build_library.py /path/to/dpd_idx.pkl
"""
import glob, importlib.util, json, os, pickle, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools", "texts"))
OUT = os.path.join(ROOT, "data", "library")

idx, info = pickle.load(open(sys.argv[1], "rb"))
by_lemma = {}
for i, d in info.items():
    by_lemma.setdefault(d["lemma_1"], []).append(i)

GEN = {"masc": "masculine", "nt": "neuter", "fem": "feminine"}
CASE = {"nom": "nominative", "acc": "accusative", "instr": "instrumental", "dat": "dative",
        "abl": "ablative", "gen": "genitive", "loc": "locative", "voc": "vocative"}
NUM = {"sg": "singular", "pl": "plural"}
TENSE = {"pr": "present", "imp": "imperative", "opt": "optative", "fut": "future",
         "aor": "aorist", "cond": "conditional", "perf": "perfect"}
POS = {"adj": "adjective", "pp": "past participle", "prp": "present participle",
       "ptp": "future passive participle", "ordin": "ordinal number", "card": "number",
       "pron": "pronoun", "ind": "indeclinable", "abs": "absolutive", "inf": "infinitive",
       "sandhi": "sandhi", "prefix": "prefix", "suffix": "suffix", "num": "number", "ger": "absolutive"}


def clean_lemma(l):
    return re.sub(r"\s+\d[\d.]*$", "", l)


def case(c):
    return " or ".join(CASE[x] for x in c.split("/"))


def label(g, pos):
    """Readable grammar label from a grammar code and the DPD part of speech."""
    t = g.split()
    if g == "sandhi":
        return "two words joined (sandhi)"
    if g in ("ind", "") and pos in ("ind", "", None):
        return "indeclinable"
    if t and t[0] == "prp" or pos == "prp" and len(t) == 3 and t[0] in GEN:
        t2 = t[1:] if t[0] == "prp" else t
        return f"present participle · {GEN[t2[0]]} {case(t2[1])} {NUM[t2[2]]}"
    if t and t[0] in TENSE:  # verb: pr 1st sg
        person = t[1] + " person" if len(t) > 1 else ""
        num = NUM.get(t[2], "") if len(t) > 2 else ""
        return f"verb · {TENSE[t[0]]}, {person} {num}".strip()
    if t and t[0] in ("1st", "2nd", "3rd"):  # personal pronoun: 1st nom sg
        return f"pronoun, {t[0]} person · {case(t[1])} {NUM[t[2]]}"
    if len(t) == 4 and t[0] in POS and t[1] in GEN:  # manual: adj masc nom sg
        return f"{POS[t[0]]} · {GEN[t[1]]} {case(t[2])} {NUM[t[3]]}"
    if t and t[0] == "pron" and len(t) == 4:  # manual: pron nt nom sg
        return f"pronoun · {GEN[t[1]]} {case(t[2])} {NUM[t[3]]}"
    if len(t) == 3 and t[0] in GEN:
        g_, c, n = t
        if pos in GEN:
            return f"{GEN[g_]} noun · {case(c)} {NUM[n]}"
        kind = POS.get(pos, "adjective")
        if pos == "pron":
            kind = "pronoun"
        return f"{kind} · {GEN[g_]} {case(c)} {NUM[n]}"
    if t and t[0] in GEN:
        return f"{GEN[t[0]]} noun"
    return POS.get(g, g)


def dpd_entry(lemma_1):
    ids = by_lemma.get(lemma_1)
    if not ids:
        raise SystemExit(f"DPD lemma not found: {lemma_1}")
    return ids[0], info[ids[0]]


def other_senses(lemma_1):
    base = clean_lemma(lemma_1)
    out = []
    for l, ids in by_lemma.items():
        if clean_lemma(l) == base and l != lemma_1:
            d = info[ids[0]]
            m = d["meaning_1"] or d["meaning_2"]
            if m and m not in out and "name of" not in m:
                out.append(f"({d['pos']}) {m}" if d["pos"] != info[by_lemma[lemma_1][0]]["pos"] else m)
    return out[:8]


def build_word(form, spec):
    w = {"form": form}
    if spec.get("l"):
        did, d = dpd_entry(spec["l"])
        w["lemma"] = clean_lemma(spec["l"])
        w["dpdId"] = did
        w["pos"] = d["pos"]
        w["dpd"] = spec.get("dpd") or d["meaning_1"] or d["meaning_2"]
        if d["meaning_lit"]:
            w["lit"] = d["meaning_lit"]
        if d["construction"]:
            w["construction"] = re.sub(r"\s*\n.*", "", d["construction"])
        if d["root_key"]:
            w["root"] = d["root_key"]
        more = other_senses(spec["l"])
        if more:
            w["more"] = more
        w["label"] = label(spec["g"], d["pos"])
        w["q"] = w["lemma"]
    else:
        w["lemma"] = spec["lemma"]
        w["pos"] = spec.get("pos", spec["g"])
        w["label"] = label(spec["g"], spec.get("pos", ""))
        if spec.get("dpd"):
            w["dpd"] = spec["dpd"]
        w["q"] = form
    w["ctx"] = spec["ctx"]
    for k in ("role", "note"):
        if spec.get(k):
            w[k] = spec[k]
    if spec.get("parts"):
        parts = []
        for pf, pl, pg, pm in spec["parts"]:
            p = {"form": pf, "meaning": pm}
            if pl:
                pid, pd = dpd_entry(pl)
                p["lemma"] = clean_lemma(pl)
                p["dpdId"] = pid
                p["label"] = label(pg, pd["pos"])
                p["dpd"] = pd["meaning_1"] or pd["meaning_2"]
            else:
                p["label"] = label(pg, pg.split()[0] if pg else "")
            parts.append(p)
        w["parts"] = parts
    # review cards: a meaning card for each dictionary headword, a parsing card
    # for each inflected form (not for indeclinables)
    cards = []
    heads = []
    if spec.get("l"):
        heads.append((w["lemma"], w["dpd"], w["pos"]))
    for p in w.get("parts", []):
        if p.get("lemma") and p.get("dpd"):
            heads.append((p["lemma"], p["dpd"], ""))
    w["heads"] = [{"lemma": h[0], "meaning": h[1]} for h in heads]
    w["parse"] = bool(spec.get("l")) and spec["g"] not in ("ind", "sandhi", "inf", "ger")
    return w


TOKEN = re.compile(r"[^\s,.;:!?“”\"‘()…*—–]+(?:\([^\s()]+\))?|[\s,.;:!?“”\"‘()…*—–]+")


def build_text(t):
    words = {}
    for form, spec in t["words"].items():
        words[form] = build_word(form, spec)
    paras = []
    for pali, en in t["paras"]:
        toks = []
        for m in TOKEN.finditer(pali):
            s = m.group(0)
            key = s.lower()
            if re.match(r"[\s,.;:!?“”\"‘()…*—–]+$", s):
                toks.append([s])
            elif key in words:
                toks.append([s, key])
            else:
                raise SystemExit(f"{t['id']}: no analysis for '{s}'")
        paras.append({"t": toks, "en": en})
    unused = set(words) - {k for p in paras for tok in p["t"] if len(tok) > 1 for k in [tok[1]]}
    if unused:
        print(f"  note: {t['id']} unused analyses: {sorted(unused)}")
    out = {k: t[k] for k in ("id", "ref", "title", "titleEn", "source", "credit") if k in t}
    m = re.match(r"ncrp-(\d+)-(\d+)-\d+$", t["id"])
    if m:
        out["bookLesson"] = int(m.group(1))
        out["section"] = "initial" if m.group(2) == "1" else "further"
    else:
        out["section"] = "extra"
    if t.get("intro"):
        out["intro"] = t["intro"]
    out["paras"] = paras
    out["words"] = words
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    catalogue = []
    for f in sorted(glob.glob(os.path.join(ROOT, "tools", "texts", "[!_]*.py"))):
        spec = importlib.util.spec_from_file_location("m", f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for t in getattr(m, "TEXTS", []):
            data = build_text(t)
            with open(os.path.join(OUT, t["id"] + ".json"), "w", encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))
            catalogue.append({k: data[k] for k in ("id", "ref", "title", "titleEn", "source", "bookLesson", "section") if k in data})
            print("built", t["id"], len(data["words"]), "words")
    catalogue.sort(key=lambda c: [int(x) if x.isdigit() else x for x in re.split(r"[-.]", c["id"])])
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(catalogue, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
