import os
import pandas as pd
from tqdm.auto import tqdm


def main():
    concat_video_list = pd.read_csv("concat_video_list.csv")
    video_id_list = concat_video_list["videoId"].values
    author_list = []
    for video_id in tqdm(video_id_list):
        video_path = f"comment_list_output/{video_id}.csv"
        if os.path.exists(video_path):
            _video = pd.read_csv(video_path, sep="\t")
            _authors = _video["authorChannel"].unique().tolist()
        else:
            _authors = []
        author_list.append(_authors)
    video_authors_df = pd.DataFrame()
    video_authors_df["videoId"] = video_id_list
    video_authors_df["authors"] = author_list
    video_authors_df.to_csv("video_authors_df.csv", index=None)


if __name__ == "__main__":
    main()
