import streamlit as st
import numpy as np
import pandas as pd

import importlib
import lib.game_simulator as gs
importlib.reload(gs)
import lib.display as display
importlib.reload(display)

def one_game(players):
    st.subheader("1試合のシミュレーション")

    # 試合をシミュレート
    score, game_log = gs.simulate_game(players)
    st.write(f"最終スコア: {score}")

    # イニングごとの詳細をデータフレームで表示
    log_data = {}
    # for inning, events in game_log:
    #     for player_name, result in events:
    #         if player_name not in log_data:
    #             log_data[player_name] = [""] * 9
    #         log_data[player_name][inning - 1] = result

    # game_flow_df = pd.DataFrame.from_dict(log_data, orient="index", columns=[f"{i+1}回" for i in range(9)])

    columns = []  # 列名を管理
    for inning, events in game_log:
        batter_count = 0  # イニングごとの打者数をカウント
        for player_name, result in events:
            batter_count += 1
            inning_column = f"{inning}回" if batter_count <= 9 else f"{inning}回{batter_count // 9 + 1}"
            
            # 列がまだ存在しなければ追加
            if inning_column not in columns:
                columns.append(inning_column)
            
            # プレイヤーのデータ初期化
            if player_name not in log_data:
                log_data[player_name] = [""] * len(columns)
            
            # 必要なら列数を調整
            while len(log_data[player_name]) < len(columns):
                log_data[player_name].append("")
            
            # 結果を記録
            log_data[player_name][columns.index(inning_column)] = result

    # データフレームを作成
    game_flow_df = pd.DataFrame.from_dict(log_data, orient="index", columns=columns).fillna("")

    st.write("試合の流れ:")
    st.dataframe(game_flow_df,use_container_width=True)

    st.write("成績:")
    df_stats = display.diplay_stats(players)
    st.dataframe(df_stats,use_container_width=True)
    
