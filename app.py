import streamlit as st
import pandas as pd
import plotly.express as px
from predict import run_prediction
import subprocess
import os

st.set_page_config(
    page_title="北海道1〜3区 選挙予測",
    layout="wide"
)

st.title("🗳️ 北海道1・2・3区 衆議院選挙予測")

# --- 最終更新時刻取得関数 ---
def get_last_updated():
    if os.path.exists("last_updated.txt"):
        with open("last_updated.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    return "まだ更新されていません"

st.markdown(f"**最終更新時刻:** {get_last_updated()}")

st.markdown("""
このアプリは以下のデータを用いて予測しています：
- 候補者情報
- 選挙区区割り
- 世論・政党モメンタム（JSON）
""")

# --- データ更新ボタン ---
if st.button("データを最新化"):
    st.info("更新中…少し待ってね")
    subprocess.run(["python", "run_all.py"])
    st.success("更新完了！")
    st.markdown(f"**最終更新時刻:** {get_last_updated()}")

# --- 予測ボタン ---
if st.button("予測を実行"):
    st.info("予測中…")
    df = run_prediction()  # DataFrameを返す
    st.success("予測完了！")

    st.subheader("当選予測結果")
    st.dataframe(df)

    # --- グラフ表示 ---
    fig = px.bar(df, x="候補者届出政党の名称", y="win_probability",
                 color="候補者届出政党の名称", text="win_probability")
    st.plotly_chart(fig, use_container_width=True)

    # --- CSVダウンロード ---
    st.download_button(
        "CSVをダウンロード",
        df.to_csv(index=False, encoding="utf-8-sig"),
        file_name="hokkaido_1to3_final_prediction.csv"
    )
