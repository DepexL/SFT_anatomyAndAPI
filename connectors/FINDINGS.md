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
| - | - |
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
| - | - |
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

Pavyzdys

| Pavadinimas | Taškai | Komentarai | Laikas                  | URL                                                                           |
| - | - | - | - | - |
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

Pavyzdys

| Pavadinimas                                                                     | Taškai | Komentarai | Laikas              |
| - | - | - | - |
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

## 3 užduotis – Wikipedia ir Hacker News palyginimas

### Pasirinkta tema

2026 FIFA World Cup

### Stebėjimai

Hacker News paieška parodė, kad su 2026 FIFA World Cup susiję įrašai buvo publikuojami visą analizuojamą laikotarpį. Tačiau birželio–liepos mėnesiais jų kiekis akivaizdžiai padidėjo. Taip pat atsirado daugiau įrašų su didesniu `score` ir komentarų skaičiumi, kas rodo išaugusį bendruomenės susidomėjimą.

Wikipedia Pageviews duomenyse matomas dar ryškesnis pokytis. Iki 2026 m. gegužės straipsnio peržiūros buvo gana stabilios (apie 20–75 tūkst. per dieną), gegužės pabaigoje jos išaugo iki ~136 tūkst., o birželio pabaigoje pasiekė daugiau kaip 1,5 mln. peržiūrų per dieną.

Pavyzdys Hacker News

| Pavadinimas                                                                      | Taškai | Komentarai | Laikas               |
| - | - | - | - |
| FIFA World Cup-A Technological Revolution and New Standard for Live Broadcasting | 2      | 1          | 2026-07-20T20:32:18Z | 
| How to Watch the 2026 FIFA World Cup Finals: Spain vs. Argentina                 | 2      | 0          | 2026-07-19T11:02:34Z | 
| FIFA World Cup 2026 Data Portraits                                               | 37     | 14         | 2026-07-16T22:21:59Z | 
| FIFA World Cup 2026 · Data Portraits                                             | 1      | 1          | 2026-07-15T03:01:09Z | 
| FIFA World Cup 2026 · Data Portraits                                             | 3      | 1          | 2026-07-09T20:15:29Z | 
| Statistical Analysis on World Cup Bias [pdf]                                     | 2      | 0          | 2026-07-09T16:17:48Z | 
| Trump intervention causes World Cup storm as FIFA clears US striker Balogun      | 15     | 6          | 2026-07-06T15:36:39Z | 
| Trump Asked FIFA to Review U.S. Player's Suspension. Now He's Eligible to Play   | 26     | 14         | 2026-07-05T22:11:11Z | 
| The AI-powered World Cup runs on thousands of data workers                       | 5      | 0          | 2026-07-02T13:27:42Z | 
| FIFA WORLD CUP 2026 Live widget using Orbit, zumly libs                          | 2      | 0          | 2026-07-01T12:36:05Z | 
| Show HN: FIFA 2026 bracket predictor – see live crowd % as picks come in         | 2      | 1          | 2026-06-27T23:57:17Z | 
| 2026 FIFA Worldcup Predictor                                                     | 1      | 2          | 2026-06-27T04:04:14Z | 
| Show HN: OpenSoccer – open-source soccer game in browser in 128 prompts          | 3      | 0          | 2026-06-23T16:04:26Z | 
| The AI-powered World Cup runs on thousands of data workers                       | 1      | 0          | 2026-06-23T14:17:56Z | 
| FIFA's World Cup Typography Foul: UI Design Learnings                            | 2      | 2          | 2026-06-23T12:47:54Z | 
| World Cup 2026 qualification calculator from FIFA Docs                           | 3      | 2          | 2026-06-22T15:38:24Z | 
| FIFA World Cup 2026: 45 Cameras Will Capture Every Moment of the Action          | 2      | 0          | 2026-06-20T22:08:17Z | 
| Show HN: No-Nonsense Table of FIFA World Cup 2026 Top Scorers and Assist Leaders | 2      | 0          | 2026-06-17T19:06:17Z | 
| Bug in FIFA World Cup internal system gave anyone ability to modify TV stream    | 3      | 1          | 2026-06-16T18:41:46Z | 
| Post‑match summary reports for all FIFA World Cup 2026                           | 3      | 3          | 2026-06-13T21:10:19Z | 
| Apple Made a Sports App That Does Almost Nothing. It's Incredible                | 22     | 15         | 2026-06-10T19:43:20Z | 
| World Cup 2026: Does referee case show FIFA has lost control of its tournament?  | 5      | 0          | 2026-06-09T23:33:47Z | 
| World Cup 2026 predictor with FIFA's full Annex C bracket logic                  | 3      | 0          | 2026-06-09T03:52:39Z | 
| Show HN: I revived Scoragora, a World Cup prediction game                        | 2      | 0          | 2026-06-08T11:48:49Z | 
| 2026 FIFA World Cup Squads                                                       | 2      | 0          | 2026-06-01T16:03:46Z | 
| NY and NJ subpoena FIFA over 'manipulated' World Cup ticketing                   | 8      | 3          | 2026-05-28T21:07:33Z | 
| Show HN: World Cup History MCP – every FIFA tournament 1930–2026                 | 1      | 4          | 2026-05-12T07:30:54Z | 
| FIFA World Cup's best shirts are 30 years old                                    | 2      | 0          | 2026-04-10T10:53:34Z | 
| FIFA raises World Cup final top ticket price to $10,990, up from $1,600 in 2022  | 3      | 5          | 2026-04-02T20:43:57Z | 
| World Cup games in Boston at risk                                                | 1      | 0          | 2026-03-04T13:58:13Z | 
| FIFA World Cup 2026                                                              | 1      | 1          | 2026-01-31T08:55:26Z | 
| The influencer World Cup: FIFA and TikTok deal targeting an avalanche of posts   | 2      | 0          | 2026-01-24T12:06:39Z | 
| Do World Cup teams need a 50% prize money hike after tickets furore?             | 1      | 0          | 2026-01-20T14:54:39Z | 
| FIFA Arrives on Netflix Games                                                    | 37     | 49         | 2025-12-17T20:10:12Z | 
| FIFA's 2026 ticket scheme is a late-capitalist hellscape                         | 50     | 19         | 2025-10-26T21:00:54Z | 
| FIFA's 2026 ticket scheme is a late-capitalist hellscape                         | 5      | 1          | 2025-10-11T13:38:46Z | 
| FIFA Turns World Cup Tickets into a Variable-Priced Luxury Marketplace           | 6      | 2          | 2025-09-08T21:39:42Z | 
| 2026 FIFA World Cup expansion will have a big climate footprint                  | 5      | 2          | 2025-07-27T22:22:49Z | 

Pavyzdys Wikipedia pageviews

| Laikas     | Peržiūros |
| - | - |
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

### Ar signalai sutampa?

Taip. Abu šaltiniai rodo padidėjusį susidomėjimą ta pačia tema 2026 m. birželio–liepos mėnesiais.

### Kuris pajuda pirmas?

Hacker News pradėjo rodyti daugiau įrašų apie pasaulio čempionatą dar prieš didžiausią Wikipedia peržiūrų šuolį. Tuo tarpu Wikipedia didžiausias peržiūrų pikas pasirodė jau prasidėjus pagrindiniams įvykiams.

### Išvada

Abu šaltiniai papildo vienas kitą. Hacker News leidžia anksti pastebėti, kad tema tampa aktyvi technologijų bendruomenėje, o Wikipedia Pageviews parodo, kada tema pradeda domėtis daug platesnė auditorija. Todėl kelių šaltinių naudojimas suteikia daugiau informacijos nei vien tik Wikipedia arba vien tik Hacker News.
