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
