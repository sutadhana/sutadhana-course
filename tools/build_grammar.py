#!/usr/bin/env python3
"""Build data/grammar/index.json.

Until Mor's own grammar guide is added, each section holds a short interim
note (marked interim) so that grammar links in the reader lead somewhere useful."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tablewrap"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


DHAMMA = table(["", "singular", "plural"], [
    ["nominative", "dhammo", "dhammā"],
    ["accusative", "dhammaṃ", "dhamme"],
    ["instrumental", "dhammena", "dhammehi"],
    ["dative", "dhammāya, dhammassa", "dhammānaṃ"],
    ["ablative", "dhammā, dhammasmā, dhammamhā", "dhammehi"],
    ["genitive", "dhammassa", "dhammānaṃ"],
    ["locative", "dhamme, dhammasmiṃ, dhammamhi", "dhammesu"],
    ["vocative", "dhamma", "dhammā"],
])


def case(id_, title, text, example):
    return dict(id=id_, title=title, interim=True,
                html=f"<p>{text}</p><p><b>In our texts:</b> {example}</p>"
                     f"<p>The a-stem masculine noun <b>dhamma</b>, for reference:</p>{DHAMMA}")


SECTIONS = [
    case("nominative", "Nominative",
         "The case of the subject: the one who does the action, or the thing a sentence is about. "
         "A word describing the subject (an adjective or participle) is also nominative.",
         "<b>cittaṃ</b> … saṃvattati, “the mind … leads”; <b>dhammā</b> uppajjanti, “qualities arise”."),
    case("accusative", "Accusative",
         "The case of the direct object, and of the goal of a verb of motion. The neuter accusative singular "
         "is also used as an adverb.",
         "buddhaṃ saraṇaṃ <b>gacchāmi</b>, “I go to the Buddha as refuge”; <b>dutiyaṃ</b>, “for the second time”."),
    case("instrumental", "Instrumental",
         "“By, with, by means of”. It also expresses cause: “because of, on account of”.",
         "<b>yena</b> … nūppajjanti, “on account of which … do not arise”."),
    case("dative", "Dative",
         "“To, for”. Very common for purpose or result, especially with saṃvattati, “leads to”, and with "
         "abstract nouns: “for the sake of …”. It also marks the person for whom something is so.",
         "mahato <b>anatthāya</b> saṃvattati, “leads to great harm”; <b>pahānāya</b>, “for the abandoning”; "
         "<b>micchādiṭṭhikassa</b>, “for one of wrong view”."),
    case("ablative", "Ablative",
         "“From”: separation, origin, and also cause (“because of”) and comparison (“than”).",
         "Coming up in later readings."),
    case("genitive", "Genitive",
         "“Of”: possession and other relations between two nouns. Its forms are often the same as the dative’s, "
         "so the context decides.",
         "anuppannānaṃ … <b>dhammānaṃ</b> anuppādāya, “for the non-arising of unarisen … qualities”."),
    case("locative", "Locative",
         "“In, on, at, among”: place, time and circumstance.",
         "Coming up in later readings."),
    case("vocative", "Vocative",
         "The case of address: the person or people spoken to.",
         "<b>bhikkhave</b>, “O bhikkhus” (vocative plural of bhikkhu)."),
    dict(id="present", title="Present tense", interim=True, html=
         "<p>Describes what happens now, what usually happens, or a general truth. "
         "The endings show person and number.</p>" + table(["", "singular", "plural"], [
             ["3rd person", "gacchati", "gacchanti"],
             ["2nd person", "gacchasi", "gacchatha"],
             ["1st person", "gacchāmi", "gacchāma"]]) +
         "<p><b>In our texts:</b> saraṇaṃ <b>gacchāmi</b>, “I go for refuge”; <b>samanupassāmi</b>, “I see”; "
         "<b>saṃvattati</b>, “it leads”; <b>uppajjanti</b>, “they arise”.</p>"),
    dict(id="imperative", title="Imperative", interim=True, html=
         "<p>Commands, requests and wishes: “go!”, “may he go”.</p>" + table(["", "singular", "plural"], [
             ["3rd person", "gacchatu", "gacchantu"],
             ["2nd person", "gaccha, gacchāhi", "gacchatha"],
             ["1st person", "gacchāmi", "gacchāma"]])),
    dict(id="optative", title="Optative", interim=True, html=
         "<p>What should, would or might happen: advice, possibility and conditions. "
         "Recognise it by <b>-eyya-</b> (and the short 3rd person singular in <b>-e</b>).</p>" +
         table(["", "singular", "plural"], [
             ["3rd person", "gaccheyya, gacche", "gaccheyyuṃ"],
             ["2nd person", "gaccheyyāsi", "gaccheyyātha"],
             ["1st person", "gaccheyyāmi", "gaccheyyāma"]])),
    dict(id="future", title="Future tense", interim=True, html=
         "<p>What will happen. Recognise it by <b>-issa-</b>: gacchissati, “he will go”; "
         "gacchissanti, “they will go”.</p>"),
    dict(id="aorist", title="Aorist (past tense)", interim=True, html=
         "<p>The usual past tense of narrative: “he went, they said”. Many verbs form it with <b>-i</b> "
         "(3rd singular) and <b>-iṃsu</b> (3rd plural): pucchi, “he asked”; pucchiṃsu, “they asked”. "
         "Several common verbs are irregular.</p>"),
    dict(id="past-participle", title="Past participle", interim=True, html=
         "<p>A verbal adjective in <b>-ta</b> or <b>-na</b>: “tamed, arisen, guarded”. Like any adjective "
         "it agrees with its noun in gender, case and number, and it can also stand as the main verb "
         "of a sentence.</p><p><b>In our texts:</b> <b>dantaṃ</b> cittaṃ, “a tamed mind”; "
         "<b>uppannā</b> dhammā, “arisen qualities”. With the prefix a(n)-: adanta, anuppanna.</p>"),
    dict(id="present-participle", title="Present participle", interim=True, html=
         "<p>A verbal adjective in <b>-nta</b> or <b>-māna</b>: “going, seeing”. It describes an action "
         "happening at the same time as the main verb.</p>"),
    dict(id="absolutive", title="Absolutive", interim=True, html=
         "<p>An indeclinable verb form in <b>-tvā</b>, <b>-ya</b> or <b>-tvāna</b>: “having done”. It describes "
         "an action completed before the main verb, by the same subject.</p>"),
    dict(id="infinitive", title="Infinitive", interim=True, html=
         "<p>“To do”: an indeclinable form in <b>-tuṃ</b>, often expressing purpose: gantuṃ, “to go”.</p>"),
    dict(id="sandhi", title="Sandhi and compounds", interim=True, html=
         "<p>When two words meet, their sounds often join and change (sandhi). In our texts:</p>"
         "<ul><li>The parts of a compound are separated by a hyphen: dhammavādī → <b>dhamma-vādī</b>.</li>"
         "<li>Where sandhi changes the sounds, an apostrophe goes with the first word: dhamma + anupassī → "
         "<b>dhamm’ānupassī</b> (not dhammā’nupassī).</li>"
         "<li>But when the change reflects the grammar of the first word and not the second, the apostrophe "
         "goes before the second word: dhammo + amhi → <b>dhammo’mhi</b> (not dhamm’omhi).</li>"
         "<li>Where a joining sound is inserted between the words, there is no apostrophe: yathā + idaṃ → <b>yathayidaṃ</b>.</li></ul>" +
         table(["in the text", "from"], [
             ["n’āhaṃ", "na + ahaṃ"], ["saṃvattatī’ti", "saṃvattati + iti"], ["n’uppajjanti", "na + uppajjanti"],
             ["c’eva", "ca + eva"], ["yathayidaṃ", "yathā + idaṃ (a y is inserted, so no apostrophe)"],
             ["eka-dhammaṃ", "eka + dhammaṃ (compound)"]]) +
         "<p>Tap a joined word in the reader to see its parts.</p>"),
    dict(id="pronouns", title="Pronouns", interim=True, html=
         "<p>Personal pronouns (<b>ahaṃ</b>, “I”) and the relative pronoun <b>ya-</b>, “who, which”, "
         "which opens a clause of its own. The relative clause is often picked up by a word in the main "
         "clause.</p><p><b>In our texts:</b> aññaṃ ekadhammaṃ … <b>yaṃ</b> evaṃ … saṃvattati, "
         "“one other thing <b>which</b> thus leads …”; <b>yena</b>, “on account of which”.</p>"),
    dict(id="indeclinables", title="Indeclinables", interim=True, html=
         "<p>Words that never change their form: particles, conjunctions and adverbs such as <b>ca</b> "
         "“and”, <b>vā</b> “or”, <b>pi</b> “also, even”, <b>evaṃ</b> “thus”, <b>na</b> “not” and <b>iti</b>, "
         "which closes a quotation.</p>"),
    dict(id="adjectives", title="Adjectives", interim=True, html=
         "<p>An adjective takes the gender, case and number of the noun it describes, and may stand "
         "before or after it.</p><p><b>In our texts:</b> <b>kusalā</b> dhammā (masculine nominative plural); "
         "<b>mahato</b> anatthāya (masculine dative singular).</p>"),
    dict(id="numbers", title="Numbers", interim=True, html=
         "<p>Ordinals such as <b>dutiya</b> “second” and <b>tatiya</b> “third” decline like adjectives. "
         "Their neuter accusative singular serves as an adverb: <b>dutiyaṃ pi</b>, “for the second time too”.</p>"),
]

DATA = dict(
    title="Grammar guide",
    intro="Choose a topic. In the reader, the grammar line for each word links straight to the matching section.",
    interimNote="A short note for now. This section will be replaced by Mor’s own grammar guide.",
    sections=SECTIONS,
)

with open(os.path.join(ROOT, "data", "grammar", "index.json"), "w", encoding="utf-8") as fh:
    json.dump(DATA, fh, ensure_ascii=False, indent=1)
print(len(SECTIONS), "sections")
