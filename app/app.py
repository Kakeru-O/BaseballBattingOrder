import random
from itertools import permutations
import importlib

import streamlit as st
import numpy as np
import pandas as pd

import pages.game_simulator as gs
importlib.reload(gs)
import pages.one_game as og
importlib.reload(og)
import pages.display as display
importlib.reload(display)
import pages.get_data as get_data
importlib.reload(get_data)

#############################################################
st.set_page_config(layout="wide")

Player = gs.Player

# 選手のデータを設定
players = [
    Player("藤岡裕大", np.array([61, 13, 1, 5, 49, 240])/369),
    Player("岡大海", np.array([67, 28, 2, 7, 57, 259])/420),
    Player("ポランコ", np.array([57, 21, 0, 23, 50, 317])/468),
    Player("ソト", np.array([87, 22, 2, 21, 49, 361])/542),
    Player("佐藤都志也", np.array([89, 20, 0, 5, 34, 304])/452),
    Player("荻野貴司", np.array([47,6, 1, 1, 13, 145])/213),
    Player("藤原恭大", np.array([53, 8, 4, 2, 28, 169])/264),
    Player("中村奨吾", np.array([66, 18, 0, 4, 46, 299])/433),
    Player("小川龍成", np.array([61, 2, 0, 0, 31, 219])/313),
]


# 選手のリストを作成
df_true,df = get_data.pre_data()
players = df["名前"].tolist()

# 並べ替え用のセレクトボックス
st.title("最適打順シミュレーション")
st.subheader("各打順の選手を選んでください")

# 並べ替え用の入力UI
new_order = []
for i in range(9):
    selected_player = st.selectbox(f"{i + 1}番打者", players,index=i, key=f"batter_{i+1}")
    new_order.append(selected_player)

# 並べ替え後の順序を表示
st.write("現在の打順:")
st.write(new_order)

# 並べ替えた結果でシミュレーション実行
#if st.button("シミュレーションを開始"):

# 新しい順序に基づいてPlayerインスタンスを作成
players = [
    Player(row["名前"], list(row)[1:])
    for name in new_order
    for _, row in df.iterrows() if row["名前"] == name
]

# 並べ替えた結果でシミュレーション実行
if st.button("シミュレーションを開始"):
    # 1試合
    og.one_game(players)

    # 143試合
    st.subheader("143試合")
    n_games = 143
    # 数回繰り返して平均を取る
    n_traial = 3

    total_score = 0
    for i in range(n_games*n_traial):
        score, game_log = gs.simulate_game(players)
        total_score += score
    #score, _ = gs.simulate_game(order)
    stats = display.diplay_stats(players)
    columns_to_divide = stats.columns.difference(["名前","打率","長打率","出塁率","OPS"])
    stats[columns_to_divide] = (stats[columns_to_divide] / n_traial).round()
    total_score = round(total_score/n_traial)
    
    st.write(total_score)
    st.dataframe(stats,use_container_width=True)


    # 名前リストの順番で抽出
    st.dataframe(df_true[df_true['名前'].isin(new_order)].set_index('名前').loc[new_order].reset_index())



if st.button("ランダムシミュレーションを開始"):
    n_games = 143
    # 数回繰り返して平均を取る
    n_traial = 3

    # ランダムな打順を生成
    unique_orders = set()
    while len(unique_orders) < 100:
        random.shuffle(players)  # playersをランダムに並べ替える
        # タプル化して集合に追加（リストはハッシュ不可なのでタプルを使用）
        unique_orders.add(tuple(players))

    # リストに変換
    orders = [list(order) for order in unique_orders]


    # スコアを記録
    results = []

    #for order in batting_orders:
    for order in orders:
        
        # プレイヤーオブジェクトをリセット
        for player in order:
            player.__init__(player.name, player.probabilities)

        # 試合をシミュレーション
        total_score = 0
        for i in range(n_games*n_traial):
            score, game_log = gs.simulate_game(order)
            total_score += score
        #score, _ = gs.simulate_game(order)
        stats = display.diplay_stats(order)
        columns_to_divide = stats.columns.difference(["名前","打率","長打率","出塁率","OPS"])
        stats[columns_to_divide] = (stats[columns_to_divide] / n_traial).round()
        total_score = round(total_score/n_traial)
        results.append((total_score, order,stats))

    # 一番得点が高かった打順とその詳細
    best_score, best_order,best_stats = max(results, key=lambda x: x[0])
    #best_stats = display.diplay_stats(best_order)
    st.write("最適打順")
    st.write(best_score)
    st.dataframe(best_stats,use_container_width=True)

    # 一番得点が低かった打順とその詳細
    worst_score, worst_order,worst_stats = min(results, key=lambda x: x[0])
    #st.write(worst_score,worst_order[0])
    #worst_stats = display.diplay_stats(worst_order)
    st.write("不適打順")
    st.write(worst_score)
    st.dataframe(worst_stats,use_container_width=True)

