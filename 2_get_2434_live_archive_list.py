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

    for streamer_name, channel_URL in channel_ID_config.items():
        if os.path.exists(f"video_list_output/{streamer_name}_videos.csv"):
            print(f"already exists: {streamer_name}")
            continue
        print(f"now processing...{streamer_name}")
        CHANNEL_ID = channel_URL.split("/")[-1]
        url = (
            base_url
            + "/search?key=%s&channelId=%s&part=snippet,id&order=date&maxResults=50"
        )
        infos = []

        # quotaを節約するために最新50件のみ取得する
        time.sleep(10)
        response = requests.get(url % (API_KEY, CHANNEL_ID))
        if response.status_code != 200:
            print("exit by error")
            continue

        result = response.json()
        infos.extend(
            [
                [
                    streamer_name,
                    item["id"]["videoId"],
                    item["snippet"]["title"],
                    item["snippet"]["description"],
                    item["snippet"]["publishedAt"],
                ]
                for item in result["items"]
                if item["id"]["kind"] == "youtube#video"
            ]
        )

        if "nextPageToken" in result.keys():
            if "pageToken" in url:
                url = url.split("&pageToken")[0]
            url += f'&pageToken={result["nextPageToken"]}'
        else:
            print("success")

        videos = pd.DataFrame(
            infos,
            columns=["streamer_name", "videoId", "title", "description", "publishedAt"],
        )
        videos.to_csv(f"video_list_output/{streamer_name}_videos.csv", index=None)


if __name__ == "__main__":
    main()
