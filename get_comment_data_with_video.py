import pandas as pd
import requests
import os
from pytchat import Extractor, VideoInfo, TSVArchiver
from pytchat.exceptions import InvalidVideoIdException

import signal, os


def disp(*args):
    print(".", end="", flush=True)


def main():
    video_id = "eu90PK3bpuw"
    save_path = "test.txt"
    archiver = TSVArchiver(save_path)

    try:
        # Extractorの生成
        ex = Extractor(video_id, div=10, callback=disp, processor=archiver)
    except InvalidVideoIdException as e:
        print(e)
        exit(0)

    # Ctrl+Cでキャンセルする
    signal.signal(signal.SIGINT, (lambda a, b: ex.cancel()))

    # 抽出の開始
    info = VideoInfo(video_id)
    if info.get_duration() == 0:
        print("指定した動画はアーカイブされていないか、チャットデータが存在しません")
        exit(0)
    print("Extracting: " + info.get_title())
    print(
        "Save path: ",
        os.path.realpath(save_path)[: -len(os.path.basename(save_path))]
        + os.path.basename(archiver.save_path),
    )
    result = ex.extract()

    # 抽出完了
    print("\nFinished extraction.")


if __name__ == "__main__":
    main()
