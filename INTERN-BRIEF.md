# Praktikanto užduotys

Sveikas!

Trumpai apie tai, ką darome: kuriame DI sistemą, kuri stebi interneto tendencijas,
aptinka kylančias temas ir automatiškai ištiria, kodėl jos auga - tada parašo ataskaitą
su šaltiniais. Projektas dar tik prasideda, tai kodo bazės kaip ir nėra - dirbsi nuo
nulio ir nieko sugadinti negalėsi.

Užduotys savarankiškos - nereikės nieko laukti iš kitų. Daryk iš eilės, savo tempu:
kiek spėsi, tiek spėsi. Ir tai nėra užimtumo kūrimas - rezultatus realiai naudosime.

---

## Pasiruošimas

Veikia bet kurioje OS - Windows, macOS, Linux.

1. Įsidiek `git`, jei dar neturi: https://git-scm.com/downloads
2. Įsidiek `uv`:
   - Linux / macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
3. Šiame aplanke paleisk:
   ```
   uv run bootstrap.py --check   # patikrina, ar viskas tvarkoje
   uv run bootstrap.py           # parsisiunčia ~760 MB duomenų
   ```
   `uv` pats parsisiųs reikiamą Python versiją - nieko atskirai diegti nereikia.

Savo skriptams naudok Python 3.11 (`uv venv --python 3.11` arba tiesiog
`uv run skriptas.py`) - naujausių Python versijų mūsų bibliotekos dar nepalaiko.

Jokių paskyrų ar API raktų šiam etapui nereikia - duomenų rinkiniai vieši.
(Reddit paskyra prireiks tik 2 užduotyje.)

---

## 1 užduotis - Išsiaiškink, kas iš tikrųjų yra SFT duomenyse

Vėliau derinsime (fine-tune) kalbos modelį naudodami `data/dr-tulu-sft-cleaned` rinkinį -
12 010 pavyzdžių. Prieš tai reikia tiksliai žinoti, kokios formos tie duomenys, nes
kiekvieną pavyzdį reikės perrašyti taip, kad jis naudotų mūsų įrankius vietoj tų, su
kuriais rinkinys buvo sukurtas.

Parašyk Python skriptą (`analysis/sft_anatomy.py`), kuris užkrauna rinkinį ir atsako:

1. **Įrašo struktūra.** Kokie top-level laukai? Kaip atrodo vienas pilnas pavyzdys nuo
   pradžios iki galo? Gražiai atspausdink du ar tris pilnus.
2. **Kokie įrankiai naudojami ir kaip dažnai?** Rinkinys suktas apie įrankius tipo
   `google_search` ir `browse_webpage`. Reikia tikslaus sąrašo su dažniais.
3. **Kokius argumentus priima kiekvienas įrankis?** Argumentų pavadinimai, tipai,
   pavyzdinė reikšmė. Čia svarbiausia dalis - padaryk lentelę.
4. **Kokio ilgio trajektorijos?** Įrankių iškvietimų skaičius pavyzdyje: min, max,
   mediana. Kiek vieno iškvietimo, kiek tikrų daugiažingsnių grandinių?
5. **Kaip formatuojami galutiniai atsakymai?** Citatos inline? Išnašose? Parodyk porą
   realių pavyzdžių.
6. **Ar yra sugadintų įrašų?** Lūžęs JSON argumentuose, tušti atsakymai, nutrūkusios
   trajektorijos. Apytikslis kiekis.

Tada surašyk išvadas į `analysis/SFT-ANATOMY.md` - tekstu, su lentelėmis. Tikslas, kad
kolega perskaitytų per penkias minutes ir suprastų, su kuo turi reikalą. Jei kuri dalis
pasirodys neįdomi, vienas sakinys ir yra teisingas ilgis.

Kam to reikia: visus tuos 12 tūkstančių pavyzdžių vėliau reikės perrašyti mūsų įrankių
formatui. Kuo tiksliau dabar žinosime argumentų formas, tuo mažiau skausmo bus tada.
Tavo ataskaita bus tiesioginis įnašas į tą sprendimą.

---

## 2 užduotis - Du duomenų šaltinių konektoriai

Sistema trauks duomenis iš kelių šaltinių. Du iš jų visiškai nemokami ir nereikalauja
jokių patvirtinimų, tai juos gali pasidaryti pats.

Kokybė gali būti vienkartinė - tai bandymai išsiaiškinti, kaip API elgiasi iš tikrųjų,
o ne produkcinis kodas. Vėliau juos kažkas perrašys normaliai.

### Wikipedia Pageviews (`connectors/wikipedia_pageviews.py`)

API rakto nereikia. Tik nustatyk aiškų `User-Agent` headerį su realiu kontaktu - kitaip
gali apriboti užklausas.

Parašyk funkciją, kuri priima straipsnio pavadinimą ir datų intervalą, o grąžina dienos
peržiūras. Tada su ja atsakyk (lentele ar grafiku):

- Išsirink 5 temas, kurios per paskutinius 12 mėn. aiškiai šoktelėjo, ir 5 nuobodžiai
  stabilias. Ar matosi skirtumas vien iš peržiūrų?
- Koks vėlavimas? Kai kažkas išsprogsta, per kiek laiko tai pasimato Wikipedia
  peržiūrose?
- Kiek toli atgal siekia duomenys ir koks granuliarumas?

### Reddit (`connectors/reddit_spike.py`)

Užsiregistruok script-tipo aplikaciją reddit.com/prefs/apps - dvi minutės, nemokama,
daryk su savo paskyra. Tada naudok PRAW.

Parašyk funkciją, kuri ištraukia naujausius postus iš subreddito su score, komentarų
skaičiumi ir laiku. Tada:

- Patrauk iš `r/marketing`, `r/entrepreneur`, `r/startups` - mūsų būsimi naudotojai
  skaito būtent šiuos.
- Koks realus rate limit? Rask praktinę lubą.
- Ar gali pastebėti temą, įgaunančią pagreitį, vien iš postų kiekio ir score? Pabandyk.

### Surašyk

`connectors/FINDINGS.md`. Kiekvienam šaltiniui: kaip atrodo duomenys, kokie apribojimai,
koks šviežumas ir - naudingiausia - kas nustebino. Nedokumentuotas elgesys, dalykai,
kurie veikia ne taip, kaip rašo dokumentacija, rate limitai, kurie kanda anksčiau nei
skelbiama. Būtent tokie dalykai vėliau kainuoja dienas, jei niekas jų neužrašo.

---

## 3 užduotis (papildoma, jei baigei ankstesnes)

Sukryžmink abu šaltinius. Paimk vieną temą, kuri šoktelėjo, ir ištrauk jos Wikipedia
peržiūras bei Reddit aktyvumą tame pačiame laiko lange. Ar signalai sutampa? Kuris
pajuda pirmas?

Tai iš esmės pagrindinis viso produkto klausimas - ar kelių šaltinių sujungimas duoda
daugiau nei bet kuris vienas. Net grubus atsakymas yra vertingas.

---

## Kaip dirbti

- Bendros repozitorijos dar neturime. Susikurk lokalų git'ą (`git init`) savo darbo
  aplanke ir commit'ink ten - maži commit'ai, dėl grožio nesijaudink. Kai turėsime
  bendrą repo, viską perkelsime.
- Jokių raktų ar slaptažodžių į failus, kuriuos commit'ini. Raktus laikyk `.env` faile
  ir įsirašyk jį į `.gitignore` pirmu commit'u.
- Viskas, ko reikia, yra nemokama: Wikipedia, Reddit, Hugging Face. Jei kažkur prašo
  banko kortelės - sustok, to nereikia.
- Įstrigai ilgiau nei ~30 min? Užsirašyk, ką bandei, ir eik prie kito punkto. Grįši
  vėliau. Sąrašas „štai kas neveikė" yra visiškai normalus rezultatas.
- Galutinis rezultatas - markdown failai: `SFT-ANATOMY.md`, `FINDINGS.md` ir (jei
  spėjai) papildomos užduoties išvados. Kada juos atiduosi, priklauso nuo tempo -
  spaudimo nėra.

Klausk, kai užstringi. Geriau paklausti nei prasėdėti valandą.
