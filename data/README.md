# 🏏 IPL Cricket Analytics Dashboard

> **Real Data · 1,243 Matches · 288,226 Deliveries · IPL 2008–2026**

An interactive multi-page analytics dashboard for the Indian Premier League built with **Streamlit**, **Plotly**, and **scikit-learn** — powered by real ball-by-ball data.

---

## 📁 Folder Structure

```
IPL-Cricket-Analytics-Dashboard/
│
├── data/
│   ├── matches.csv          ← 1,243 IPL matches (2008–2026)
│   └── deliveries.csv       ← 288,226 ball-by-ball deliveries
│
├── dashboard/
│   └── app.py               ← Main Streamlit application
│
├── notebooks/
│   └── IPL_EDA.ipynb        ← Exploratory data analysis
│
├── images/                  ← (optional screenshots)
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the dashboard
```bash
streamlit run dashboard/app.py
```

---

## 📊 Dashboard Pages

| Page | What you get |
|------|-------------|
| 🏠 **Home Overview** | Total matches, runs, wickets, toss effect, season trends |
| 🏟️ **Team Analysis** | Wins, win%, season trends, head-to-head for any franchise |
| 👤 **Player Analysis** | Top batters (runs/SR/avg/50s/100s), top bowlers (wkts/eco/avg), Orange & Purple Cap trends |
| 📍 **Venue Analysis** | Avg scores, highest totals, chasing vs defending % by ground |
| 🪙 **Toss Analysis** | Toss→match win correlation, field vs bat decisions, team-wise toss impact |
| 📅 **Season Analysis** | Season champions, runs/wickets/sixes trends, all-time title count |
| 🤖 **Predictive** | Logistic Regression / Random Forest / XGBoost match winner prediction with live probability |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Core language |
| **Pandas / NumPy** | Data wrangling & aggregation |
| **Plotly** | Interactive charts |
| **Streamlit** | Web dashboard framework |
| **scikit-learn** | ML models (LR, RF) |
| **XGBoost** | Gradient boosting predictor |

---

## 📦 requirements.txt

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
scikit-learn>=1.3.0
xgboost>=2.0.0
```

---

## 🎯 Key Stats in the Dataset

- **19 seasons**: 2008–2026
- **19 franchises** (including defunct: Deccan Chargers, Kochi Tuskers, etc.)
- **Toss impact**: 51.6% win rate after winning toss (field = 54.7%, bat = 45.3%)
- **Top run scorer**: V Kohli (9,040 runs)
- **Top wicket taker**: YS Chahal (228+ wickets)
- **Most titles**: Mumbai Indians (5) & Chennai Super Kings (5)

---

## 📸 Screenshot Guide

After running the dashboard, you can screenshot each page and drop images into the `images/` folder for documentation.
