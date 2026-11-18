# Pali (as in the printed book, checked against the scan, written with Mor's conventions) and
# English (natural translations from the course translation document) for NCRP Lessons 6-7.
# Word analyses: ncrp_l6_l7_words.py. Choices are listed in NOTES at the bottom.
from _paras_l4_l5 import AN, MN, DHP, verse

KHP = "English: course exercise book, after Piyadassi Thera’s translation (accesstoinsight.org)."
SNP = "English: course exercise book, after Bhikkhu Thanissaro’s translation (accesstoinsight.org)."
MIL_RD = "English: course exercise book, after T. W. Rhys Davids, The Questions of King Milinda (1890–1894)."
MIL_P = "English: course exercise book, after Bhikkhu Pesala, The Debate of King Milinda (2001)."

# ---------------------------------------------------------------- 6.1.1
SIKKHA = [
    ("Pāṇ’ātipātā", "killing living creatures"),
    ("Adinn’ādānā", "taking what has not been given"),
    ("Kāmesu micchā-cārā", "sensual misconduct"),
    ("Musā-vādā", "false speech"),
    ("Surā-meraya-majja-pamāda-ṭṭhānā", "liquor, wines, or intoxicants which cause heedlessness"),
]
P611 = [(f"{p} veramaṇī-sikkhā-padaṃ samādiyāmi.", f"I undertake the training rule of abstaining from {e}.")
        for p, e in SIKKHA]

# ---------------------------------------------------------------- 6.1.2
P612 = [
    (verse("Yathāpi cando vimalo", "gacchaṃ ākāsa-dhātuyā", "sabbe tārā-gaṇe loke", "ābhāya atirocati"),
     "As the stainless moon\nmoving through the space element\noutshines with its radiance\nall the multitude of stars in the world,"),
    (verse("Tath’eva sīla-sampanno", "saddho purisa-puggalo", "sabbe maccharino loke", "cāgena atirocati"),
     "so one accomplished in virtuous behaviour,\na person of faith,\noutshines by generosity\nall the misers in the world."),
    (verse("Yathāpi megho thanayaṃ", "vijju-mālī satakkaku", "thalaṃ ninnaṃ ca pūreti", "abhivassaṃ vasundharaṃ"),
     "As the rain cloud, thundering,\nwreathed in lightning, hundred-peaked,\nfills the highland and lowland,\nraining upon the earth,"),
    (verse("Evaṃ dassana-sampanno", "sammā-sambuddha-sāvako", "macchariṃ adhigaṇhāti", "pañca-ṭhānehi paṇḍito"),
     "so the Perfectly Enlightened One’s disciple,\none accomplished in vision,\na wise person, in five respects\nsurpasses the miser:"),
    (verse("Āyunā yasasā c’eva", "vaṇṇena ca sukhena ca", "sa ve bhoga-paribyūḷho", "pecca sagge pamodatī’ti"),
     "in life span and glory,\nin beauty and happiness.\nHe, indeed, possessed of wealth,\nafter death rejoices in heaven."),
]

# ---------------------------------------------------------------- 6.1.3
P613 = [
    ("Tena kho pana samayena Keṇiyo jaṭilo Sele brāhmaṇe abhippasanno hoti. Atha kho Selo brāhmaṇo tīhi māṇavaka-satehi parivuto … yena Keṇiyassa jaṭilassa assamo ten’upasaṅkami. Addasā kho Selo brāhmaṇo Keṇiy’assamiye jaṭile app’ekacce uddhanāni khaṇante, app’ekacce kaṭṭhāni phālente, app’ekacce bhājanāni dhovante, app’ekacce udaka-maṇikaṃ patiṭṭhāpente, app’ekacce āsanāni paññapente, Keṇiyaṃ pana jaṭilaṃ sāmaṃ yeva maṇḍala-māḷaṃ paṭiyādentaṃ.",
     "At that time the matted-hair ascetic Keṇiya had full confidence in the brahmin Sela. Then the brahmin Sela … attended by three hundred brahmin students, came to the matted-hair ascetic Keṇiya’s hermitage. There the brahmin Sela saw some of the matted-hair ascetics of Keṇiya’s hermitage digging out ovens, some chopping wood, some washing dishes, some setting up a water-pot, some preparing seats, and the matted-hair ascetic Keṇiya himself preparing the pavilion."),
    ("Disvāna Keṇiyaṃ jaṭilaṃ etadavoca: “Kiṃ nu kho bhoto Keṇiyassa āvāho vā bhavissati, vivāho vā bhavissati, mahā-yañño vā paccupaṭṭhito, rājā vā Māgadho Seniyo Bimbisāro nimantito svātanāya saddhiṃ bala-kāyenā’”ti?",
     "Having seen this, he asked the matted-hair ascetic Keṇiya: “What, is Master Keṇiya having a marriage or a giving in marriage? Or has a great sacrifice been arranged? Or has King Seniya Bimbisāra of Magadha been invited for tomorrow’s meal along with his army?”"),
    ("“Na me, bho Sela, āvāho vā bhavissati, vivāho vā bhavissati, n’api rājā Māgadho Seniyo Bimbisāro nimantito svātanāya saddhiṃ bala-kāyena. Api ca kho me mahā-yañño paccupaṭṭhito atthi. Samaṇo Gotamo Sakya-putto Sakya-kulā pabbajito Aṅguttarāpesu cārikaṃ caramāno mahatā bhikkhu-saṅghena … Āpaṇaṃ anuppatto … So me nimantito svātanāya saddhiṃ bhikkhu-saṅghenā’”ti.",
     "“I do not have a marriage or a giving in marriage, Master Sela, nor has King Seniya Bimbisāra of Magadha been invited for tomorrow’s meal along with his army, but I have arranged a great sacrifice. The recluse Gotama, the son of the Sakyans, who went forth from a Sakyan clan, has been wandering on tour among the Aṅguttarāpans with a large Saṅgha of bhikkhus … and has come to Āpaṇa … He has been invited by me for tomorrow’s meal along with the Saṅgha of bhikkhus.”"),
    ("“‘Buddho’ti, bho Keṇiya, vadesi?”\n“‘Buddho’ti, bho Sela, vadāmi.”\n“‘Buddho’ti, bho Keṇiya, vadesi?”\n“‘Buddho’ti, bho Sela, vadāmī’”ti.",
     "“Do you say ‘Buddha,’ Keṇiya?”\n“I say ‘Buddha,’ Sela.”\n“Do you say ‘Buddha,’ Keṇiya?”\n“I say ‘Buddha,’ Sela.”"),
    ("Atha kho Selassa brāhmaṇassa etadahosi: “Ghoso pi kho eso dullabho lokasmiṃ yadidaṃ ‘buddho’”ti.",
     "Then it occurred to the brahmin Sela: “Even this sound is hard to encounter in the world, that is, ‘Buddha.’”"),
]

# ---------------------------------------------------------------- 6.1.4
_TWO = "Tathāgato ca arahaṃ sammā-sambuddho, rājā ca cakka-vattī."
_TWO_EN = "The Tathāgata, the Arahant, the Perfectly Enlightened One and the king who is a wheel-turner."
P614 = [
    (f"“Dve’me, bhikkhave, puggalā loke uppajjamānā uppajjanti bahu-jana-hitāya bahu-jana-sukhāya, bahuno janassa atthāya hitāya sukhāya … Katame dve? {_TWO} Ime kho, bhikkhave, dve puggalā loke uppajjamānā uppajjanti bahu-jana-hitāya bahu-jana-sukhāya, bahuno janassa atthāya hitāya sukhāya …”ti.",
     f"“Monks, these two people arising in the world arise for the welfare of many people, for the happiness of many people, for the good, welfare, and happiness of devas and humans. What two? {_TWO_EN} These, monks, are the two people arising in the world who arise for the welfare of many people, for the happiness of many people, for the good, welfare, and happiness of devas and humans.”\n(AN 2.52)"),
    (f"“Dve’me, bhikkhave, puggalā loke uppajjamānā uppajjanti acchariya-manussā. Katame dve? {_TWO} Ime kho, bhikkhave, dve puggalā loke uppajjamānā uppajjanti acchariya-manussā’ti.",
     f"“Bhikkhus, there are these two people arising in the world who are extraordinary humans. What two? {_TWO_EN} These are the two people arising in the world who are extraordinary humans.”\n(AN 2.53)"),
    ("“Dvinnaṃ, bhikkhave, puggalānaṃ kāla-kiriyā bahuno janassa anutappā hoti. Katamesaṃ dvinnaṃ? Tathāgatassa ca arahato sammā-sambuddhassa, rañño ca cakka-vattissa. Imesaṃ kho, bhikkhave, dvinnaṃ puggalānaṃ kāla-kiriyā bahuno janassa anutappā hotī’ti.",
     f"“Bhikkhus, the passing away of two people is mourned by many people. What two? {_TWO_EN} The passing away of these two people is mourned by many people.”\n(AN 2.54)"),
    (f"“Dve’me, bhikkhave, thūp’ārahā. Katame dve? {_TWO} Ime kho, bhikkhave, dve thūp’ārahā’ti.",
     f"“Bhikkhus, there are these two who are worthy of a stupa. What two? {_TWO_EN} These are the two who are worthy of a stupa.”\n(AN 2.55)"),
]

# ---------------------------------------------------------------- 6.1.5
P615 = [
    (verse("Tameva vācaṃ bhāseyya", "yāy’attānaṃ na tāpaye", "pare ca na vihiṃseyya", "sā ve vācā subhāsitā"),
     "One should speak only the speech\nthat neither torments self\nnor does harm to others.\nThat speech is truly well spoken."),
    (verse("Piya-vācameva bhāseyya", "yā vācā paṭinanditā", "yaṃ anādāya pāpāni", "paresaṃ bhāsate piyaṃ"),
     "One should speak only endearing speech,\nspeech that is welcomed.\nSpeech that brings no evils\nis pleasant to others."),
    (verse("“Saccaṃ ve amatā vācā”", "esa dhammo sanantano", "“sacce atthe ca dhamme ca”", "āhu santo “patiṭṭhitā”"),
     "Truth, indeed, is deathless speech:\nthis is an ancient principle.\nThe goal and the Dhamma,\nthe good say, are established on truth."),
]

# ---------------------------------------------------------------- 6.2.1
_VINA = "api nu te vīṇā tasmiṃ samaye saravatī vā hoti kammaññā vā’”ti?"
P621 = [
    ("“Nanu te, Soṇa, raho-gatassa paṭisallīnassa evaṃ cetaso parivitakko udapādi: ‘ye kho keci bhagavato sāvakā āraddha-viriyā viharanti, ahaṃ tesaṃ aññataro. Atha ca pana me na anupādāya āsavehi cittaṃ vimuccati. Saṃvijjanti kho pana me kule bhogā, sakkā bhoge ca bhuñjituṃ puññāni ca kātuṃ. Yannūn’āhaṃ sikkhaṃ paccakkhāya hīnāy’āvattitvā bhoge ca bhuñjeyyaṃ puññāni ca kareyyan’”ti?\n“Evaṃ, bhante.”",
     "“Soṇa, didn’t the following course of thought arise in your mind when you were alone in seclusion: ‘[As to] those who are the Blessed One’s energetic disciples, I am one of them. Yet my mind has not been liberated from the taints by non-clinging. Now there is wealth in my family, and it is possible to enjoy wealth and do meritorious deeds. Shouldn’t I then, having given up the training, having returned to the lower [life], enjoy wealth and do meritorious deeds’?”\n“Yes, Bhante.”"),
    ("“Taṃ kiṃ maññasi, Soṇa, kusalo tvaṃ pubbe agāriya-bhūto vīṇāya tanti-ssare’”ti?\n“Evaṃ, bhante.”",
     "“What do you think, Soṇa, in the past, when you were at home, weren’t you skilled at playing the lute?”\n“Yes, Bhante.”"),
    (f"“Taṃ kiṃ maññasi, Soṇa, yadā te vīṇāya tantiyo accāyatā honti, {_VINA}\n“No h’etaṃ, bhante.”",
     "“What do you think, Soṇa, when the strings of the lute were too tight, was your lute well tuned and easy to play?”\n“No, Bhante.”"),
    (f"“Taṃ kiṃ maññasi, Soṇa, yadā te vīṇāya tantiyo atisithilā honti, {_VINA}\n“No h’etaṃ, bhante.”",
     "“What do you think, Soṇa, when the strings of the lute were too loose, was your lute well tuned and easy to play?”\n“No, Bhante.”"),
    (f"“Yadā pana te, Soṇa, vīṇāya tantiyo na accāyatā honti n’ātisithilā same guṇe patiṭṭhitā, {_VINA}\n“Evaṃ, bhante.”",
     "“But, Soṇa, when the strings of the lute were not too tight, not too loose, but established in a balanced pitch, was your lute at that time well tuned and easy to play?”\n“Yes, Bhante.”"),
    ("“Evameva kho, Soṇa, accāraddha-viriyaṃ uddhaccāya saṃvattati, atisithila-viriyaṃ kosajjāya saṃvattati. Tasmātiha tvaṃ, Soṇa, viriya-samataṃ adhiṭṭhaha, indriyānaṃ ca samataṃ paṭivijjha, tattha ca nimittaṃ gaṇhāhī’”ti.",
     "“So too, Soṇa, energy that is aroused to excess leads to restlessness; energy that is too lax leads to laziness. Therefore, Soṇa, resolve on a balance of energy, establish evenness of the [spiritual] faculties, and take up the object there.”"),
]

# ---------------------------------------------------------------- 6.2.2
P622 = [
    (verse("Kodhano dubbaṇṇo hoti", "atho dukkhaṃ pi seti so", "atho atthaṃ gahetvāna", "anatthaṃ adhipajjati"),
     "The angry one is ugly;\nhe also sleeps badly;\nhaving gained some benefit,\nit turns out to be harmful."),
    (verse("Tato kāyena vācāya", "vadhaṃ katvāna kodhano", "kodh’ābhibhūto puriso", "dhana-jāniṃ nigacchati"),
     "The angry one,\nhaving slain by body and speech,\na person overcome by anger,\nundergoes the loss of wealth."),
    (verse("Kodha-sammada-sammatto", "āyasakyaṃ nigacchati", "ñāti-mittā suhajjā ca", "parivajjanti kodhanaṃ"),
     "Maddened by the madness of anger,\nhe acquires a bad reputation.\nHis relatives, friends, and loved ones\navoid the angry one."),
    (verse("Anattha-janano kodho", "kodho citta-ppakopano", "bhayamantarato jātaṃ", "taṃ jano n’āvabujjhati"),
     "Anger is a producer of harm;\nanger [is] turmoil of mind.\nPeople do not recognize\nthe peril arisen from within."),
    (verse("Kuddho atthaṃ na jānāti", "kuddho dhammaṃ na passati", "andha-tamaṃ tadā hoti", "yaṃ kodho sahate naraṃ"),
     "The angry person doesn’t know the good;\nthe angry person doesn’t see the Dhamma.\nThere is just blinding darkness\nwhen anger overcomes a person."),
    (verse("N’āssa hirī na ottappaṃ", "na vāco hoti gāravo", "kodhena abhibhūtassa", "na dīpaṃ hoti kiñcanaṃ"),
     "For him [there is] no shame or moral dread,\nhis speech is not respectful;\nfor one overcome by anger\nthere is no island [of safety] at all."),
]

# ---------------------------------------------------------------- 6.2.3
P623 = [
    ("Rājā āha: “Kiṃ-lakkhaṇo, bhante Nāgasena, manasikāro, kiṃ-lakkhaṇā paññā’”ti?\n“Ūhana-lakkhaṇo kho, mahārāja, manasikāro, chedana-lakkhaṇā paññā’”ti.",
     "The king said: “What does reflection have as its characteristic mark? What does wisdom have as its characteristic mark?”\n“Reflection has comprehension as its characteristic mark, great king; wisdom has cutting off as its characteristic mark.”"),
    ("“Kathaṃ ūhana-lakkhaṇo manasikāro, kathaṃ chedana-lakkhaṇā paññā? Opammaṃ karohī’”ti.\n“Jānāsi tvaṃ, mahārāja, yava-lāvake’”ti?\n“Āma, bhante, jānāmī’”ti.\n“Kathaṃ, mahārāja, yava-lāvakā yavaṃ lunantī’”ti?\n“Vāmena, bhante, hatthena yava-kalāpaṃ gahetvā dakkhiṇena hatthena dāttaṃ gahetvā dāttena chindantī’”ti.",
     "“But how does reflection have comprehension as its characteristic mark? How does wisdom have cutting off as its characteristic mark? Give me an illustration.”\n“You know, great king, the barley reapers?”\n“Yes, Bhante, I know.”\n“How do the barley reapers reap the barley?”\n“With the left hand they grasp a stack of barley, and having taken a sickle with the right hand, they cut it off with the sickle.”"),
    ("“Yathā, mahārāja, yava-lāvako vāmena hatthena yava-kalāpaṃ gahetvā dakkhiṇena hatthena dāttaṃ gahetvā yavaṃ chindati, evameva kho, mahārāja, yog’āvacaro manasikārena mānasaṃ gahetvā paññāya kilese chindati. Evaṃ kho, mahārāja, ūhana-lakkhaṇo manasikāro, evaṃ chedana-lakkhaṇā paññā’”ti.\n“Kallo’si, bhante Nāgasenā’”ti.",
     "“As the barley reaper grasps a stack of barley with the left hand, and having taken a sickle with the right hand, cuts off the barley, even so, great king, the meditator by reflection grasps his mind, and by wisdom cuts off the defilements. In this way reflection has comprehension as its characteristic mark. In this way wisdom has cutting off as its characteristic mark.”\n“You are clever, Bhante Nāgasena!”"),
]

# ---------------------------------------------------------------- 6.2.4
def _sand(pe):
    return f"santaṃ vā ajjhattaṃ {pe}"

P624 = [
    ("Atha kho aññataro brāhmaṇo yena bhagavā ten’upasaṅkami; upasaṅkamitvā bhagavatā saddhiṃ sammodi … ekamantaṃ nisīdi. Ekamantaṃ nisinno kho so brāhmaṇo bhagavantaṃ etadavoca:\n“Sandiṭṭhiko dhammo, sandiṭṭhiko dhammo’ti, bho Gotama, vuccati. Kittāvatā nu kho, bho Gotama, sandiṭṭhiko dhammo hoti akāliko ehipassiko opaneyyiko paccattaṃ veditabbo viññūhī’”ti?",
     "Then a certain brahmin approached the Blessed One. Having approached, he exchanged greetings with the Blessed One … and he sat down to one side. Seated to one side, that brahmin said this to the Blessed One:\n“It is said: ‘The directly visible Dhamma, the directly visible Dhamma,’ Master Gotama. In what way, Master Gotama, is the Dhamma directly visible, timeless, a ‘come and see’ matter, applicable, to be personally understood by the wise?”"),
    ("“Tena hi, brāhmaṇa, taññev’ettha paṭipucchissāmi. Yathā te khameyya tathā naṃ byākareyyāsi. Taṃ kiṃ maññasi, brāhmaṇa, santaṃ vā ajjhattaṃ rāgaṃ ‘atthi me ajjhattaṃ rāgo’ti pajānāsi, asantaṃ vā ajjhattaṃ rāgaṃ ‘n’atthi me ajjhattaṃ rāgo’ti pajānāsī’”ti?\n“Evaṃ, bho.”",
     "“Well then, brahmin, I will question you about this. As you see fit, so you should answer. What do you think, brahmin? (1) When there is lust within you, do you know: ‘There is lust within me,’ and when there is no lust within you, do you know: ‘There is no lust within me’?”\n“Yes, sir.”"),
    ("“Yaṃ kho tvaṃ, brāhmaṇa, santaṃ vā ajjhattaṃ rāgaṃ ‘atthi me ajjhattaṃ rāgo’ti pajānāsi, asantaṃ vā ajjhattaṃ rāgaṃ ‘n’atthi me ajjhattaṃ rāgo’ti pajānāsi – evaṃ pi kho, brāhmaṇa, sandiṭṭhiko dhammo hoti … pe …",
     "“Since, brahmin, when there is lust within you, you know: ‘There is lust within me,’ and when there is no lust within you, you know: ‘There is no lust within me,’ in this way the Dhamma is directly visible …"),
    ("“Taṃ kiṃ maññasi, brāhmaṇa, santaṃ vā ajjhattaṃ dosaṃ … pe … santaṃ vā ajjhattaṃ mohaṃ … pe … santaṃ vā ajjhattaṃ kāya-sandosaṃ … pe … santaṃ vā ajjhattaṃ vacī-sandosaṃ … pe … santaṃ vā ajjhattaṃ mano-sandosaṃ ‘atthi me ajjhattaṃ mano-sandoso’ti pajānāsi, asantaṃ vā ajjhattaṃ mano-sandosaṃ ‘n’atthi me ajjhattaṃ mano-sandoso’ti pajānāsī’”ti?\n“Evaṃ, bho.”",
     "“What do you think, brahmin? (2) When there is hatred within you … (3) … when there is delusion within you … (4) … when there is a bodily fault within you … (5) … when there is a verbal fault within you … (6) … when there is a mental fault within you, do you know: ‘There is a mental fault within me,’ and when there is no mental fault within you, do you know: ‘There is no mental fault within me’?”\n“Yes, sir.”"),
    ("“Yaṃ kho tvaṃ, brāhmaṇa, santaṃ vā ajjhattaṃ mano-sandosaṃ ‘atthi me ajjhattaṃ mano-sandoso’ti pajānāsi, asantaṃ vā ajjhattaṃ mano-sandosaṃ ‘n’atthi me ajjhattaṃ mano-sandoso’ti pajānāsi – evaṃ kho, brāhmaṇa, sandiṭṭhiko dhammo hoti akāliko ehipassiko opaneyyiko paccattaṃ veditabbo viññūhī’”ti.",
     "“Since, brahmin, when there is a mental fault within you, you know: ‘There is a mental fault within me,’ and when there is no mental fault within you, you know: ‘There is no mental fault within me,’ in this way the Dhamma is directly visible, timeless, a ‘come and see’ matter, applicable, to be personally understood by the wise.”"),
    ("“Abhikkantaṃ, bho Gotama, abhikkantaṃ, bho Gotama … upāsakaṃ maṃ bhavaṃ Gotamo dhāretu ajjatagge pāṇ’upetaṃ saraṇaṃ gatan’”ti.",
     "“Excellent, Master Gotama! Excellent, Master Gotama! … Let Master Gotama consider me a lay follower who from today has gone for refuge as long as I have life.”"),
]

# ---------------------------------------------------------------- 6.2.5
P625 = [
    (verse("Manujassa pamatta-cārino", "taṇhā vaḍḍhati māluvā viya", "so palavati hurāhuraṃ", "phalamicchaṃ’va vanasmiṃ vānaro"),
     "The craving of a human living heedlessly\ngrows like a creeper.\nHe leaps here and there,\nlike the monkey in the forest seeking fruits.\n(Dhp 334)"),
    (verse("Yaṃ esā sahatī jammī", "taṇhā loke visattikā", "sokā tassa pavaḍḍhanti", "abhivaḍḍhaṃ’va bīraṇaṃ"),
     "Whoever this wretched and sticky craving\novercomes in the world,\nhis sorrows increase,\nas bīraṇa grass has grown.\n(Dhp 335)"),
    (verse("Yo c’etaṃ sahati jammiṃ", "taṇhaṃ loke duraccayaṃ", "sokā tamhā papatanti", "uda-bindu’va pokkharā"),
     "But whoever overcomes this wretched craving,\nso difficult to pass beyond in the world,\nfrom him sorrows fall away\nlike a drop of water from a lotus leaf.\n(Dhp 336)"),
]

# ---------------------------------------------------------------- 7.1.1
def _kal(root, adj, inst, en_root, en_adj, n):
    return [
        (f"“Taṃ kiṃ maññatha, Kālāmā, {root} purisassa ajjhattaṃ uppajjamāno uppajjati hitāya vā ahitāya vā’”ti?\n“Ahitāya, bhante.”",
         f"({n}) “What do you think, Kālāmas? When {en_root} arises in a person, does it arise for welfare or for harm?”\n“For harm, Bhante.”"),
        (f"“{adj} pan’āyaṃ, Kālāmā, purisa-puggalo {inst} abhibhūto pariyādinna-citto, pāṇaṃ pi hanati, adinnaṃ pi ādiyati, para-dāraṃ pi gacchati, musā pi bhaṇati, paraṃ pi tathattāya samādapeti, yaṃ’sa hoti dīgha-rattaṃ ahitāya dukkhāyā’”ti.\n“Evaṃ, bhante.”",
         f"“Kālāmas, {en_adj} person, overcome by {en_root}, with mind obsessed [by {en_root}], destroys life, takes what is not given, goes to another’s wife, and speaks falsely; and he encourages others, too, to do the same. Will that lead to harm and suffering for a long time?”\n“Yes, Bhante.”"),
    ]

P711 = [
    ("“Etha tumhe, Kālāmā, mā anussavena, mā paramparāya, mā itikirāya, mā piṭaka-sampadānena … mā ‘samaṇo no garū’ti. Yadā tumhe, Kālāmā, attanā’va jāneyyātha: ‘ime dhammā akusalā, ime dhammā sāvajjā, ime dhammā viññu-garahitā, ime dhammā samattā samādinnā ahitāya dukkhāya saṃvattantī’ti, atha tumhe, Kālāmā, pajaheyyātha.",
     "“Come, Kālāmas, do not go by oral tradition, by lineage [of teaching], by hearsay, by a collection of scriptures … [because you think]: ‘The ascetic is our guru.’ When, Kālāmas, you know for yourselves: ‘These things are unwholesome; these things are blameworthy; these things are censured by the wise; these things, if accepted and undertaken, lead to harm and suffering,’ then, Kālāmas, you should abandon them."),
] + _kal("lobho", "Luddho", "lobhena", "greed", "this greedy", 1) \
  + _kal("doso", "Duṭṭho", "dosena", "hatred", "a hateful", 2) \
  + _kal("moho", "Mūḷho", "mohena", "delusion", "a deluded", 3) + [
    ("“Taṃ kiṃ maññatha, Kālāmā, ime dhammā kusalā vā akusalā vā’”ti?\n“Akusalā, bhante.”\n“Sāvajjā vā anavajjā vā’”ti?\n“Sāvajjā, bhante.”\n“Viññu-garahitā vā viññu-ppasatthā vā’”ti?\n“Viññu-garahitā, bhante.”\n“Samattā samādinnā ahitāya dukkhāya saṃvattanti, no vā? Kathaṃ vā ettha hotī’”ti?\n“Samattā, bhante, samādinnā ahitāya dukkhāya saṃvattantī’ti. Evaṃ no ettha hotī’”ti.",
     "“What do you think, Kālāmas? Are these things wholesome or unwholesome?”\n“Unwholesome, Bhante.”\n“Blameworthy or blameless?”\n“Blameworthy, Bhante.”\n“Censured or praised by the wise?”\n“Censured by the wise, Bhante.”\n“Accepted and undertaken, do they lead to harm and suffering, or not, or how is it here?”\n“Accepted and undertaken, Bhante, these things lead to harm and suffering. So is it here for us.”"),
]

# ---------------------------------------------------------------- 7.1.2
SENSE = [("diṭṭhaṃ", "seen"), ("sutaṃ", "heard"), ("mutaṃ", "sensed"), ("viññātaṃ", "cognized")]
P712 = [
    ("“" + "; ".join(f"n’āhaṃ, brāhmaṇa, sabbaṃ {x} bhāsitabban’ti vadāmi; na pan’āhaṃ, brāhmaṇa, sabbaṃ {x} na bhāsitabban’ti vadāmi" for x, _ in SENSE) + ".",
     " ".join(f"({i}) {'“' if i == 1 else ''}I do not say{', brahmin,' if i == 1 else ''} that everything {e} should be spoken about, nor do I say that nothing {e} should be spoken about." for i, (_, e) in enumerate(SENSE, 1))),
] + [
    (f"“Yaṃ hi, brāhmaṇa, {x} bhāsato akusalā dhammā abhivaḍḍhanti, kusalā dhammā parihāyanti, evarūpaṃ {x} na bhāsitabban’ti vadāmi. Yaṃ ca khv’assa, brāhmaṇa, {x} abhāsato kusalā dhammā parihāyanti, akusalā dhammā abhivaḍḍhanti, evarūpaṃ {x} bhāsitabban’ti {'vadāmi.' if i < 4 else 'vadāmī’”ti.'}",
     f"({i}) “{'For, brahmin, if' if i == 1 else 'If'}, when one speaks about what one has {e}, unwholesome qualities increase and wholesome qualities decline, I say ‘One should not speak about such a thing that one has {e}.’ But if, when one does not speak about what one has {e}, wholesome qualities decline and unwholesome qualities increase, I say ‘One should speak about such a thing that one has {e}.’{'”' if i == 4 else ''}")
    for i, (x, e) in enumerate(SENSE, 1)]

# ---------------------------------------------------------------- 7.1.3
P713 = [
    (verse("Saccaṃ bhaṇe na kujjheyya", "dajjā’ppasmiṃ pi yācito", "etehi tīhi ṭhānehi", "gacche devāna santike"),
     "Speak the truth; do not get angry;\nwhen asked, one should give\neven [if you have] a little.\nBy these three means\ncan one go to the presence of the gods.\n(Dhp 224)"),
    (verse("Kāya-ppakopaṃ rakkheyya", "kāyena saṃvuto siyā", "kāya-duccaritaṃ hitvā", "kāyena sucaritaṃ care"),
     "One should guard against bodily anger;\none should be restrained by body.\nHaving abandoned bodily misconduct,\none should practise good conduct by body.\n(Dhp 231)"),
    (verse("Vacī-pakopaṃ rakkheyya", "vācāya saṃvuto siyā", "vacī-duccaritaṃ hitvā", "vācāya sucaritaṃ care"),
     "One should guard against speech anger;\none should be restrained by speech.\nHaving abandoned misconduct of speech,\none should practise good conduct by speech.\n(Dhp 232)"),
    (verse("Mano-pakopaṃ rakkheyya", "manasā saṃvuto siyā", "mano-duccaritaṃ hitvā", "manasā sucaritaṃ care"),
     "One should guard against mental anger;\none should be restrained by mind.\nHaving abandoned mental misconduct,\none should practise good conduct by mind.\n(Dhp 233)"),
    (verse("Yo pāṇamatipāteti", "musā-vādaṃ ca bhāsati", "loke adinnaṃ ādiyati", "para-dāraṃ ca gacchati"),
     "One who destroys life,\nutters false speech,\ntakes what is not given in the world,\ngoes to another’s wife,\n(Dhp 246)"),
    (verse("Surā-meraya-pānaṃ ca", "yo naro anuyuñjati", "idh’evameso lokasmiṃ", "mūlaṃ khaṇati attano"),
     "and pursues drinks of liquor and wine –\nthis man, even here in this world,\ndigs his own root.\n(Dhp 247)"),
]

# ---------------------------------------------------------------- 7.1.4
P714 = [
    (verse("Sace labhetha nipakaṃ sahāyaṃ", "saddhiṃ-caraṃ sādhu-vihāri-dhīraṃ", "abhibhuyya sabbāni parissayāni",
           "careyya tena’ttamano satīmā"),
     "If you can find a prudent friend,\na wise companion who leads a good life,\nhaving overcome all impediments,\nyou should travel with him, joyously and mindfully.\n(Dhp 328)"),
    (verse("No ce labhetha nipakaṃ sahāyaṃ", "saddhiṃ-caraṃ sādhu-vihāri-dhīraṃ", "rājā’va raṭṭhaṃ vijitaṃ pahāya",
           "eko care mātaṅg’araññe’va nāgo"),
     "If you cannot find a prudent friend,\na wise companion who leads a good life,\nthen, like a king who abandons a conquered kingdom,\nyou should travel alone, like a bull elephant in the Mātaṅga forest.\n(Dhp 329)"),
]

# ---------------------------------------------------------------- 7.2.1
def _aggi(x, adj, inst, en, en_adj, n):
    return (f"Kasmā c’āyaṃ, brāhmaṇa, {x}’aggi pahātabbo parivajjetabbo, na sevitabbo? {adj} kho, brāhmaṇa, {inst} abhibhūto pariyādinna-citto kāyena duccaritaṃ carati, vācāya duccaritaṃ carati, manasā duccaritaṃ carati. So kāyena duccaritaṃ caritvā, vācāya duccaritaṃ caritvā, manasā duccaritaṃ caritvā kāyassa bhedā paraṃ maraṇā apāyaṃ duggatiṃ vinipātaṃ nirayaṃ upapajjati. Tasmā’yaṃ {x}’aggi pahātabbo parivajjetabbo, na sevitabbo.",
            f"({n}) “And why, brahmin, should the fire of {en} be abandoned and avoided, and not be cultivated? One {en_adj}, overcome by {en}, with mind obsessed by it, engages in misconduct by body, engages in misconduct by speech, engages in misconduct by mind. Having engaged in misconduct by body, engaged in misconduct by speech, engaged in misconduct by mind, with the breakup of the body, after death, he is reborn in the plane of misery, in a bad destination, in the lower world, in hell. Therefore this fire of {en} should be abandoned and avoided, and should not be cultivated.")

P721 = [
    ("“Tayo’me, brāhmaṇa, aggī pahātabbā parivajjetabbā, na sevitabbā. Katame tayo? Rāg’aggi, dos’aggi, moh’aggi.",
     "“There are, brahmin, these three fires that should be abandoned and avoided, and should not be cultivated. What three? The fire of lust, the fire of hatred, and the fire of delusion."),
    _aggi("rāg", "Ratto", "rāgena", "lust", "excited by lust", 1),
    _aggi("dos", "Duṭṭho", "dosena", "hatred", "full of hatred", 2),
    _aggi("moh", "Mūḷho", "mohena", "delusion", "who is deluded", 3),
    ("Ime kho tayo, brāhmaṇa, aggī pahātabbā parivajjetabbā, na sevitabbā.”",
     "“These, brahmin, are the three fires that should be abandoned and avoided and should not be cultivated.”"),
]

# ---------------------------------------------------------------- 7.2.2
_PANNA = "paññā, mahārāja, uppajjamānā avijj’andhakāraṃ vidhameti, vijj’obhāsaṃ janeti, ñāṇ’ālokaṃ vidaṃseti, ariya-saccāni pākaṭāni karoti; tato yog’āvacaro ‘aniccan’ti vā ‘dukkhan’ti vā ‘anattā’ti vā sammappaññāya passati"
_PANNA_EN = "when wisdom arises it dispels the darkness of ignorance, it produces the radiance of vision, it spreads out the light of knowledge, and makes the noble truths plain. Thus does the meditator see with clear wisdom impermanence, unsatisfactoriness, and non-self"
P722 = [
    ("Rājā āha: “Bhante Nāgasena, kiṃ-lakkhaṇā paññā’”ti?\n“Pubbe’va kho, mahārāja, mayā vuttaṃ: ‘chedana-lakkhaṇā paññā’ti, api ca obhāsana-lakkhaṇā pi paññā’”ti.\n“Kathaṃ, bhante, obhāsana-lakkhaṇā paññā’”ti?",
     "The king said: “Bhante Nāgasena, what does wisdom have as its characteristic mark?”\n“Previously, great king, it was said by me: ‘Wisdom has cutting off as its characteristic mark.’ But wisdom also has illuminating as its characteristic mark.”\n“How, Bhante, does wisdom have illuminating as its characteristic mark?”"),
    (f"“P{_PANNA[1:-1]}ī’”ti.\n“Opammaṃ karohī’”ti.",
     f"“Great king, {_PANNA_EN}.”\n“Give me an illustration.”"),
    (f"“Yathā, mahārāja, puriso andhakāre gehe padīpaṃ paveseyya, paviṭṭho padīpo andhakāraṃ vidhameti, obhāsaṃ janeti, ālokaṃ vidaṃseti, rūpāni pākaṭāni karoti, evameva kho, mahārāja, {_PANNA}. Evaṃ kho, mahārāja, obhāsana-lakkhaṇā paññā’”ti.\n“Kallo’si, bhante Nāgasenā’”ti.",
     f"“It is as if, great king, a man would bring a lamp into a dark house. When the lamp has entered, it would dispel darkness, produce radiance, and spread light, and would make the objects there plainly visible. Just so, great king, {_PANNA_EN}.”\n“You are clever, Bhante Nāgasena.”"),
]

# ---------------------------------------------------------------- 7.2.3
P723 = [
    ("“Bhante Nāgasena, nav’ime puggalā mantitaṃ guyhaṃ vivaranti, na dhārenti. Katame nava? Rāga-carito, dosa-carito, moha-carito, bhīruko, āmisa-garuko, itthī, soṇḍo, paṇḍako, dārako’”ti.\nThero āha: “Tesaṃ ko doso’”ti?",
     "“Bhante Nāgasena, these nine kinds of people reveal a secret that has been discussed with them, and do not preserve it. What nine? The one of lustful character, the one of hating character, the one of deluded character, the coward, one greedy for gain, a woman, a drunkard, a eunuch, a child.”\nThe Elder said: “Of these, what is the fault?”"),
    ("“Rāga-carito, bhante Nāgasena, rāga-vasena mantitaṃ guyhaṃ vivarati, na dhāreti; duṭṭho dosa-vasena mantitaṃ guyhaṃ vivarati, na dhāreti; mūḷho moha-vasena mantitaṃ guyhaṃ vivarati, na dhāreti; bhīruko bhaya-vasena mantitaṃ guyhaṃ vivarati, na dhāreti; āmisa-garuko āmisa-hetu mantitaṃ guyhaṃ vivarati, na dhāreti; itthī ittaratāya mantitaṃ guyhaṃ vivarati, na dhāreti; soṇḍiko surā-lolatāya mantitaṃ guyhaṃ vivarati, na dhāreti; paṇḍako anekaṃsikatāya mantitaṃ guyhaṃ vivarati, na dhāreti; dārako capalatāya mantitaṃ guyhaṃ vivarati, na dhāreti.",
     "“The lustful character, Bhante Nāgasena, on account of lust, reveals a secret that has been discussed, and does not preserve it; the hating character, on account of hatred …; the deluded character, on account of delusion …; a coward, on account of fear …; the one greedy for material gain, to get material goods …; a woman reveals it because of inconstancy [unreliability] …; a drunkard because of his desire for drink …; a eunuch because of his indeterminacy …; a child through fickleness."),
    ("Bhavatī’ha:\n" + verse("Ratto duṭṭho ca mūḷho ca", "bhīru āmisa-cakkhuko", "itthī soṇḍo paṇḍako ca", "navamo bhavati dārako",
                                 "nav’ete puggalā loke", "ittarā calitā calā", "etehi mantitaṃ guyhaṃ", "khippaṃ bhavati pākaṭan’”ti"),
     "“Therefore is it said:\nThe lustful, hating and deluded person,\nthe coward, and one with an eye on material gain,\na woman, a drunkard, a eunuch,\nand the child as ninth –\nthese nine persons in the world\nare unreliable, changeable, fickle.\nWhen secret things are discussed with them,\nthey quickly become well known.”"),
]

# ---------------------------------------------------------------- 7.2.4
P724 = [
    (verse("Middhī yadā hoti mahagghaso ca", "niddāyitā samparivatta-sāyī", "mahā-varāho’va nivāpa-puṭṭho", "punappunaṃ gabbhamupeti mando"),
     "When one is sluggish and gluttonous,\nsleeping and rolling around in bed\nlike a fat pig eating fodder,\nagain and again that dullard goes to the womb.\n(Dhp 325)"),
    (verse("Appamāda-ratā hotha", "sacittamanurakkhatha", "duggā uddharath’attānaṃ", "paṅke sanno’va kuñjaro"),
     "Take delight in heedfulness!\nGuard well your own mind!\nDraw yourself out from this swamp,\nlike an elephant sunk in the mud.\n(Dhp 327)"),
]

META = [
    ("ncrp-6-1-1", "Khp 2", "Dasasikkhāpada", "Five Training Rules", "NCRP Lesson 6 · Initial reading 1", KHP, P611),
    ("ncrp-6-1-2", "AN 5.31", "Sumanāsutta", "Sumanā", "NCRP Lesson 6 · Initial reading 2", AN, P612),
    ("ncrp-6-1-3", "MN 92 (Snp 3.7)", "Selasutta", "Sela", "NCRP Lesson 6 · Initial reading 3", MN, P613),
    ("ncrp-6-1-4", "AN 2.52–55", "Puggalavagga", "Two People", "NCRP Lesson 6 · Initial reading 4", AN, P614),
    ("ncrp-6-1-5", "Snp 3.3", "Subhāsitasutta", "Well Spoken", "NCRP Lesson 6 · Initial reading 5", SNP, P615),
    ("ncrp-6-2-1", "AN 6.55", "Soṇasutta", "Soṇa", "NCRP Lesson 6 · Further reading 1", AN, P621),
    ("ncrp-6-2-2", "AN 7.64", "Kodhanasutta", "The Angry Person", "NCRP Lesson 6 · Further reading 2", AN, P622),
    ("ncrp-6-2-3", "Mil 2.1.8", "Milindapañha", "Reflection and Wisdom", "NCRP Lesson 6 · Further reading 3", MIL_RD, P623),
    ("ncrp-6-2-4", "AN 6.48", "Dutiyasandiṭṭhikasutta", "Directly Visible (2)", "NCRP Lesson 6 · Further reading 4", AN, P624),
    ("ncrp-6-2-5", "Dhp 334–336", "Dhammapada", "Craving", "NCRP Lesson 6 · Further reading 5", DHP, P625),
    ("ncrp-7-1-1", "AN 3.65", "Kesamuttisutta", "The Kālāmas", "NCRP Lesson 7 · Initial reading 1", AN, P711),
    ("ncrp-7-1-2", "AN 4.183", "Sutasutta", "Heard", "NCRP Lesson 7 · Initial reading 2", AN, P712),
    ("ncrp-7-1-3", "Dhp 224, 231–233, 246–247", "Dhammapada", "Anger and Impurity", "NCRP Lesson 7 · Initial reading 3", DHP, P713),
    ("ncrp-7-1-4", "Dhp 328–329", "Dhammapada", "The Wise Companion", "NCRP Lesson 7 · Initial reading 4", DHP, P714),
    ("ncrp-7-2-1", "AN 7.47", "Dutiyaaggisutta", "Three Fires", "NCRP Lesson 7 · Further reading 1", AN, P721),
    ("ncrp-7-2-2", "Mil 2.1.14", "Milindapañha", "Wisdom Illuminates", "NCRP Lesson 7 · Further reading 2", MIL_P, P722),
    ("ncrp-7-2-3", "Mil 4.1.6", "Milindapañha", "Nine Who Cannot Keep a Secret", "NCRP Lesson 7 · Further reading 3", MIL_RD, P723),
    ("ncrp-7-2-4", "Dhp 325, 327", "Dhammapada", "The Elephant", "NCRP Lesson 7 · Further reading 4", DHP, P724),
]

NOTES = """
- 6.1.1: written as in Mor's workshop pañcasīlāni (pāṇ’ātipātā, veramaṇī-sikkhā-padaṃ).
- 6.1.3: the opening sentence (Tena kho pana samayena …) and "Atha kho Selassa brāhmaṇassa etadahosi" are in the
  translation document, not in the book; included. Keṇiy’assamiye jaṭile follows the book (the translation document
  changed it to Keṇiyassa jaṭilassa assame); translation adjusted.
- 6.2.1: the scan's "same guṇe paṭṭhitā" written patiṭṭhitā (translation document, AN 6.55).
- 6.2.4: the book shortens "hoti …"; written out as in the translation document.
- 7.1.2: the translation document's (2)-(4) said "when one speaks … unwholesome qualities decline"; corrected to match (1).
- 7.1.3: Dhp 233 (mano-pakopaṃ) is in the translation document only; included. vacī- with long ī.
- 7.2.2: "Pubbe’va kho" as in the book (pubbe + eva).
- 7.2.3: āmisa-cakkhuko in the verse follows the book (the translation document has āmisagaruko); duṭṭho, mūḷho, soṇḍiko
  in the prose follow the book.
- 7.2.4: the book's "paṅke satto’va" written sanno’va (translation document, Dhp 327: "sunk").
"""
