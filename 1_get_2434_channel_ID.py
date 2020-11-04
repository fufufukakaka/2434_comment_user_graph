from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

target_url = "https://www.itsukaralink.jp/livers"


def main():
    options = Options()
    options.set_headless(True)
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(target_url)

    soup = BeautifulSoup(driver.page_source.encode("utf-8"), "html.parser")
    # 最後はにじさんじ公式のため除く
    streamer_names = [
        v.text for v in soup.find_all("span", attrs={"class": "liver-followBoxText"})
    ][:-1]
    channel_URL = [
        v.a["href"].split("?")[0]
        for v in soup.find_all("div", attrs={"class": "liver-linkImage"})
        if "youtube" in v.a["href"]
    ][:-1]
    print(channel_URL)
    config_json = {}
    for name, url in zip(streamer_names, channel_URL):
        config_json[name] = url

    with open("config/2434_streamer_channel_IDs.json", "w") as f:
        json.dump(config_json, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
