# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///

import requests
from datetime import datetime


HN_API = "https://hacker-news.firebaseio.com/v0"


def get_story(story_id):
    """
    Gauna vienos Hacker News istorijos informaciją.
    """

    url = f"{HN_API}/item/{story_id}.json"

    response = requests.get(url)

    response.raise_for_status()

    return response.json()


def get_top_stories(limit=50):
    """
    Gauna populiariausias Hacker News istorijas.
    """

    url = f"{HN_API}/topstories.json"

    response = requests.get(url)

    response.raise_for_status()

    story_ids = response.json()

    stories = []

    for story_id in story_ids[:limit]:

        story = get_story(story_id)

        if story:

            stories.append({
                "title": story.get("title"),
                "score": story.get("score"),
                "comments": story.get("descendants", 0),
                "time": datetime.fromtimestamp(
                    story.get("time")
                ).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "url": story.get("url")
            })

    return stories



def search_topic(topic, limit=20):
    """
    Ieško istorijų pagal temą naudojant Algolia API.
    """

    url = "https://hn.algolia.com/api/v1/search_by_date"

    params = {
        "query": topic,
        "tags": "story",
        "hitsPerPage": limit
    }

    response = requests.get(
        url,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data["hits"]:

        results.append({
            "title": item.get("title"),
            "points": item.get("points"),
            "comments": item.get("num_comments"),
            "date": item.get("created_at")
        })

    return results

def search_topic_by_time(topic, start_time, end_time, limit=20):
    """
    Ieško istorijų pagal temą ir laiko intervalą naudojant Algolia API.
    """

    url = "https://hn.algolia.com/api/v1/search_by_date"

    start_timestamp = int(start_time.timestamp())
    end_timestamp = int(end_time.timestamp())

    params = {
        "query": topic,
        "tags": "story",
        "hitsPerPage": limit,
        "numericFilters": [
            f"created_at_i>={start_timestamp}",
            f"created_at_i<={end_timestamp}"
        ]
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    results = []

    for item in data["hits"]:
        results.append({
            "title": item.get("title"),
            "points": item.get("points"),
            "comments": item.get("num_comments"),
            "date": item.get("created_at")
        })

    return results

if __name__ == "__main__":

    stories = get_top_stories(10)

    print("\nTOP Hacker News istorijos:\n")

    for story in stories:
        print(story)


    print("\nAI temos paieška:\n")

    ai_posts = search_topic(
        "artificial intelligence",
        10
    )

    for post in ai_posts:
        print(post)

    print("\nAI temos paieška pagal laiką:\n")
    start_time = datetime(2025, 7, 1)
    end_time = datetime(2026, 7, 29)
    ai_posts_by_time = search_topic_by_time(
        "2026 FIFA World Cup",
        start_time,
        end_time,
        100
    )
    for post in ai_posts_by_time:
        print(post) 