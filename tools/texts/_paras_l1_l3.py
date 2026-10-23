# Pali (as in the printed book, written with Mor's conventions) and English for
# NCRP Lesson 1 further readings and Lessons 2-3. Word analyses: ncrp_l1_l3_words.py.
# Notes on choices are in NOTES at the bottom.

AN = ("English: course exercise book, after Bhikkhu Bodhi, The Numerical Discourses of the Buddha "
      "(Wisdom Publications, 2012).")
DHP = "English: course exercise book, after Ācariya Buddharakkhita’s translation of the Dhammapada."
OTHER = "English: course exercise book."


def rep(template, items):
    return [(template[0].format(**i), template[1].format(**i)) for i in items]


# ---------------------------------------------------------------- 1.2.1
P121 = [
    ("N’āhaṃ, bhikkhave, aññaṃ eka-dhammaṃ pi samanupassāmi yo evaṃ saddhammassa sammosāya antaradhānāya saṃvattati yathayidaṃ, bhikkhave, pamādo. Pamādo, bhikkhave, saddhammassa sammosāya antaradhānāya saṃvattatī’ti.",
     "“Bhikkhus, I do not see even a single thing that so leads to the decline and disappearance of the good Dhamma as heedlessness. Heedlessness leads to the decline and disappearance of the good Dhamma.”"),
    ("N’āhaṃ, bhikkhave, aññaṃ eka-dhammaṃ pi samanupassāmi yo evaṃ saddhammassa ṭhitiyā asammosāya anantaradhānāya saṃvattati yathayidaṃ, bhikkhave, appamādo. Appamādo, bhikkhave, saddhammassa ṭhitiyā asammosāya anantaradhānāya saṃvattatī’ti.",
     "“Bhikkhus, I do not see even a single thing that so leads to the continuation, non-decline, and non-disappearance of the good Dhamma as heedfulness. Heedfulness leads to the continuation, non-decline, and non-disappearance of the good Dhamma.”"),
    ("N’āhaṃ, bhikkhave, aññaṃ eka-dhammaṃ pi samanupassāmi yaṃ evaṃ saddhammassa sammosāya antaradhānāya saṃvattati yathayidaṃ, bhikkhave, kosajjaṃ. Kosajjaṃ, bhikkhave, saddhammassa sammosāya antaradhānāya saṃvattatī’ti.",
     "“Bhikkhus, I do not see even a single thing that so leads to the decline and disappearance of the good Dhamma as laziness …”"),
    ("N’āhaṃ, bhikkhave, aññaṃ eka-dhammaṃ pi samanupassāmi yo evaṃ saddhammassa ṭhitiyā asammosāya anantaradhānāya saṃvattati yathayidaṃ, bhikkhave, viriy’ārambho. Viriy’ārambho, bhikkhave, saddhammassa ṭhitiyā asammosāya anantaradhānāya saṃvattatī’ti.",
     "“… that so leads to the continuation, non-decline, and non-disappearance of the good Dhamma as arousal of energy …”"),
    ("N’āhaṃ, bhikkhave, aññaṃ eka-dhammaṃ pi samanupassāmi yo evaṃ saddhammassa ṭhitiyā asammosāya anantaradhānāya saṃvattati yathayidaṃ, bhikkhave, anuyogo kusalānaṃ dhammānaṃ, ananuyogo akusalānaṃ dhammānaṃ. Anuyogo, bhikkhave, kusalānaṃ dhammānaṃ, ananuyogo akusalānaṃ dhammānaṃ saddhammassa ṭhitiyā asammosāya anantaradhānāya saṃvattatī’ti.",
     "“… the pursuit of wholesome qualities and the non-pursuit of unwholesome qualities. The pursuit of wholesome qualities and the non-pursuit of unwholesome qualities leads to the continuation, non-decline, and non-disappearance of the good Dhamma.”"),
]

# ---------------------------------------------------------------- 1.2.2
SENSES = [
    dict(obj="eka-rūpaṃ", subj="rūpaṃ", en="form", art="the form"),
    dict(obj="eka-saddaṃ", subj="saddo", en="sound", art="the sound"),
    dict(obj="eka-gandhaṃ", subj="gandho", en="odor", art="the odor"),
    dict(obj="eka-rasaṃ", subj="raso", en="taste", art="the taste"),
    dict(obj="eka-phoṭṭhabbaṃ", subj="phoṭṭhabbaṃ", en="touch", art="the touch"),
]
P122 = []
for who, other, gen_who, en_who, en_other in [("purisassa", "itthi", "purisassa", "a man", "a woman"),
                                               ("itthiyā", "purisa", "itthiyā", "a woman", "a man")]:
    for s in SENSES:
        thing = f"{other}-{s['subj']}"
        P122.append((
            f"N’āhaṃ, bhikkhave, aññaṃ {s['obj']} pi samanupassāmi yaṃ evaṃ {gen_who} cittaṃ pariyādāya tiṭṭhati yathayidaṃ, bhikkhave, {thing}. "
            f"{thing[0].upper() + thing[1:]}, bhikkhave, {gen_who} cittaṃ pariyādāya tiṭṭhatī’ti.",
            f"“Bhikkhus, I do not see even one other {s['en']} that so obsesses the mind of {en_who} as the {s['en']} of {en_other}. "
            f"The {s['en']} of {en_other} obsesses the mind of {en_who}.”"))

# ---------------------------------------------------------------- 2.1.1
P211 = [
    ("Kiccho manussa-paṭilābho\nkicchaṃ maccānaṃ jīvitaṃ\nkicchaṃ saddhamma-savanaṃ\nkiccho buddhānaṃ uppādo.",
     "Hard is it to be born a man,\nhard is the life of mortals,\nhard is it to gain the opportunity of hearing the Sublime Truth,\nhard to encounter is the arising of the Buddhas.\n(Dhp 182)"),
    ("Sabba-pāpassa akaraṇaṃ\nkusalassa upasampadā\nsacitta-pariyodapanaṃ\netaṃ buddhāna(ṃ) sāsanaṃ.",
     "To avoid all evil,\nto cultivate good,\nand to cleanse one’s mind:\nthis is the teaching of the Buddhas.\n(Dhp 183)"),
    ("Na hi verena verāni\nsammant’īdha kudācanaṃ\naverena ca sammanti\nesa dhammo sanantano.",
     "Hatred is never appeased\nby hatred in this world.\nBy non-hatred alone is hatred appeased.\nThis is a law eternal.\n(Dhp 5)"),
]

# ---------------------------------------------------------------- 2.1.2
P212 = [
    ("Tīhi, bhikkhave, aṅgehi samannāgato pāpaṇiko abhabbo anadhigataṃ vā bhogaṃ adhigantuṃ, adhigataṃ vā bhogaṃ phātiṃ kātuṃ. Katamehi tīhi? Idha, bhikkhave, pāpaṇiko pubbaṇha-samayaṃ na sakkaccaṃ kammantaṃ adhiṭṭhāti, majjhaṇhika-samayaṃ na sakkaccaṃ kammantaṃ adhiṭṭhāti, sāyaṇha-samayaṃ na sakkaccaṃ kammantaṃ adhiṭṭhāti. Imehi kho, bhikkhave, tīhi aṅgehi samannāgato pāpaṇiko abhabbo anadhigataṃ vā bhogaṃ adhigantuṃ, adhigataṃ vā bhogaṃ phātiṃ kātuṃ.",
     "“Bhikkhus, possessing three factors, a shopkeeper is incapable of acquiring wealth not yet acquired or of increasing wealth already acquired. What three? Here, a shopkeeper does not diligently apply himself to his work in the morning, in the middle of the day, or in the evening. Possessing these three factors, a shopkeeper is incapable of acquiring wealth not yet acquired or of increasing wealth already acquired."),
    ("Evameva kho, bhikkhave, tīhi dhammehi samannāgato bhikkhu abhabbo anadhigataṃ vā kusalaṃ dhammaṃ adhigantuṃ, adhigataṃ vā kusalaṃ dhammaṃ phātiṃ kātuṃ. Katamehi tīhi? Idha, bhikkhave, bhikkhu pubbaṇha-samayaṃ na sakkaccaṃ samādhi-nimittaṃ adhiṭṭhāti, majjhaṇhika-samayaṃ na sakkaccaṃ samādhi-nimittaṃ adhiṭṭhāti, sāyaṇha-samayaṃ na sakkaccaṃ samādhi-nimittaṃ adhiṭṭhāti. Imehi kho, bhikkhave, tīhi dhammehi samannāgato bhikkhu abhabbo anadhigataṃ vā kusalaṃ dhammaṃ adhigantuṃ, adhigataṃ vā kusalaṃ dhammaṃ phātiṃ kātuṃ.",
     "“So too, possessing three factors, a bhikkhu is incapable of achieving a wholesome state not yet attained or of increasing a wholesome state already attained. What three? Here, a bhikkhu does not diligently apply himself to an object of concentration in the morning, in the middle of the day, or in the evening. Possessing these three factors, a bhikkhu is incapable of achieving a wholesome state not yet attained or of increasing a wholesome state already attained."),
    ("Tīhi, bhikkhave, aṅgehi samannāgato pāpaṇiko bhabbo anadhigataṃ vā bhogaṃ adhigantuṃ, adhigataṃ vā bhogaṃ phātiṃ kātuṃ. Katamehi tīhi? Idha, bhikkhave, pāpaṇiko pubbaṇha-samayaṃ sakkaccaṃ kammantaṃ adhiṭṭhāti, majjhaṇhika-samayaṃ … pe … sāyaṇha-samayaṃ sakkaccaṃ kammantaṃ adhiṭṭhāti. Imehi kho, bhikkhave, tīhi aṅgehi samannāgato pāpaṇiko bhabbo anadhigataṃ vā bhogaṃ adhigantuṃ, adhigataṃ vā bhogaṃ phātiṃ kātuṃ.",
     "“Bhikkhus, possessing three factors, a shopkeeper is capable of acquiring wealth not yet acquired and of increasing wealth already acquired. What three? Here, a shopkeeper diligently applies himself to his work in the morning, in the middle of the day, and in the evening. Possessing these three factors, a shopkeeper is capable of acquiring wealth not yet acquired and of increasing wealth already acquired."),
    ("Evameva kho, bhikkhave, tīhi dhammehi samannāgato bhikkhu bhabbo anadhigataṃ vā kusalaṃ dhammaṃ adhigantuṃ, adhigataṃ vā kusalaṃ dhammaṃ phātiṃ kātuṃ. Katamehi tīhi? Idha, bhikkhave, bhikkhu pubbaṇha-samayaṃ sakkaccaṃ samādhi-nimittaṃ adhiṭṭhāti, majjhaṇhika-samayaṃ … pe … sāyaṇha-samayaṃ sakkaccaṃ samādhi-nimittaṃ adhiṭṭhāti. Imehi kho, bhikkhave, tīhi dhammehi samannāgato bhikkhu bhabbo anadhigataṃ vā kusalaṃ dhammaṃ adhigantuṃ, adhigataṃ vā kusalaṃ dhammaṃ phātiṃ kātun’ti.",
     "“So too, possessing three factors, a bhikkhu is capable of achieving a wholesome state not yet attained and of increasing a wholesome state already attained. What three? Here, a bhikkhu diligently applies himself to an object of concentration in the morning, in the middle of the day, and in the evening. Possessing these three factors, a bhikkhu is capable of achieving a wholesome state not yet attained and of increasing a wholesome state already attained.”"),
]

# ---------------------------------------------------------------- 2.1.3
P213 = [
    ("… Evameva kho, bhikkhave, appakā te sattā ye manussesu paccājāyanti; atha kho ete’va sattā bahutarā ye aññatra manussehi paccājāyanti.",
     "“… so too those beings are few who are reborn among human beings; more numerous are those beings who have been reborn elsewhere than among human beings.”"),
    ("… Evameva kho, bhikkhave, appakā te sattā ye majjhimesu janapadesu paccājāyanti; atha kho ete’va sattā bahutarā ye paccantimesu janapadesu paccājāyanti …",
     "“… so too those beings are few who are reborn in the middle provinces; more numerous are those who have been reborn in the outlying provinces …”"),
    ("… Evameva kho, bhikkhave, appakā te sattā ye paññavanto, ajaḷā, aneḷa-mūgā, paṭibalā subhāsita-dubbhāsitassa atthamaññātuṃ; atha kho ete’va sattā bahutarā ye duppaññā jaḷā eḷa-mūgā na paṭibalā subhāsita-dubbhāsitassa atthamaññātuṃ.",
     "“… so too those beings are few who are wise, intelligent, astute, able to understand the meaning of what has been well stated and badly stated; more numerous are those who are unwise, stupid, obtuse, unable to understand the meaning of what has been well stated and badly stated.”"),
    ("… Evameva kho, bhikkhave, appakā te sattā ye ariyena paññā-cakkhunā samannāgatā; atha kho ete’va sattā bahutarā ye avijjā-gatā sammūḷhā.",
     "“… so too those beings are few who are endowed with the noble eye of wisdom; more numerous are those beings who are confused and immersed in ignorance.”"),
    ("… Evameva kho, bhikkhave, appakā te sattā ye labhanti tathāgataṃ dassanāya; atha kho ete’va sattā bahutarā ye na labhanti tathāgataṃ dassanāya.",
     "“… so too those beings are few who get to see the Tathāgata; more numerous are those beings who do not get to see him.”"),
    ("… Evameva kho, bhikkhave, appakā te sattā ye labhanti tathāgata-ppaveditaṃ dhamma-vinayaṃ savanāya; atha kho ete’va sattā bahutarā ye na labhanti tathāgata-ppaveditaṃ dhamma-vinayaṃ savanāya.",
     "“… so too those beings are few who get to hear the Dhamma and discipline expounded by the Tathāgata; more numerous are those who do not get to hear it.”"),
]

# ---------------------------------------------------------------- 2.2.1
def kamma_para(root, neg):
    a = "a" if neg else ""
    R = (a + root)
    good = neg
    q = ("kusalaṃ", "anavajjaṃ", "sukha-vipākaṃ", "kamma-nirodhāya", "kamma-samudayāya") if good else \
        ("akusalaṃ", "sāvajjaṃ", "dukkha-vipākaṃ", "kamma-samudayāya", "kamma-nirodhāya")
    return (f"Yaṃ, bhikkhave, {R}-pakataṃ kammaṃ {R}-jaṃ {R}-nidānaṃ {R}-samudayaṃ, taṃ kammaṃ {q[0]}, taṃ kammaṃ {q[1]}, "
            f"taṃ kammaṃ {q[2]}, taṃ kammaṃ {q[3]} saṃvattati; na taṃ kammaṃ {q[4]} saṃvattati.")

EN_ROOT = {"lobha": "greed", "dosa": "hatred", "moha": "delusion"}
def kamma_en(root, neg, n):
    w = ("non-" if neg else "") + EN_ROOT[root]
    if neg:
        return (f"({n}) “Any kamma fashioned by {w}, born of {w}, caused by {w}, originating from {w}, is wholesome and blameless "
                f"and results in happiness. That kamma leads to the cessation of kamma, not to the origination of kamma.")
    return (f"({n}) “Any kamma fashioned by {w}, born of {w}, caused by {w}, originating from {w}, is unwholesome and blameworthy "
            f"and results in suffering. That kamma leads to the origination of kamma, not to the cessation of kamma.")

P221 = [
    ("Tīṇi’māni, bhikkhave, nidānāni kammānaṃ samudayāya. Katamāni tīṇi? Lobho nidānaṃ kammānaṃ samudayāya, doso nidānaṃ kammānaṃ samudayāya, moho nidānaṃ kammānaṃ samudayāya.",
     "“Monks, there are these three causes for the origination of kamma. What three? Greed is a cause for the origination of kamma; hatred is a cause for the origination of kamma; delusion is a cause for the origination of kamma."),
] + [(kamma_para(r, False), kamma_en(r, False, i + 1)) for i, r in enumerate(["lobha", "dosa", "moha"])] + [
    ("Imāni kho, bhikkhave, tīṇi nidānāni kammānaṃ samudayāya.",
     "“These are the three causes for the origination of kamma."),
    ("Tīṇi’māni, bhikkhave, nidānāni kammānaṃ samudayāya. Katamāni tīṇi? Alobho nidānaṃ kammānaṃ samudayāya, adoso nidānaṃ kammānaṃ samudayāya, amoho nidānaṃ kammānaṃ samudayāya.",
     "“There are, monks, these three [other] causes for the origination of kamma. What three? Non-greed is a cause for the origination of kamma; non-hatred is a cause for the origination of kamma; non-delusion is a cause for the origination of kamma."),
] + [(kamma_para(r, True), kamma_en(r, True, i + 1)) for i, r in enumerate(["lobha", "dosa", "moha"])] + [
    ("Imāni kho, bhikkhave, tīṇi nidānāni kammānaṃ samudayāyā’ti.",
     "“These are the three [other] causes for the origination of kamma.”"),
]

# ---------------------------------------------------------------- 2.2.2
P222 = [
    ("Pañcahi, bhikkhave, dhammehi samannāgato bhikkhu cavati, nappatiṭṭhāti saddhamme. Katamehi pañcahi? Assaddho, bhikkhave, bhikkhu cavati, nappatiṭṭhāti saddhamme. Ahiriko, bhikkhave, bhikkhu cavati, nappatiṭṭhāti saddhamme. Anottappī, bhikkhave, bhikkhu cavati, nappatiṭṭhāti saddhamme. Kusīto, bhikkhave, bhikkhu cavati, nappatiṭṭhāti saddhamme. Duppañño, bhikkhave, bhikkhu cavati, nappatiṭṭhāti saddhamme. Imehi kho, bhikkhave, pañcahi dhammehi samannāgato bhikkhu cavati, nappatiṭṭhāti saddhamme.",
     "“Bhikkhus, possessing five qualities a bhikkhu falls away and is not established in the good Dhamma. What five? (1) A bhikkhu devoid of faith falls away and is not established in the good Dhamma. (2) A morally shameless bhikkhu … (3) A morally reckless bhikkhu … (4) A lazy bhikkhu … (5) An unwise bhikkhu falls away and is not established in the good Dhamma. Possessing these five qualities, a bhikkhu falls away and is not established in the good Dhamma."),
    ("Pañcahi, bhikkhave, dhammehi samannāgato bhikkhu na cavati, patiṭṭhāti saddhamme. Katamehi pañcahi? Saddho, bhikkhave, bhikkhu na cavati, patiṭṭhāti saddhamme. Hirimā, bhikkhave, bhikkhu na cavati, patiṭṭhāti saddhamme. Ottappī, bhikkhave, bhikkhu na cavati, patiṭṭhāti saddhamme. Akusīto, bhikkhave, bhikkhu na cavati, patiṭṭhāti saddhamme. Paññavā, bhikkhave, bhikkhu na cavati, patiṭṭhāti saddhamme. Imehi kho, bhikkhave, pañcahi dhammehi samannāgato bhikkhu na cavati, patiṭṭhāti saddhamme.",
     "“Bhikkhus, possessing five [other] qualities a bhikkhu does not fall away but is established in the good Dhamma. What five? (1) A bhikkhu endowed with faith does not fall away but is established in the good Dhamma. (2) A bhikkhu who has a sense of moral shame … (3) A bhikkhu who has moral dread … (4) An energetic bhikkhu … (5) A wise bhikkhu does not fall away but is established in the good Dhamma. Possessing these five qualities, a bhikkhu does not fall away but is established in the good Dhamma.”"),
]

# ---------------------------------------------------------------- 3.1.1 (Milindapañha, two passages)
P311 = [
    ("“Bhante Nāgasena, atthi koci satto yo imamhā kāyā aññaṃ kāyaṃ saṅkamatī’”ti?\n“Na hi, mahārājā’”ti.\n“Yadi, bhante Nāgasena, imamhā kāyā aññaṃ kāyaṃ saṅkamanto natthi, nanu mutto bhavissati pāpakehi kammehī’”ti?\n“Āma, mahārāja. Yadi na paṭisandaheyya, mutto bhavissati pāpakehi kammehi; yasmā ca kho, mahārāja, paṭisandahati, tasmā na parimutto pāpakehi kammehī’”ti.",
     "“Is there any being, Bhante Nāgasena, who transmigrates from this body to another?”\n“No, there is not.”\n“But if, Bhante Nāgasena, there is no being who transmigrates from this body to another, would one not get free from evil deeds?”\n“Yes, if one were not reborn, one would get free from evil deeds. But since one is reborn, one is not freed from evil deeds.”"),
    ("“Bhante Nāgasena, na ca saṅkamati, paṭisandahati cā’”ti?\n“Āma, mahārāja, na ca saṅkamati, paṭisandahati cā’”ti.\n“Kathaṃ, bhante Nāgasena, na ca saṅkamati, paṭisandahati ca? Opammaṃ karohī’”ti.\n“Yathā, mahārāja, kocideva puriso padīpato padīpaṃ padīpeyya, kinnu kho so, mahārāja, padīpo padīpamhā saṅkamanto’”ti?\n“Na hi, bhante’”ti.\n“Evameva kho, mahārāja, na ca saṅkamati, paṭisandahati cā’”ti.",
     "“Bhante Nāgasena, is it that one does not transmigrate but one is reborn?”\n“Yes, great king, one does not transmigrate but one is reborn.”\n“But how is it, Bhante Nāgasena, that one does not transmigrate yet one is reborn? Give me an illustration.”\n“Suppose, great king, a man would light a lamp from another lamp, can it be said that the lamp [light] transmigrates from the [first] lamp?”\n“Certainly not.”\n“Just so, great king, one does not transmigrate but one is reborn.”"),
]

# ---------------------------------------------------------------- 3.1.2
P312 = [
    ("“Taṃ kiṃ maññatha, Sāḷhā, atthi lobho’”ti?\n“Evaṃ, bhante.”\n“Abhijjhā’ti kho ahaṃ, Sāḷhā, etamatthaṃ vadāmi. Luddho kho ayaṃ, Sāḷhā, abhijjhālu pāṇaṃ pi hanati, adinnaṃ pi ādiyati, para-dāraṃ pi gacchati, musā pi bhaṇati … yaṃ’sa hoti dīgha-rattaṃ ahitāya dukkhāyā’”ti.\n“Evaṃ, bhante.”",
     "“What do you think, Sāḷha, is there greed?”\n“Yes, bhante.”\n“I say its meaning is longing. This greedy person, full of longing, destroys life, takes what is not given, goes to another’s wife, and speaks falsely, which will lead to his harm and suffering for a long time.”\n“Yes, bhante.”"),
    ("“Taṃ kiṃ maññatha, Sāḷhā, atthi doso’”ti?\n“Evaṃ, bhante.”\n“Byāpādo’ti kho ahaṃ, Sāḷhā, etamatthaṃ vadāmi. Duṭṭho kho ayaṃ, Sāḷhā, byāpanna-citto pāṇaṃ pi hanati, adinnaṃ pi ādiyati, para-dāraṃ pi gacchati, musā pi bhaṇati … yaṃ’sa hoti dīgha-rattaṃ ahitāya dukkhāyā’”ti.\n“Evaṃ, bhante.”",
     "“What do you think, Sāḷha, is there hatred?”\n“Yes, bhante.”\n“I say its meaning is ill will. This hating one, with a mind of ill will, destroys life, takes what is not given, goes to another’s wife, and speaks falsely, which will lead to his harm and suffering for a long time.”\n“Yes, bhante.”"),
    ("“Taṃ kiṃ maññatha, Sāḷhā, atthi moho’”ti?\n“Evaṃ, bhante.”\n“Avijjā’ti kho ahaṃ, Sāḷhā, etamatthaṃ vadāmi. Mūḷho kho ayaṃ, Sāḷhā, avijjā-gato pāṇaṃ pi hanati, adinnaṃ pi ādiyati, para-dāraṃ pi gacchati, musā pi bhaṇati … yaṃ’sa hoti dīgha-rattaṃ ahitāya dukkhāyā’”ti.\n“Evaṃ, bhante.”",
     "“What do you think, Sāḷha, is there delusion?”\n“Yes, bhante.”\n“I say its meaning is ignorance. A deluded one, immersed in ignorance, destroys life, takes what is not given, goes to another’s wife, and speaks falsely, which will lead to his harm and suffering for a long time.”\n“Yes, bhante.”"),
    ("“Taṃ kiṃ maññatha, Sāḷhā, ime dhammā kusalā vā akusalā vā’”ti?\n“Akusalā, bhante.”\n“Sāvajjā vā anavajjā vā’”ti?\n“Sāvajjā, bhante.”\n“Viññu-garahitā vā viññu-ppasatthā vā’”ti?\n“Viññu-garahitā, bhante.”",
     "“What do you think, Sāḷha? Are these things wholesome or unwholesome?”\n“Unwholesome, bhante.”\n“Blameworthy or blameless?”\n“Blameworthy, bhante.”\n“Censured by the wise or praised by the wise?”\n“Censured by the wise, bhante.”"),
]

# ---------------------------------------------------------------- 3.1.3
P313 = [
    ("“Akusalaṃ, bhikkhave, pajahatha. Sakkā, bhikkhave, akusalaṃ pajahituṃ … Yasmā ca kho, bhikkhave, sakkā akusalaṃ pajahituṃ, tasm’āhaṃ evaṃ vadāmi: ‘akusalaṃ, bhikkhave, pajahathā’ti. Akusalaṃ ca h’idaṃ, bhikkhave, pahīnaṃ ahitāya dukkhāya saṃvatteyya, n’āhaṃ evaṃ vadeyyaṃ: ‘akusalaṃ, bhikkhave, pajahathā’ti. Yasmā ca kho, bhikkhave, akusalaṃ pahīnaṃ hitāya sukhāya saṃvattati, tasm’āhaṃ evaṃ vadāmi: ‘akusalaṃ, bhikkhave, pajahathā’ti.",
     "“Monks, abandon the unwholesome! It is possible to abandon the unwholesome … But because it is possible to abandon the unwholesome, therefore I say: ‘Monks, abandon the unwholesome!’ If this abandoning of the unwholesome led to harm and suffering, I would not say thus: ‘Monks, abandon the unwholesome!’ But because the abandoning of the unwholesome leads to welfare and happiness, therefore I say: ‘Monks, abandon the unwholesome!’"),
    ("Kusalaṃ, bhikkhave, bhāvetha. Sakkā, bhikkhave, kusalaṃ bhāvetuṃ … Yasmā ca kho, bhikkhave, sakkā kusalaṃ bhāvetuṃ, tasm’āhaṃ evaṃ vadāmi: ‘kusalaṃ, bhikkhave, bhāvethā’ti. Kusalaṃ ca h’idaṃ, bhikkhave, bhāvitaṃ ahitāya dukkhāya saṃvatteyya, n’āhaṃ evaṃ vadeyyaṃ: ‘kusalaṃ, bhikkhave, bhāvethā’ti. Yasmā ca kho, bhikkhave, kusalaṃ bhāvitaṃ hitāya sukhāya saṃvattati, tasm’āhaṃ evaṃ vadāmi: ‘kusalaṃ, bhikkhave, bhāvethā’”ti.",
     "“Monks, develop the wholesome! It is possible to develop the wholesome … But because it is possible to develop the wholesome, therefore I say: ‘Monks, develop the wholesome!’ If this developing of the wholesome led to harm and suffering, I would not say thus: ‘Monks, develop the wholesome!’ But because the developing of the wholesome leads to welfare and happiness, therefore I say: ‘Monks, develop the wholesome!’”"),
]

# ---------------------------------------------------------------- 3.2.1
P321 = [
    ("“Taṃ kiṃ maññatha, Sāḷhā, atthi alobho’”ti?\n“Evaṃ, bhante.”\n“Anabhijjhā’ti kho ahaṃ, Sāḷhā, etamatthaṃ vadāmi. Aluddho kho ayaṃ, Sāḷhā, anabhijjhālu n’eva pāṇaṃ hanati, na adinnaṃ ādiyati, na para-dāraṃ gacchati, na musā bhaṇati, paraṃ pi na tathattāya samādapeti, yaṃ’sa hoti dīgha-rattaṃ hitāya sukhāyā’”ti.\n“Evaṃ, bhante.”",
     "“What do you think, Sāḷha, is there non-greed?”\n“Yes, bhante.”\n“I say the meaning of this is absence of longing. One without greed, without longing, does not destroy life, take what is not given, go to another’s wife, or speak falsely; nor does he encourage others to do likewise, which will lead to his welfare and happiness for a long time.”\n“Yes, bhante.”"),
    ("“Taṃ kiṃ maññatha, Sāḷhā, atthi adoso’”ti?\n“Evaṃ, bhante.”\n“Abyāpādo’ti kho ahaṃ, Sāḷhā, etamatthaṃ vadāmi. Aduṭṭho kho ayaṃ, Sāḷhā, abyāpanna-citto n’eva pāṇaṃ hanati, na adinnaṃ ādiyati, na para-dāraṃ gacchati, na musā bhaṇati, paraṃ pi na tathattāya samādapeti, yaṃ’sa hoti dīgha-rattaṃ hitāya sukhāyā’”ti.\n“Evaṃ, bhante.”",
     "“What do you think, Sāḷha, is there non-hatred?”\n“Yes, bhante.”\n“I say the meaning of this is good will. A non-hater, with a mind of good will, does not destroy life, take what is not given, go to another’s wife, or speak falsely; nor does he encourage others to do likewise, which will lead to his welfare and happiness for a long time.”\n“Yes, bhante.”"),
    ("“Taṃ kiṃ maññatha, Sāḷhā, atthi amoho’”ti?\n“Evaṃ, bhante.”\n“Vijjā’ti kho ahaṃ, Sāḷhā, etamatthaṃ vadāmi. Amūḷho kho ayaṃ, Sāḷhā, vijjā-gato n’eva pāṇaṃ hanati, na adinnaṃ ādiyati, na para-dāraṃ gacchati, na musā bhaṇati, paraṃ pi na tathattāya samādapeti, yaṃ’sa hoti dīgha-rattaṃ hitāya sukhāyā’”ti.\n“Evaṃ, bhante.”",
     "“What do you think, Sāḷha, is there non-delusion?”\n“Yes, bhante.”\n“I say the meaning of this is true knowledge. An undeluded one, who has arrived at true knowledge, does not destroy life, take what is not given, go to another’s wife, or speak falsely; nor does he encourage others to do likewise, which will lead to his welfare and happiness for a long time.”\n“Yes, bhante.”"),
    ("“Taṃ kiṃ maññatha, Sāḷhā, ime dhammā kusalā vā akusalā vā’”ti?\n“Kusalā, bhante.”\n“Sāvajjā vā anavajjā vā’”ti?\n“Anavajjā, bhante.”\n“Viññu-garahitā vā viññu-ppasatthā vā’”ti?\n“Viññu-ppasatthā, bhante.”\n“Samattā samādinnā hitāya sukhāya saṃvattanti, no vā?”\n“Samattā, bhante, samādinnā hitāya sukhāya saṃvattantī’”ti.",
     "“What do you think, Sāḷha? Are these things wholesome or unwholesome?”\n“Wholesome, bhante.”\n“Blameworthy or blameless?”\n“Blameless, bhante.”\n“Censured by the wise or praised by the wise?”\n“Praised by the wise, bhante.”\n“Accepted and undertaken, do they lead to welfare and happiness or not?”\n“Accepted and undertaken, bhante, these things lead to welfare and happiness.”"),
    ("“Yadā tumhe, Sāḷhā, attanā’va jāneyyātha: ‘ime dhammā kusalā, ime dhammā anavajjā, ime dhammā viññu-ppasatthā, ime dhammā samattā samādinnā dīgha-rattaṃ hitāya sukhāya saṃvattantī’ti, atha tumhe, Sāḷhā, upasampajja vihareyyāthā’”ti.",
     "“When, Sāḷha, you know for yourselves: ‘These things are wholesome; these things are blameless; these things are praised by the wise; these things, if accepted and undertaken, lead to welfare and happiness for a long time,’ then you should live in accordance with them.”"),
]

# ---------------------------------------------------------------- 3.2.2
MIND = [
    ("abhāvitaṃ akammaniyaṃ hoti", "that when undeveloped is so unwieldy as the mind. An undeveloped mind is unwieldy."),
    ("bhāvitaṃ kammaniyaṃ hoti", "that when developed is so wieldy as the mind. A developed mind is wieldy."),
    ("abhāvitaṃ mahato anatthāya saṃvattati", "that when undeveloped leads to such great harm as the mind. An undeveloped mind leads to great harm."),
    ("bhāvitaṃ mahato atthāya saṃvattati", "that when developed leads to such great good as the mind. A developed mind leads to great good."),
    ("abhāvitaṃ apātu-bhūtaṃ mahato anatthāya saṃvattati", "that, when undeveloped and unmanifested, leads to such great harm as the mind. The mind, when undeveloped and unmanifested, leads to great harm."),
    ("bhāvitaṃ pātu-bhūtaṃ mahato atthāya saṃvattati", "that, when developed and manifested, leads to such great good as the mind. The mind, when developed and manifested, leads to great good."),
    ("abhāvitaṃ abahulī-kataṃ mahato anatthāya saṃvattati", "that, when undeveloped and uncultivated, leads to such great harm as the mind. The mind, when undeveloped and uncultivated, leads to great harm."),
    ("bhāvitaṃ bahulī-kataṃ mahato atthāya saṃvattati", "that, when developed and cultivated, leads to such great good as the mind. The mind, when developed and cultivated, leads to great good."),
    ("abhāvitaṃ abahulī-kataṃ dukkh’ādhivāhaṃ hoti", "that, when undeveloped and uncultivated, brings such suffering as the mind. The mind, when undeveloped and uncultivated, brings suffering."),
    ("bhāvitaṃ bahulī-kataṃ sukh’ādhivāhaṃ hoti", "that, when developed and cultivated, brings such happiness as the mind. The mind, when developed and cultivated, brings happiness."),
]
def _final(clause):
    head, last = clause.rsplit(" ", 1)
    return head + " " + last[:-1] + "ī’ti"   # hoti → hotī’ti, saṃvattati → saṃvattatī’ti
P322 = [(f"“N’āhaṃ, bhikkhave, aññaṃ eka-dhammaṃ pi samanupassāmi yaṃ evaṃ {c} yathayidaṃ, bhikkhave, cittaṃ. Cittaṃ, bhikkhave, {_final(c)}.”",
         f"“Bhikkhus, I do not see even one other thing {e}”") for c, e in MIND]

# ---------------------------------------------------------------- 3.2.3
P323 = [
    ("“Idaṃ kho pana, bhikkhave, dukkhaṃ ariya-saccaṃ: jāti pi dukkhā, jarā pi dukkhā, vyādhi pi dukkhā, maraṇaṃ pi dukkhaṃ, appiyehi sampayogo dukkho, piyehi vippayogo dukkho, yaṃ p’icchaṃ na labhati taṃ pi dukkhaṃ, saṅkhittena pañc’upādāna-kkhandhā pi dukkhā.”",
     "“Now this, monks, is the noble truth of suffering: birth is suffering, aging is suffering, illness is suffering, death is suffering; union with what is displeasing is suffering; separation from what is pleasing is suffering; not to get what one wants is suffering; in brief, the five aggregates subject to clinging are suffering.”"),
]

# ---------------------------------------------------------------- 3.2.4
P324 = [
    ("“Bhante Nāgasena, kiṃ-lakkhaṇaṃ viññāṇan’”ti?\n“Vijānana-lakkhaṇaṃ, mahārāja, viññāṇan’”ti.\n“Opammaṃ karohī’”ti.",
     "“Bhante Nāgasena, what is the characteristic mark of consciousness?”\n“Consciousness has knowing as its characteristic mark, great king.”\n“Give me an illustration.”"),
    ("“Yathā, mahārāja, nagara-guttiko majjhe nagare siṅghāṭake nisinno passeyya puratthima-disato purisaṃ āgacchantaṃ, passeyya dakkhiṇa-disato purisaṃ āgacchantaṃ, passeyya pacchima-disato purisaṃ āgacchantaṃ, passeyya uttara-disato purisaṃ āgacchantaṃ, evameva kho, mahārāja, yañ ca puriso cakkhunā rūpaṃ passati taṃ viññāṇena vijānāti, yañ ca sotena saddaṃ suṇāti taṃ viññāṇena vijānāti, yañ ca ghānena gandhaṃ ghāyati taṃ viññāṇena vijānāti, yañ ca jivhāya rasaṃ sāyati taṃ viññāṇena vijānāti, yañ ca kāyena phoṭṭhabbaṃ phusati taṃ viññāṇena vijānāti, yañ ca manasā dhammaṃ vijānāti taṃ viññāṇena vijānāti.",
     "“As, great king, a city-watchman, sitting in the middle, in the city square, would see a man coming from the eastern direction, would see a man coming from the southern direction, would see a man coming from the western direction, would see a man coming from the northern direction; so, great king, when a man sees a form with the eye, he knows it by consciousness; when he hears a sound with the ear, he knows it by consciousness; when he smells an odour with the nose, he knows it by consciousness; when he tastes a taste with the tongue, he knows it by consciousness; when he feels a touch with the body, he knows it by consciousness; and when he knows a mental object with the mind, he knows it by consciousness."),
    ("Evaṃ kho, mahārāja, vijānana-lakkhaṇaṃ viññāṇan’”ti.\n“Kallo’si, bhante Nāgasenā’”ti.",
     "“It is in this way that consciousness has knowing as its characteristic mark, great king.”\n“You are clever, Bhante Nāgasena.”"),
]

META = [
    ("ncrp-1-2-1", "AN 1.114–117, 129", "Dutiyapamādādivagga", "Heedlessness", "NCRP Lesson 1 · Further reading 1", AN, P121),
    ("ncrp-1-2-2", "AN 1.1–10", "Cittapariyādānavagga", "Obsession of the Mind", "NCRP Lesson 1 · Further reading 2", AN, P122),
    ("ncrp-2-1-1", "Dhp 182, 183, 5", "Dhammapada", "Three Verses", "NCRP Lesson 2 · Initial reading 1", DHP, P211),
    ("ncrp-2-1-2", "AN 3.19", "Paṭhamapāpaṇikasutta", "The Shopkeeper", "NCRP Lesson 2 · Initial reading 2", AN, P212),
    ("ncrp-2-1-3", "AN 1.333–339", "Jambudīpapeyyāla", "Few and Many", "NCRP Lesson 2 · Initial reading 3", AN, P213),
    ("ncrp-2-2-1", "AN 3.111", "Paṭhamanidānasutta", "Causes", "NCRP Lesson 2 · Further reading 1", OTHER + " Translation adapted from published versions.", P221),
    ("ncrp-2-2-2", "AN 5.8", "Cavanasutta", "Falling Away", "NCRP Lesson 2 · Further reading 2", AN, P222),
    ("ncrp-3-1-1", "Mil 3.5.5–7", "Milindapañha", "Not Transmigrating, yet Reborn", "NCRP Lesson 3 · Initial reading 1", OTHER, P311),
    ("ncrp-3-1-2", "AN 3.66", "Sāḷhasutta", "Sāḷha (1)", "NCRP Lesson 3 · Initial reading 2", AN, P312),
    ("ncrp-3-1-3", "AN 2.19", "Adhikaraṇavagga", "Abandon the Unwholesome", "NCRP Lesson 3 · Initial reading 3", OTHER, P313),
    ("ncrp-3-2-1", "AN 3.66", "Sāḷhasutta", "Sāḷha (2)", "NCRP Lesson 3 · Further reading 1", AN, P321),
    ("ncrp-3-2-2", "AN 1.21–30", "Akammaniyavagga", "Unwieldy", "NCRP Lesson 3 · Further reading 2", AN, P322),
    ("ncrp-3-2-3", "DN 22", "Mahāsatipaṭṭhānasutta", "The Noble Truth of Suffering", "NCRP Lesson 3 · Further reading 3", OTHER + " “Illness is suffering” added to match the book.", P323),
    ("ncrp-3-2-4", "Mil 2.3.12", "Milindapañha", "The Mark of Consciousness", "NCRP Lesson 3 · Further reading 4", OTHER, P324),
]
