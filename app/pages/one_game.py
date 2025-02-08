import streamlit as st
import numpy as np
import pandas as pd

import importlib
import pages.game_simulator as gs
importlib.reload(gs)
import pages.display as display
importlib.reload(display)

def one_game(players):
    st.write("1試合のシミュレーション")

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

    st.write("選手成績:")
    df_stats = display.diplay_stats(players)
    st.dataframe(df_stats,use_container_width=True)
    
