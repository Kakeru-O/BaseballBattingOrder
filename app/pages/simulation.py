import random
from itertools import permutations
import importlib

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
#import matplotlib.pyplot as plt
import seaborn as sns

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

st.title("最適打順シミュレーション")

# 選択した打順に基づいてPlayerインスタンスを作成
players = [
    Player(row["名前"], list(row)[1:])
    for name in ss.order
    for _, row in ss.df_selected.iterrows() if row["名前"] == name
]


# 数回繰り返して平均を取る
n_traial = 3

# 試す打順数
n_order = st.selectbox("何通りの打順を試すか選択する",[10,20,50,100],index=2)

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

    # 得点との相関を調べる
    df_res = pd.DataFrame(columns=["打席数","打数","安打","単打","二塁打","三塁打","本塁打","四死球","打率","出塁率","長打率","OPS","打点",])
    
    for order in orders:
        
        # プレイヤーオブジェクトをリセット
        for player in order:
            player.__init__(player.name, player.probabilities)

        # 試合をシミュレーション
        total_score = 0
        for i in range(n_games*n_traial):
            score = gs.simulate_game(order)
            total_score += score
        
        stats = display.diplay_stats(order)
        columns_to_divide = stats.columns.difference(["名前","打率","長打率","出塁率","OPS"])
        stats[columns_to_divide] = (stats[columns_to_divide] / n_traial).round()
        total_score = round(total_score/n_traial)
        results.append((total_score, order,stats))

        df_res = pd.concat([df_res,stats.iloc[9:,:].reset_index(drop=True)],axis=0)

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

    # 得点との相関
    # 相関行列を計算
    correlation_matrix = df_res.corr()

    # col1と最も相関の強い列を特定
    col1_corr = correlation_matrix['打点'].drop('打点')
    most_correlated_col = col1_corr.idxmax()
    max_correlation_value = col1_corr.max()

    # ヒートマップを作成
    heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        #y=list(reversed(correlation_matrix.columns)),
        y=correlation_matrix.columns,
        colorscale=[
            [0.0, "red"],
            [.5, "rgba(255,255,255,1)"],
            [1.0, "green"]
        ],
        zmin=-1, zmax=1
    ))
    heatmap.update_yaxes(autorange='reversed')
    #heatmap.update_layout(title="Correlation Matrix Heatmap",)

    
    st.subheader("得点との相関")

    # ヒートマップの表示
    st.subheader("Correlation Matrix Heatmap")
    st.plotly_chart(heatmap)

    # col1と最も相関の強い列を表示
    st.subheader("Most Correlated Column with 打点")
    st.write(f"Most correlated column: {most_correlated_col}")
    st.write(f"Correlation value: {max_correlation_value:.4f}")


    # 散布図行列を表示
    st.subheader("Scatter Plot Matrix")
    scatter_matrix = px.scatter_matrix(
        df_res,
        dimensions=df_res.columns,
        #title="Scatter Plot Matrix",
        template="plotly",
        labels={col: col for col in df_res.columns}
    )

    scatter_matrix.update_traces(diagonal_visible=True)
    st.plotly_chart(scatter_matrix)

    # #sns.pairplot(df_res)
    # st.pyplot(sns.pairplot(df_res))