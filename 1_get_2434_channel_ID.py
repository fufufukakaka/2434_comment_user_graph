import requests
from bs4 import BeautifulSoup
import json

target_url = "https://2434.fun/channels"


def main():
    r = requests.get(target_url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    streamer_names = [
        v.text for v in soup.find_all("a", attrs={"class": "channel-owner"})
    ]
    channel_URL = [
        v["href"] for v in soup.find_all("a", attrs={"class": "youtube-channel"})
    ]
    config_json = {}
    for name, url in zip(streamer_names, channel_URL):
        config_json[name] = url

    with open("config/2434_streamer_channel_IDs.json", "w") as f:
        json.dump(config_json, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
