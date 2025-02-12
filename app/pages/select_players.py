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

#st.set_page_config(layout="wide")
################################################################
st.title("最適打順シミュレーション")

Player = gs.Player

ss = st.session_state

if "team" not in ss:
    ss.team = ""
if "year" not in ss:
    ss.year = ""
if "order" not in ss:
    ss.order = None
if "df_selected" not in ss:
    ss.df_selected = None

# 
st.subheader("")

col1,col2,_ = st.columns([1,1,5])
with col1:
    team = st.selectbox("チームを選択する", ["F","E","L","M","Bs","H","G","S","B","D","T","C"],index=3,key="selct_team")
with col2:
    year = st.selectbox("年を選択する",[2024,2023,2022])
ss.team = team

# 選手のリストを作成
df_true,df_seletcted = get_data.pre_data(team)
team_players_list :list = df_seletcted["名前"].tolist()
ss.df_selected = df_seletcted

# 並べ替え用のセレクトボックス
st.subheader("各打順の選手を選んでください")

# 並べ替え用の入力UI
order = []
# テスト用
#default_order = ["岡大海","藤岡裕大","ポランコ","ソト","佐藤都志也","荻野貴司","藤原恭大","中村奨吾","小川龍成",]
default_list = [8,5,7,14,10,0,1,6,13]
for i in range(9):
    selected_player = st.selectbox(f"{i + 1}番打者", team_players_list,index=default_list[i], key=f"batter_{i+1}")
    order.append(selected_player)

# 並べ替え後の順序を表示
st.write("現在の打順:")
st.write(order)
ss.order = order

# 選択した打順に基づいてPlayerインスタンスを作成
players = [
    Player(row["名前"], list(row)[1:])
    for name in order
    for _, row in df_seletcted.iterrows() if row["名前"] == name
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
        score = gs.simulate_game(players)
        total_score += score
    
    stats = display.diplay_stats(players)
    columns_to_divide = stats.columns.difference(["名前","打率","長打率","出塁率","OPS"])
    stats[columns_to_divide] = (stats[columns_to_divide] / n_traial).round()
    total_score = round(total_score/n_traial)
    
    st.write(f"最終スコア: {total_score}")
    st.write("成績:")
    st.dataframe(stats,use_container_width=True)

    # 名前リストの順番で抽出
    st.dataframe(df_true[df_true['名前'].isin(order)].set_index('名前').loc[order])#.reset_index())

