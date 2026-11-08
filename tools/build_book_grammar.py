# -*- coding: utf-8 -*-
"""Builds data/grammar/book.json: a simple grammar guide that follows the
grammar sections of the course book (Grammar I, II, III, ...), written in
our own words with examples from the course readings.

Run:  python3 tools/build_book_grammar.py
"""
import json, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- small helpers ----------

def fm(s):
    """'dhamm|o / dhamm|ena' -> dhamm<b>o</b> / dhamm<b>ena</b>"""
    return re.sub(r"\|([^\s/,()]+)", r"<b>\1</b>", s)

CASES = {
    "nom": "Nominative", "acc": "Accusative", "ins": "Instrumental", "dat": "Dative",
    "abl": "Ablative", "gen": "Genitive", "loc": "Locative", "voc": "Vocative",
}
ORDER = ["nom", "acc", "ins", "dat", "abl", "gen", "loc", "voc"]


def table(head, rows, first="Case"):
    """head: column titles after the first; rows: [(label, [cells])]"""
    h = f'<tr><td class="c-yel"><p><b>{first}</b></p></td>' + "".join(
        f'<td class="c-blu"><p class="ctr"><b>{x}</b></p></td>' for x in head) + "</tr>"
    body = ""
    for label, cells in rows:
        lab = CASES.get(label, label)
        body += f'<tr><td class="c-yel"><p>{lab}</p></td>' + "".join(
            f'<td><p class="ctr">{fm(c)}</p></td>' for c in cells) + "</tr>"
    return f'<div class="tbl"><table lang="pi">{h}{body}</table></div>'


def paradigm(d, head=("Singular", "Plural")):
    return table(list(head), [(k, d[k]) for k in ORDER if k in d])


def glue(t):
    """join the last two words with a no-break space, so no word is left alone on a line"""
    parts = re.split(r"(<[^>]+>)", t)
    seen = False  # has real text been seen after this point?
    for i in range(len(parts) - 1, -1, -1):
        x = parts[i]
        if x.startswith("<"):
            continue
        for k in range(len(x) - 1, -1, -1):
            if x[k] == "\u00a0" and (seen or x[k + 1:].strip()):
                return t  # already glued
            if x[k] == " " and (seen or x[k + 1:].strip()):
                plain = re.sub(r"<[^>]+>", "", "".join(parts)).rstrip()
                if len(" ".join(plain.split()[-2:])) > 27:
                    return t  # two long words: gluing them would leave a lone word before them
                if k == 0 and not "".join(p for p in parts[:i] if not p.startswith("<")).strip():
                    return t
                parts[i] = x[:k] + "\u00a0" + x[k + 1:]
                return "".join(parts)
            if not x[k].isspace():
                seen = True
    return t


def tidy(html):
    """no lone last word in paragraphs, list items and example lines (tables are left alone)"""
    def fix(m):
        inner = "<br>".join(glue(x) for x in m.group(3).split("<br>"))
        return m.group(1) + inner + m.group(4)
    for tag in ("div", "p", "li"):
        html = re.sub(r"(<(%s)( [^>]*)?>)((?:(?!<table|<div|</?\2[ >]).)*?)(</\2>)" % tag,
                      lambda m: m.group(1) + "<br>".join(glue(x) for x in m.group(4).split("<br>")) + m.group(5), html)
    return html


def nobreak(t):
    """keep hyphenated Pāḷi compounds on one line"""
    parts = re.split(r"(<[^>]+>)", t)
    return "".join(x if x.startswith("<") else re.sub(r"([^\s<>…]+-[^\s<>…]+)", r'<span class="nw">\1</span>', x) for x in parts)


def ex(*items):
    """items: (pali, english, source)"""
    out = "".join(f'<li><span lang="pi">{nobreak(glue(p))}</span><br>{e}{f"&nbsp;<span class=\"src\">({s})</span>" if s else ""}</li>'
                  for p, e, s in items)
    return f'<ol class="bg-ex">{out}</ol>'


def tip(t):
    return f'<p class="bg-tip">{t}</p>'


def h(t):
    return f'<p class="bg-h"><b><u>{t}</u></b></p>'

# ---------- GRAMMAR I ----------

G1 = []

G1.append(("nouns", "Nouns: stem, gender, number and case", f"""
<p>A Pāḷi noun is made of two parts: a <b>stem</b> (the basic form) and an <b>ending</b>.
The ending tells us how the word works in the sentence. For example, the stem <span lang="pi">dhamma-</span> becomes <span lang="pi">dhamm<b>o</b></span>, <span lang="pi">dhamm<b>aṃ</b></span>, <span lang="pi">dhamm<b>assa</b></span> and so on.</p>
<p>Every noun has three features:</p>
<ul>
<li><b>Gender</b> – masculine, feminine or neuter. This is a grammar label, not always the natural gender: <span lang="pi">dhamma</span> is masculine, <span lang="pi">ratti</span> (night) is feminine, <span lang="pi">citta</span> (mind) is neuter. It is best to learn the gender together with each new word.</li>
<li><b>Number</b> – singular (one) or plural (more than one).</li>
<li><b>Case</b> – the job of the word in the sentence. Pāḷi has eight cases.</li>
</ul>
{h("The eight cases at a glance")}
{table(["Main job", "English helper words", "Example from our readings"], [
 ("nom", ["the subject, the one who does the action", "–", "<span lang='pi'><b>pamādo</b> … saṃvattati</span><br><b>heedlessness</b> leads … (Heedlessness)"]),
 ("acc", ["the object of the action; also the place one goes to", "–", "<span lang='pi'><b>cittaṃ</b> paggaṇhāti</span><br>he applies his <b>mind</b> (Finger Snap)"]),
 ("ins", ["the means, the tool, the company", "by, with, through", "<span lang='pi'>pañcahi <b>dhammehi</b> samannāgato</span><br>endowed <b>with</b> five <b>qualities</b> (Falling Away)"]),
 ("dat", ["the purpose, the one who benefits", "to, for", "<span lang='pi'>mahato <b>atthāya</b> saṃvattati</span><br>leads <b>to</b> great <b>good</b> (Untamed)"]),
 ("abl", ["the starting point, the cause", "from, because of", "<span lang='pi'>imamhā <b>kāyā</b></span><br><b>from</b> this <b>body</b> (Not Transmigrating)"]),
 ("gen", ["belonging, ‘of’", "of, ’s", "<span lang='pi'><b>purisassa</b> cittaṃ</span><br>the mind <b>of a man</b> (Obsession of the Mind)"]),
 ("loc", ["the place or time where something happens", "in, on, at, among", "<span lang='pi'><b>manussesu</b> paccājāyanti</span><br>are reborn <b>among human beings</b> (Few and Many)"]),
 ("voc", ["calling or addressing someone", "O …!", "<span lang='pi'><b>bhikkhave</b></span><br><b>monks!</b>"]),
], first="Case")}
{tip("The English helper words are only a first guide. Each case has more uses, and we will meet them step by step.")}
{h("Masculine nouns in -a: dhamma (Dhamma, quality, thing)")}
<p>This is the most common type of noun. In a glossary it usually appears with the ending <b>-o</b> (<span lang="pi">dhammo</span>).</p>
{paradigm({
 "nom": ["dhamm|o", "dhamm|ā"], "acc": ["dhamm|aṃ", "dhamm|e"], "ins": ["dhamm|ena", "dhamm|ehi (dhamm|ebhi)"],
 "dat": ["dhamm|āya / dhamm|assa", "dhamm|ānaṃ"], "abl": ["dhamm|ā / dhamm|asmā / dhamm|amhā", "dhamm|ehi (dhamm|ebhi)"],
 "gen": ["dhamm|assa", "dhamm|ānaṃ"], "loc": ["dhamm|e / dhamm|asmiṃ / dhamm|amhi", "dhamm|esu"], "voc": ["dhamm|a", "dhamm|ā"]})}
<p>Forms joined by “/” are alternatives with the same meaning. Forms in brackets are less common.</p>
{ex(("uppannā ca kusalā <b>dhammā</b> parihāyanti", "and arisen wholesome <b>qualities</b> decline (nominative plural)", "One Thing"),
    ("anuppannānaṃ kusalānaṃ <b>dhammānaṃ</b> uppādāya", "for the arising of unarisen wholesome <b>qualities</b> (genitive plural)", "Finger Snap"))}
{h("Neuter nouns in -a: rūpa (form)")}
<p>Neuter nouns in -a are almost the same as the masculine ones. Only the nominative, accusative and vocative are different. In a glossary they appear with <b>-aṃ</b> (<span lang="pi">rūpaṃ</span>).</p>
{paradigm({
 "nom": ["rūp|aṃ", "rūp|āni"], "acc": ["rūp|aṃ", "rūp|āni"], "ins": ["rūp|ena", "rūp|ehi (rūp|ebhi)"],
 "dat": ["rūp|āya / rūp|assa", "rūp|ānaṃ"], "abl": ["rūp|ā / rūp|asmā / rūp|amhā", "rūp|ehi (rūp|ebhi)"],
 "gen": ["rūp|assa", "rūp|ānaṃ"], "loc": ["rūp|e / rūp|asmiṃ / rūp|amhi", "rūp|esu"], "voc": ["rūp|a", "rūp|āni"]})}
{tip("In all neuter nouns, the nominative and the accusative look exactly the same. Only the sentence tells us which one it is.")}
{ex(("<b>cittaṃ</b>, bhikkhave, adantaṃ mahato anatthāya saṃvattati", "an untamed <b>mind</b> leads to great harm (nominative singular)", "Untamed"),
    ("yathayidaṃ, bhikkhave, itthi-<b>rūpaṃ</b>", "as the <b>form</b> of a woman (nominative singular)", "Obsession of the Mind"))}
{h("Feminine nouns in -i and -ī: ratti (night), nadī (river)")}
<p>These are two groups, but they are almost identical. The only real difference is the nominative singular: <span lang="pi">ratt<b>i</b></span> but <span lang="pi">nad<b>ī</b></span>.</p>
{paradigm({
 "nom": ["ratt|i", "ratt|iyo / ratt|ī"], "acc": ["ratt|iṃ", "ratt|iyo / ratt|ī"], "ins": ["ratt|iyā", "ratt|īhi (ratt|ībhi)"],
 "dat": ["ratt|iyā", "ratt|īnaṃ"], "abl": ["ratt|iyā", "ratt|īhi (ratt|ībhi)"], "gen": ["ratt|iyā", "ratt|īnaṃ"],
 "loc": ["ratt|iyā / ratt|iyaṃ", "ratt|īsu"], "voc": ["ratt|i", "ratt|iyo / ratt|ī"]}, head=("Singular (-i)", "Plural (-i)"))}
{paradigm({
 "nom": ["nad|ī", "nad|iyo / nad|ī"], "acc": ["nad|iṃ", "nad|iyo / nad|ī"], "ins": ["nad|iyā", "nad|īhi (nad|ībhi)"],
 "dat": ["nad|iyā", "nad|īnaṃ"], "abl": ["nad|iyā", "nad|īhi (nad|ībhi)"], "gen": ["nad|iyā", "nad|īnaṃ"],
 "loc": ["nad|iyā / nad|iyaṃ", "nad|īsu"], "voc": ["nad|ī / nad|i", "nad|iyo / nad|ī"]}, head=("Singular (-ī)", "Plural (-ī)"))}
{tip("The one ending <b>-iyā</b> can be instrumental, dative, ablative, genitive or locative. Context tells us which one is meant.")}
{ex(("yathayidaṃ, bhikkhave, micchā-<b>diṭṭhi</b>", "as wrong <b>view</b> (nominative singular of diṭṭhi)", "One Thing"),
    ("<b>itthiyā</b> cittaṃ pariyādāya tiṭṭhati", "obsesses the mind <b>of a woman</b> (genitive singular of itthī)", "Obsession of the Mind"))}
"""))

G1.append(("verbs", "Verbs: root, present stem and the present tense", f"""
<p>Every verb has a <b>root</b> – the core of its meaning, from which all its forms are built. Roots are marked with √.
For the present tense we use the <b>present stem</b>. Sometimes the stem looks very much like the root, and sometimes quite different:</p>
{table(["Present stem", "Present tense (he/she)"], [
 ("√pat (fall)", ["pata-", "patati"]), ("√jīv (live)", ["jīva-", "jīvati"]),
 ("√gam (go)", ["gaccha-", "gacchati"]), ("√ṭhā (stand)", ["tiṭṭha-", "tiṭṭhati"]), ("√nī (lead)", ["naya-", "nayati / neti"])], first="Root")}
{h("The present tense")}
<p>The present tense is made by adding these endings to the present stem. Before <b>-mi</b> and <b>-ma</b>, a short <b>a</b> of the stem becomes long <b>ā</b>.</p>
{table(["Ending (sing.)", "labhati (gets)", "Ending (pl.)", "labhati (gets)"], [
 ("1st person (I / we)", ["-:mi", "labh|āmi", "-:ma", "labh|āma"]),
 ("2nd person (you)", ["-si", "labha|si", "-tha", "labha|tha"]),
 ("3rd person (he, she, it / they)", ["-ti", "labha|ti", "-nti", "labha|nti"])], first="Person")}
<p>The colon in <b>-:mi</b> means “lengthen the vowel before it”: <span lang="pi">labha + mi → labh<b>āmi</b></span>.</p>
{tip("Dictionaries and glossaries list verbs in the 3rd person singular: <span lang='pi'>labhati, gacchati, saṃvattati</span>.")}
{ex(("buddhaṃ saraṇaṃ <b>gacchāmi</b>", "<b>I go</b> to the Buddha for refuge (1st person singular)", "Going for Refuge"),
    ("n’āhaṃ, bhikkhave, aññaṃ eka-dhammampi <b>samanupassāmi</b>", "monks, <b>I do</b> not <b>see</b> even one other thing (1st person singular)", "One Thing"),
    ("anuppannā c’eva akusalā dhammā <b>uppajjanti</b>", "unarisen unwholesome qualities <b>arise</b> (3rd person plural)", "One Thing"))}
"""))

G1.append(("clitics", "Little words that follow: pi, (i)ti, eva, ca, vā", f"""
<p>Pāḷi has small words that never stand first. They lean on the word before them, and are often joined to it. They are called <b>clitics</b>. Five of them appear in Lesson 1:</p>
{table(["Meaning"], [("pi", ["also, too, even"]), ("(i)ti", ["marks the end of something said or thought, like closing quotation marks"]),
 ("eva", ["just, only, indeed"]), ("ca", ["and"]), ("vā", ["or"])], first="Word")}
{h("ca and vā")}
<p><b>ca</b> (and) and <b>vā</b> (or) usually come <b>after</b> each of the things they join, and after the first word of each group:</p>
{ex(("na <b>ca</b> saṅkamati, paṭisandahati <b>ca</b>", "it does not transmigrate, <b>and</b> (yet) it is reborn", "Not Transmigrating"),
    ("anuppannā <b>vā</b> kusalā dhammā n’uppajjanti, uppannā <b>vā</b> kusalā dhammā parihāyanti", "<b>either</b> unarisen wholesome qualities do not arise, <b>or</b> arisen wholesome qualities decline", "One Thing"))}
{h("pi and eva")}
{ex(("jāti <b>pi</b> dukkhā, jarā <b>pi</b> dukkhā", "birth <b>too</b> is suffering, ageing <b>too</b> is suffering", "The Noble Truth of Suffering"),
    ("aññaṃ eka-dhammam<b>pi</b>", "<b>even</b> one other thing (ṃ + pi is written mpi)", "One Thing"),
    ("anuppannā c’<b>eva</b> akusalā dhammā uppajjanti", "unarisen unwholesome qualities <b>indeed</b> arise (ca + eva → c’eva)", "One Thing"))}
{h("The quotation marker (i)ti")}
<p><b>iti</b> comes right after words that someone says or thinks. After a vowel it becomes <b>ti</b>, and the vowel before it becomes long:</p>
{ex(("saṃvattati + iti → saṃvatta<b>tī’ti</b>", "… leads.”", "Untamed"))}
"""))

G1.append(("relative", "The relative pronoun ya (who, which, that)", f"""
<p>The relative pronoun has the stem <b>ya-</b>. It works like English <i>who, which, that</i>, and it introduces a clause that describes a noun.</p>
{table(["Masculine", "Neuter"], [("nom", ["y|o", "y|aṃ"]), ("ins", ["y|ena", "y|ena"])])}
<p>The pronoun takes the case of <b>its own job</b> inside its clause, not the case of the noun it describes:</p>
{ex(("aññaṃ eka-dhammampi … <b>yo</b> evaṃ saddhammassa sammosāya … saṃvattati", "one other thing <b>that</b> so leads to the decline of the good Dhamma (yo is the subject of saṃvattati → nominative)", "Heedlessness"),
    ("aññaṃ eka-dhammampi … <b>yena</b> anuppannā vā kusalā dhammā n’uppajjanti", "one other thing <b>on account of which</b> unarisen wholesome qualities do not arise (yena → instrumental)", "One Thing"),
    ("aññaṃ eka-rūpampi … <b>yaṃ</b> evaṃ purisassa cittaṃ pariyādāya tiṭṭhati", "one other form <b>that</b> so obsesses the mind of a man (yaṃ → neuter, because rūpa is neuter)", "Obsession of the Mind"))}
{tip("More often, Pāḷi uses a pair of words – a <b>ya-</b> word and a <b>ta-</b> word – to build such sentences. This is explained in Grammar II.")}
"""))

G1.append(("sandhi", "Sandhi: when sounds meet", f"""
<p><b>Sandhi</b> means “joining”. When two words (or two parts of a word) come together, the sounds at the meeting point may change. In Pāḷi this happens mostly with short, common words that are closely linked. Three changes appear in Lesson 1:</p>
<ul class="rules">
<li class="rule"><b>1. The first vowel drops.</b> We mark the missing vowel with ’.
<div class="ex">c<b>a</b> + <b>e</b>va → c<b>’e</b>va (and indeed)</div><div class="ex">n<b>a</b> + <b>a</b>tthi → n<b>’a</b>tthi (there is not)</div></li>
<li class="rule"><b>2. Two vowels become one long vowel.</b>
<div class="ex">n<b>a</b> + <b>a</b>haṃ → n<b>’ā</b>haṃ (not I)</div><div class="ex">saṃvattat<b>i</b> + <b>i</b>ti → saṃvattat<b>ī’</b>ti</div></li>
<li class="rule"><b>3. ṃ takes the sound of the next consonant.</b> Before c it becomes ñ.
<div class="ex">sacca<b>ṃ</b> + <b>c</b>a → sacca<b>ñc</b>a (and truth)</div></li>
</ul>
{tip("The book marks a vowel lengthened by sandhi with a circumflex (â). In our texts we write it with the apostrophe instead: n’āhaṃ.")}
"""))

G1.append(("negatives", "Saying “not”: na and a- / an-", f"""
{h("na – not")}
<p><b>na</b> makes a whole sentence negative. Before a vowel, its a usually drops (or merges into a long ā):</p>
{ex(("na + uppajjanti → <b>n’uppajjanti</b>", "they do <b>not</b> arise", "One Thing"),
    ("<b>n’āhaṃ</b>, bhikkhave, aññaṃ eka-dhammampi samanupassāmi", "monks, I do <b>not</b> see even one other thing", "Heedlessness"))}
<p>Notice that <b>na</b> does not have to stand next to the verb. In the last example it stands first, and the verb comes at the end.</p>
{h("a- / an- – un-, non-")}
<p>The prefix <b>a-</b> makes a single word negative, like English <i>un-</i> or <i>non-</i>. Before a vowel it becomes <b>an-</b>:</p>
{table(["Negative"], [("danta (tamed)", ["<b>a</b>danta (untamed)"]), ("kusala (wholesome)", ["<b>a</b>kusala (unwholesome)"]),
 ("uppanna (arisen)", ["<b>an</b>uppanna (unarisen)"]), ("attha (good, benefit)", ["<b>an</b>attha (harm)"])], first="Word")}
{tip("If you meet a word in a- or an- and cannot find it in the glossary, look up the word without it: for <span lang='pi'>asukha</span>, look up <span lang='pi'>sukha</span>.")}
"""))

G1.append(("agreement", "Adjectives agree with their nouns", f"""
<p>An adjective takes the <b>same gender, number and case</b> as the noun it describes:</p>
{ex(("<b>kusalā</b> dhammā", "wholesome qualities (masculine, nominative, plural)", "One Thing"),
    ("<b>akusalānaṃ</b> dhammānaṃ", "of unwholesome qualities (masculine, genitive, plural)", "Finger Snap"),
    ("cittaṃ … <b>adantaṃ</b>", "the mind … untamed (neuter, nominative, singular)", "Untamed"))}
<p>Adjectives in -a take the same endings as the nouns: like <span lang="pi">dhammo</span> with a masculine noun, like <span lang="pi">rūpaṃ</span> with a neuter noun.</p>
<p>The adjective usually comes before the noun, but it may also come after it: <span lang="pi">cittaṃ adantaṃ</span>.</p>
"""))



G1.append(("compounds", "Compounds", f"""
<p>As in English (<i>bookshop, sunlight</i>), two nouns can join to make one word. In our texts the parts are linked with a hyphen.</p>
{table(["+", "Compound"], [("itthi (woman)", ["sadda (sound)", "itthi-saddo – the sound of a woman"]),
 ("purisa (man)", ["rūpa (form)", "purisa-rūpaṃ – the form of a man"])], first="First word")}
<p>The <b>first word has no ending</b> – it stays in its stem form. Only the last word takes the ending. For nouns in -a, the stem looks like the vocative singular (<span lang="pi">purisa-</span>, <span lang="pi">dhamma-</span>).</p>
{tip("Compounds are very common in Pāḷi. When a long word is not in the glossary, try to split it and look up each part.")}
"""))

# ---------- GRAMMAR II ----------

G2 = []

G2.append(("nouns", "More nouns: -ā, and -u", f"""
{h("Feminine nouns in -ā: sālā (hall)")}
<p>The stem and the nominative singular are the same: <span lang="pi">sālā</span>.</p>
{paradigm({
 "nom": ["sāl|ā", "sāl|āyo / sāl|ā"], "acc": ["sāl|aṃ", "sāl|āyo / sāl|ā"], "ins": ["sāl|āya", "sāl|āhi (sāl|ābhi)"],
 "dat": ["sāl|āya", "sāl|ānaṃ"], "abl": ["sāl|āya", "sāl|āhi (sāl|ābhi)"], "gen": ["sāl|āya", "sāl|ānaṃ"],
 "loc": ["sāl|āya / sāl|āyaṃ", "sāl|āsu"], "voc": ["sāl|e", "sāl|āyo / sāl|ā"]})}
<ul><li>These endings look much like the feminine -i / -ī nouns, but with <b>-āya</b> instead of <b>-iyā</b>.</li>
<li>The accusative singular has a short a: <span lang="pi">sāl<b>aṃ</b></span>.</li>
<li>The vocative singular ends in <b>-e</b>: <span lang="pi">sāl<b>e</b></span>!</li></ul>
{ex(("kusalassa <b>upasampadā</b>", "the <b>undertaking</b> of the wholesome (nominative singular)", "Dhammapada"),
    ("ṭhitiyā asammosāya … <b>bhāvanāya</b> pāripūriyā", "for maintenance, non-decline … for fulfilment <b>by development</b> (instrumental singular)", "Finger Snap"))}
{h("Masculine nouns in -u: bhikkhu (monk)")}
{paradigm({
 "nom": ["bhikkh|u", "bhikkh|ū / bhikkh|avo"], "acc": ["bhikkh|uṃ", "bhikkh|ū / bhikkh|avo"], "ins": ["bhikkh|unā", "bhikkh|ūhi (bhikkh|ūbhi)"],
 "dat": ["bhikkh|uno / bhikkh|ussa", "bhikkh|ūnaṃ"], "abl": ["bhikkh|unā / bhikkh|usmā / bhikkh|umhā", "bhikkh|ūhi (bhikkh|ūbhi)"],
 "gen": ["bhikkh|uno / bhikkh|ussa", "bhikkh|ūnaṃ"], "loc": ["bhikkh|umhi / bhikkh|usmiṃ", "bhikkh|ūsu"],
 "voc": ["bhikkh|u", "bhikkh|ave / bhikkh|avo / bhikkh|ū"]})}
{tip("The vocative plural <span lang='pi'>bhikkh<b>ave</b></span> (“monks!”) is special to this word, and very frequent in the suttas. Other nouns of this type usually have -ū.")}
{ex(("assaddho, bhikkhave, <b>bhikkhu</b> cavati", "a <b>bhikkhu</b> without faith falls away (nominative singular)", "Falling Away"))}
{h("Neuter nouns in -u: cakkhu (eye)")}
<p>These are the same as <span lang="pi">bhikkhu</span>, except in the nominative, accusative and vocative:</p>
{table(["Singular", "Plural"], [("nom", ["cakkh|u / cakkh|uṃ", "cakkh|ū / cakkh|ūni"]), ("acc", ["cakkh|u / cakkh|uṃ", "cakkh|ū / cakkh|ūni"]),
 ("Other cases", ["like bhikkhu: cakkh|unā, cakkh|uno …", "like bhikkhu: cakkh|ūhi, cakkh|ūnaṃ …"]), ("voc", ["cakkh|u", "cakkh|ū / cakkh|ūni"])])}
{ex(("ariyena paññā-<b>cakkhunā</b> samannāgatā", "endowed <b>with</b> the noble <b>eye</b> of wisdom (instrumental singular)", "Few and Many"))}
"""))

G2.append(("pronouns", "Pronouns: so / sā / taṃ, eso, ya, ayaṃ", f"""
{h("so / sā / taṃ – he, she, it; that")}
{table(["Masculine", "Neuter", "Feminine"], [
 ("nom", ["so", "taṃ", "sā"]), ("acc", ["taṃ", "taṃ", "taṃ"]), ("ins", ["tena", "tena", "tāya"]),
 ("dat", ["tassa", "tassa", "tassā / tissā"]), ("abl", ["tamhā / tasmā", "tamhā / tasmā", "tāya"]),
 ("gen", ["tassa", "tassa", "tassā / tissā"]), ("loc", ["tamhi / tasmiṃ", "tamhi / tasmiṃ", "tassaṃ / tissaṃ / tāyaṃ"])], first="Singular")}
{table(["Masculine", "Neuter", "Feminine"], [
 ("nom", ["te", "tāni", "tā / tāyo"]), ("acc", ["te", "tāni", "tā / tāyo"]), ("ins", ["tehi", "tehi", "tāhi"]),
 ("dat", ["tesaṃ / tesānaṃ", "tesaṃ / tesānaṃ", "tāsaṃ / tāsānaṃ"]), ("abl", ["tehi", "tehi", "tāhi"]),
 ("gen", ["tesaṃ / tesānaṃ", "tesaṃ / tesānaṃ", "tāsaṃ / tāsānaṃ"]), ("loc", ["tesu", "tesu", "tāsu"])], first="Plural")}
{ex(("appakā <b>te</b> sattā", "few are <b>those</b> beings", "Few and Many"),
    ("<b>taṃ</b> kammaṃ akusalaṃ", "<b>that</b> kamma is unwholesome", "Causes"))}
{h("eso / esā / etaṃ – this, that (more pointed)")}
<p>The meaning is close to <span lang="pi">so / sā / taṃ</span>, but more definite: “<b>this</b> very one”. The forms are the same with <b>e-</b> in front:
<span lang="pi">eso, esā, etaṃ, etassa, etena, ete, etāni, etesaṃ</span> …</p>
{ex(("<b>etaṃ</b> buddhāna(ṃ) sāsanaṃ", "<b>this</b> is the teaching of the Buddhas", "Dhammapada"),
    ("atha kho <b>ete</b>’va sattā bahutarā", "but <b>those very</b> beings are more numerous (’va = eva)", "Few and Many"))}
{h("yo / yā / yaṃ – who, which (the relative pronoun)")}
<p>It has the same endings as <span lang="pi">so / sā / taṃ</span>, with <b>y-</b> in place of t- (and <span lang="pi">yo</span> in place of <span lang="pi">so</span>):
<span lang="pi">yo, yā, yaṃ, yassa, yena, yasmā, ye, yāni, yesaṃ</span> …</p>
{ex(("appakā te sattā <b>ye</b> manussesu paccājāyanti", "few are those beings <b>who</b> are reborn among human beings", "Few and Many"))}
{h("ayaṃ / idaṃ – this (nominative and accusative)")}
{table(["Masculine", "Neuter", "Feminine"], [("nom", ["ayaṃ", "idaṃ / imaṃ", "ayaṃ"]), ("acc", ["imaṃ", "idaṃ / imaṃ", "imaṃ"])], first="Singular")}
{table(["Masculine", "Neuter", "Feminine"], [("nom", ["ime", "imāni", "imā / imāyo"]), ("acc", ["ime", "imāni", "imā / imāyo"])], first="Plural")}
<p>The other forms follow in Grammar IV. They are easy to recognise: <span lang="pi">imehi, imassa, imesaṃ</span> …</p>
{ex(("<b>imāni</b> kho, bhikkhave, tīṇi nidānāni", "<b>these</b>, monks, are the three causes", "Causes"),
    ("<b>idaṃ</b> kho pana, bhikkhave, dukkhaṃ ariya-saccaṃ", "now <b>this</b>, monks, is the noble truth of suffering", "The Noble Truth of Suffering"))}
{h("Alone or with a noun")}
<p>All these pronouns can stand <b>alone</b> (“he”, “that one”) or <b>before a noun</b> (“that lamp”):</p>
{ex(("kinnu kho <b>so</b> … padīpo …", "is <b>that</b> lamp …? (so describes padīpo)", "Not Transmigrating"))}
"""))

G2.append(("katama", "katama – which? what?", f"""
<p><b>katama</b> asks “which one (of several)?”. It takes the same endings as the pronouns above:</p>
{table(["Masculine", "Neuter", "Feminine"], [
 ("nom", ["katamo", "katamaṃ", "katamā"]), ("acc", ["katamaṃ", "katamaṃ", "katamaṃ"]), ("ins", ["katamena", "katamena", "katamāya"]),
 ("dat", ["katamassa", "katamassa", "katamassā"]), ("abl", ["katamamhā / katamasmā", "katamamhā / katamasmā", "katamāya"]),
 ("gen", ["katamassa", "katamassa", "katamassā"]), ("loc", ["katamamhi / katamasmiṃ", "katamamhi / katamasmiṃ", "katamāyaṃ / katamassaṃ"])], first="Singular")}
<p>The plural, too, is like <span lang="pi">te / tāni / tā</span>: <span lang="pi">katame, katamāni, katamā, katamehi, katamesaṃ</span> …</p>
{ex(("<b>katamehi</b> tīhi?", "<b>with which</b> three? (instrumental plural)", "The Shopkeeper"),
    ("<b>katamāni</b> tīṇi?", "<b>which</b> three? (neuter nominative plural)", "Causes"))}
"""))

G2.append(("infinitive", "The infinitive in -tuṃ (“to do”)", f"""
<p>The infinitive is the “to …” form of the verb: <i>to go, to see, to get</i>. It has <b>no endings</b> for person or number.</p>
{h("How it is made")}
<p><b>1.</b> Verbs with a stem in <b>-a</b>: the a becomes <b>i</b>, then add <b>-tuṃ</b>:</p>
{table(["Stem", "Infinitive"], [("labhati (gets)", ["labha-", "labh|ituṃ"]), ("bhavati (becomes)", ["bhava-", "bhav|ituṃ"]), ("passati (sees)", ["passa-", "pass|ituṃ"])], first="Verb")}
<p><b>2.</b> Verbs with a stem in <b>-ā, -e</b> or <b>-o</b>: just add <b>-tuṃ</b>:</p>
{table(["Infinitive"], [("deseti (teaches)", ["dese|tuṃ"]), ("neti (leads)", ["ne|tuṃ"]), ("hoti (is)", ["ho|tuṃ"]), ("yāti (goes)", ["yā|tuṃ"])], first="Verb")}
<p><b>3.</b> Some common verbs are irregular. These are worth learning by heart:</p>
{table(["Infinitive"], [("karoti (does)", ["kātuṃ"]), ("gacchati (goes)", ["gantuṃ"]), ("adhigacchati (attains)", ["adhigantuṃ"]),
 ("jānāti (knows)", ["ñātuṃ"]), ("ājānāti (understands)", ["aññātuṃ"]), ("tiṭṭhati (stands)", ["ṭhātuṃ"]), ("deti / dadāti (gives)", ["dātuṃ"]),
 ("passati (sees)", ["daṭṭhuṃ (also passituṃ)"]), ("pivati (drinks)", ["pātuṃ"]), ("labhati (gets)", ["laddhuṃ (also labhituṃ)"]),
 ("suṇāti (hears)", ["sotuṃ (also suṇituṃ)"]), ("marati (dies)", ["marituṃ"])], first="Verb")}
{h("How it is used")}
<p><b>1. Purpose</b> – after another verb, “in order to”: <span lang="pi">dhammaṃ <b>sotuṃ</b> gacchāmi</span> – I go <b>to hear</b> the Dhamma.</p>
<p><b>2. After words like bhabba (able) and abhabba (unable):</b></p>
{ex(("pāpaṇiko abhabbo anadhigataṃ vā bhogaṃ <b>adhigantuṃ</b>, adhigataṃ vā bhogaṃ phātiṃ <b>kātuṃ</b>", "a shopkeeper is unable <b>to acquire</b> wealth not yet acquired, or <b>to increase</b> wealth already acquired", "The Shopkeeper"),
    ("paṭibalā subhāsita-dubbhāsitassa attham<b>aññātuṃ</b>", "able <b>to understand</b> the meaning of what is well spoken and badly spoken", "Few and Many"))}
{tip("The infinitive keeps its object in the usual case (<span lang='pi'>bhogaṃ</span> is accusative). Its subject is the same as the subject of the main word, so it is not repeated.")}
"""))

G2.append(("equational", "“X is Y” without “is”", f"""
<p>In English we say “life <b>is</b> hard”. Pāḷi often leaves out the word “is”. The two parts simply stand side by side.</p>
{h("With an adjective")}
<p>The adjective agrees with its noun in gender, number and case:</p>
{ex(("<b>kicchaṃ</b> maccānaṃ jīvitaṃ", "<b>hard</b> (is) the life of mortals (kicchaṃ and jīvitaṃ are both neuter)", "Dhammapada"),
    ("<b>kiccho</b> manussa-paṭilābho", "<b>hard</b> (is) gaining a human birth (both masculine)", "Dhammapada"),
    ("<b>appakā</b> te sattā", "<b>few</b> (are) those beings (both masculine plural)", "Few and Many"))}
<p>As these examples show, the describing word often comes <b>first</b>, for emphasis.</p>
{h("With a noun")}
{ex(("etaṃ buddhāna(ṃ) <b>sāsanaṃ</b>", "this (is) the <b>teaching</b> of the Buddhas", "Dhammapada"))}
"""))

G2.append(("correlative", "The ya … ta construction", f"""
<p>Pāḷi likes to build “who / which” sentences in <b>two parts</b>:
a part with a <b>ya-</b> word, then a part with a matching <b>ta-</b> word. It is as if English said:
“<i>Which</i> book I read, <i>that</i> book is good” instead of “The book that I read is good”.</p>
{table(["…", "Together"], [("yo … (who)", ["so … (he)", "the one who …, he …"]), ("yaṃ … (what)", ["taṃ … (that)", "what …, that …"]), ("ye … (those who)", ["te … (they)", "those who …, they …"])], first="ya- part")}
{ex(("<b>yaṃ</b>, bhikkhave, lobha-pakataṃ kammaṃ …, <b>taṃ</b> kammaṃ akusalaṃ", "<b>whatever</b> kamma, monks, is fashioned by greed …, <b>that</b> kamma is unwholesome", "Causes"))}
<p>Usually the ya- part comes first, but it can also come second:</p>
{ex(("appakā <b>te</b> sattā <b>ye</b> manussesu paccājāyanti", "few are <b>those</b> beings <b>who</b> are reborn among human beings", "Few and Many"))}
"""))




G2.append(("acc-time", "Time words in the accusative", f"""
<p>A noun for a time, put in the <b>accusative</b>, works as an <b>adverb</b>: it tells us <b>when</b> or <b>for how long</b> something happens. (The traditional Pāḷi grammars list this as one of the uses of the accusative.)</p>
{ex(("<b>pubbaṇha-samayaṃ</b> … <b>majjhaṇhika-samayaṃ</b> … <b>sāyaṇha-samayaṃ</b>", "<b>in the morning</b> … <b>in the middle of the day</b> … <b>in the evening</b>", "The Shopkeeper"),
    ("yaṃ’sa hoti <b>dīgha-rattaṃ</b> ahitāya dukkhāya", "which will be for his harm and suffering <b>for a long time</b>", "Sāḷha (1)"))}
"""))

G2.append(("compounds", "“And” compounds (dvanda)", f"""
<p>Two or more things can be joined in one compound to mean “X <b>and</b> Y”. Such a compound often takes the <b>neuter singular</b> ending:</p>
{ex(("<b>dhamma-vinayaṃ</b>", "the <b>Dhamma and</b> the <b>Discipline</b>", "Few and Many"),
    ("<b>subhāsita-dubbhāsitassa</b>", "of what is <b>well spoken and</b> what is <b>badly spoken</b>", "Few and Many"))}
"""))

G2.append(("sandhi", "Sandhi: doubled consonants", f"""
<p>Some words <b>double their first consonant</b> when something ending in a vowel is put before them (a prefix, or the first part of a compound):</p>
<ul class="rules">
<li class="rule"><div class="ex">a + <b>p</b>amāda → a<b>pp</b>amāda (heedfulness)</div>
<div class="ex">tathāgata + <b>p</b>avedita → tathāgata-<b>pp</b>avedita (made known by the Tathāgata)</div>
<div class="ex">na + <b>p</b>atiṭṭhāti → na<b>pp</b>atiṭṭhāti (is not established)</div></li></ul>
<p>Only certain words do this. For example, <span lang="pi">putta</span> (son) does not: <span lang="pi">sa + putta → saputta</span> (with his son).
These are mostly words that once began with two consonants (compare Sanskrit <i>pramāda</i>), so it is best to learn them as you meet them.</p>
{ex(("pañcahi, bhikkhave, dhammehi samannāgato bhikkhu cavati, <b>nappatiṭṭhāti</b> saddhamme", "possessing five qualities, monks, a bhikkhu falls away and <b>is not established</b> in the good Dhamma", "Falling Away"))}
"""))

# ---------- GRAMMAR III ----------

G3 = []

G3.append(("ka", "ko / kā / kiṃ – who? what?", f"""
<p>The question word has the stem <b>ka-</b>. It has the same endings as <span lang="pi">yo / yā / yaṃ</span>, but the neuter is <b>kiṃ</b>, and a few forms may begin with ki-.</p>
{table(["Masculine", "Neuter", "Feminine"], [
 ("nom", ["ko", "kiṃ", "kā"]), ("acc", ["kaṃ", "kiṃ", "kaṃ"]), ("ins", ["kena", "kena", "kāya"]),
 ("dat", ["kassa (kissa)", "kassa (kissa)", "kassā"]), ("abl", ["kamhā / kasmā", "kamhā / kasmā", "kāya"]),
 ("gen", ["kassa (kissa)", "kassa (kissa)", "kassā"]), ("loc", ["kamhi / kasmiṃ (kimhi / kismiṃ)", "kamhi / kasmiṃ (kimhi / kismiṃ)", "kassaṃ / kāyaṃ"])], first="Singular")}
{table(["Masculine", "Neuter", "Feminine"], [
 ("nom", ["ke", "kāni", "kā / kāyo"]), ("acc", ["ke", "kāni", "kā / kāyo"]), ("ins", ["kehi", "kehi", "kāhi"]),
 ("dat", ["kesaṃ / kesānaṃ", "kesaṃ / kesānaṃ", "kāsaṃ / kāsānaṃ"]), ("abl", ["kehi", "kehi", "kāhi"]),
 ("gen", ["kesaṃ / kesānaṃ", "kesaṃ / kesānaṃ", "kāsaṃ / kāsānaṃ"]), ("loc", ["kesu", "kesu", "kāsu"])], first="Plural")}
{ex(("taṃ <b>kiṃ</b> maññatha, Sāḷhā?", "<b>what</b> do you think, Sāḷha?", "Sāḷha (1)"),
    ("<b>kiṃ</b>-lakkhaṇaṃ viññāṇaṃ?", "<b>what</b> is the characteristic mark of consciousness?", "The Mark of Consciousness"))}
"""))

G3.append(("be", "“To be”: atthi, hoti, bhavati, natthi", f"""
{h("atthi – there is, exists")}
{table(["Singular", "Plural"], [("1st person", ["asmi / amhi", "asma / amha"]), ("2nd person", ["asi", "attha"]), ("3rd person", ["atthi", "santi"])], first="Person")}
<p>As a main verb, <b>atthi</b> says that something <b>exists</b>: “there is”.</p>
{ex(("<b>atthi</b> koci satto …?", "<b>is there</b> any being …?", "Not Transmigrating"),
    ("taṃ kiṃ maññatha, Sāḷhā, <b>atthi</b> lobho?", "what do you think, Sāḷha, <b>is there</b> greed?", "Sāḷha (1)"))}
{h("hoti – is, becomes")}
{table(["Singular", "Plural"], [("1st person", ["homi", "homa"]), ("2nd person", ["hosi", "hotha"]), ("3rd person", ["hoti", "honti"])], first="Person")}
<p><b>hoti</b> can also say that something exists, but it can also mean “<b>becomes</b>”, and it is the usual verb when “X <b>is</b> Y” is said with a verb:</p>
{ex(("cittaṃ, bhikkhave, abhāvitaṃ akammaniyaṃ <b>hoti</b>", "an undeveloped mind <b>is</b> unwieldy", "Unwieldy"))}
{h("bhavati – becomes, is")}
<p><b>bhavati</b> has the regular endings (<span lang="pi">bhavāmi, bhavasi, bhavati</span> …). In the present tense it usually means “becomes”.
In other tenses and moods it is often used where we would expect hoti: the future <span lang="pi">bhavissati</span> (will be), the optative <span lang="pi">bhaveyya</span> (would be).</p>
{h("natthi – there is not")}
<p><b>natthi</b> (also written <span lang="pi">n’atthi</span>) is <span lang="pi">na + atthi</span>: “there is not, does not exist”.</p>
{ex(("yadi … imamhā kāyā aññaṃ kāyaṃ saṅkamanto <b>natthi</b> …", "if … <b>there is no</b> one who transmigrates from this body to another …", "Not Transmigrating"))}
"""))


G3.append(("optative", "The optative (“would, should, might”)", f"""
{h("How it is made")}
<p>The optative endings are added to the present stem, and the last vowel of the stem drops: <span lang="pi">labha + eyya → labh<b>eyya</b></span>.</p>
{table(["Singular", "Plural"], [
 ("1st person (I / we)", ["labh|eyyāmi / labh|eyyaṃ", "labh|eyyāma"]),
 ("2nd person (you)", ["labh|eyyāsi (labh|eyya)", "labh|eyyātha"]),
 ("3rd person (he, she / they)", ["labh|eyya (labh|eyyāti)", "labh|eyyuṃ"])], first="Person")}
<p>The optative of <b>hoti</b> is made from <span lang="pi">bhava-</span>: <span lang="pi">bhaveyyāmi, bhaveyyāsi, bhaveyya, bhaveyyāma, bhaveyyātha, bhaveyyuṃ</span>.
More endings come in Grammar IV.</p>
{h("How it is used")}
<p>The optative speaks about something <b>not real yet</b>: what might happen, would happen, or should happen. In English we use <i>would, could, might, may, should</i>.</p>
<p><b>1. Something imagined</b>, or “if” (even without a word for “if”):</p>
{ex(("kusalaṃ ca h’idaṃ, bhikkhave, bhāvitaṃ ahitāya dukkhāya <b>saṃvatteyya</b>, n’āhaṃ evaṃ <b>vadeyyaṃ</b>", "if this developing of the wholesome <b>led</b> to harm and suffering, I <b>would</b> not <b>say</b> so", "Abandon the Unwholesome"),
    ("kocideva puriso padīpato padīpaṃ <b>padīpeyya</b>", "(suppose) a man <b>were to light</b> a lamp from a lamp", "Not Transmigrating"))}
<p>In the first example the first optative is the “if” part, and the second one says what would follow.</p>
<p><b>2. A gentle instruction</b> (“you should …”):</p>
{ex(("atha tumhe, Sāḷhā, upasampajja <b>vihareyyātha</b>", "then, Sāḷha, you <b>should</b> enter and <b>dwell</b> in them", "Sāḷha (2)"))}
"""))

G3.append(("imperative", "The imperative (commands)", f"""
<p>To tell someone to do something, add these endings to the present stem:</p>
{table(["Singular (you)", "Plural (you all)"], [("Ending", ["-:hi (or the bare stem)", "-tha"]),
 ("labhati (gets)", ["labh|āhi / labha", "labha|tha"]), ("gacchati (goes)", ["gacch|āhi / gaccha", "gaccha|tha"]),
 ("jānāti (knows)", ["jān|āhi", "jānā|tha"]), ("pajahati (gives up)", ["pajah|āhi / pajaha", "pajaha|tha"]),
 ("bhāveti (develops)", ["bhāve|hi", "bhāve|tha"]), ("karoti (does)", ["karo|hi", "karo|tha"])], first="Verb")}
<ul><li>In the singular, a short a becomes long before <b>-hi</b>: <span lang="pi">labh<b>ā</b>hi</span>. A stem in -a may also be used alone as a command: <span lang="pi">labha!</span></li>
<li>The plural looks <b>the same</b> as the present tense “you (all) …”. Only the context shows whether it is a statement or a command.</li></ul>
{ex(("akusalaṃ, bhikkhave, <b>pajahatha</b>", "<b>abandon</b> the unwholesome, monks!", "Abandon the Unwholesome"),
    ("kusalaṃ, bhikkhave, <b>bhāvetha</b>", "<b>develop</b> the wholesome, monks!", "Abandon the Unwholesome"),
    ("opammaṃ <b>karohī</b>’ti", "<b>give</b> an illustration!", "Not Transmigrating"))}
"""))

G3.append(("participle", "The present participle in -nt (“…ing”)", f"""
{h("How it is made")}
<p>Add <b>-nt-</b> to the present stem: <span lang="pi">gaccha- → gaccha<b>nt</b>-</span> (going), <span lang="pi">labha- → labha<b>nt</b>-</span> (getting).
Then add endings like those of a masculine noun in -a:</p>
{table(["Singular", "Plural"], [("nom", ["gacch|anto / gacch|aṃ", "gacch|antā"]), ("acc", ["gacch|antaṃ", "gacch|ante"])])}
{h("How it is used")}
<p><b>1. As a noun</b> – “one who is doing”:</p>
{ex(("imamhā kāyā aññaṃ kāyaṃ <b>saṅkamanto</b> natthi", "there is no <b>one who transmigrates</b> from this body to another", "Not Transmigrating"))}
<p><b>2. As an adjective</b> – describing a noun, like English “a man <i>coming</i>”. It agrees with the noun:</p>
{ex(("passeyya puratthima-disato purisaṃ <b>āgacchantaṃ</b>", "he would see a man <b>coming</b> from the eastern direction (accusative, like purisaṃ)", "The Mark of Consciousness"),
    ("kinnu kho so … padīpo padīpamhā <b>saṅkamanto</b>?", "is that lamp <b>passing over</b> from the (other) lamp?", "Not Transmigrating"))}
{tip("A participle can have its own object, like a verb: <span lang='pi'>aññaṃ kāyaṃ saṅkamanto</span> – passing over <b>to another body</b>.")}
"""))

G3.append(("e-o-verbs", "Verbs with stems in -e and -o", f"""
<p>Many verbs have a present stem ending in <b>-e</b>, and a few in <b>-o</b>. They take the same endings as -a verbs, but their vowel <b>never changes</b> (e and o have no short/long pair).</p>
{table(["bhāveti (develops)", "karoti (does)"], [
 ("1st person sing.", ["bhāve|mi", "karo|mi"]), ("2nd person sing.", ["bhāve|si", "karo|si"]), ("3rd person sing.", ["bhāve|ti", "karo|ti"]),
 ("1st person pl.", ["bhāve|ma", "karo|ma"]), ("2nd person pl.", ["bhāve|tha", "karo|tha"]), ("3rd person pl.", ["bhāve|nti", "karo|nti"])], first="Person")}
<p>The present participle is made in the same way: <span lang="pi">karo<b>nt</b>-</span> (also <span lang="pi">kara<b>nt</b>-</span>), <span lang="pi">dese<b>nt</b>-</span>.</p>
{h("Making something happen")}
<p>Verbs in -e often mean <b>to make something happen</b>. They are often paired with a simpler verb:</p>
{table(["-e verb"], [("bhavati – becomes", ["bhāveti – develops (makes become)"]), ("jāyati – is born", ["janeti – generates (makes be born)"])], first="Simple verb")}
{ex(("chandaṃ <b>janeti</b>", "he <b>generates</b> desire", "Finger Snap"),
    ("sakkā, bhikkhave, kusalaṃ <b>bhāvetuṃ</b>", "it is possible, monks, <b>to develop</b> the wholesome", "Abandon the Unwholesome"))}
"""))


G3.append(("yadi", "yadi – if", f"""
<p><b>yadi</b> means “if”.</p>
<p><b>With the optative</b>, the “if” is only imagined – “if it were so (but it isn’t)”:</p>
{ex(("<b>yadi</b> na <b>paṭisandaheyya</b>, mutto bhavissati pāpakehi kammehi", "<b>if</b> one <b>were</b> not <b>reborn</b>, one would be freed from evil deeds", "Not Transmigrating"))}
<p><b>Without the optative</b>, the speaker accepts the “if” at least for the sake of the argument:</p>
{ex(("<b>yadi</b> … imamhā kāyā aññaṃ kāyaṃ saṅkamanto <b>natthi</b> …", "<b>if</b> there <b>is</b> no one who transmigrates from this body to another …", "Not Transmigrating"))}
"""))

G3.append(("particles", "More little words: ci, kho, hi, eva, nu", f"""
{h("ci – any, some")}
<p>Added to the question words, <b>ci</b> makes them mean “any-” or “some-”:</p>
{table(["Meaning"], [("ko + ci → koci", ["anyone, someone"]), ("kiṃ + ci → kiñci", ["anything, something"]), ("kassa + ci → kassaci", ["of / to anyone"])], first="Form")}
{ex(("atthi <b>koci</b> satto …?", "is there <b>any</b> being …?", "Not Transmigrating"),
    ("<b>kocideva</b> puriso", "<b>some</b> man (ci + eva)", "Not Transmigrating"))}
{h("Words of emphasis")}
<p>These words add emphasis. They are hard to translate exactly, and are often left out in English.</p>
<ul>
<li><b>kho</b> – indeed, now, as for:
<span lang="pi">evameva <b>kho</b>, mahārāja, na ca saṅkamati</span> – just so, great king, it does not transmigrate (Not Transmigrating)</li>
<li><b>hi</b> – indeed, surely; sometimes “for, because”:
<span lang="pi">na <b>hi</b>, mahārāja</span> – no <b>indeed</b>, great king (Not Transmigrating)</li>
<li><b>eva</b> – just, only, indeed: <span lang="pi">evaṃ + eva → evameva</span> – just so</li>
<li><b>nu</b> – makes a question stronger (“then?”), or turns a statement into a question:
<span lang="pi">kiṃ + nu → <b>kinnu</b></span> – is it then …?;
<span lang="pi">na + nu → <b>nanu</b></span> – isn’t it so that …? (expecting “yes”)</li>
</ul>
{ex(("<b>nanu</b> mutto bhavissati pāpakehi kammehi?", "<b>would</b> one <b>not</b> be freed from evil deeds?", "Not Transmigrating"))}
"""))

G3.append(("sakka", "sakkā – it is possible", f"""
<p><b>sakkā</b> means “it is possible, one can”. It is used with an infinitive:</p>
{ex(("<b>sakkā</b>, bhikkhave, akusalaṃ <b>pajahituṃ</b>", "<b>it is possible</b>, monks, <b>to abandon</b> the unwholesome", "Abandon the Unwholesome"))}
"""))

G3.append(("yasma", "yasmā … tasmā – since … therefore", f"""
<p><b>yasmā</b> and <b>tasmā</b> are the ablatives of ya and ta (“from which”, “from that”). Used together they mean “<b>since</b> …, <b>therefore</b> …”:</p>
{ex(("<b>yasmā</b> ca kho, bhikkhave, sakkā akusalaṃ pajahituṃ, <b>tasm’</b>āhaṃ evaṃ vadāmi", "<b>because</b> it is possible to abandon the unwholesome, <b>therefore</b> I say so", "Abandon the Unwholesome"),
    ("<b>yasmā</b> ca kho, mahārāja, paṭisandahati, <b>tasmā</b> na parimutto pāpakehi kammehi", "<b>but since</b> one is reborn, <b>therefore</b> one is not freed from evil deeds", "Not Transmigrating"))}
"""))


G3.append(("compounds", "Compounds with hidden case meanings", f"""
<p>The first part of a compound has no ending, but it still has a relation to the second part, <b>as if</b> it were in a case. To translate, ask which case fits:</p>
{table(["Hidden case", "Meaning"], [("lobha-pakata", ["instrumental – by", "made <b>by</b> greed"]), ("lobha-ja", ["ablative – from", "born <b>of</b> greed"]),
 ("viññu-garahita", ["instrumental – by", "censured <b>by</b> the wise"]), ("saddhamma-savana", ["genitive – of", "hearing <b>of</b> the good Dhamma"]),
 ("kamma-nirodha", ["genitive – of", "the cessation <b>of</b> kamma"])], first="Compound")}
{ex(("<b>viññu-garahitā</b>, bhante", "<b>censured by the wise</b>, venerable sir", "Sāḷha (1)"))}
"""))

G3.append(("abl-to", "The ablative in -to (“from”)", f"""
<p>The ending <b>-to</b> added to a noun stem is another very common way to say “<b>from</b>”:</p>
{ex(("<b>padīpato</b> padīpaṃ padīpeyya", "would light a lamp <b>from a lamp</b>", "Not Transmigrating"),
    ("<b>puratthima-disato</b> purisaṃ āgacchantaṃ", "a man coming <b>from the eastern direction</b>", "The Mark of Consciousness"))}
"""))


G3.append(("sandhi", "Sandhi: ṃ before consonants and vowels", f"""
<ul class="rules">
<li class="rule"><b>1. Before a consonant, ṃ takes the nasal of that consonant’s group</b> (ṅ before k, g; ñ before c, j; n before t, d; m before p, b).
<div class="ex">ya<b>ṃ</b> + <b>c</b>a → ya<b>ñc</b>a</div><div class="ex">viññāṇa<b>ṃ</b> + <b>t</b>i → viññāṇa<b>n’t</b>i</div><div class="ex">eka-dhamma<b>ṃ</b> + <b>p</b>i → eka-dhamma<b>mp</b>i</div></li>
<li class="rule"><b>2. ṃ never stands between two vowels.</b> Before a vowel it becomes <b>m</b>.
<div class="ex">eta<b>ṃ</b> + <b>a</b>tthaṃ → eta<b>ma</b>tthaṃ</div><div class="ex">eva<b>ṃ</b> + <b>e</b>va → eva<b>me</b>va</div></li>
</ul>
"""))

# ---------- GRAMMAR IV ----------

G4 = []

G4.append(("ima", "ayaṃ / idaṃ – this: all the forms", f"""
<p>Grammar II gave the nominative and accusative. Here are all the forms. Many have a short alternative beginning with a- or e-.</p>
{table(["Masculine", "Neuter", "Feminine"], [
 ("nom", ["ayaṃ", "idaṃ / imaṃ", "ayaṃ"]), ("acc", ["imaṃ", "idaṃ / imaṃ", "imaṃ"]), ("ins", ["iminā / anena", "iminā / anena", "imāya"]),
 ("dat", ["imassa / assa", "imassa / assa", "imissā / imāya / assā"]), ("abl", ["imamhā / imasmā / asmā", "imamhā / imasmā / asmā", "imāya"]),
 ("gen", ["imassa / assa", "imassa / assa", "imissā / imāya / assā"]), ("loc", ["imasmiṃ / imamhi / asmiṃ", "imasmiṃ / imamhi / asmiṃ", "imissaṃ / imāyaṃ / assaṃ"])], first="Singular")}
{table(["Masculine", "Neuter", "Feminine"], [
 ("nom", ["ime", "imāni", "imā / imāyo"]), ("acc", ["ime", "imāni", "imā / imāyo"]), ("ins", ["imehi / ehi", "imehi / ehi", "imāhi"]),
 ("dat", ["imesaṃ / esaṃ", "imesaṃ / esaṃ", "imāsaṃ"]), ("abl", ["imehi / ehi", "imehi / ehi", "imāhi"]),
 ("gen", ["imesaṃ / esaṃ", "imesaṃ / esaṃ", "imāsaṃ"]), ("loc", ["imesu / esu", "imesu / esu", "imāsu"])], first="Plural")}
{ex(("<b>imamhā</b> kāyā aññaṃ kāyaṃ", "from <b>this</b> body to another (ablative)", "Not Transmigrating"),
    ("<b>imehi</b> kho, bhikkhave, pañcahi dhammehi samannāgato", "possessing <b>these</b> five qualities, monks (instrumental)", "Falling Away"),
    ("cattāro’<b>me</b> = cattāro + <b>ime</b>", "<b>these</b> four", "Lesson 4"))}
"""))


G4.append(("absolutive", "The absolutive in -tvā and -ya (“having done”)", f"""
<p>This form means “<b>having done</b>” something. It has <b>no endings</b> – it never changes. The book calls it the “gerund”; it is also called the absolutive.</p>
{h("-tvā (or -tvāna)")}
<p><b>1.</b> Verbs with a stem in <b>-a</b>: the a becomes i, as in the infinitive: <span lang="pi">labhati → labh<b>itvā</b></span>, <span lang="pi">bhavati → bhav<b>itvā</b></span>, <span lang="pi">garahati → garah<b>itvā</b></span>.</p>
<p><b>2.</b> Verbs with a stem in <b>-e</b>: add -tvā directly: <span lang="pi">neti → ne<b>tvā</b></span>, <span lang="pi">deseti → dese<b>tvā</b></span>.</p>
<p><b>3.</b> Other verbs: -tvā is added to the root, which often changes:</p>
{table(["Absolutive"], [("karoti (does)", ["katvā"]), ("gacchati (goes)", ["gantvā"]), ("suṇāti (hears)", ["sutvā"]), ("pivati (drinks)", ["pitvā"]),
 ("passati (sees)", ["disvā"]), ("deti (gives)", ["datvā"]), ("jānāti (knows)", ["ñatvā / jānitvā"]), ("labhati (gets)", ["laddhā (also labhitvā)"])], first="Verb")}
{h("-ya")}
<p>Verbs with a prefix often use <b>-ya</b> instead:</p>
{table(["Absolutive"], [("pariyādiyati (takes over)", ["pariyādāya – having overpowered"]), ("pajahati (abandons)", ["pahāya – having abandoned"])], first="Verb")}
{h("How it is used")}
<p>It shows an action that happens <b>before</b> the main verb, done by the same person. Translate “having done X, he …” or “he does X and …”:</p>
{ex(("āyuṃ kho pana <b>datvā</b> āyussa bhāginī hoti", "<b>having given</b> long life, she has a share in long life", "Lesson 4"),
    ("attānaṃ upamaṃ <b>katvā</b>, na haneyya na ghātaye", "<b>having made</b> oneself the example, one should not kill nor cause to kill", "Dhammapada 129"),
    ("purisassa cittaṃ <b>pariyādāya</b> tiṭṭhati", "<b>having overpowered</b> the mind of a man, it remains (= it obsesses his mind)", "Obsession of the Mind"))}
{tip("Like a verb, the absolutive can have its own object: <span lang='pi'>attānaṃ upamaṃ katvā</span>.")}
"""))

G4.append(("mana", "The present participle in -māna and -āna", f"""
<p>Besides <span lang="pi">-nt-</span> (Grammar III), there is a second present participle in <b>-māna</b>, added to the present stem:</p>
{table(["-māna participle"], [("gacchati (goes)", ["gaccha|māna – going"]), ("uppajjati (arises)", ["uppajja|māna – arising"]), ("bhāsati (speaks)", ["bhāsa|māna – speaking, reciting"]),
 ("deseti (teaches)", ["desaya|māna – teaching (-e becomes -aya)"])], first="Verb")}
<p>It is often called the “middle” participle, but in practice it means the same as the -nt form: <span lang="pi">gacchanto</span> or <span lang="pi">gacchamāno</span> – going.</p>
<p>A few verbs have <b>-āna</b> instead: <span lang="pi">anupādiyāno</span> – not clinging; <span lang="pi">sampajāno</span> – fully aware.</p>
<p>These participles take the endings of adjectives in -a, and can be used as nouns (“one who …”) or as adjectives:</p>
{ex(("bahumpi ce sahitaṃ <b>bhāsamāno</b>", "even if <b>reciting</b> many of the texts", "Dhammapada 19"),
    ("sammappajāno suvimutta-citto <b>anupādiyāno</b>", "fully understanding, with mind well freed, <b>not clinging</b>", "Dhammapada 20"))}
"""))

G4.append(("fem-participle", "Feminine participles in -ī and -ā", f"""
<p>When a participle describes a woman, or means “<b>she who</b> …”:</p>
<ul><li>the <b>-nt</b> participle takes <b>-ī</b>, like <span lang="pi">nadī</span>: <span lang="pi">de<b>ntī</b></span> – she who gives; <span lang="pi">karo<b>ntī</b></span> – she who does;</li>
<li>the <b>-māna</b> participle takes <b>-ā</b>, like <span lang="pi">sālā</span>: <span lang="pi">gaccha<b>mānā</b></span> – she who goes.</li></ul>
{ex(("bhojanaṃ, Suppavāse, <b>dentī</b> ariya-sāvikā", "Suppavāsā, a noble woman disciple <b>who gives</b> a meal", "Lesson 4"))}
"""))

G4.append(("optative", "More optative endings", f"""
<p>Besides the endings in Grammar III, the optative has some shorter endings:</p>
{table(["Singular", "Plural"], [("1st person", ["-e", "-ema (-eyyāmhe)"]), ("2nd person", ["-e (-etho)", "-etha (-eyyavho)"]), ("3rd person", ["-e (-etha)", "(-eraṃ)"])], first="Person")}
<p>The endings in brackets are called “middle” endings, but the meaning is the same.</p>
{ex(("na <b>bhaje</b> pāpake mitte", "one <b>should</b> not <b>associate</b> with bad friends (-e)", "Dhammapada 78"),
    ("<b>bhajetha</b> mitte kalyāṇe", "one <b>should associate</b> with good friends (-etha)", "Dhammapada 78"),
    ("na haneyya na <b>ghātaye</b>", "one should not kill nor <b>cause to kill</b> (-e)", "Dhammapada 129"))}
"""))

G4.append(("numerals", "Numbers 1 to 5", f"""
<p>The stems are: <b>eka</b> (1), <b>dvi</b> (2), <b>ti</b> (3), <b>catu</b> (4), <b>pañca</b> (5).</p>
{h("eka – one")}
<p><b>eka</b> takes the endings of <span lang="pi">so / sā / taṃ</span>. In the singular it means “one”; in the plural (<span lang="pi">eke</span>) it means “<b>some</b>”.</p>
{table(["Masculine", "Neuter", "Feminine"], [
 ("nom", ["eko", "ekaṃ", "ekā"]), ("acc", ["ekaṃ", "ekaṃ", "ekaṃ"]), ("ins", ["ekena", "ekena", "ekāya"]),
 ("dat", ["ekassa", "ekassa", "ekissā (ekāya)"]), ("abl", ["ekamhā / ekasmā", "ekamhā / ekasmā", "ekāya"]),
 ("gen", ["ekassa", "ekassa", "ekissā (ekāya)"]), ("loc", ["ekamhi / ekasmiṃ", "ekamhi / ekasmiṃ", "ekissaṃ (ekāyaṃ)"])], first="Singular")}
{table(["Masculine", "Neuter", "Feminine"], [
 ("nom", ["eke", "ekāni", "ekā / ekāyo"]), ("acc", ["eke", "ekāni", "ekā / ekāyo"]), ("ins", ["ekehi", "ekehi", "ekāhi"]),
 ("dat", ["ekesaṃ (ekesānaṃ)", "ekesaṃ (ekesānaṃ)", "ekāsaṃ (ekāsānaṃ)"]), ("abl", ["ekehi", "ekehi", "ekāhi"]),
 ("gen", ["ekesaṃ (ekesānaṃ)", "ekesaṃ (ekesānaṃ)", "ekāsaṃ (ekāsānaṃ)"]), ("loc", ["ekesu", "ekesu", "ekāsu"])], first="Plural")}
{h("dvi, ti, catu, pañca")}
<p><b>ti</b> and <b>catu</b> have different forms for each gender. <b>dvi</b>, <b>pañca</b> and the higher numbers have one set of forms for all genders.</p>
{table(["dvi (2)", "ti (3) m. / n. / f.", "catu (4) m. / n. / f.", "pañca (5)"], [
 ("nom", ["dve / duve", "tayo / tīṇi / tisso", "cattāro, caturo / cattāri / catasso", "pañca"]),
 ("acc", ["dve / duve", "tayo / tīṇi / tisso", "cattāro, caturo / cattāri / catasso", "pañca"]),
 ("ins", ["dvīhi", "tīhi", "catūhi", "pañcahi"]),
 ("dat", ["dvinnaṃ / duvinnaṃ", "tiṇṇaṃ, tiṇṇannaṃ / f. tissannaṃ", "catunnaṃ / f. catassannaṃ", "pañcannaṃ"]),
 ("abl", ["dvīhi", "tīhi", "catūhi", "pañcahi"]),
 ("gen", ["dvinnaṃ / duvinnaṃ", "tiṇṇaṃ, tiṇṇannaṃ / f. tissannaṃ", "catunnaṃ / f. catassannaṃ", "pañcannaṃ"]),
 ("loc", ["dvīsu", "tīsu", "catūsu", "pañcasu"])], first="Case")}
{ex(("<b>tīhi</b>, bhikkhave, aṅgehi samannāgato", "possessing <b>three</b> factors, monks (instrumental)", "The Shopkeeper"),
    ("<b>tīṇi</b>’māni, bhikkhave, nidānāni", "there are these <b>three</b> causes, monks (neuter nominative)", "Causes"),
    ("<b>cattāri</b> ṭhānāni deti", "she gives <b>four</b> things (neuter accusative)", "Lesson 4"),
    ("<b>eke</b> samaṇa-brāhmaṇā", "<b>some</b> ascetics and brahmins (masculine plural)", "Lesson 4"))}
"""))

G4.append(("sabba-para", "sabba (all) and para (other)", f"""
<p><b>sabba</b> (all) and <b>para</b> (other) take the endings of the pronouns (<span lang="pi">te, tesaṃ</span> …), not of the nouns:
<span lang="pi">sabbe</span> (all, masculine plural), <span lang="pi">sabbāni</span> (neuter), <span lang="pi">sabbā</span> (feminine), <span lang="pi">sabbesaṃ</span> (of all), <span lang="pi">paresaṃ</span> (of others).</p>
{ex(("<b>sabbe</b> tasanti daṇḍassa", "<b>all</b> tremble at the rod", "Dhammapada 129"),
    ("<b>sabbesaṃ</b> jīvitaṃ piyaṃ", "life is dear <b>to all</b>", "Dhammapada 130"),
    ("gopo’va gāvo gaṇayaṃ <b>paresaṃ</b>", "like a cowherd counting the cattle <b>of others</b>", "Dhammapada 19"))}
"""))


G4.append(("iva", "iva / ’va – like, as", f"""
<p><b>iva</b> means “<b>like, as</b>”. It is used in comparisons, and it comes <b>after</b> the word it compares. It usually appears in its short form <b>’va</b>:</p>
{ex(("gopo’<b>va</b> gāvo gaṇayaṃ paresaṃ", "<b>like</b> a cowherd counting the cattle of others (gopo + iva)", "Dhammapada 19"))}
{tip("’va can also be a short form of <b>eva</b> (just, indeed): <span lang='pi'>ete’va sattā</span> = <span lang='pi'>ete eva sattā</span> (Few and Many). Context tells us which one it is.")}
"""))

G4.append(("ce", "ce – if", f"""
<p><b>ce</b> is another word for “<b>if</b>”. It is a clitic, so it never stands first: it comes after the first word of its clause.</p>
{ex(("bahumpi <b>ce</b> sahitaṃ bhāsamāno … na bhāgavā sāmaññassa hoti", "<b>even if</b> he recites many of the texts …, he has no share in the recluse’s life", "Dhammapada 19"),
    ("appampi <b>ce</b> sahitaṃ bhāsamāno … sa bhāgavā sāmaññassa hoti", "<b>even if</b> he recites few of the texts …, he has a share in the recluse’s life", "Dhammapada 20"))}
<p>With the optative, <b>ce</b> describes something imagined. The optative of <b>atthi</b> is useful here: <span lang="pi"><b>assaṃ</b></span> – I would be; <span lang="pi"><b>assa</b></span> (or <span lang="pi">siyā</span>) – he / she would be; <span lang="pi"><b>assu</b></span> – they would be.</p>
"""))

CHAPTERS = [
    {"n": 1, "title": "Grammar I", "lesson": 1, "pages": "20–27", "topics": G1},
    {"n": 2, "title": "Grammar II", "lesson": 2, "pages": "33–41", "topics": G2},
    {"n": 3, "title": "Grammar III", "lesson": 3, "pages": "48–56", "topics": G3},
    {"n": 4, "title": "Grammar IV", "lesson": 4, "pages": "65–72", "topics": G4},
]

def main():
    out = {
        "title": "Grammar Guide for the Book",
        "subtitle": "A New Course in Reading Pāḷi",
        "intro": "This guide follows the grammar sections of the course book, one by one. Each point is explained in simple words, with examples from the texts we read in class.",
        "credit": "Written for this course. Forms checked against Ṭhānuttamo Bhikkhu, Māgadhabhāsā (Pāḷi): A Compendious Grammar (Pariyatti, 2024).",
        "chapters": [],
    }
    for ch in CHAPTERS:
        out["chapters"].append({
            "n": ch["n"], "title": ch["title"], "lesson": ch["lesson"], "pages": ch["pages"],
            "topics": [{"id": i, "title": glue(t), "html": tidy(re.sub(r"\s*\n\s*", " ", html).strip())} for i, t, html in ch["topics"]],
        })
    p = os.path.join(ROOT, "data", "grammar", "book.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote", p, sum(len(c["topics"]) for c in out["chapters"]), "topics")

if __name__ == "__main__":
    main()
