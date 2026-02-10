import streamlit as st
import pandas as pd
from predict import run_prediction

st.set_page_config(page_title="北海道1〜3区 選挙予測", layout="wide")
st.title("🗳️ 北海道1・2・3区 衆議院選挙予測")

# 候補者名リスト
df_candidates = pd.read_csv("hokkaido_candidates_1to3.csv")
candidate_names = ["全員表示"] + df_candidates["候補者氏名（ふりがな）"].tolist()

# サイドバー
candidate = st.sidebar.selectbox("候補者を選択", candidate_names)

if st.sidebar.button("予測を実行"):
    result = run_prediction(candidate=candidate)

    st.subheader("当選予測結果")
    st.dataframe(result)

    st.download_button(
        "CSVをダウンロード",
        result.to_csv(index=False, encoding="utf-8-sig"),
        file_name="hokkaido_1to3_final_prediction.csv"
    )

    # グラフ表示
    import plotly.express as px
    fig = px.bar(result, x="候補者氏名（ふりがな）", y="win_probability", color="候補者氏名（ふりがな）", text="win_probability")
    st.plotly_chart(fig, use_container_width=True)
