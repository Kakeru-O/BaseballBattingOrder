import numpy as np
import pandas as pd
import streamlit as st

# 小数点以下3桁で表示するフォーマットを設定
pd.options.display.float_format = '{:.2f}'.format

# 各選手の成績をデータフレームで表示
def diplay_stats(players):
    player_stats = {
        "名前": [],
        "打席数": [],
        "打数": [],
        "安打":[],
        "単打": [],
        "二塁打": [],
        "三塁打": [],
        "本塁打": [],
        "四死球": [],
        "打率": [],
        "出塁率": [],
        "長打率": [],
        "OPS": [],
        "打点": [],        
    }

    for player in players:
        stats = player.detailed_stats()
        player_stats["名前"].append(player.name)
        player_stats["打席数"].append(stats["打席数"])
        player_stats["打数"].append(stats["打数"])
        player_stats["安打"].append(stats["安打"])
        player_stats["単打"].append(stats["単打"])
        player_stats["二塁打"].append(stats["二塁打"])
        player_stats["三塁打"].append(stats["三塁打"])
        player_stats["本塁打"].append(stats["本塁打"])
        player_stats["四死球"].append(stats["四死球"])
        player_stats["打率"].append(player.batting_average())
        player_stats["出塁率"].append(player.on_base_percentage())
        player_stats["長打率"].append(player.sllugging_percentage())
        player_stats["OPS"].append(player.ops())
        player_stats["打点"].append(player.runs_batted_in)

    #st.write(player_stats)
    player_stats_df = pd.DataFrame(player_stats)

    # 合算した成績を計算して追加
    totals = {
        "名前": "合計",
        "打席数": player_stats_df["打席数"].sum(),
        "打数": player_stats_df["打数"].sum(),
        "安打": player_stats_df["安打"].sum(),
        "単打": player_stats_df["単打"].sum(),
        "二塁打": player_stats_df["二塁打"].sum(),
        "三塁打": player_stats_df["三塁打"].sum(),
        "本塁打": player_stats_df["本塁打"].sum(),
        "四死球": player_stats_df["四死球"].sum(),
        "打率": np.nan,  # 打率は個別選手の打率ではなく合算しないためNaN
        "出塁率": np.nan,  # 出塁率も合算しない
        "長打率": np.nan,  # 出塁率も合算しない
        "OPS": np.nan,  # 出塁率も合算しない
        "打点": player_stats_df["打点"].sum(),
        
    }
    #total_hits = totals["単打"] + totals["二塁打"] + totals["三塁打"] + totals["本塁打"]
    totals["打率"] = totals["安打"] / totals["打数"] if totals["打数"] > 0 else 0.
    totals["出塁率"] = (totals["安打"] + totals["四死球"]) / totals["打席数"] if totals["打席数"] > 0 else 0.
    total_sllugings = totals["単打"] + 2*totals["二塁打"] + 3*totals["三塁打"] + 4*totals["本塁打"]
    totals["長打率"] = total_sllugings / totals["打数"] if totals["打数"] > 0 else 0.
    totals["OPS"] = totals["出塁率"] + totals["長打率"]

    # データフレームに行を追加
    player_stats_df = pd.concat([player_stats_df, pd.DataFrame([totals])], ignore_index=True)

    player_stats_df.set_index(["名前"],inplace=True)
    
    return player_stats_df
