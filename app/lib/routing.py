import streamlit as st

def run_navi():

    pages = [
        st.Page(
            "pages/select_players.py",
            title="SELECT_PLAYERS",
            icon="",
            url_path="/",
            default=True,
        ),
        st.Page(
            "pages/simulation.py",
            title="random simuletion",
            icon="",
            url_path="/random_simulation",
        ),
    ]

    hierarchy_pages = {
        "シミュレーション": [*pages[0:4]],  # 機能のセクション名は適宜変更する
        "ユーザガイド": [*pages[4:]],
    }

    pg = st.navigation(hierarchy_pages)
    pg.run()
    return
