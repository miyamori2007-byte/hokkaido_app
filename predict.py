import pandas as pd
import json
from sklearn.linear_model import LogisticRegression

def run_prediction(prefecture="北海道", candidate=None):
    # CSV読み込み
    candidates = pd.read_csv("hokkaido_candidates_1to3.csv")

    # JSON読み込み
    with open("election_survey.json", "r", encoding="utf-8") as f:
        survey = json.load(f)

    # 政党支持率
    party_support = {
        "自由民主党": survey["party_momentum"]["ldp"]["support_rate"],
        "中道改革連合": survey["party_momentum"]["chudou"]["support_rate"],
        "日本維新の会": survey["party_momentum"]["ishin"]["support_rate"],
        "国民民主党": survey["party_momentum"]["dpfp"]["support_rate"],
        "日本共産党": survey["party_momentum"]["jcp"]["support_rate"],
        "参政党": survey["party_momentum"]["sansei"]["support_rate"]
    }
    candidates["party_support"] = candidates["候補者届出政党の名称"].map(lambda x: party_support.get(x, 0.5))

    # 特徴量
    candidates["is_incumbent"] = candidates["新前元の別"].map({"新":0,"前":1,"元":1})
    candidates["has_dual"] = candidates["重複立候補の有無"].map({"有":1,"無":0})
    candidates["district_type"] = candidates["選挙区"].apply(lambda x: 0 if "第1区" in x else 1)

    X = candidates[["年齢","party_support","is_incumbent","has_dual","district_type"]]

    # 仮ターゲット
    y = (0.4*candidates["party_support"] + 0.3*candidates["is_incumbent"] + 0.2*candidates["has_dual"] + 0.1*(1-candidates["district_type"])) > 5

    # モデル学習
    model = LogisticRegression()
    model.fit(X, y.astype(int))

    candidates["win_probability"] = model.predict_proba(X)[:,1]

    # 特定候補者だけ抽出
    if candidate is not None and candidate != "全員表示":
        candidates = candidates[candidates["候補者氏名（ふりがな）"] == candidate]

    # CSV出力
    candidates.to_csv("hokkaido_1to3_final_prediction.csv", index=False, encoding="utf-8-sig")

    return candidates

if __name__ == "__main__":
    print(run_prediction())
