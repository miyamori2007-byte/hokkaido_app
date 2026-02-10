import streamlit as st
import pandas as pd
import plotly.express as px
from predict import run_prediction
import subprocess
import os

# ────────────────
# ページ設定
# ────────────────
st.set_page_config(
    page_title="北海道1〜3区 選挙予測",
    layout="wide"
)

st.title("🗳️ 北海道1・2・3区 衆議院選挙予測")

# ────────────────
# 最終更新時刻表示
# ────────────────
def get_last_updated():
    if os.path.exists("last_updated.txt"):
        with open("last_updated.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        return "まだ更新されていません"

st.markdown(f"**最終更新時刻:** {get_last_updated()}")

st.markdown("""
このアプリは以下のデータを用いて予測しています：
- 候補者情報
- 選挙区区割り
- 世論・政党モメンタム（JSON）
""")

# ────────────────
# データ更新ボタン
# ────────────────
if st.button("データを最新化"):
    st.info("更新中…少し待ってね")
    subprocess.run(["python", "run_all.py"])
    st.success("更新完了！")
    st.markdown(f"**最終更新時刻:** {get_last_updated()}")

# ────────────────
# run_predictionで結果取得
# ────────────────
results = run_prediction()  # DataFrameで返ってくる前提

# 候補者リストを動的に取得
candidate_list = results["候補者氏名"].tolist()

# ────────────────
# サイドバーで選択
# ────────────────
st.sidebar.title("操作パネル")
candidate = st.sidebar.selectbox("候補者を選択", candidate_list)

# ────────────────
# 選択候補者のフィルタ
# ────────────────
selected_result = results[results["候補者氏名"] == candidate]

# ────────────────
# グラフ表示 (Plotly)
# ────────────────
st.subheader("当選確率グラフ")
fig = px.bar(
    selected_result,
    x="候補者氏名",
    y="win_probability",
    color="候補者氏名",
    text="win_probability",
    range_y=[0, 1]
)
st.plotly_chart(fig, use_container_width=True)

# ────────────────
# データテーブル表示
# ────────────────
st.subheader("予測データ")
st.dataframe(selected_result)

# ────────────────
# CSVダウンロード
# ────────────────
st.download_button(
    "CSVをダウンロード",
    selected_result.to_csv(index=False, encoding="utf-8-sig"),
    file_name="hokkaido_1to3_prediction.csv"
)
