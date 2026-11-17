# Pali (as in the printed book, checked against the scan, written with Mor's conventions) and
# English (natural translations from the course translation document) for NCRP Lessons 4-5.
# Word analyses: ncrp_l4_l5_words.py. Choices are listed in NOTES at the bottom.

AN = ("English: course exercise book, after Bhikkhu Bodhi, The Numerical Discourses of the Buddha "
      "(Wisdom Publications, 2012).")
SN = ("English: course exercise book, after Bhikkhu Bodhi, The Connected Discourses of the Buddha "
      "(Wisdom Publications, 2000).")
MN = ("English: course exercise book, after Bhikkhu Bodhi, The Middle Length Discourses of the Buddha "
      "(Wisdom Publications, 1995).")
DHP = "English: course exercise book, after Ācariya Buddharakkhita’s translation of the Dhammapada."
KHP = "English: course exercise book, after Piyadassi Thera’s translation (accesstoinsight.org)."
MIL = "English: course exercise book, after Bhikkhu Pesala, The Debate of King Milinda (2001)."


def verse(*lines):
    """verse lines: a comma at the end of each line, a full stop (or ?) only on the last"""
    out = []
    for i, ln in enumerate(lines):
        ln = ln.rstrip(" ,.;")
        if i < len(lines) - 1:
            out.append(ln + ",")
        else:
            out.append(ln if ln.endswith(("?", "”", "’")) else ln + ".")
    return "\n".join(out)


# ---------------------------------------------------------------- 4.1.1
def _upak(n, what, ref_en):
    return (f"Santi, bhikkhave, eke samaṇa-brāhmaṇā {what}. Ayaṃ, bhikkhave, {n} samaṇa-brāhmaṇānaṃ upakkileso, yena upakkilesena upakkiliṭṭhā eke samaṇa-brāhmaṇā na tapanti, na bhāsanti, na virocanti.",
            ref_en)

P411 = [
    ("Evameva kho, bhikkhave, cattāro’me samaṇa-brāhmaṇānaṃ upakkilesā, yehi upakkilesehi upakkiliṭṭhā eke samaṇa-brāhmaṇā na tapanti, na bhāsanti, na virocanti. Katame cattāro?",
     "“So too, bhikkhus, there are these four defilements of ascetics and brahmins, defiled by which some ascetics and brahmins do not shine, blaze, and radiate. What four?"),
    _upak("paṭhamo", "suraṃ pivanti merayaṃ, surā-meraya-pānā appaṭiviratā",
          "(1) “There are, bhikkhus, some ascetics and brahmins who drink liquor and wine and do not refrain from drinking liquor and wine. This is the first defilement of ascetics and brahmins, defiled by which some ascetics and brahmins do not shine, blaze, and radiate."),
    _upak("dutiyo", "methunaṃ dhammaṃ paṭisevanti, methunasmā dhammā appaṭiviratā",
          "(2) “There are some ascetics and brahmins who indulge in sexual intercourse and do not refrain from sexual intercourse. This is the second defilement of ascetics and brahmins, defiled by which some ascetics and brahmins do not shine, blaze, and radiate."),
    _upak("tatiyo", "jāta-rūpa-rajataṃ sādiyanti, jāta-rūpa-rajata-paṭiggahaṇā appaṭiviratā",
          "(3) “There are some ascetics and brahmins who accept gold and silver and do not refrain from receiving gold and silver. This is the third defilement of ascetics and brahmins, defiled by which some ascetics and brahmins do not shine, blaze, and radiate."),
    _upak("catuttho", "micchā-jīvena jīvanti, micchā-jīvā appaṭiviratā",
          "(4) “There are some ascetics and brahmins who earn their living by wrong livelihood and do not refrain from wrong livelihood. This is the fourth defilement of ascetics and brahmins, defiled by which some ascetics and brahmins do not shine, blaze, and radiate."),
    ("Ime kho, bhikkhave, cattāro samaṇa-brāhmaṇānaṃ upakkilesā, yehi upakkilesehi upakkiliṭṭhā eke samaṇa-brāhmaṇā na tapanti, na bhāsanti, na virocantī’ti.",
     "“These, bhikkhus, are the four defilements of ascetics and brahmins, defiled by which some ascetics and brahmins do not shine, blaze, and radiate.”"),
    (verse("Suraṃ pivanti merayaṃ", "paṭisevanti methunaṃ", "rajataṃ jāta-rūpaṃ ca", "sādiyanti aviddasū",
           "micchā-jīvena jīvanti", "eke samaṇa-brāhmaṇā"),
     "They drink liquor and wines,\nindulge in sex;\nthe ignorant accept\nsilver and gold.\nSome ascetics and brahmins\nlive by wrong livelihood."),
]

# ---------------------------------------------------------------- 4.1.2
def _bhagini(x):
    return f"{x}ṃ datvā {x.lower()}ssa bhāginī hoti dibbassa vā mānusassa vā."

P412 = [
    ("Bhojanaṃ, Suppavāse, dentī ariya-sāvikā paṭiggāhakānaṃ cattāri ṭhānāni deti. Katamāni cattāri? Āyuṃ deti, vaṇṇaṃ deti, sukhaṃ deti, balaṃ deti.",
     "“Suppavāsā, a female noble disciple, giving food, gives the recipients four things. What four? She gives life, she gives beauty, she gives happiness, she gives strength."),
    ("Āyuṃ kho pana datvā āyussa bhāginī hoti dibbassa vā mānusassa vā. " + " ".join(_bhagini(x) for x in ("Vaṇṇa", "Sukha", "Bala")),
     "(1) Having given life, she is a partaker of life, whether celestial or human. (2) Having given beauty, she is a partaker of beauty, whether celestial or human. (3) Having given happiness, she is a partaker of happiness, whether celestial or human. (4) Having given strength, she is a partaker of strength, whether celestial or human."),
    ("Bhojanaṃ, Suppavāse, dentī ariya-sāvikā paṭiggāhakānaṃ imāni cattāri ṭhānāni detī’ti.",
     "Suppavāsā, a female noble disciple, giving food, gives the recipients these four things.”"),
]

# ---------------------------------------------------------------- 4.1.3
def _piya(src, en, n):
    return (verse(f"{src} jāyatī soko", f"{src} jāyatī bhayaṃ", f"{src} vippamuttassa", "n’atthi soko, kuto bhayaṃ?"),
            f"From {en} arises sorrow,\nfrom {en} arises fear.\nFor one who is wholly free from {en}\nthere is no sorrow, whence then fear?\n(Dhp {n})")

P413 = [
    (verse("Na bhaje pāpake mitte", "na bhaje puris’ādhame", "bhajetha mitte kalyāṇe", "bhajetha puris’uttame"),
     "One should not associate with evil companions;\none should not associate with low persons.\nAssociate with good friends;\nassociate with the supreme persons.\n(Dhp 78)"),
    (verse("Sabbe tasanti daṇḍassa", "sabbe bhāyanti maccuno", "attānaṃ upamaṃ katvā", "na haneyya na ghātaye"),
     "All tremble at violence;\nall are afraid of death.\nHaving made an example of oneself,\none should not kill or cause [others] to kill.\n(Dhp 129)"),
    (verse("Sabbe tasanti daṇḍassa", "sabbesaṃ jīvitaṃ piyaṃ", "attānaṃ upamaṃ katvā", "na haneyya na ghātaye"),
     "All tremble at violence;\nlife is dear to all.\nHaving made an example of oneself,\none should not kill or cause [others] to kill.\n(Dhp 130)"),
    (verse("Bahuṃ pi ce sahitaṃ bhāsamāno", "na takkaro hoti naro pamatto", "gopo’va gāvo gaṇayaṃ paresaṃ",
           "na bhāgavā sāmaññassa hoti"),
     "Even if one is reciting much scripture,\n[but] the heedless man is not one who acts upon it,\nlike a cowherd counting the cows of others,\nhe is not one who partakes of the spiritual life.\n(Dhp 19)"),
    (verse("Appaṃ pi ce sahitaṃ bhāsamāno", "dhammassa hoti anudhamma-cārī", "rāgañ ca dosañ ca pahāya mohaṃ",
           "sammappajāno suvimutta-citto", "anupādiyāno idha vā huraṃ vā", "sa bhāgavā sāmaññassa hoti"),
     "Even if one is reciting little scripture,\n[but] he is a practitioner of Dhamma in accordance with Dhamma,\nhaving abandoned lust and hate and delusion,\none of right understanding, well liberated in mind,\nnot clinging [to anything] here or beyond,\nhe is one who partakes of the spiritual life.\n(Dhp 20)"),
    _piya("Piyato", "endearment", 212),
    _piya("Pemato", "affection", 213),
    _piya("Ratiyā", "attachment", 214),
    _piya("Kāmato", "lust", 215),
    _piya("Taṇhāya", "craving", 216),
]

# ---------------------------------------------------------------- 4.2.1
P421 = [
    ("Dve’mā, bhikkhave, parisā. Katamā dve? Uttānā ca parisā gambhīrā ca parisā.",
     "“Bhikkhus, there are these two kinds of assemblies. What two? The shallow assembly and the deep assembly."),
    ("Katamā ca, bhikkhave, uttānā parisā? Idha, bhikkhave, yassaṃ parisāyaṃ bhikkhū uddhatā honti unnaḷā capalā mukharā vikiṇṇa-vācā … asampajānā asamāhitā vibbhanta-cittā pākat’indriyā. Ayaṃ vuccati, bhikkhave, uttānā parisā.",
     "“And what is the shallow assembly? Here, bhikkhus, the assembly in which the bhikkhus are restless, puffed up, vain, talkative, rambling in their talk … lacking in clear comprehension, unconcentrated, with wandering minds, with loose sense faculties – this is called the shallow assembly."),
    ("Katamā ca, bhikkhave, gambhīrā parisā? Idha, bhikkhave, yassaṃ parisāyaṃ bhikkhū anuddhatā honti anunnaḷā acapalā amukharā avikiṇṇa-vācā … sampajānā samāhitā ekagga-cittā saṃvut’indriyā. Ayaṃ vuccati, bhikkhave, gambhīrā parisā.",
     "“And what is the deep assembly? The assembly in which the bhikkhus are not restless, puffed up, vain, talkative, and rambling in their talk … are clearly comprehending, concentrated, with one-pointed minds, with restrained sense faculties – this is called the deep assembly."),
    ("Imā kho, bhikkhave, dve parisā. Etad-aggaṃ, bhikkhave, imāsaṃ dvinnaṃ parisānaṃ yadidaṃ gambhīrā parisā’ti.",
     "“These, bhikkhus, are the two kinds of assemblies. The foremost of these two kinds of assemblies, bhikkhus, is the deep assembly.”\n(AN 2.42)"),
    ("Dve’mā, bhikkhave, parisā. Katamā dve? Vaggā ca parisā samaggā ca parisā.",
     "“Bhikkhus, there are these two kinds of assemblies. What two? The divided assembly and the harmonious assembly."),
    ("Katamā ca, bhikkhave, vaggā parisā? Idha, bhikkhave, yassaṃ parisāyaṃ bhikkhū bhaṇḍana-jātā kalaha-jātā vivād’āpannā aññamaññaṃ mukha-sattīhi vitudantā viharanti. Ayaṃ vuccati, bhikkhave, vaggā parisā.",
     "“And what is the divided assembly? Here, bhikkhus, the assembly in which the bhikkhus dwell argumentative, quarrelsome, involved in disputes, stabbing each other with the knives of their mouths – this is called the divided assembly."),
    ("Katamā ca, bhikkhave, samaggā parisā? Idha, bhikkhave, yassaṃ parisāyaṃ bhikkhū samaggā sammodamānā avivadamānā khīr’odakī-bhūtā aññamaññaṃ piya-cakkhūhi sampassantā viharanti. Ayaṃ vuccati, bhikkhave, samaggā parisā. Imā kho, bhikkhave, dve parisā.",
     "“And what is the harmonious assembly? Here, bhikkhus, the assembly in which the bhikkhus dwell in concord, harmonizing, not disputing, [blending like] milk and water, viewing each other with eyes of affection – this is called the harmonious assembly. These, bhikkhus, are the two kinds of assemblies.”\n(AN 2.43)"),
    ("Dve’mā, bhikkhave, parisā. Katamā dve? Visamā ca parisā samā ca parisā.",
     "“Bhikkhus, there are these two kinds of assemblies. What two? The unrighteous assembly and the righteous assembly."),
    ("Katamā ca, bhikkhave, visamā parisā? Idha, bhikkhave, yassaṃ parisāyaṃ adhamma-kammāni pavattanti dhamma-kammāni nappavattanti, avinaya-kammāni pavattanti vinaya-kammāni nappavattanti, adhamma-kammāni dippanti dhamma-kammāni na dippanti, avinaya-kammāni dippanti vinaya-kammāni na dippanti. Ayaṃ vuccati, bhikkhave, visamā parisā.",
     "“And what is the unrighteous assembly? Here, in this assembly disciplinary acts contrary to the Dhamma are enacted and disciplinary acts in accordance with the Dhamma are not enacted; disciplinary acts contrary to the discipline are enacted and disciplinary acts in accordance with the discipline are not enacted. Disciplinary acts contrary to the Dhamma are explained and disciplinary acts in accordance with the Dhamma are not explained; disciplinary acts contrary to the discipline are explained and disciplinary acts in accordance with the discipline are not explained. This, bhikkhus, is called the unrighteous assembly."),
    ("Katamā ca, bhikkhave, samā parisā? Idha, bhikkhave, yassaṃ parisāyaṃ dhamma-kammāni pavattanti adhamma-kammāni nappavattanti, vinaya-kammāni pavattanti avinaya-kammāni nappavattanti, dhamma-kammāni dippanti adhamma-kammāni na dippanti, vinaya-kammāni dippanti avinaya-kammāni na dippanti. Ayaṃ vuccati, bhikkhave, samā parisā. Imā kho, bhikkhave, dve parisā.",
     "“And what is the righteous assembly? Here, in this assembly disciplinary acts that accord with the Dhamma are enacted and disciplinary acts contrary to the Dhamma are not enacted; disciplinary acts that accord with the discipline are enacted and disciplinary acts contrary to the discipline are not enacted. Disciplinary acts that accord with the Dhamma are explained and disciplinary acts contrary to the Dhamma are not explained; disciplinary acts that accord with the discipline are explained and disciplinary acts contrary to the discipline are not explained. This, bhikkhus, is called the righteous assembly. These, bhikkhus, are the two kinds of assemblies.”\n(AN 2.49)"),
]

# ---------------------------------------------------------------- 4.2.2
P422 = [
    (verse("Appamādo amata-padaṃ", "pamādo maccuno padaṃ", "appamattā na mīyanti", "ye pamattā yathā matā"),
     "Heedfulness is the path to the Deathless.\nHeedlessness is the path to death.\nThe heedful do not die.\nThe heedless are as if dead.\n(Dhp 21)"),
    (verse("Etaṃ visesato ñatvā", "appamādamhi paṇḍitā", "appamāde pamodanti", "ariyānaṃ gocare ratā"),
     "Clearly understanding this as a distinction,\nthe wise [remain] in heedfulness;\nthey exult in heedfulness,\ndelighted in the resort of the Noble Ones.\n(Dhp 22)"),
    (verse("Yathā pi rahado gambhīro", "vippasanno anāvilo", "evaṃ dhammāni sutvāna", "vippasīdanti paṇḍitā"),
     "Like a lake deep,\nclear and still,\nso, having heard the teachings,\nthe wise become clarified (purified).\n(Dhp 82)"),
    (verse("Selo yathā eka-ghano", "vātena na samīrati", "evaṃ nindā-pasaṃsāsu", "na samiñjanti paṇḍitā"),
     "Just as a mountain, one mass [of stone],\nis not shaken by the wind,\neven so amid blame and praises,\nthe wise are not agitated.\n(Dhp 81)"),
    (verse("Andha-bhūto ayaṃ loko", "tanuk’ettha vipassati", "sakunto jāla-mutto’va", "appo saggāya gacchati"),
     "Blind is this world;\nfew here see clearly.\nLike birds freed from the net,\nfew go to heaven.\n(Dhp 174)"),
    (verse("Udakaṃ hi nayanti nettikā", "usu-kārā namayanti tejanaṃ", "dāruṃ namayanti tacchakā", "attānaṃ damayanti paṇḍitā"),
     "Irrigators regulate the water,\narrow-makers straighten the arrow shaft,\ncarpenters bend the wood,\nthe wise tame themselves.\n(Dhp 80)"),
]

# ---------------------------------------------------------------- 4.2.3
SUKHA = [
    ("Gihi-sukhaṃ ca pabbajita-sukhaṃ ca", "pabbajita-sukhan’ti",
     "The happiness of a layperson and the happiness of one who has gone forth [into homelessness]", "the happiness of one who has gone forth", "AN 2.64"),
    ("Kāma-sukhaṃ ca nekkhamma-sukhaṃ ca", "nekkhamma-sukhan’ti",
     "Sensual happiness and the happiness of renunciation", "the happiness of renunciation", "AN 2.65"),
    ("Upadhi-sukhaṃ ca nirupadhi-sukhaṃ ca", "nirupadhi-sukhan’ti",
     "The happiness bound up with acquisitions and the happiness without acquisitions", "the happiness without acquisitions", "AN 2.66"),
    ("Sāsava-sukhaṃ ca anāsava-sukhaṃ ca", "anāsava-sukhan’ti",
     "The happiness with taints and the happiness without taints", "the happiness without taints", "AN 2.67"),
    ("Sāmisaṃ ca sukhaṃ nirāmisaṃ ca sukhaṃ", "nirāmisaṃ sukhan’ti",
     "Material happiness and spiritual happiness", "spiritual happiness", "AN 2.68"),
    ("Ariya-sukhaṃ ca anariya-sukhaṃ ca", "ariya-sukhan’ti",
     "Noble happiness and ignoble happiness", "noble happiness", "AN 2.69"),
    ("Kāyikaṃ ca sukhaṃ cetasikaṃ ca sukhaṃ", "cetasikaṃ sukhan’ti",
     "Bodily happiness and mental happiness", "mental happiness", "AN 2.70"),
]
P423 = [(f"Dve’māni, bhikkhave, sukhāni. Katamāni dve? {pair}. Imāni kho, bhikkhave, dve sukhāni. "
         f"Etad-aggaṃ, bhikkhave, imesaṃ dvinnaṃ sukhānaṃ yadidaṃ {best}.",
         f"“Bhikkhus, there are these two kinds of happiness. What two? {en_pair}. These are the two kinds of happiness. "
         f"Of these two kinds of happiness, {en_best} is foremost.”\n({ref})")
        for pair, best, en_pair, en_best, ref in SUKHA]

# ---------------------------------------------------------------- 4.2.4
P424 = [
    ("Pañcahi, bhikkhave, aṅgehi samannāgato rājā cakka-vattī dhammen’eva cakkaṃ pavatteti, taṃ hoti cakkaṃ appaṭivattiyaṃ kenaci manussa-bhūtena paccatthikena pāṇinā. Katamehi pañcahi?",
     "“Bhikkhus, possessing five factors, a wheel-turning monarch sets the wheel in motion solely through the Dhamma, a wheel that cannot be turned back by any hostile creature in human form. What five?"),
    ("Idha, bhikkhave, rājā cakka-vattī atthaññū ca hoti, dhammaññū ca, mattaññū ca, kālaññū ca, parisaññū ca. Imehi kho, bhikkhave, pañcahi aṅgehi samannāgato rājā cakka-vattī dhammen’eva cakkaṃ pavatteti, taṃ hoti cakkaṃ appaṭivattiyaṃ kenaci manussa-bhūtena paccatthikena pāṇinā.",
     "“Here, a wheel-turning monarch is one who knows what is good, who knows the Dhamma, who knows the right measure, who knows the proper time, and who knows the assembly. Possessing these five factors, a wheel-turning monarch sets the wheel in motion solely through the Dhamma, a wheel that cannot be turned back by any hostile creature in human form."),
    ("Evameva kho, bhikkhave, pañcahi dhammehi samannāgato tathāgato arahaṃ sammā-sambuddho dhammen’eva anuttaraṃ dhamma-cakkaṃ pavatteti, taṃ hoti cakkaṃ appaṭivattiyaṃ samaṇena vā brāhmaṇena vā devena vā mārena vā brahmunā vā kenaci vā lokasmiṃ. Katamehi pañcahi?",
     "“So too, bhikkhus, possessing five qualities, the Tathāgata, the Arahant, the Perfectly Enlightened One sets in motion the unsurpassed wheel of the Dhamma solely through the Dhamma, a wheel that cannot be turned back by any ascetic, brahmin, deva, Māra, or Brahmā, or by anyone in the world. What five?"),
    ("Idha, bhikkhave, tathāgato arahaṃ sammā-sambuddho atthaññū, dhammaññū, mattaññū, kālaññū, parisaññū. Imehi kho, bhikkhave, pañcahi dhammehi samannāgato tathāgato arahaṃ sammā-sambuddho dhammen’eva anuttaraṃ dhamma-cakkaṃ pavatteti, taṃ hoti dhamma-cakkaṃ appaṭivattiyaṃ samaṇena vā brāhmaṇena vā devena vā mārena vā brahmunā vā kenaci vā lokasmin’ti.",
     "“Here, the Tathāgata, the Arahant, the Perfectly Enlightened One is one who knows what is good, who knows the Dhamma, who knows the right measure, who knows the proper time, and who knows the assembly. Possessing these five qualities, the Tathāgata … sets in motion the unsurpassed wheel of the Dhamma solely through the Dhamma, a wheel that cannot be turned back … by anyone in the world.”"),
]

# ---------------------------------------------------------------- 5.1.1
P511 = [
    ("“Jāneyya nu kho, bho Gotama, asappuriso asappurisaṃ: ‘asappuriso ayaṃ bhavan’”ti?\n“Aṭṭhānaṃ kho etaṃ, brāhmaṇa, anavakāso yaṃ asappuriso asappurisaṃ jāneyya: ‘asappuriso ayaṃ bhavan’”ti.",
     "(1) “Master Gotama, can a bad person know a bad person [thus]: ‘This fellow is a bad person’?”\n“It is, brahmin, impossible, there is no chance, that a bad person can know a bad person [thus]: ‘This fellow is a bad person.’”"),
    ("“Jāneyya pana, bho Gotama, asappuriso sappurisaṃ: ‘sappuriso ayaṃ bhavan’”ti?\n“Etaṃ pi kho, brāhmaṇa, aṭṭhānaṃ anavakāso yaṃ asappuriso sappurisaṃ jāneyya: ‘sappuriso ayaṃ bhavan’”ti.",
     "(2) “Then can a bad person know a good person [thus]: ‘This fellow is a good person’?”\n“It is also impossible, there is no chance, that a bad person can know a good person [thus]: ‘This fellow is a good person.’”"),
    ("“Jāneyya nu kho, bho Gotama, sappuriso sappurisaṃ: ‘sappuriso ayaṃ bhavan’”ti?\n“Ṭhānaṃ kho etaṃ, brāhmaṇa, vijjati yaṃ sappuriso sappurisaṃ jāneyya: ‘sappuriso ayaṃ bhavan’”ti.",
     "(3) “Then can a good person know a good person [thus]: ‘This fellow is a good person’?”\n“It is possible that a good person can know a good person [thus]: ‘This fellow is a good person.’”"),
    ("“Jāneyya pana, bho Gotama, sappuriso asappurisaṃ: ‘asappuriso ayaṃ bhavan’”ti?\n“Etaṃ pi kho, brāhmaṇa, ṭhānaṃ vijjati yaṃ sappuriso asappurisaṃ jāneyya: ‘asappuriso ayaṃ bhavan’”ti.",
     "(4) “Then can a good person know a bad person [thus]: ‘This fellow is a bad person’?”\n“It is also possible that a good person can know a bad person [thus]: ‘This fellow is a bad person.’”"),
]

# ---------------------------------------------------------------- 5.1.2
VAS = [
    ("go-rakkhaṃ upajīvati", "kassako", "so", "by cattle-keeping", "a farmer"),
    ("puthu-sippena jīvati", "sippiko", "so", "by various crafts", "a craftsman"),
    ("vohāraṃ upajīvati", "vāṇijo", "so", "by trade", "a merchant"),
    ("para-pessena jīvati", "pessiko", "so", "by serving others", "a servant"),
    ("adinnaṃ upajīvati", "coro", "eso", "by stealing [“what is not given”]", "a thief"),
    ("issatthaṃ upajīvati", "yodh’ājīvo", "", "by archery", "a soldier"),
    ("porohiccena jīvati", "yājako", "so", "by priestly craft", "a priest [sacrificer]"),
]
P512 = [(verse("Yo hi koci manussesu", how, "evaṃ, Vāseṭṭha, jānāhi", f"“{who}” {so}, na brāhmaṇo" if so else f"“{who}”, na brāhmaṇo"),
         f"One who makes his living among men {en_how},\nyou should know thus, Vāseṭṭha,\nis [called] {en_who};\nhe is not a brahmin.")
        for how, who, so, en_how, en_who in VAS] + [
    (verse("Yo hi koci manussesu", "gāmaṃ raṭṭhañ ca bhuñjati", "evaṃ, Vāseṭṭha, jānāhi", "“rājā” eso, na brāhmaṇo"),
     "One who among men governs [lit. “eats, enjoys”] the village and realm,\nyou should know thus, Vāseṭṭha,\nis [called] a king;\nhe is not a brahmin."),
    (verse("Na c’āhaṃ “brāhmaṇaṃ” brūmi", "yonijaṃ matti-sambhavaṃ", "“bhovādi” nāma so hoti", "sace hoti sakiñcano",
           "akiñcanaṃ anādānaṃ", "tamahaṃ brūmi “brāhmaṇaṃ”"),
     "I call him not a brahmin\nbecause of his origin [“womb-born”] and maternal lineage.\nHe is just a “sir-sayer”\nif he still has attachments.\nOne without attachment, without grasping,\nis the one I call a brahmin."),
    (verse("Sabba-saṃyojanaṃ chetvā", "yo ve na paritassati", "saṅg’ātigaṃ visaṃyuttaṃ", "taṃ ahaṃ brūmi “brāhmaṇaṃ”"),
     "Having cut off all fetters,\nhe indeed is not excited [agitated, distressed].\nOne gone beyond the ties, detached:\nhe is the one I call a brahmin."),
]

# ---------------------------------------------------------------- 5.1.3
P513 = [
    (verse("Appamādena Maghavā", "devānaṃ seṭṭhataṃ gato", "appamādaṃ pasaṃsanti", "pamādo garahito sadā"),
     "By heedfulness did Maghavā [Indra]\nbecome the foremost of the gods.\nThey praise heedfulness,\nheedlessness is always blamed [despised, criticized].\n(Dhp 30)"),
    (verse("Yathāpi ruciraṃ pupphaṃ", "vaṇṇavantaṃ agandhakaṃ", "evaṃ subhāsitā vācā", "aphalā hoti akubbato"),
     "Like a beautiful flower,\nfull of color but without fragrance,\neven so, fruitless is the good speech\nof one who does not act [who does not practise it].\n(Dhp 51)"),
    (verse("Yathāpi ruciraṃ pupphaṃ", "vaṇṇavantaṃ sagandhakaṃ", "evaṃ subhāsitā vācā", "saphalā hoti sakubbato"),
     "Like a beautiful flower,\nfull of color and fragrant,\neven so, fruitful is the good speech\nof one who acts [who practises it].\n(Dhp 52)"),
    (verse("Dīghā jāgarato ratti", "dīghaṃ santassa yojanaṃ", "dīgho bālānaṃ saṃsāro", "saddhammaṃ avijānataṃ"),
     "Long is the night to one who is awake;\nlong is the league to the weary.\nLong is saṃsāra to fools\nwho do not understand the good Dhamma.\n(Dhp 60)"),
]

# ---------------------------------------------------------------- 5.1.4
def _mang(a, b, c, en):
    return (verse(a, b, c, "etaṃ maṅgalam uttamaṃ"), en + "\nthis is the highest blessing.")

P514 = [
    _mang("Asevanā ca bālānaṃ", "paṇḍitānañ ca sevanā", "pūjā ca pūjanīyānaṃ",
          "Non-association with fools,\nand association with the wise,\nand honouring those worthy of honour –"),
    _mang("Bāhusaccaṃ ca sippañ ca", "vinayo ca susikkhito", "subhāsitā ca yā vācā",
          "Much learning, and a craft,\ndiscipline well trained in,\nand well-spoken words –"),
    _mang("Dānañ ca dhamma-cariyā ca", "ñātakānaṃ ca saṅgaho", "anavajjāni kammāni",
          "Giving, righteous conduct,\nand assistance to relatives,\nblameless deeds –"),
    _mang("Ārati virati pāpā", "majja-pānā ca saṃyamo", "appamādo ca dhammesu",
          "Ceasing and abstaining from evil,\nrestraint from intoxicating drinks,\nheedfulness in righteous acts –"),
    _mang("Gāravo ca nivāto ca", "santuṭṭhī ca kataññutā", "kālena dhamma-savanaṃ",
          "Reverence, and humility,\ncontentment and gratitude,\ntimely hearing of the Dhamma –"),
    _mang("Khantī ca sovacassatā", "samaṇānañ ca dassanaṃ", "kālena dhamma-sākacchā",
          "Patience, obedience,\nseeing of monastics,\ntimely discussion on the Dhamma –"),
]

# ---------------------------------------------------------------- 5.2.1
SIX = [
    ("Cakkhunā rūpaṃ disvā", "(1) Here, having seen a form with the eye"),
    ("Sotena saddaṃ sutvā", "(2) Having heard a sound with the ear"),
    ("Ghānena gandhaṃ ghāyitvā", "(3) Having smelled an odor with the nose"),
    ("Jivhāya rasaṃ sāyitvā", "(4) Having tasted a taste with the tongue"),
    ("Kāyena phoṭṭhabbaṃ phusitvā", "(5) Having touched a tactile object with the body"),
    ("Manasā dhammaṃ viññāya", "(6) Having cognized a mental phenomenon with the mind"),
]
P521 = [
    ("“Chahi, bhikkhave, dhammehi samannāgato bhikkhu āhuneyyo hoti pāhuneyyo dakkhiṇeyyo añjali-karaṇīyo, anuttaraṃ puñña-kkhettaṃ lokassa. Katamehi chahi?",
     "“Bhikkhus, possessing six qualities, a bhikkhu is worthy of gifts, worthy of hospitality, worthy of offerings, worthy of reverential salutation, an unsurpassed field of merit for the world. What six?"),
] + [(("Idha, bhikkhave, bhikkhu " + p[0].lower() + p[1:] if i == 0 else p) + " n’eva sumano hoti na dummano, upekkhako viharati sato sampajāno.",
      e + ", a bhikkhu is neither joyful nor saddened, but dwells equanimous, mindful, and clearly comprehending.")
     for i, (p, e) in enumerate(SIX)] + [
    ("Imehi kho, bhikkhave, chahi dhammehi samannāgato bhikkhu āhuneyyo hoti pāhuneyyo dakkhiṇeyyo añjali-karaṇīyo, anuttaraṃ puñña-kkhettaṃ lokassā’”ti.",
     "“Possessing these six qualities, a bhikkhu is worthy of gifts, worthy of hospitality, worthy of offerings, worthy of reverential salutation, an unsurpassed field of merit for the world.”"),
]

# ---------------------------------------------------------------- 5.2.2
P522 = [
    ("“Tena hi, Sīvaka, taññev’ettha paṭipucchāmi. Yathā te khameyya tathā naṃ byākareyyāsi. Taṃ kiṃ maññasi, Sīvaka, santaṃ vā ajjhattaṃ lobhaṃ ‘atthi me ajjhattaṃ lobho’ti pajānāsi, asantaṃ vā ajjhattaṃ lobhaṃ ‘n’atthi me ajjhattaṃ lobho’ti pajānāsī’”ti?\n“Evaṃ, bhante.”",
     "“Well then, Sīvaka, I will question you in turn about this. As you see fit, so you should answer that. What do you think, Sīvaka? (1) When there is greed existing within you, do you know it: ‘There is greed within me,’ or when there is no greed existing within you, do you know it: ‘There is no greed within me’?”\n“Yes, Bhante.”"),
    ("“Yaṃ kho tvaṃ, Sīvaka, santaṃ vā ajjhattaṃ lobhaṃ ‘atthi me ajjhattaṃ lobho’ti pajānāsi, asantaṃ vā ajjhattaṃ lobhaṃ ‘n’atthi me ajjhattaṃ lobho’ti pajānāsi – evaṃ pi kho, Sīvaka, sandiṭṭhiko dhammo hoti … pe …",
     "“Since, Sīvaka, when there is greed existing within you, you know it: ‘There is greed within me,’ and when there is no greed existing within you, you know it: ‘There is no greed within me,’ in this way the Dhamma is directly visible …"),
    ("“Taṃ kiṃ maññasi, Sīvaka, santaṃ vā ajjhattaṃ dosaṃ … pe … santaṃ vā ajjhattaṃ mohaṃ … pe … santaṃ vā ajjhattaṃ lobha-dhammaṃ … pe … santaṃ vā ajjhattaṃ dosa-dhammaṃ … pe … santaṃ vā ajjhattaṃ moha-dhammaṃ ‘atthi me ajjhattaṃ moha-dhammo’ti pajānāsi, asantaṃ vā ajjhattaṃ moha-dhammaṃ ‘n’atthi me ajjhattaṃ moha-dhammo’ti pajānāsī’”ti?\n“Evaṃ, bhante.”",
     "“What do you think, Sīvaka? (2) When there is hatred within you … (3) … delusion within you … (4) … a state connected with greed within you … (5) … a state connected with hatred within you … (6) … a state connected with delusion within you, do you know: ‘There is a state connected with delusion existing within me,’ and when there is no state connected with delusion existing within you, do you know: ‘There is no state connected with delusion existing within me’?”\n“Yes, Bhante.”"),
    ("“Yaṃ kho tvaṃ, Sīvaka, santaṃ vā ajjhattaṃ moha-dhammaṃ ‘atthi me ajjhattaṃ moha-dhammo’ti pajānāsi, asantaṃ vā ajjhattaṃ moha-dhammaṃ ‘n’atthi me ajjhattaṃ moha-dhammo’ti pajānāsi – evaṃ kho, Sīvaka, sandiṭṭhiko dhammo hoti.”",
     "“Since, Sīvaka, when there is a state connected with delusion existing within you, you know: ‘There is a state connected with delusion within me,’ and when there is no state connected with delusion existing within you, you know: ‘There is no state connected with delusion within me,’ in this way the Dhamma is directly visible.”"),
    ("“Abhikkantaṃ, bhante, abhikkantaṃ, bhante … pe … upāsakaṃ maṃ, bhante, bhagavā dhāretu ajjatagge pāṇ’upetaṃ saraṇaṃ gatan’”ti.",
     "“Excellent, Bhante! … Let the Blessed One consider me a lay follower who from today has gone for refuge for life.”"),
]

# ---------------------------------------------------------------- 5.2.3
P523 = [
    ("Rājā āha: “Bhante Nāgasena, yo jānanto pāpa-kammaṃ karoti, yo ca ajānanto pāpa-kammaṃ karoti, kassa bahutaraṃ apuññan’”ti?\nThero āha: “Yo kho, mahārāja, ajānanto pāpa-kammaṃ karoti, tassa bahutaraṃ apuññan’”ti.",
     "The king said: “Bhante Nāgasena, one who does an evil deed knowingly, or one who does an evil deed unknowingly, for whom is there greater demerit?”\nThe Elder said: “Great king, one who does an evil deed unknowingly, for him there is greater demerit.”"),
    ("“Tena hi, bhante Nāgasena, yo amhākaṃ rāja-putto vā rāja-mahāmatto vā ajānanto pāpa-kammaṃ karoti, taṃ mayaṃ diguṇaṃ daṇḍemā’”ti.",
     "“Then, Bhante Nāgasena, when our prince or royal minister does an evil deed unknowingly, we should doubly punish him.”"),
    ("“Taṃ kiṃ maññasi, mahārāja: tattaṃ ayo-guḷaṃ ādittaṃ sampajjalitaṃ sajoti-bhūtaṃ eko jānanto gaṇheyya, eko ajānanto gaṇheyya, katamo balikataraṃ ḍayheyyā’”ti?\n“Yo kho, bhante, ajānanto gaṇheyya, so balikataraṃ ḍayheyyā’”ti.",
     "“What do you think, great king, suppose one man would seize a red-hot iron ball knowingly, and one would seize it unknowingly, which one would be burned more [severely]?”\n“One who would seize it unknowingly would be burned more [severely].”"),
    ("“Evameva kho, mahārāja, yo ajānanto pāpa-kammaṃ karoti, tassa bahutaraṃ apuññan’”ti.\n“Kallo’si, bhante Nāgasenā’”ti.",
     "“Just so, great king, one who does an evil deed unknowingly, for him there is greater demerit.”\n“You are clever, Bhante Nāgasena.”"),
]

# ---------------------------------------------------------------- 5.2.4
P524 = [
    ("“Taṃ kiṃ maññatha, bhikkhave, rūpaṃ niccaṃ vā aniccaṃ vā’”ti?\n“Aniccaṃ, bhante.”\n“Yaṃ pan’āniccaṃ, dukkhaṃ vā taṃ sukhaṃ vā’”ti?\n“Dukkhaṃ, bhante.”\n“Yaṃ pan’āniccaṃ dukkhaṃ vipariṇāma-dhammaṃ, kallaṃ nu taṃ samanupassituṃ: ‘etaṃ mama, eso’hamasmi, eso me attā’”ti?\n“No h’etaṃ, bhante.”",
     "“What do you think, bhikkhus, is form permanent or impermanent?”\n“Impermanent, Bhante.”\n“Is what is impermanent suffering or happiness?”\n“Suffering, Bhante.”\n“Is what is impermanent, suffering, subject to change, fit to be regarded thus: ‘This is mine, this I am, this is my self’?”\n“No, Bhante.”"),
    ("“Vedanā … saññā … saṅkhārā … viññāṇaṃ niccaṃ vā aniccaṃ vā’”ti?\n“Aniccaṃ, bhante.”\n“Yaṃ pan’āniccaṃ, dukkhaṃ vā taṃ sukhaṃ vā’”ti?\n“Dukkhaṃ, bhante.”\n“Yaṃ pan’āniccaṃ dukkhaṃ vipariṇāma-dhammaṃ, kallaṃ nu taṃ samanupassituṃ: ‘etaṃ mama, eso’hamasmi, eso me attā’”ti?\n“No h’etaṃ, bhante.”",
     "“Is feeling … perception … volitional formations … consciousness permanent or impermanent?”\n“Impermanent, Bhante.”\n“Is what is impermanent suffering or happiness?”\n“Suffering, Bhante.”\n“Is what is impermanent, suffering, and subject to change fit to be regarded thus: ‘This is mine, this I am, this is my self’?”\n“No, Bhante.”"),
]

META = [
    ("ncrp-4-1-1", "AN 4.50", "Upakkilesasutta", "Defilements", "NCRP Lesson 4 · Initial reading 1", AN, P411),
    ("ncrp-4-1-2", "AN 4.57", "Suppavāsāsutta", "Suppavāsā", "NCRP Lesson 4 · Initial reading 2", AN, P412),
    ("ncrp-4-1-3", "Dhp 78, 129–130, 19–20, 212–216", "Dhammapada", "Friends, Fear and Sorrow", "NCRP Lesson 4 · Initial reading 3", DHP, P413),
    ("ncrp-4-2-1", "AN 2.42–43, 49", "Parisavagga", "Assemblies", "NCRP Lesson 4 · Further reading 1", AN, P421),
    ("ncrp-4-2-2", "Dhp 21–22, 82, 81, 174, 80", "Dhammapada", "The Wise", "NCRP Lesson 4 · Further reading 2", DHP, P422),
    ("ncrp-4-2-3", "AN 2.64–70", "Sukhavagga", "Happiness", "NCRP Lesson 4 · Further reading 3", AN, P423),
    ("ncrp-4-2-4", "AN 5.131", "Paṭhamacakkānuvattanasutta", "Turning the Wheel", "NCRP Lesson 4 · Further reading 4", AN, P424),
    ("ncrp-5-1-1", "AN 4.187", "Vassakārasutta", "Vassakāra", "NCRP Lesson 5 · Initial reading 1", AN, P511),
    ("ncrp-5-1-2", "MN 98 (Snp 3.9)", "Vāseṭṭhasutta", "Vāseṭṭha", "NCRP Lesson 5 · Initial reading 2", MN, P512),
    ("ncrp-5-1-3", "Dhp 30, 51–52, 60", "Dhammapada", "Heedfulness, Flowers and Fools", "NCRP Lesson 5 · Initial reading 3", DHP, P513),
    ("ncrp-5-1-4", "Khp 5 (Snp 2.4)", "Maṅgalasutta", "Blessings", "NCRP Lesson 5 · Initial reading 4", KHP, P514),
    ("ncrp-5-2-1", "AN 6.1", "Paṭhamaāhuneyyasutta", "Worthy of Gifts", "NCRP Lesson 5 · Further reading 1", AN, P521),
    ("ncrp-5-2-2", "AN 6.47", "Paṭhamasandiṭṭhikasutta", "Directly Visible", "NCRP Lesson 5 · Further reading 2", AN, P522),
    ("ncrp-5-2-3", "Mil 3.7.8", "Milindapañha", "Knowingly or Unknowingly", "NCRP Lesson 5 · Further reading 3", MIL, P523),
    ("ncrp-5-2-4", "SN 22.59", "Anattalakkhaṇasutta", "The Characteristic of Nonself", "NCRP Lesson 5 · Further reading 4", SN, P524),
]

NOTES = """
- 4.2.1: the translation document adds the closing sentence of AN 2.42 (etad-aggaṃ … gambhīrā parisā’ti) and the two
  phrases of AN 2.43 (aññamaññaṃ mukha-sattīhi vitudantā / piya-cakkhūhi sampassantā); included (Mor's default).
- 4.2.4: the scan has atthaññū (the digital book's aṭṭhaññū is a slip); dhammen’eva throughout.
- 5.1.2: the book's "sa ve hoti sakiñcano" is a slip for "sace hoti sakiñcano" (translation document, MN 98).
- 5.1.3: the book's sagandhakaṃ / sakubbato kept (Grammar V 8 uses sa- 'with').
- 5.1.4: word division as in Mor's workshop booklet (maṅgalam uttamaṃ, paṇḍitānañ ca).
- 5.2.1: the book abbreviates the senses 2-5 with pe; written out as in the translation document.
- 5.2.3: the scan has "eko ajānanto … eko jānanto"; the order of the translation document and the digital book is used.
  sajoti-bhūtaṃ is in the translation document but not in the scan; included.
"""
