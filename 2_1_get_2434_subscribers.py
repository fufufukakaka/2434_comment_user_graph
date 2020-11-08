import json
import pandas as pd
import requests
import os
import time


def main():

    API_KEY = os.environ["API_KEY"]
    base_url = "https://www.googleapis.com/youtube/v3"

    with open("config/2434_streamer_channel_IDs.json", "r") as f:
        channel_ID_config = json.load(f)

    infos = []
    for streamer_name, channel_URL in channel_ID_config.items():
        print(f"now processing...{streamer_name}")
        CHANNEL_ID = channel_URL.split("/")[-1]
        url = base_url + "/channels?part=statistics&id=%s&key=%s"

        response = requests.get(url % (CHANNEL_ID, API_KEY))
        if response.status_code != 200:
            print("exit by error")
            continue

        result = response.json()
        infos.append(
            [streamer_name, result["items"][0]["statistics"]["subscriberCount"]]
        )
    infos = pd.DataFrame(
        infos,
        columns=["streamer_name", "subscriberCount"],
    )
    infos.to_csv(f"subscribe_count.csv", index=None)


if __name__ == "__main__":
    main()
