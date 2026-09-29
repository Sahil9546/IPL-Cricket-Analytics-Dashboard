# 🏏 IPL Cricket Analytics Dashboard

An interactive, data-driven web dashboard built to analyze and visualize Indian Premier League (IPL) performance metrics[cite: 1]. From match outcomes and toss impacts to ball-by-ball player breakdowns, this application provides dynamic insights into T20 cricket analytics[cite: 1].

🚀 **Live Demo:** https://ipl-cricket-analytics-dashboard-6qwvjvaayejkzgesteo8kd.streamlit.app/



---

## 🌟 Key Features

* **Match & Season Overview:** Filter match results, win margins, and season standings across various IPL editions[cite: 1].
* **Team Performance Analytics:** Analyze win/loss ratios, head-to-head records, and toss decision advantages[cite: 1].
* **Player Deep-Dives:** Granular batting and bowling stats, including strike rates, economy rates, boundary frequencies, and wicket dismissals.
* **Interactive Visualizations:** High-contrast charts, heatmaps, and filtering tools powered by Plotly and Streamlit.
* **Delivery-Level Insights:** Ball-by-ball analysis to examine over-by-over scoring trends and phase performance (Powerplay vs. Death Overs).

---

## 🛠️ Tech Stack

* **Language:** Python
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly / Matplotlib / Seaborn
* **Dashboard Framework:** Streamlit (or Dash)
* **Deployment:** Streamlit Community Cloud / Render / GitHub Pages

---

## 📁 Repository Structure

```text
IPL-Cricket-Analytics-Dashboard/
├── data/
│   ├── matches.csv             # Match-level summaries
│   └── deliveries.csv          # Ball-by-ball delivery details
├── dashboard/
│   └── app.py                  # Main dashboard application code
├── notebooks/
│   └── exploratory_analysis.ipynb # Data cleaning & EDA
├── .gitignore
├── requirements.txt
└── README.md
