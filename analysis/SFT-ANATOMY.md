# DR-Tulu SFT Dataset Anatomy

## 1. Dataset struktūra

Dataset buvo analizuotas iš:

`data/dr-tulu-sft-cleaned/deep-research-tulu-sft-data-cleaned.parquet`

Bendras dataset dydis:

- Įrašų skaičius: 12 010
- Laukų skaičius: 8

Top-level laukai:

| Laukas           | Aprašymas                             |
| id               | Unikalus įrašo identifikatorius       |
| source_id        | Originalaus šaltinio identifikatorius |
| question         | Pradinė vartotojo užklausa            |
| source           | Dataset šaltinis                      |
| type             | Klausimo tipas                        |
| num_tool_calls   | Įrankių iškvietimų skaičius           |
| tokenized_length | Apytikslis tokenų kiekis              |
| conversations    | Pokalbio eiga su role ir content      |

Vienas įrašas susideda iš kelių pokalbio žingsnių:

    system - sistemos instrukcijos ir įrankių aprašymas
    user - vartotojo klausimas
    reasoning - modelio mąstymo žingsniai
    tool_call - įrankio iškvietimas JSON formatu
    tool_output - įrankio grąžinti duomenys
    answer - galutinis atsakymas

---

## 2. Naudojami įrankiai

Dataset naudojami įrankiai:

| Įrankis                    | Iškvietimų kiekis |
| google_search              | 17277             |
| browse_webpage             | 3687              |
| snippet_search             | 21367             |
| search_papers_by_relevance | 14                |

Įrankiai kviečiami per:

```xml
<tool_call>
{"name": "tool_name", "arguments": {...}}
</tool_call>
```

formatą.

---

## 3. Įrankių argumentai

Išanalizavus `tool_call` įrašus nustatyti naudojami argumentai.

| Tool                       | Argumentas       | Tipas    | Pavyzdinė reikšmė                                    |
| google_search              | query            | str      | AMD EPYC LLM inference user feedback Reddit          |
| google_search              | num              | int      | 10                                                   |
| google_search              | gl               | str      | us                                                   |
| google_search              | hl               | str      | en                                                   |
| google_search              | limit            | int      | 10                                                   |
| browse_webpage             | query            | str      | https://www.reddit.com/...                           |
| snippet_search             | query            | str      | CO2 plume detection power plant                      |
| snippet_search             | limit            | int      | 10                                                   |
| snippet_search             | year             | str, int | 2022-2025                                            |
| snippet_search             | fieldsOfStudy    | str      | Environmental Science,Engineering                    |
| snippet_search             | minCitationCount | int      | 300                                                  |
| snippet_search             | venues           | str      | ICWSM,WWW,TheWebConf                                 |
| search_papers_by_relevance | query            | str      | Stringency of COVID-19 Containment Response Policies |
| search_papers_by_relevance | year             | str, int | 2020-2025                                            |
| search_papers_by_relevance | fieldsOfStudy    | str      | Environmental Science,Public Health                  |
| search_papers_by_relevance | limit            | int      | 5                                                    |

---

## 4. Trajektorijų ilgis

Kiekvienam pavyzdžiui buvo suskaičiuotas `tool_call` kiekis.

Rezultatai:

| Metodas    | Reikšmė |
| Minimumas  | 0       |
| Maksimumas | 63      |
| Mediana    | 3.0     |

Grandinių tipai:

| Tipas                                 | Kiekis |
| Vienas įrankio iškvietimas            | 848    |
| Daugiažingsnė grandinė (>1 tool_call) | 11015  |

Dataset daugiažingsnės grandinės atrodo taip:

user -> reasoning -> tool_call -> tool_output -> reasoning -> tool_call -> tool_output -> answer


---

## 5. Galutinių atsakymų formatas

### Answer žymas

Atsakymas pateikiamas:

```xml
<answer>
Galutinis atsakymas
</answer>
```

### Trumpi atsakymai

Trumpiems atsakymams naudojamas:

```
\boxed{}
```

formatas.

---

### Citavimas

Informacija gauta iš įrankių cituojama inline:

```xml
<cite id="SNIPPET_ID">
Tekstas paremtas šaltiniu
</cite>
```

Pavyzdys:
1.--------------------------

```xml
<answer>\boxed{92%}</answer>
```

2.--------------------------

```xml
<answer>
Robert K. Merton nustatė 92% dispute rate.
<cite id="S_UD6WfAE">
Robert K. Merton found that 92% of cases...
</cite>
</answer>
```

Citatos nurodo konkrečius paieškos rezultatų snippet ID.

---

## 6. Sugadinti įrašai

Buvo tikrinamos galimos dataset problemos:

| Tikrinimas                | Kiekis |
| Lūžę JSON argumentai      | 0      |
| Tušti atsakymai           | 0      |
| Nutrūkusios trajektorijos | 0      |

Patikrinimo metu nenustatyta sugadintų įrašų.

Papildomai dataset dokumentacijoje nurodoma, kad galutinė versija buvo išvalyta ir validuota:

- Galutinis dydis: 12 010 pavyzdžių
- JSON klaidos: 0
- Validuoti tool_call įrašai: 100%

---

## Išvada

DR-Tulu SFT dataset yra skirtas mokyti kalbos modelius naudoti įrankius atliekant tyrimo užduotis.

Svarbiausi pastebėjimai:

- Duomenys yra multi-turn formato.
- Įrankių naudojimas vyksta per JSON pagrįstus `tool_call`.
- Dažniausiai naudojami paieškos įrankiai.
- Argumentų struktūra turi būti išsaugota norint ateityje perrašyti dataset į naują įrankių formatą.
- Galutiniai atsakymai naudoja citatas, susietas su paieškos rezultatais.

Ši analizė leidžia suprasti dataset struktūrą prieš atliekant tolimesnį fine-tuning duomenų paruošimą.

---