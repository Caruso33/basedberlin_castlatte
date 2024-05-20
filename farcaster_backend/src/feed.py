import datetime
import os
from typing import List, Any

import requests


from dotenv import load_dotenv

load_dotenv()

NEYNAR_API_KEY = os.getenv("NEYNAR_API_KEY")


def _filter_old_casts(casts):
    threshold_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        hours=48
    )

    filtered_casts = []
    filtered_count = 0

    for cast in casts:
        cast_time = datetime.datetime.fromisoformat(cast["timestamp"])

        if cast_time >= threshold_time:
            filtered_casts.append(cast)

        else:
            filtered_count += 1

    return filtered_casts, filtered_count


def get_following_feed(fid: int) -> List[Any]:

    base_url = f"https://api.neynar.com/v2/farcaster/feed/following"

    query_params = {"fid": fid, "limit": 100, "with_recasts": True}

    following_feed = []

    headers = {"api_key": NEYNAR_API_KEY}

    runs = 0

    while True:
        runs += 1

        url = (
            base_url
            + f"?fid={query_params['fid']}"
            + f"&limit={query_params['limit']}"
            + f"&with_recasts={query_params['with_recasts']}"
        )
        if "cursor" in query_params:
            url += f"&cursor={query_params['cursor']}"

        print(f"url {url}\n")

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Error occurred:", response.text)
            break

        data = response.json()

        [casts, filtered_count] = _filter_old_casts(data["casts"])
        print(f"filtered_count {filtered_count}\n")

        query_params["cursor"] = data["next"]["cursor"]
        following_feed.extend(casts)

        if len(casts) >= 200 or runs > 4:
            break

    print(f"retrieved {len(following_feed)} following feed for fid {fid}\n")

    return following_feed


if __name__ == "__main__":
    get_following_feed(3)
