import streamlit as st
import numpy as np
import pandas as pd

import importlib
import pages.game_simulator as gs
importlib.reload(gs)



st.write("test")

Player = gs.Player

# 選手のデータを設定
players = [
    Player("岡大海", np.array([67, 28, 2, 7, 57, 259])/420),
    Player("藤岡裕大", np.array([61, 13, 1, 5, 49, 240])/369),
    Player("ポランコ", np.array([57, 21, 0, 23, 50, 317])/468),
    Player("ソト", np.array([87, 22, 2, 21, 49, 361])/542),
    Player("佐藤都志也", np.array([89, 20, 0, 5, 34, 304])/452),
    Player("荻野貴司", np.array([47,6, 1, 1, 13, 145])/213),
    Player("藤原恭大", np.array([53, 8, 4, 2, 28, 169])/264),
    Player("中村奨吾", np.array([66, 18, 0, 4, 46, 299])/433),
    Player("小川龍成", np.array([61, 2, 0, 0, 31, 219])/313),
]

# 試合をシミュレート
score, game_log = gs.simulate_game(players)
st.write(f"最終スコア: {score}")

# イニングごとの詳細をデータフレームで表示
log_data = {}
for inning, events in game_log:
    for player_name, result in events:
        if player_name not in log_data:
            log_data[player_name] = [""] * 9
        log_data[player_name][inning - 1] = result

game_flow_df = pd.DataFrame.from_dict(log_data, orient="index", columns=[f"{i+1}回" for i in range(9)])
st.write("試合の流れ:")
st.dataframe(game_flow_df)

# 各選手の成績をデータフレームで表示
player_stats = {
    "名前": [],
    "打率": [],
    "出塁率": [],
    "長打率": [],
    "OPS": [],
    "打点": [],
    "単打": [],
    "二塁打": [],
    "三塁打": [],
    "本塁打": [],
    "打席数": [],
    "四死球": []
}

for player in players:
    stats = player.detailed_stats()
    player_stats["名前"].append(player.name)
    player_stats["打率"].append(player.batting_average())
    player_stats["出塁率"].append(player.on_base_percentage())
    player_stats["長打率"].append(player.sllugging_percentage())
    player_stats["OPS"].append(player.ops())
    player_stats["打点"].append(player.runs_batted_in)
    player_stats["単打"].append(stats["単打"])
    player_stats["二塁打"].append(stats["二塁打"])
    player_stats["三塁打"].append(stats["三塁打"])
    player_stats["本塁打"].append(stats["本塁打"])
    player_stats["打席数"].append(stats["打席数"])
    player_stats["四死球"].append(stats["四死球"])

player_stats_df = pd.DataFrame(player_stats)

# 合算した成績を計算して追加
totals = {
    "名前": "合計",
    "打率": np.nan,  # 打率は個別選手の打率ではなく合算しないためNaN
    "出塁率": np.nan,  # 出塁率も合算しない
    "長打率": np.nan,  # 出塁率も合算しない
    "OPS": np.nan,  # 出塁率も合算しない
    "打点": player_stats_df["打点"].sum(),
    "単打": player_stats_df["単打"].sum(),
    "二塁打": player_stats_df["二塁打"].sum(),
    "三塁打": player_stats_df["三塁打"].sum(),
    "本塁打": player_stats_df["本塁打"].sum(),
    "打席数": player_stats_df["打席数"].sum(),
    "四死球": player_stats_df["四死球"].sum()
}
total_hits = totals["単打"] + totals["二塁打"] + totals["三塁打"] + totals["本塁打"]
totals["打率"] = total_hits / totals["打席数"] if totals["打席数"] > 0 else 0
total_plate_appearances = totals["打席数"] + totals["四死球"]
totals["出塁率"] = (total_hits + totals["四死球"]) / total_plate_appearances if total_plate_appearances > 0 else 0
total_sllugings = totals["単打"] + 2*totals["二塁打"] + 3*totals["三塁打"] + 4*totals["本塁打"]
totals["長打率"] = total_sllugings / totals["打席数"] if totals["打席数"] > 0 else 0
totals["OPS"] = totals["出塁率"] + totals["長打率"]

# データフレームに行を追加
player_stats_df = pd.concat([player_stats_df, pd.DataFrame([totals])], ignore_index=True)


st.write("選手成績:")
st.dataframe(player_stats_df)
