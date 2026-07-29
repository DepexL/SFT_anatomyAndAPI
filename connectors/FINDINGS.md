# FINDINGS

## 1. Wikipedia Pageviews (`connectors/wikipedia_pageviews.py`)

Wikipedia Pageviews API grąžina JSON objektą su dienos straipsnio peržiūrų statistika. Kiekvienas įrašas turi:

    timestamp – data;
    views – peržiūrų skaičius.

Funkcija priima straipsnio pavadinimą ir datų intervalą (`YYYYMMDD` formatu) bei grąžina dienos peržiūras.

---

### Pastebėjimai

Buvo palygintos 5 temos, kurios per paskutinius 12 mėnesių aiškiai šoktelėjo, ir 5 stabilios temos.

---

### Temos su dideliais šuoliais

- Grand Theft Auto VI
- ChatGPT
- 2026 FIFA World Cup
- Nvidia
- Donald Trump

Didžiausias šuolis buvo matomas 2026 FIFA World Cup straipsnyje. Turnyro metu peržiūros padidėjo nuo dešimčių tūkstančių iki daugiau nei 1,5 milijono per dieną.

Taip pat aiškūs šuoliai buvo matomi Nvidia, Donald Trump ir Grand Theft Auto VI straipsniuose, kai įvykdavo svarbūs įvykiai ar naujienos.

Pavyzdys (2026 FIFA World Cup)

| Laikas     | Peržiūros |
| 2025-07-01 | 28127     |
| 2025-07-31 | 22510     |
| 2025-08-30 | 25730     |
| 2025-09-29 | 29278     |
| 2025-10-29 | 26144     |
| 2025-11-28 | 44385     |
| 2025-12-28 | 34627     |
| 2026-01-27 | 36702     |
| 2026-02-26 | 48423     |
| 2026-03-28 | 75715     |
| 2026-04-27 | 47143     |
| 2026-05-27 | 136164    |
| 2026-06-26 | 1543683   |
| 2026-07-26 | 90165     |

---

## Stabilios temos

- Sun
- Machine learning
- Python (programming language)
- Piano
- OpenAI

Šių straipsnių peržiūros svyravo nedaug ir neturėjo labai didelių vienadienių šuolių.

Pavyzdys (Piano)

| Laikas     | Peržiūros |
| 2025-07-01 | 1625      |
| 2025-07-31 | 1211      |
| 2025-08-30 | 1280      |
| 2025-09-29 | 1896      |
| 2025-10-29 | 1526      |
| 2025-11-28 | 1643      |
| 2025-12-28 | 1888      |
| 2026-01-27 | 1883      |
| 2026-02-26 | 1749      |
| 2026-03-28 | 1332      |
| 2026-04-27 | 1866      |
| 2026-05-27 | 1593      |
| 2026-06-26 | 1367      |
| 2026-07-26 | 1406      |

---

### Ar skirtumas matomas vien iš peržiūrų?

Taip. Aktualių naujienų ar įvykių temos turi ryškius peržiūrų šuolius, o stabilios temos išlieka panašiame lygyje visus metus.

---

### Vėlavimas

Wikipedia Pageviews API pateikia dienos statistiką, todėl įvykio poveikis dažniausiai matomas tą pačią arba kitą dieną.

---

### Istoriniai duomenys ir granuliarumas

- Granuliarumas – dienos.
- API leidžia pasiekti kelerių metų istorinius duomenis.
- API raktas nereikalingas, tačiau rekomenduojama naudoti aiškų `User-Agent`.

---

### Apribojimai

- Nėra valandinių duomenų.
- Reikia tiksliai nurodyti straipsnio pavadinimą.
- Didelis užklausų kiekis gali būti ribojamas.

---

### Kas nustebino

API yra labai paprasta naudoti ir nereikalauja autentifikacijos. Peržiūrų statistika gana aiškiai atspindi didelius pasaulio įvykius.

---

## 2. Hacker News (`connectors/hackernews_spike.py`)

> Pradinėje užduotyje buvo numatytas Reddit konektorius, tačiau dėl pasikeitusios Reddit API registracijos tvarkos užduotis buvo pakeista į Hacker News.

### Duomenų struktūra

Naudotos dvi API:

- Hacker News Firebase API;
- Hacker News Algolia Search API.

Iš Firebase API gaunami:

- pavadinimas (`title`);
- score;
- komentarų skaičius (`descendants`);
- paskelbimo laikas (`time`);
- URL.

pavyzdys

| Pavadinimas | Taškai | Komentarai | Laikas                  | URL                                                                           |
| KOReader    | 46     | 8          | 2026-07-29 14:05:08 UTC | https://enklypesalt.com/posts/context-collapse-part3-ai-worming-through-word/ |

Iš Algolia API galima atlikti paiešką pagal raktažodžius.

---

### Temos analizė

Buvo atlikta paieška pagal temą"artificial intelligence".

Rezultatai parodė naujausius įrašus su jų:

- score;
- komentarų skaičiumi;
- paskelbimo data.

Tai leidžia stebėti, kokios temos pradeda populiarėti Hacker News bendruomenėje.

pavyzdys

| Pavadinimas                                                                     | Taškai | Komentarai | Laikas              |
| Unpacking Open Source AI: Toward a Framework for Openness in Foundation Models  | 2      | 0          | 2026-07-29 10:24:42 |
| New York school pauses plan to deploy humanlike AI robot teacher after backlash | 5      | 0          | 2026-07-28 22:15:02 |
| Artificial Intelligence Is Artificial Thinking                                  | 2      | 0          | 2026-07-28 19:16:03 |

---

### Rate limit

Bandymų metu nepastebėtas griežtas rate limit. API leidžia atlikti daug skaitymo užklausų be autentifikacijos.

---

### Apribojimai

- Firebase API neturi sudėtingos paieškos.
- Paieškai naudojama papildoma Algolia API.
- Auditorija orientuota daugiausia į technologijas ir startupus.

---

### Kas nustebino

Hacker News API yra visiškai atvira, nereikalauja API rakto ir leidžia labai paprastai pasiekti populiariausias istorijas bei jų statistiką.

---