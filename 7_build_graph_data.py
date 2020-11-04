import ast
import itertools
import pandas as pd
from tqdm.auto import tqdm


def get_edge(streamers, all_chat_users, chat_user):
    _edge_list = []
    _chated_streamers = []
    for streamer, chat_users in zip(streamers, all_chat_users):
        if chat_user in chat_users:
            _chated_streamers.append(streamer)
    # コメントしたstreamerのリストをcombinationして組み合わせをすべて出す
    combinations = list(itertools.combinations(_chated_streamers, 2))
    # networkxで読める形式に出力する
    for combi in combinations:
        # source, target, edge_name
        edge = [combi[0], combi[1], chat_user]
        _edge_list.append(edge)
    return _edge_list


def main():
    streamer_unique_chat_authors = pd.read_csv(
        "streamer_unique_chat_authors.csv",
        converters={"unique_chat_authors": ast.literal_eval},
    )
    # chatしたuser IDのリストを作る
    unique_chat_users = list(
        set(sum(streamer_unique_chat_authors["unique_chat_authors"].tolist(), []))
    )
    streamer2chat_users = streamer_unique_chat_authors.set_index("streamer_name")[
        "unique_chat_authors"
    ].to_dict()

    streamers = list(streamer2chat_users.keys())
    all_chat_users = list(streamer2chat_users.values())
    _edge_list = []
    for chat_user in tqdm(unique_chat_users):
        edges = get_edge(streamers, all_chat_users, chat_user)
        _edge_list.append(edges)
    edge_list = sum(_edge_list, [])
    edge_df = pd.DataFrame(edge_list, columns=["source", "target", "edge_name"])
    edge_df.to_csv("streamer_chat_user_edge_df.csv", index=None)


if __name__ == "__main__":
    main()
