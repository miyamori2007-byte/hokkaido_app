import streamlit as st
import pandas as pd
import plotly.express as px
from predict import run_prediction

# ────────────────
# サイドバー
# ────────────────
st.sidebar.title("操作パネル")

prefecture = st.sidebar.selectbox("都道府県を選択", ["北海道"])  # 今回は北海道だけ
candidate = st.sidebar.selectbox("候補者を選択", ["Aさん", "Bさん", "Cさん"])  # データに合わせて

if st.sidebar.button("予測する"):
    # run_prediction関数を使って得票率データを取得
    results = run_prediction(prefecture, candidate)  
    # 例: results = {"Aさん": 35, "Bさん": 40, "Cさん": 25}

    # ────────────────
    # データフレーム化
    # ────────────────
    df = pd.DataFrame({
        "候補者": list(results.keys()),
        "得票率": list(results.values())
    })

    # ────────────────
    # グラフ表示 (Plotly)
    # ────────────────
    fig = px.bar(df, x="候補者", y="得票率", color="候補者", text="得票率")
    st.plotly_chart(fig, use_container_width=True)

    # ────────────────
    # データ表としても表示
    # ────────────────
    st.write(df)
import streamlit as st
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
    else:
        return "まだ更新されていません"

# 初期表示
st.markdown(f"**最終更新時刻:** {get_last_updated()}")

st.markdown("""
このアプリは以下のデータを用いて予測しています：
- 候補者情報
- 選挙区区割り
- 世論・政党モメンタム（JSON）
""")

# --- run_all.py を丸ごと実行して更新 ---
if st.button("データを最新化"):
    st.info("更新中…少し待ってね")
    
    # run_all.py を subprocess で呼び出し
    subprocess.run(["python", "run_all.py"])
    
    st.success("更新完了！")
    
    # 更新後の最終更新時刻を再表示
    st.markdown(f"**最終更新時刻:** {get_last_updated()}")

# --- 予測ボタン ---
if st.button("予測を実行"):
    result = run_prediction()

    st.subheader("当選予測結果")
    st.dataframe(result)

    st.download_button(
        "CSVをダウンロード",
        result.to_csv(index=False, encoding="utf-8-sig"),
        file_name="hokkaido_1to3_final_prediction.csv"
    )
# 例: 予測結果を確認
results = run_prediction("北海道", "Aさん")

# ターミナルで確認する場合
print(results)

# Streamlit 上で確認する場合
st.write("### run_prediction の返り値")
st.write(results)


