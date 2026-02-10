import streamlit as st
import pandas as pd
import plotly.express as px
from predict import run_prediction
import os
import subprocess

st.set_page_config(
    page_title="北海道1〜3区 選挙予測",
    layout="wide"
)

st.title("🗳️ 北海道1〜3区 衆議院選挙予測")

# --- 最終更新時刻 ---
def get_last_updated():
    if os.path.exists("last_updated.txt"):
        with open("last_updated.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        return "まだ更新されていません"

st.markdown(f"**最終更新:** {get_last_updated()}")

# --- サイドバー ---
st.sidebar.title("操作パネル")
prefecture = st.sidebar.selectbox("都道府県を選択", ["北海道"])

# CSVから候補者名を取得
candidates_df = pd.read_csv("hokkaido_candidates_1to3.csv")
candidate_list = candidates_df["候補者名"].tolist()
candidate_list.insert(0, "全員表示")  # 先頭に「全員表示」を追加
candidate = st.sidebar.selectbox("候補者を選択", candidate_list)

# --- データ更新 ---
if st.sidebar.button("データを最新化"):
    st.info("更新中…少し待ってね")
    subprocess.run(["python", "run_all.py"])
    st.success("更新完了！")
    st.markdown(f"**最終更新:** {get_last_updated()}")

# --- 予測 ---
if st.sidebar.button("予測を実行"):
    if candidate == "全員表示":
        results = run_prediction(prefecture)
    else:
        results = run_prediction(prefecture, candidate)

    st.subheader("当選予測結果")
    st.dataframe(results)

    # CSVダウンロード
    st.download_button(
        "CSVをダウンロード",
        results.to_csv(index=False, encoding="utf-8-sig"),
        file_name="hokkaido_1to3_final_prediction.csv"
    )

    # グラフ表示
    fig = px.bar(
        results,
        x="候補者名",
        y="win_probability",
        color="候補者届出政党の名称",
        text="win_probability",
        title="当選確率グラフ"
    )
    st.plotly_chart(fig, use_container_width=True)
