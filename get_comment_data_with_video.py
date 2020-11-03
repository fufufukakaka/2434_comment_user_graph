import pandas as pd
import os
from pytchat import Extractor, VideoInfo, TSVArchiver
from pytchat.exceptions import InvalidVideoIdException

import signal, os


def disp(*args):
    print(".", end="", flush=True)


def main():
    all_video_list = pd.read_csv("concat_video_list.csv")
    video_author_list = (
        all_video_list.groupby(["streamer_name"])["videoId"].apply(list).reset_index()
    )
    video_author_list["video_num"] = video_author_list["videoId"].apply(len)
    video_author_list = video_author_list.query("video_num > 30")
    video_author_list["use_videos"] = video_author_list["videoId"].apply(
        lambda x: x[:30]
    )
    streamers = video_author_list["streamer_name"].unique()
    for idx, s in enumerate(streamers):
        print(f"now: {idx}/{len(streamers)}")
        video_list = video_author_list.query(f"streamer_name == @s")[
            "use_videos"
        ].values[0]
        for video_id in video_list:
            save_path = f"comment_list_output/{video_id}.csv"
            if os.path.exists(save_path):
                print(f"already exists: {video_id}")
                continue
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
            try:
                result = ex.extract()
            except BaseException:
                print("コメント取得時にエラー")

            # 抽出完了
            print("...Finised")


if __name__ == "__main__":
    main()
