import streamlit as st


# ページタイトル、ファビコン指定等のページ共通指定
# page_icon,initial_sidebar_stateの設定は変更しないこと
def set_page_config(page_title="batting-order-estimation", layout="wide"):
    try:
        st.set_page_config(
            page_title=page_title,
            page_icon=":ball:",  # 設定は固定、変更しないこと
            layout=layout,
            initial_sidebar_state="expanded",  # 設定は固定、変更しないこと
        )
    except:
        pass

    # サイドバーの高さの最小を調整
    # min-heightはサイドバーのメニュー数に応じて調整
    st.html(
        """
        <style>
            [data-testid='stSidebarNav'] > ul {
            min-height: 28em;
            }
        </style>
        """
    )