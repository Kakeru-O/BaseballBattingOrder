import random
from itertools import permutations
import importlib

import streamlit as st
import numpy as np
import pandas as pd

import lib.game_simulator as gs
importlib.reload(gs)
import lib.one_game as og
importlib.reload(og)
import lib.display as display
importlib.reload(display)
import lib.get_data as get_data
importlib.reload(get_data)

#############################################################
#st.set_page_config(layout="wide")

Player = gs.Player
ss = st.session_state



# 選択した打順に基づいてPlayerインスタンスを作成
players = [
    Player(row["名前"], list(row)[1:])
    for name in ss.order
    for _, row in ss.df_selected.iterrows() if row["名前"] == name
]


# 数回繰り返して平均を取る
n_traial = 3

# 試す打順数
n_order = st.selectbox("",[10,20,50,100],index=2)

if st.button("ランダムシミュレーションを開始"):
    n_games = 143
    

    # ランダムな打順を生成
    unique_orders = set()
    while len(unique_orders) < n_order:
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

