import ast
import pandas as pd


def main():
    concat_video_list = pd.read_csv("concat_video_list.csv")
    video_authors_df = pd.read_csv(
        "video_authors_df.csv", converters={"authors": ast.literal_eval}
    )
    joined = pd.merge(concat_video_list, video_authors_df)
    streamer_chat_authors = (
        joined.groupby("streamer_name")["authors"].apply(list).reset_index()
    )
    streamer_chat_authors["unique_chat_authors"] = streamer_chat_authors[
        "authors"
    ].apply(lambda x: sum(x, []))
    streamer_chat_authors[["streamer_name", "unique_chat_authors"]].to_csv(
        "streamer_unique_chat_authors.csv", index=None
    )


if __name__ == "__main__":
    main()
