# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///

import requests


def get_pageviews(article, start_date, end_date):
    """
    Gauna Wikipedia straipsnio dienos peržiūras.

    article:
        Straipsnio pavadinimas

    start_date:
        YYYYMMDD

    end_date:
        YYYYMMDD
    """

    article = article.replace(" ", "_")

    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"en.wikipedia/all-access/all-agents/"
        f"{article}/daily/"
        f"{start_date}/{end_date}"
    )

    headers = {
        "User-Agent": "AI-Praktikantas/1.0 liutauraskuzma1@gmail.com"
    }

    response = requests.get(
        url,
        headers=headers
    )

    response.raise_for_status()

    data = response.json()

    result = []

    for item in data["items"]:
        result.append({
            "date": item["timestamp"][:8],
            "views": item["views"]
        })

    return result


if __name__ == "__main__":

    big_spikes = [
        "Grand Theft Auto VI",
        "ChatGPT",
        "2026 FIFA World Cup",
        "Nvidia",
        "Donald Trump"

    ]

    stable_spikes = [
        "Sun",
        "Machine learning",
        "Python (programming language)",
        "Piano",
        "OpenAI"
    ]

    for article in big_spikes:
        views = get_pageviews(
            article,
            "20250701",
            "20260729"
        )
        print(f"\n{article} peržiūros:")
        for day in views[::30]:
            print(day)

    for article in stable_spikes:
        views = get_pageviews(
            article,
            "20250701",
            "20260729"
        )
        print(f"\n{article} peržiūros:")
        for day in views[::30]:
            print(day)
