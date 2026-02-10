import streamlit as st
import pandas as pd
import plotly.express as px
from predict import run_prediction
import subprocess
import os

# ────────────────
# Streamlitページ設定
# ────────────────
st.set_page_config(
    page_title="北海道1〜3区 選挙予測",
    layout="wide"
)

st.title("🗳️ 北海道1・2・3区 衆議院選挙予測")

# ────────────────
# 最終更新時刻関数
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
