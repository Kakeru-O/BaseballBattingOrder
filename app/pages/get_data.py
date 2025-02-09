import requests
import urllib  #HTMLにアクセス＆取得
from bs4 import BeautifulSoup #HTMLからデータ抽出
import pandas as pd
import numpy as np
import streamlit as st
# st.set_page_config(layout="wide")

def get_data():
    # URL
    url = 'https://nf3.sakura.ne.jp/php/stat_disp/stat_disp.php?y=0&leg=1&tm=M&fp=0&dn=1&dk=0'
    r = requests.get(url)

    # 接続確認
    if r.status_code == 200:
        print("接続に成功しました")
    else:
        print("接続に失敗しました")

    soup = BeautifulSoup(r.text, "html.parser")#"lxml")

    table = soup.find_all('table')[0] # HTMLから表部分を全て取得
    rows = table.find_all('tr') # 表から行データを取得

    # データ格納
    head_data = []
    player_data = []

    for i, row in enumerate(rows):
        if i == 0: # 1行目
            for headerValue in row.find_all('th'):
                head_data.append(headerValue.get_text())
        elif (i > 1) and (i + 1 < len(rows)): # 2行目〜最終行未満
            player_row = []
            for playerValue in row.find_all('td'):
                player_row.append(playerValue.get_text())
            player_data.append(player_row)

    # データフレーム型に変換
    df = pd.DataFrame(data = player_data, columns = head_data)
    df.to_csv("data/lotte_2024.csv",index=False)

#get_data()
def pre_data():
    df = pd.read_csv("data/lotte_2024.csv")

    df_filt = df[df["打席"]>=100]
    df_filt = df_filt[["名前","打席","打数","安打","２Ｂ","３Ｂ","本塁","打点","四球","敬遠","死球"]]

    df_filt["単打"] = df_filt["安打"]-df_filt["２Ｂ"]-df_filt["３Ｂ"]-df_filt["本塁"]
    df_filt["四死球"] = df_filt["死球"]+df_filt["四球"]+df_filt["敬遠"]
    df_filt["アウト"] = df_filt["打席"]-df_filt["安打"]-df_filt["四死球"]

    df_filt["1B_ratio"] = df_filt["単打"] / df_filt["打席"]
    df_filt["2B_ratio"] = df_filt["２Ｂ"] / df_filt["打席"]
    df_filt["3B_ratio"] = df_filt["３Ｂ"] / df_filt["打席"]
    df_filt["HR_ratio"] = df_filt["本塁"] / df_filt["打席"]
    df_filt["BB_ratio"] = df_filt["四死球"] / df_filt["打席"]
    df_filt["out_ratio"] = df_filt["アウト"] / df_filt["打席"]
    # ホームラン,3Bが０の人に微小な確率を付与
    df_filt.loc[df_filt["HR_ratio"]==0,"1B_ratio"] -= 1e-4
    df_filt.loc[df_filt["3B_ratio"]==0,"1B_ratio"] -= 1e-4
    df_filt.loc[df_filt["HR_ratio"]==0,"HR_ratio"] = 1e-4
    df_filt.loc[df_filt["3B_ratio"]==0,"3B_ratio"] = 1e-4

    df_res = df_filt[["名前","1B_ratio","2B_ratio","3B_ratio","HR_ratio","BB_ratio","out_ratio"]].reset_index(drop=True)

    return df,df_res

# df = pre_data()
# st.dataframe(df,use_container_width=True)

