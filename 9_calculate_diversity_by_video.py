import ast
import itertools
import pandas as pd
from tqdm.auto import tqdm


def main():
    streamer_unique_chat_authors = pd.read_csv(
        "streamer_unique_chat_authors.csv",
        converters={"unique_chat_authors": ast.literal_eval},
    )
    streamer2chat_users = streamer_unique_chat_authors.set_index("streamer_name")[
        "unique_chat_authors"
    ].to_dict()
    for key, value in streamer2chat_users.items():
        streamer2chat_users[key] = set(value)
    streamers = list(streamer2chat_users.keys())

    video_authors_df = pd.read_csv(
        "video_authors_df.csv", converters={"authors": ast.literal_eval}
    )
    diversity_list = []
    for index, row in tqdm(video_authors_df.iterrows()):
        video_id = row["videoId"]
        chat_authors_set = set(row["authors"])
        _diversity = [video_id]
        for video_chat_authors_set in streamer2chat_users.values():
            if len(chat_authors_set) > 0:
                diversity_score = len(chat_authors_set & video_chat_authors_set)
            else:
                diversity_score = 0
            _diversity.append(diversity_score)
        diversity_list.append(_diversity)
    diversity_df = pd.DataFrame(diversity_list, columns=["videoId"] + streamers)
    diversity_df["sum_score"] = diversity_df[streamers].sum(axis=1)
    diversity_df = diversity_df.query("sum_score > 0")
    diversity_df.to_csv("diversity_df.csv", index=None)


if __name__ == "__main__":
    main()
