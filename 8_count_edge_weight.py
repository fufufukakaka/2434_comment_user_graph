import pandas as pd
from sklearn import preprocessing


def main():
    """
    7で作ったエッジにチャットユーザのIDを名前としてつけたバージョンから、

    source・targetでgroupbyし、その数を0.1~0.9にスケーリングした
    重みとしたエッジデータに変換する
    """
    streamer_chat_user_edge_df = pd.read_csv("streamer_chat_user_edge_df.csv")
    groupby_counted = (
        streamer_chat_user_edge_df.groupby(["source", "target"]).count().reset_index()
    )
    groupby_counted.columns = ["source", "target", "edge_count"]
    # edge_countをスケーリングする
    mmscaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    groupby_counted["scaled_edge_count"] = mmscaler.fit_transform(
        groupby_counted["edge_count"].values.reshape(-1, 1)
    )
    # ギルザレンが重複してしまったので除外する
    groupby_counted = groupby_counted.query("source!='ギルザレンIII世'").query(
        "target!='ギルザレンIII世'"
    )
    groupby_counted.to_csv("streamer_chat_edge_scaled.csv", index=None)


if __name__ == "__main__":
    main()
