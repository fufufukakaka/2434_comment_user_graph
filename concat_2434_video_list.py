import glob
import pandas as pd


def main():
    video_list = glob.glob("video_list_output/*.csv")
    df_list = []
    for v in video_list:
        df_list.append(pd.read_csv(v))
    concat_df = pd.concat(df_list)
    concat_df.to_csv("concat_video_list.csv", index=False)


if __name__ == "__main__":
    main()
