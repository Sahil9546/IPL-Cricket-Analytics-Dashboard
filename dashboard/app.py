"""
IPL Cricket Analytics Dashboard 
Real data: IPL 2008–2026  |  1,243 matches · 288,226 deliveries
Run: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots   
import warnings, os

warnings.filterwarnings("ignore")

# ── paths ─────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")

st.set_page_config(page_title="IPL Analytics Dashboard",
                   page_icon="🏏", layout="wide",
                   initial_sidebar_state="expanded")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  html,body,[class*="css"]{font-family:'Inter',sans-serif;}
  .main{background:#0a1628;}
  .block-container{padding:1rem 2rem 2rem;}
  .dash-header{background:linear-gradient(135deg,#0a1628 0%,#1a3a6b 60%,#0a1628 100%);
    border-radius:12px;padding:20px 28px 14px;margin-bottom:20px;border:1px solid #1e3a5f;}
  .dash-header h1{color:#fff;font-size:26px;font-weight:700;margin:0;}
  .dash-header p{color:#8ab4d8;font-size:13px;margin:4px 0 0;}
  .kpi-card{background:#111d2e;border-radius:10px;padding:14px 16px;
    border:1px solid #1e3a5f;border-top:3px solid var(--ac,#1a73e8);}
  .kpi-card .lbl{font-size:11px;color:#8ab4d8;text-transform:uppercase;letter-spacing:.6px;}
  .kpi-card .val{font-size:24px;font-weight:700;color:#fff;margin:2px 0;}
  .kpi-card .sub{font-size:11px;color:#4a7090;}
  .sec-title{font-size:16px;font-weight:600;color:#c9d8e8;
    border-left:3px solid #f57c00;padding-left:10px;margin:20px 0 12px;}
  .warn-box{background:#1a1a0a;border:1px solid #f57c00;border-radius:8px;
    padding:16px 20px;color:#f0c040;font-size:14px;margin:20px 0;}
  section[data-testid="stSidebar"]{background:#080f1a;border-right:1px solid #1e3a5f;}
  .stTabs [data-baseweb="tab-list"]{gap:6px;background:#080f1a;padding:4px 8px;border-radius:8px;}
  .stTabs [data-baseweb="tab"]{background:#111d2e;color:#8ab4d8;border-radius:6px;
    padding:6px 14px;font-size:13px;font-weight:500;border:1px solid #1e3a5f;}
  .stTabs [aria-selected="true"]{background:#1a3a6b;color:#fff;border-color:#1a73e8;}
  /* winners table */
  .champ-table{width:100%;border-collapse:collapse;font-size:13px;}
  .champ-table th{background:#111d2e;color:#8ab4d8;padding:8px 12px;text-align:left;
    border-bottom:2px solid #1e3a5f;font-weight:600;}
  .champ-table td{padding:8px 12px;border-bottom:1px solid #1e3a5f;color:#c9d8e8;}
  .champ-table tr:hover td{background:#1a2d45;}
  .gold{color:#ffd700;font-weight:600;}
  .silver{color:#a0b8d0;}
  .venue-cell{color:#64b5f6;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
SEASON_MAP = {
    '2007/08':2008,'2009':2009,'2009/10':2010,'2011':2011,'2012':2012,
    '2013':2013,'2014':2014,'2015':2015,'2016':2016,'2017':2017,'2018':2018,
    '2019':2019,'2020/21':2020,'2021':2021,'2022':2022,'2023':2023,
    '2024':2024,'2025':2025,'2026':2026,
}
TEAM_NORM = {
    'Delhi Daredevils':'Delhi Capitals',
    'Kings XI Punjab':'Punjab Kings',
    'Rising Pune Supergiant':'Rising Pune Supergiants',
    'Royal Challengers Bangalore':'Royal Challengers Bengaluru',
}
TEAM_COLORS = {
    'Mumbai Indians':              '#004BA0',
    'Chennai Super Kings':         '#F9CD05',
    'Royal Challengers Bengaluru': '#EC1C24',
    'Kolkata Knight Riders':       '#3A225D',
    'Delhi Capitals':              '#0078BC',
    'Sunrisers Hyderabad':         '#FB643E',
    'Rajasthan Royals':            '#EA1A85',
    'Punjab Kings':                '#A7A9AC',
    'Lucknow Super Giants':        '#A4D4FF',
    'Gujarat Titans':              '#1CB4A6',
    'Deccan Chargers':             '#F7A721',
    'Rising Pune Supergiants':     '#6B2D8B',
    'Gujarat Lions':               '#E77B21',
    'Kochi Tuskers Kerala':        '#EE1C24',
    'Pune Warriors':               '#1C4E96',
}

# Verified IPL Champions list from the provided screenshots
IPL_CHAMPIONS = [
    (2008, 'Rajasthan Royals',              'Chennai Super Kings',         'DY Patil Stadium, Mumbai'),
    (2009, 'Deccan Chargers',               'Royal Challengers Bengaluru', 'Wanderers, Johannesburg'),
    (2010, 'Chennai Super Kings',           'Mumbai Indians',              'DY Patil Stadium, Mumbai'),
    (2011, 'Chennai Super Kings',           'Royal Challengers Bengaluru', 'MA Chidambaram Stadium, Chennai'),
    (2012, 'Kolkata Knight Riders',         'Chennai Super Kings',         'MA Chidambaram Stadium, Chennai'),
    (2013, 'Mumbai Indians',                'Chennai Super Kings',         'Eden Gardens, Kolkata'),
    (2014, 'Kolkata Knight Riders',         'Punjab Kings',                'M. Chinnaswamy Stadium, Bangalore'),
    (2015, 'Mumbai Indians',                'Chennai Super Kings',         'Eden Gardens, Kolkata'),
    (2016, 'Sunrisers Hyderabad',           'Royal Challengers Bengaluru', 'M. Chinnaswamy Stadium, Bangalore'),
    (2017, 'Mumbai Indians',                'Rising Pune Supergiants',     'Rajiv Gandhi Intl. Stadium, Hyderabad'),
    (2018, 'Chennai Super Kings',           'Sunrisers Hyderabad',         'Wankhede Stadium, Mumbai'),
    (2019, 'Mumbai Indians',                'Chennai Super Kings',         'Rajiv Gandhi Intl. Stadium, Hyderabad'),
    (2020, 'Mumbai Indians',                'Delhi Capitals',              'Dubai Intl. Cricket Stadium'),
    (2021, 'Chennai Super Kings',           'Kolkata Knight Riders',       'Dubai Intl. Cricket Stadium'),
    (2022, 'Gujarat Titans',                'Rajasthan Royals',            'Narendra Modi Stadium, Ahmedabad'),
    (2023, 'Chennai Super Kings',           'Gujarat Titans',              'Narendra Modi Stadium, Ahmedabad'),
    (2024, 'Kolkata Knight Riders',         'Sunrisers Hyderabad',         'MA Chidambaram Stadium, Chennai'),
    (2025, 'Royal Challengers Bengaluru',   'Punjab Kings',                'Narendra Modi Stadium, Ahmedabad'),
    (2026, 'Royal Challengers Bengaluru',   'Gujarat Titans',              'Narendra Modi Stadium, Ahmedabad'),
]
CHAMP_DF = pd.DataFrame(IPL_CHAMPIONS, columns=['Year','Champion','Runner-Up','Final Venue'])

CHART_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(8,15,26,0.6)',
    font=dict(color='#8ab4d8', family='Inter'),
    title_font=dict(color='#c9d8e8', size=14),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(gridcolor='#1e3a5f', color='#8ab4d8', tickfont=dict(color='#8ab4d8')),
    yaxis=dict(gridcolor='#1e3a5f', color='#8ab4d8', tickfont=dict(color='#8ab4d8')),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8ab4d8')),
)

def apply_theme(fig, height=380):
    fig.update_layout(height=height, **CHART_THEME)
    return fig

def no_data_msg(reason="No season selected. Please pick at least one season from the sidebar."):
    st.markdown(f'<div class="warn-box">⚠️ {reason}</div>', unsafe_allow_html=True)

def kpi(label, value, sub='', color='#1a73e8'):
    st.markdown(f"""
    <div class="kpi-card" style="--ac:{color};border-top:3px solid {color};">
      <div class="lbl">{label}</div>
      <div class="val">{value}</div>
      <div class="sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)

def safe_val(val, fmt="{}", fallback="N/A"):
    """Format a value safely, returning fallback for NaN/None/empty."""
    try:
        if val is None or (isinstance(val, float) and np.isnan(val)):
            return fallback
        return fmt.format(val)
    except Exception:
        return fallback

# ══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Loading IPL data…")
def load_data():
    m = pd.read_csv(os.path.join(DATA, "matches.csv"))
    d = pd.read_csv(os.path.join(DATA, "deliveries.csv"))

    m['season_yr'] = m['season'].map(SEASON_MAP)
    for col in ['team1','team2','winner','toss_winner']:
        m[col] = m[col].replace(TEAM_NORM)

    # Build match_id → (venue, winner, team1, team2) by aligning sorted match_ids
    # per season with sorted match_number rows
    id_rows = []
    for yr in sorted(m['season_yr'].dropna().unique()):
        m_yr = m[m['season_yr'] == yr].sort_values('match_number').reset_index(drop=True)
        d_ids = sorted(d[d['season_id'] == yr]['match_id'].unique())
        for i, mid in enumerate(d_ids):
            if i < len(m_yr):
                row = m_yr.iloc[i]
                id_rows.append({'match_id': mid, 'season_yr': int(yr),
                                 'venue': row['venue'], 'winner': row['winner'],
                                 'team1': row['team1'], 'team2': row['team2'],
                                 'toss_winner': row['toss_winner'],
                                 'toss_decision': row['toss_decision'],
                                 'result_type': row['result_type'],
                                 'win_by_runs': row['win_by_runs'],
                                 'win_by_wickets': row['win_by_wickets'],
                                 'match_number': row['match_number']})
    mid_df = pd.DataFrame(id_rows)

    # normalise team names in mid_df too
    for col in ['team1','team2','winner','toss_winner']:
        mid_df[col] = mid_df[col].replace(TEAM_NORM)

    # Venue normalisation
    venue_norm = {
        'M Chinnaswamy Stadium':                       'M. Chinnaswamy Stadium',
        'MA Chidambaram Stadium, Chepauk':             'MA Chidambaram Stadium',
        'MA Chidambaram Stadium, Chepauk, Chennai':    'MA Chidambaram Stadium',
        'Rajiv Gandhi International Stadium, Uppal':   'Rajiv Gandhi Intl Stadium',
        'Rajiv Gandhi International Stadium':          'Rajiv Gandhi Intl Stadium',
        'Feroz Shah Kotla':                            'Arun Jaitley Stadium',
        'Feroz Shah Kotla Ground':                     'Arun Jaitley Stadium',
        'Narendra Modi Stadium, Ahmedabad':            'Narendra Modi Stadium',
        'Punjab Cricket Association Stadium, Mohali':  'PCA Stadium, Mohali',
        'Punjab Cricket Association IS Bindra Stadium, Mohali': 'PCA Stadium, Mohali',
        'Dr DY Patil Sports Academy':                  'DY Patil Stadium',
        'Dr. DY Patil Sports Academy':                 'DY Patil Stadium',
        'Brabourne Stadium, Mumbai':                   'Brabourne Stadium',
        'Maharashtra Cricket Association Stadium, Pune':'MCA Stadium, Pune',
        'BRSABV Ekana Cricket Stadium, Lucknow':       'Ekana Stadium',
        'Ekana Cricket Stadium, Lucknow':              'Ekana Stadium',
        'Wankhede Stadium, Mumbai':                    'Wankhede Stadium',
    }
    mid_df['venue'] = mid_df['venue'].replace(venue_norm)

    d_clean = d[d['is_super_over'] == False].copy()
    return m, d_clean, mid_df


# ══════════════════════════════════════════════════════════════════════════════
#  STAT COMPUTATIONS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def compute_batting(d_filtered):
    if len(d_filtered) == 0:
        return pd.DataFrame(columns=['batter','runs','balls','fours','sixes','innings','sr','avg','highest','fifties','hundreds'])

    legal = d_filtered[d_filtered['is_wide_ball'] == False]

    runs_s  = d_filtered.groupby('batter')['batter_runs'].sum()
    balls_s = legal.groupby('batter').size()
    fours_s = d_filtered.groupby('batter')['batter_runs'].apply(lambda x: (x == 4).sum())
    sixes_s = d_filtered.groupby('batter')['batter_runs'].apply(lambda x: (x == 6).sum())

    bat = pd.DataFrame({'runs': runs_s, 'balls': balls_s,
                        'fours': fours_s, 'sixes': sixes_s}).reset_index()
    bat.columns = ['batter','runs','balls','fours','sixes']

    inn_s = d_filtered.groupby('batter')['match_id'].nunique().reset_index(name='innings')
    bat = bat.merge(inn_s, on='batter', how='left')
    bat['innings'] = bat['innings'].fillna(1).astype(int)

    bat['sr']  = (bat['runs'] / bat['balls'].clip(lower=1) * 100).round(2)
    bat['avg'] = (bat['runs'] / bat['innings'].clip(lower=1)).round(2)

    # per-innings highest score
    inn_runs = d_filtered.groupby(['batter','match_id'])['batter_runs'].sum()
    highest  = inn_runs.groupby('batter').max().reset_index(name='highest')
    bat = bat.merge(highest, on='batter', how='left')

    # 50s and 100s
    inn_df = inn_runs.reset_index()
    inn_df.columns = ['batter','match_id','inn_runs']
    milestones = inn_df.groupby('batter').apply(
        lambda x: pd.Series({
            'fifties':  int(((x['inn_runs'] >= 50) & (x['inn_runs'] < 100)).sum()),
            'hundreds': int((x['inn_runs'] >= 100).sum()),
        })
    ).reset_index()
    bat = bat.merge(milestones, on='batter', how='left')
    bat[['fifties','hundreds']] = bat[['fifties','hundreds']].fillna(0).astype(int)

    return bat[bat['balls'] >= 10].sort_values('runs', ascending=False).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def compute_bowling(d_filtered):
    if len(d_filtered) == 0:
        return pd.DataFrame(columns=['bowler','wickets','balls','runs_given','dots','matches','overs','economy','avg','dot_pct'])

    NON_BOWLER_WICKETS = ['run out','retired hurt','retired out','obstructing the field']
    w = d_filtered[(d_filtered['is_wicket'] == True) &
                   (~d_filtered['wicket_kind'].isin(NON_BOWLER_WICKETS))]

    wkts  = w.groupby('bowler').size().reset_index(name='wickets')
    balls = d_filtered[d_filtered['is_wide_ball'] == False].groupby('bowler').size().reset_index(name='balls')
    runs  = d_filtered.groupby('bowler')['total_runs'].sum().reset_index(name='runs_given')
    dots  = d_filtered[(d_filtered['total_runs'] == 0) &
                       (d_filtered['is_wide_ball'] == False)].groupby('bowler').size().reset_index(name='dots')
    mats  = d_filtered.groupby('bowler')['match_id'].nunique().reset_index(name='matches')

    bowl = wkts.merge(balls, on='bowler', how='outer') \
               .merge(runs,  on='bowler', how='outer') \
               .merge(dots,  on='bowler', how='outer') \
               .merge(mats,  on='bowler', how='outer')
    bowl = bowl.fillna(0)
    bowl['overs']   = (bowl['balls'] / 6).round(1)
    bowl['economy'] = np.where(bowl['overs'] > 0,
                               (bowl['runs_given'] / bowl['overs']).round(2), np.nan)
    bowl['avg']     = np.where(bowl['wickets'] > 0,
                               (bowl['runs_given'] / bowl['wickets']).round(2), np.nan)
    bowl['dot_pct'] = np.where(bowl['balls'] > 0,
                               (bowl['dots'] / bowl['balls'] * 100).round(1), 0)
    return bowl[bowl['balls'] >= 6].sort_values('wickets', ascending=False).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def compute_team_stats(mid_df_filtered):
    if len(mid_df_filtered) == 0:
        return pd.DataFrame(columns=['team','played','wins','losses','win_pct','titles'])
    complete = mid_df_filtered[
        (mid_df_filtered['result_type'] == 'complete') &
        mid_df_filtered['winner'].notna()
    ].copy()
    if len(complete) == 0:
        return pd.DataFrame(columns=['team','played','wins','losses','win_pct','titles'])

    records = []
    for _, row in complete.iterrows():
        for team in [row['team1'], row['team2']]:
            records.append({'team': team, 'won': 1 if row['winner'] == team else 0})
    df = pd.DataFrame(records)
    grp = df.groupby('team').agg(played=('won','count'), wins=('won','sum')).reset_index()
    grp['losses']  = grp['played'] - grp['wins']
    grp['win_pct'] = (grp['wins'] / grp['played'] * 100).round(1)

    titles = CHAMP_DF['Champion'].value_counts().reset_index()
    titles.columns = ['team','titles']
    grp = grp.merge(titles, on='team', how='left')
    grp['titles'] = grp['titles'].fillna(0).astype(int)
    return grp.sort_values('wins', ascending=False).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def compute_venue_stats(mid_df_filtered, d_filtered):
    """Venue stats using the match_id mapping dataframe."""
    if len(mid_df_filtered) == 0:
        return pd.DataFrame()
    complete = mid_df_filtered[
        (mid_df_filtered['result_type'] == 'complete') &
        mid_df_filtered['winner'].notna()
    ].copy()
    if len(complete) == 0:
        return pd.DataFrame()

    # first innings scores
    fi = d_filtered[d_filtered['innings'] == 1].groupby('match_id')['total_runs'].sum().reset_index(name='fi_score')
    mv = complete.merge(fi, on='match_id', how='left')

    venue_rows = []
    for venue, grp in mv.groupby('venue'):
        total = len(grp)
        if total < 3:
            continue
        # chasing: team batting 2nd wins
        # when team2 wins -> they batted 2nd -> chased
        chasing  = (grp['winner'] == grp['team2']).sum()
        defending = (grp['winner'] == grp['team1']).sum()
        avg_fi   = grp['fi_score'].mean()
        high_fi  = grp['fi_score'].max()
        toss_eff = (grp['toss_winner'] == grp['winner']).mean() * 100
        venue_rows.append({
            'venue': venue, 'matches': total,
            'chasing_wins': int(chasing), 'defending_wins': int(defending),
            'chasing_pct': round(chasing / total * 100, 1),
            'avg_fi': round(avg_fi, 1) if not np.isnan(avg_fi) else None,
            'high_fi': int(high_fi) if not np.isnan(high_fi) else None,
            'toss_eff': round(toss_eff, 1),
        })
    return pd.DataFrame(venue_rows).sort_values('matches', ascending=False).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def compute_season_summary(mid_df_all, d_all, sel_seasons):
    rows = []
    for yr in sorted(sel_seasons):
        mf   = mid_df_all[mid_df_all['season_yr'] == yr]
        df   = d_all[d_all['season_id'] == yr]
        if len(mf) == 0:
            continue
        complete = mf[(mf['result_type'] == 'complete') & mf['winner'].notna()]
        champ  = CHAMP_DF[CHAMP_DF['Year'] == yr]['Champion'].values
        champ  = champ[0] if len(champ) > 0 else (complete.sort_values('match_number').iloc[-1]['winner'] if len(complete) > 0 else 'N/A')
        runner = CHAMP_DF[CHAMP_DF['Year'] == yr]['Runner-Up'].values
        runner = runner[0] if len(runner) > 0 else 'N/A'
        fi_scores = df[df['innings'] == 1].groupby('match_id')['total_runs'].sum()
        bat_s  = df.groupby('batter')['batter_runs'].sum()
        wk_s   = df[(df['is_wicket'] == True) & (~df['wicket_kind'].isin(
            ['run out','retired hurt','retired out','obstructing the field']))].groupby('bowler').size()
        rows.append({
            'Season': int(yr),
            'Champion': champ, 'Runner-Up': runner,
            'Matches': len(mf),
            'Total Runs': int(df['total_runs'].sum()),
            'Total Wickets': int(df[df['is_wicket'] == True].shape[0]),
            'Total Sixes': int((df['batter_runs'] == 6).sum()),
            'Total Fours': int((df['batter_runs'] == 4).sum()),
            'Avg 1st Inn': round(fi_scores.mean(), 1) if len(fi_scores) > 0 else 0,
            'High Total': int(fi_scores.max()) if len(fi_scores) > 0 else 0,
            'Orange Cap': bat_s.idxmax() if len(bat_s) > 0 else 'N/A',
            'OC Runs': int(bat_s.max()) if len(bat_s) > 0 else 0,
            'Purple Cap': wk_s.idxmax() if len(wk_s) > 0 else 'N/A',
            'PC Wickets': int(wk_s.max()) if len(wk_s) > 0 else 0,
        })
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def compute_toss(mid_df_filtered):
    if len(mid_df_filtered) == 0:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    complete = mid_df_filtered[
        (mid_df_filtered['result_type'] == 'complete') &
        mid_df_filtered['winner'].notna()
    ].copy()
    if len(complete) == 0:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    complete['toss_won_match'] = complete['toss_winner'] == complete['winner']
    all_teams = sorted(set(complete['team1'].tolist() + complete['team2'].tolist()))
    team_rows = []
    for team in all_teams:
        sub = complete[(complete['team1'] == team) | (complete['team2'] == team)]
        if len(sub) < 5:
            continue
        tw = (sub['toss_winner'] == team).sum()
        mw = (sub['winner'] == team).sum()
        both = ((sub['toss_winner'] == team) & (sub['winner'] == team)).sum()
        team_rows.append({'team': team, 'played': len(sub),
                          'toss_wins': int(tw), 'match_wins': int(mw), 'both': int(both),
                          'toss_win_pct':  round(tw / len(sub) * 100, 1),
                          'match_win_pct': round(mw / len(sub) * 100, 1)})
    td = pd.DataFrame(team_rows)

    seas = complete.groupby('season_yr')['toss_won_match'].mean().mul(100).round(1).reset_index()
    seas.columns = ['season','toss_eff']

    dec = complete['toss_decision'].value_counts().reset_index()
    dec.columns = ['decision','count']
    return td, seas, dec


# ══════════════════════════════════════════════════════════════════════════════
#  LOAD & SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
m_raw, d_all, mid_df_all = load_data()

with st.sidebar:
    st.markdown("## 🏏 IPL Analytics")
    st.markdown("---")
    page = st.selectbox("📊 **Dashboard Page**", [
        "🏠  Home Overview",
        "🏆  IPL Champions",
        "🏟️  Team Analysis",
        "👤  Player Analysis",
        "📍  Venue Analysis",
        "🪙  Toss Analysis",
        "📅  Season Analysis",
        "🤖  Predictive Analytics",
    ])
    st.markdown("---")
    all_seasons = sorted(mid_df_all['season_yr'].dropna().unique().astype(int))
    sel_seasons = st.multiselect("🗓️ Filter Seasons", all_seasons, default=all_seasons,
                                  help="Select one or more seasons to filter the dashboard.")
    st.markdown("---")
    st.markdown(f"**Dataset**\n\n📦 {len(m_raw):,} matches\n\n🏏 {len(d_all):,} deliveries\n\n📅 2008–2026")

# filtered data
mid_df_f = mid_df_all[mid_df_all['season_yr'].isin(sel_seasons)] if sel_seasons else mid_df_all.iloc[0:0]
d_f      = d_all[d_all['season_id'].isin(sel_seasons)] if sel_seasons else d_all.iloc[0:0]
no_sel   = len(sel_seasons) == 0

# ── header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <h1>🏏 IPL / Cricket Analytics Dashboard</h1>
  <p>Indian Premier League · 2008–2026 · 1,243 Matches · 288,226 Deliveries · Real Ball-by-Ball Data</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════════════════════════════
if "Home" in page:
    if no_sel:
        no_data_msg()
    else:
        complete = mid_df_f[(mid_df_f['result_type'] == 'complete') & mid_df_f['winner'].notna()]
        toss_eff = (complete['toss_winner'] == complete['winner']).mean() * 100 if len(complete) else 0
        total_runs = int(d_f['total_runs'].sum())
        total_wkts = int(d_f['is_wicket'].sum())
        fi_scores  = d_f[d_f['innings'] == 1].groupby('match_id')['total_runs'].sum()
        avg_fi  = fi_scores.mean() if len(fi_scores) else 0
        high_fi = fi_scores.max() if len(fi_scores) else 0

        section("Key Performance Indicators")
        cols = st.columns(6)
        data = [
            ("Total Matches",    f"{len(mid_df_f):,}",     f"{len(sel_seasons)} season(s)", "#1a73e8"),
            ("Total Runs",       f"{total_runs:,}",         "All innings",          "#f57c00"),
            ("Total Wickets",    f"{total_wkts:,}",         "Incl. run-outs",       "#e91e63"),
            ("Toss→Win %",       f"{toss_eff:.1f}%",        "Match correlation",    "#9c27b0"),
            ("Avg 1st Innings",  f"{avg_fi:.0f}",           "Runs per match",       "#00bcd4"),
            ("Highest Total",    f"{int(high_fi) if high_fi else 'N/A'}", "1st innings", "#ff5722"),
        ]
        for col,(lbl,val,sub,clr) in zip(cols, data):
            with col: kpi(lbl, val, sub, clr)

        c1, c2 = st.columns([1.6, 1])
        with c1:
            section("Season-wise Match Count")
            sm = mid_df_f.groupby('season_yr').size().reset_index(name='Matches')
            sm.columns = ['Season','Matches']
            fig = px.bar(sm, x='Season', y='Matches', title='Matches per Season',
                         color_discrete_sequence=['#1a73e8'])
            fig.update_xaxes(type='category')
            apply_theme(fig, 320)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            section("All-time Team Wins")
            tw = complete.groupby('winner').size().reset_index(name='Wins').sort_values('Wins')
            colors = [TEAM_COLORS.get(t,'#4a7090') for t in tw['winner']]
            fig = go.Figure(go.Bar(x=tw['Wins'], y=tw['winner'], orientation='h',
                                   marker_color=colors))
            fig.update_layout(title='Team Wins', showlegend=False, **CHART_THEME, height=320)
            fig.update_yaxes(categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            section("Season-wise Total Runs")
            sr = d_f.groupby('season_id')['total_runs'].sum().reset_index()
            sr.columns = ['Season','Total Runs']
            sr = sr[sr['Season'].isin(sel_seasons)]
            fig = go.Figure(go.Scatter(x=sr['Season'], y=sr['Total Runs'],
                                       mode='lines+markers', fill='tozeroy',
                                       line=dict(color='#f57c00', width=2),
                                       fillcolor='rgba(245,124,0,0.1)'))
            fig.update_layout(title='Runs per Season', **CHART_THEME, height=280)
            st.plotly_chart(fig, use_container_width=True)

        with c4:
            section("Win Method")
            rw = int((complete['win_by_runs']    > 0).sum())
            ww = int((complete['win_by_wickets'] > 0).sum())
            fig = px.pie(pd.DataFrame({'Method':['By Runs','By Wickets'],'Count':[rw,ww]}),
                         values='Count', names='Method', hole=0.5,
                         color_discrete_sequence=['#1a73e8','#f57c00'],
                         title='Win Method Distribution')
            fig.update_traces(textinfo='percent+label')
            apply_theme(fig, 280)
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: IPL CHAMPIONS
# ══════════════════════════════════════════════════════════════════════════════
elif "Champions" in page:
    section("IPL Champions 2008–2026")
    st.markdown("Complete list of every IPL final — champion, runner-up and venue.")

    # Build styled HTML table
    rows_html = ""
    for _, row in CHAMP_DF.iterrows():
        champ_clr = TEAM_COLORS.get(row['Champion'], '#ffd700')
        runner_clr = TEAM_COLORS.get(row['Runner-Up'], '#a0b8d0')
        rows_html += f"""
        <tr>
          <td><b>{int(row['Year'])}</b></td>
          <td class="gold" style="color:{champ_clr}">🏆 {row['Champion']}</td>
          <td style="color:{runner_clr}">{row['Runner-Up']}</td>
          <td class="venue-cell">{row['Final Venue']}</td>
        </tr>"""
    st.markdown(f"""
    <table class="champ-table">
      <thead><tr>
        <th>Year</th><th>Champion</th><th>Runner-Up</th><th>Final Venue</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        section("Title Count by Franchise")
        tc = CHAMP_DF['Champion'].value_counts().reset_index()
        tc.columns = ['Team','Titles']
        tc_colors = [TEAM_COLORS.get(t,'#4a7090') for t in tc['Team']]
        fig = go.Figure(go.Bar(x=tc['Titles'], y=tc['Team'], orientation='h',
                                marker_color=tc_colors,
                                text=tc['Titles'], textposition='outside'))
        fig.update_layout(title='IPL Titles per Franchise', showlegend=False,
                          **CHART_THEME, height=420)
        fig.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section("Most Finals Appearances (Runner-Up + Champion)")
        apps = pd.concat([CHAMP_DF['Champion'], CHAMP_DF['Runner-Up']]).value_counts().reset_index()
        apps.columns = ['Team','Finals']
        app_colors = [TEAM_COLORS.get(t,'#4a7090') for t in apps['Team']]
        fig = go.Figure(go.Bar(x=apps['Finals'], y=apps['Team'], orientation='h',
                                marker_color=app_colors,
                                text=apps['Finals'], textposition='outside'))
        fig.update_layout(title='Finals Appearances', showlegend=False,
                          **CHART_THEME, height=420)
        fig.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: TEAM ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Team" in page:
    if no_sel:
        no_data_msg()
    else:
        ts = compute_team_stats(mid_df_f)
        if ts.empty:
            no_data_msg("No complete match data for the selected season(s).")
        else:
            all_teams = sorted(ts['team'].unique())
            sel_team  = st.selectbox("🏟️ Select Team", all_teams)
            t = ts[ts['team'] == sel_team].iloc[0]
            tc = TEAM_COLORS.get(sel_team, '#1a73e8')

            section(f"{sel_team} — Key Metrics")
            cols = st.columns(5)
            with cols[0]: kpi("Matches",  f"{t['played']:,}", "", tc)
            with cols[1]: kpi("Wins",     f"{t['wins']:,}",   "", "#4caf50")
            with cols[2]: kpi("Losses",   f"{t['losses']:,}", "", "#f44336")
            with cols[3]: kpi("Win %",    f"{t['win_pct']}%", "", "#ff9800")
            with cols[4]: kpi("🏆 Titles", f"{t['titles']}",  "", "#ffd700")

            tab1, tab2, tab3 = st.tabs(["📊 All Teams", "📈 Season Trend", "⚔️ Head-to-Head"])

            with tab1:
                c1, c2 = st.columns(2)
                with c1:
                    section("All-time Wins")
                    ts_s = ts.sort_values('wins')
                    bar_colors = [TEAM_COLORS.get(t,'#4a7090') for t in ts_s['team']]
                    fig = go.Figure(go.Bar(x=ts_s['wins'], y=ts_s['team'], orientation='h',
                                           marker_color=bar_colors,
                                           text=ts_s['wins'], textposition='outside'))
                    fig.update_layout(title='Total Wins', showlegend=False, **CHART_THEME, height=440)
                    fig.update_yaxes(categoryorder='total ascending')
                    st.plotly_chart(fig, use_container_width=True)

                with c2:
                    section("Win % (min 10 matches)")
                    ts_q = ts[ts['played'] >= 10].sort_values('win_pct')
                    bar_colors2 = [TEAM_COLORS.get(t,'#4a7090') for t in ts_q['team']]
                    fig = go.Figure(go.Bar(x=ts_q['win_pct'], y=ts_q['team'], orientation='h',
                                           marker_color=bar_colors2,
                                           text=[f"{v}%" for v in ts_q['win_pct']],
                                           textposition='outside'))
                    fig.update_layout(title='Win Percentage', showlegend=False, **CHART_THEME, height=440)
                    fig.update_yaxes(categoryorder='total ascending')
                    st.plotly_chart(fig, use_container_width=True)

            with tab2:
                section(f"{sel_team} — Season-wise Performance")
                complete = mid_df_f[(mid_df_f['result_type']=='complete') & mid_df_f['winner'].notna()]
                sub = complete[(complete['team1']==sel_team)|(complete['team2']==sel_team)].copy()
                sub['won'] = sub['winner'] == sel_team
                seas = sub.groupby('season_yr').agg(played=('won','count'), wins=('won','sum')).reset_index()
                seas['losses']  = seas['played'] - seas['wins']
                seas['win_pct'] = (seas['wins']/seas['played']*100).round(1)

                if len(seas) == 0:
                    no_data_msg(f"No data for {sel_team} in selected season(s).")
                else:
                    fig = make_subplots(specs=[[{"secondary_y":True}]])
                    fig.add_trace(go.Bar(name='Wins',   x=seas['season_yr'], y=seas['wins'],
                                         marker_color='#4caf50', opacity=0.85))
                    fig.add_trace(go.Bar(name='Losses', x=seas['season_yr'], y=seas['losses'],
                                         marker_color='#f44336', opacity=0.85))
                    fig.add_trace(go.Scatter(name='Win %', x=seas['season_yr'], y=seas['win_pct'],
                                              line=dict(color='#ffd700',width=2), mode='lines+markers'),
                                  secondary_y=True)
                    fig.update_layout(barmode='stack', title=f"{sel_team} — Season Performance",
                                      height=360, **CHART_THEME)
                    fig.update_yaxes(title_text="Matches", secondary_y=False, gridcolor='#1e3a5f')
                    fig.update_yaxes(title_text="Win %",   secondary_y=True,  showgrid=False)
                    st.plotly_chart(fig, use_container_width=True)

            with tab3:
                section(f"{sel_team} — Head-to-Head")
                complete2 = mid_df_f[(mid_df_f['result_type']=='complete') & mid_df_f['winner'].notna()]
                h2h_rows = []
                for opp in all_teams:
                    if opp == sel_team: continue
                    sub2 = complete2[
                        ((complete2['team1']==sel_team)&(complete2['team2']==opp)) |
                        ((complete2['team2']==sel_team)&(complete2['team1']==opp))]
                    if len(sub2) == 0: continue
                    h2h_rows.append({'Opponent': opp, 'Played': len(sub2),
                                      'Wins':    int((sub2['winner']==sel_team).sum()),
                                      'Losses':  int((sub2['winner']==opp).sum())})
                h2h = pd.DataFrame(h2h_rows)
                if h2h.empty:
                    no_data_msg("No head-to-head data available.")
                else:
                    h2h['Win%'] = (h2h['Wins']/h2h['Played']*100).round(1)
                    opp_colors = [TEAM_COLORS.get(t,'#4a7090') for t in h2h.sort_values('Win%')['Opponent']]
                    fig = go.Figure(go.Bar(
                        x=h2h.sort_values('Win%')['Win%'],
                        y=h2h.sort_values('Win%')['Opponent'],
                        orientation='h', marker_color=opp_colors,
                        text=[f"{v}%" for v in h2h.sort_values('Win%')['Win%']],
                        textposition='outside'))
                    fig.update_layout(title=f"Win % vs each opponent", showlegend=False, **CHART_THEME, height=400)
                    fig.update_yaxes(categoryorder='total ascending')
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(h2h.sort_values('Win%',ascending=False), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: PLAYER ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Player" in page:
    if no_sel:
        no_data_msg()
    else:
        bat = compute_batting(d_f)
        bowl = compute_bowling(d_f)

        tab_b, tab_bow = st.tabs(["🏏 Batting", "🎳 Bowling"])

        with tab_b:
            if bat.empty:
                no_data_msg("No batting data for the selected season(s).")
            else:
                # Dynamic thresholds based on available data
                min_balls_sr  = max(50, bat['balls'].quantile(0.3))
                min_inn_avg   = max(3, int(bat['innings'].quantile(0.5)))

                best_sr_val  = bat[bat['balls']  >= min_balls_sr]['sr'].max()
                best_avg_val = bat[bat['innings'] >= min_inn_avg]['avg'].max()
                best_sr_name = bat[bat['balls']  >= min_balls_sr].loc[
                    bat[bat['balls']  >= min_balls_sr]['sr'].idxmax(), 'batter'] if best_sr_val else 'N/A'
                best_avg_name = bat[bat['innings'] >= min_inn_avg].loc[
                    bat[bat['innings'] >= min_inn_avg]['avg'].idxmax(), 'batter'] if not np.isnan(best_avg_val) else 'N/A'

                section("Batting KPIs")
                cols = st.columns(6)
                with cols[0]: kpi("Most Runs", f"{int(bat.iloc[0]['runs']):,}", bat.iloc[0]['batter'], "#f57c00")
                with cols[1]: kpi("Best SR",   safe_val(best_sr_val, "{:.1f}"),  best_sr_name,  "#e91e63")
                with cols[2]: kpi("Best Avg",  safe_val(best_avg_val, "{:.1f}"), best_avg_name, "#9c27b0")
                with cols[3]: kpi("Most 50s",  f"{int(bat['fifties'].max())}",
                                   bat.loc[bat['fifties'].idxmax(),'batter'], "#2196f3")
                with cols[4]: kpi("Most 100s", f"{int(bat['hundreds'].max())}",
                                   bat.loc[bat['hundreds'].idxmax(),'batter'], "#4caf50")
                with cols[5]: kpi("Most 6s",   f"{int(bat['sixes'].max())}",
                                   bat.loc[bat['sixes'].idxmax(),'batter'],   "#ff5722")

                c1, c2 = st.columns(2)
                with c1:
                    section("Top 15 Run Scorers")
                    top15 = bat.head(15)
                    fig = px.bar(top15, x='runs', y='batter', orientation='h',
                                  title='Top Run Scorers', color='runs',
                                  color_continuous_scale='OrRd', text='runs')
                    fig.update_traces(texttemplate='%{text:,}', textposition='outside')
                    fig.update_layout(showlegend=False, **CHART_THEME, height=420)
                    fig.update_yaxes(categoryorder='total ascending')
                    st.plotly_chart(fig, use_container_width=True)

                with c2:
                    section("Strike Rate vs Average")
                    qual = bat[bat['runs'] >= max(100, bat['runs'].quantile(0.4))].head(80)
                    fig = px.scatter(qual, x='avg', y='sr', size='runs',
                                      title='SR vs Average (bubble = runs)',
                                      hover_name='batter',
                                      color_discrete_sequence=['#9c27b0'])
                    apply_theme(fig, 420)
                    fig.update_xaxes(title_text='Batting Average')
                    fig.update_yaxes(title_text='Strike Rate')
                    st.plotly_chart(fig, use_container_width=True)

                section("Full Batting Stats")
                disp = bat[['batter','runs','balls','sr','avg','fifties','hundreds','fours','sixes','highest']].copy()
                disp.columns = ['Batter','Runs','Balls','SR','Avg','50s','100s','4s','6s','HS']
                st.dataframe(disp.head(60), use_container_width=True, height=380)

        with tab_bow:
            if bowl.empty:
                no_data_msg("No bowling data for the selected season(s).")
            else:
                min_overs_eco = max(2, bowl['overs'].quantile(0.3))
                min_wkts_avg  = max(3, int(bowl['wickets'].quantile(0.4)))

                best_eco_val  = bowl[bowl['overs']   >= min_overs_eco]['economy'].min()
                best_avg_val  = bowl[bowl['wickets'] >= min_wkts_avg]['avg'].min()
                best_eco_name = bowl[bowl['overs'] >= min_overs_eco].loc[
                    bowl[bowl['overs'] >= min_overs_eco]['economy'].idxmin(), 'bowler'] if not np.isnan(best_eco_val) else 'N/A'
                best_avg_name = bowl[bowl['wickets'] >= min_wkts_avg].loc[
                    bowl[bowl['wickets'] >= min_wkts_avg]['avg'].idxmin(), 'bowler'] if not np.isnan(best_avg_val) else 'N/A'

                section("Bowling KPIs")
                cols = st.columns(4)
                with cols[0]: kpi("Most Wickets", f"{int(bowl.iloc[0]['wickets'])}",
                                   bowl.iloc[0]['bowler'], "#9c27b0")
                with cols[1]: kpi("Best Economy",  safe_val(best_eco_val, "{:.2f}"), best_eco_name, "#1a73e8")
                with cols[2]: kpi("Best Avg",       safe_val(best_avg_val, "{:.1f}"), best_avg_name, "#4caf50")
                with cols[3]: kpi("Best Dot %",
                                   safe_val(bowl['dot_pct'].max(), "{:.1f}%"),
                                   bowl.loc[bowl['dot_pct'].idxmax(),'bowler'], "#ff5722")

                c1, c2 = st.columns(2)
                with c1:
                    section("Top 15 Wicket Takers")
                    top15b = bowl.head(15)
                    fig = px.bar(top15b, x='wickets', y='bowler', orientation='h',
                                  title='Top Wicket Takers', color='wickets',
                                  color_continuous_scale='Purples', text='wickets')
                    fig.update_traces(textposition='outside')
                    fig.update_layout(showlegend=False, **CHART_THEME, height=420)
                    fig.update_yaxes(categoryorder='total ascending')
                    st.plotly_chart(fig, use_container_width=True)

                with c2:
                    section("Economy vs Wickets")
                    qual_b = bowl[bowl['overs'] >= max(2, bowl['overs'].quantile(0.2))].head(80)
                    fig = px.scatter(qual_b, x='economy', y='wickets', size='overs',
                                      title='Economy vs Wickets',
                                      hover_name='bowler',
                                      color_discrete_sequence=['#9c27b0'])
                    apply_theme(fig, 420)
                    fig.update_xaxes(title_text='Economy Rate')
                    fig.update_yaxes(title_text='Wickets')
                    st.plotly_chart(fig, use_container_width=True)

                section("Full Bowling Stats")
                disp_b = bowl[['bowler','wickets','overs','economy','avg','dot_pct','matches']].copy()
                disp_b.columns = ['Bowler','Wickets','Overs','Economy','Avg','Dot%','Matches']
                st.dataframe(disp_b.head(60), use_container_width=True, height=380)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: VENUE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Venue" in page:
    if no_sel:
        no_data_msg()
    else:
        vs = compute_venue_stats(mid_df_f, d_f)
        if vs.empty:
            no_data_msg("No venue data for the selected season(s).")
        else:
            section("Venue KPIs")
            cols = st.columns(4)
            with cols[0]: kpi("Most-used Venue", vs.iloc[0]['venue'][:22], f"{vs.iloc[0]['matches']} matches", "#1a73e8")
            with cols[1]: kpi("Highest Avg Score",
                               safe_val(vs['avg_fi'].max(), "{:.0f}") if vs['avg_fi'].notna().any() else "N/A", "", "#f57c00")
            with cols[2]: kpi("Highest Score",
                               str(int(vs['high_fi'].max())) if vs['high_fi'].notna().any() else "N/A", "1st innings", "#e91e63")
            with cols[3]: kpi("Best Chasing %", f"{vs['chasing_pct'].max():.1f}%", "", "#4caf50")

            tab1, tab2, tab3 = st.tabs(["📊 Avg Scores", "🎯 Chasing Stats", "📋 Full Table"])

            with tab1:
                vs_fi = vs[vs['avg_fi'].notna()].sort_values('avg_fi', ascending=False).head(20)
                if vs_fi.empty:
                    no_data_msg("No first-innings score data.")
                else:
                    fig = px.bar(vs_fi, x='avg_fi', y='venue', orientation='h',
                                  title='Average 1st Innings Score by Venue',
                                  color='avg_fi', color_continuous_scale='Blues',
                                  text='avg_fi')
                    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
                    fig.update_layout(showlegend=False, **CHART_THEME, height=520)
                    fig.update_yaxes(categoryorder='total ascending')
                    st.plotly_chart(fig, use_container_width=True)

            with tab2:
                c1, c2 = st.columns(2)
                with c1:
                    vc = vs.sort_values('chasing_pct', ascending=False).head(18)
                    fig = px.bar(vc, x='chasing_pct', y='venue', orientation='h',
                                  title='Chasing Success %',
                                  color='chasing_pct', color_continuous_scale='RdYlGn',
                                  text='chasing_pct')
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    fig.update_layout(showlegend=False, **CHART_THEME, height=520)
                    fig.update_yaxes(categoryorder='total ascending')
                    st.plotly_chart(fig, use_container_width=True)

                with c2:
                    vc2 = vs.head(12)
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name='Chasing Wins',   y=vc2['venue'], x=vc2['chasing_wins'],
                                          orientation='h', marker_color='#1a73e8'))
                    fig.add_trace(go.Bar(name='Defending Wins', y=vc2['venue'], x=vc2['defending_wins'],
                                          orientation='h', marker_color='#f57c00'))
                    fig.update_layout(barmode='stack', title='Chasing vs Defending', **CHART_THEME, height=520)
                    fig.update_yaxes(categoryorder='total ascending')
                    st.plotly_chart(fig, use_container_width=True)

            with tab3:
                disp_v = vs[['venue','matches','avg_fi','high_fi','chasing_wins',
                               'defending_wins','chasing_pct','toss_eff']].copy()
                disp_v.columns = ['Venue','Matches','Avg 1st Inn','High Score',
                                   'Chase Wins','Def Wins','Chase%','Toss Eff%']
                st.dataframe(disp_v, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: TOSS ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Toss" in page:
    if no_sel:
        no_data_msg()
    else:
        td, ts_line, dec = compute_toss(mid_df_f)
        complete = mid_df_f[(mid_df_f['result_type']=='complete') & mid_df_f['winner'].notna()]

        if complete.empty:
            no_data_msg("No complete match data for toss analysis.")
        else:
            overall  = (complete['toss_winner']==complete['winner']).mean()*100
            field_s  = complete[complete['toss_decision']=='field']
            bat_s    = complete[complete['toss_decision']=='bat']
            field_pct = (field_s['toss_winner']==field_s['winner']).mean()*100 if len(field_s)>0 else 0
            bat_pct   = (bat_s['toss_winner']==bat_s['winner']).mean()*100 if len(bat_s)>0 else 0
            field_ch  = (complete['toss_decision']=='field').mean()*100

            section("Toss KPIs")
            cols = st.columns(4)
            with cols[0]: kpi("Overall Toss→Win", f"{overall:.1f}%",   "If toss won",       "#f57c00")
            with cols[1]: kpi("Field First Win %", f"{field_pct:.1f}%","Win after fielding", "#4caf50")
            with cols[2]: kpi("Bat First Win %",   f"{bat_pct:.1f}%",  "Win after batting",  "#e91e63")
            with cols[3]: kpi("Field Chosen %",    f"{field_ch:.1f}%", "Of all decisions",   "#1a73e8")

            c1, c2 = st.columns(2)
            with c1:
                section("Toss Decision Distribution")
                if not dec.empty:
                    fig = px.pie(dec, values='count', names='decision',
                                  title='Field vs Bat', hole=0.5,
                                  color_discrete_map={'field':'#1a73e8','bat':'#f57c00'})
                    fig.update_traces(textinfo='percent+label')
                    apply_theme(fig, 340)
                    st.plotly_chart(fig, use_container_width=True)

            with c2:
                section("Season-wise Toss Effectiveness")
                if not ts_line.empty:
                    fig = go.Figure(go.Scatter(x=ts_line['season'], y=ts_line['toss_eff'],
                                               mode='lines+markers', fill='tozeroy',
                                               line=dict(color='#ffd700', width=2),
                                               fillcolor='rgba(255,215,0,0.08)'))
                    fig.add_hline(y=50, line_dash='dash', line_color='#f44336',
                                  annotation_text='50% baseline')
                    fig.update_layout(title='Toss Win → Match Win % per Season',
                                      **CHART_THEME, height=340)
                    st.plotly_chart(fig, use_container_width=True)

            section("Team-wise Toss Impact")
            if not td.empty:
                td_s = td[td['played'] >= 5].sort_values('toss_win_pct')
                bar_colors = [TEAM_COLORS.get(t,'#4a7090') for t in td_s['team']]
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Toss Win %',  x=td_s['toss_win_pct'],  y=td_s['team'],
                                      orientation='h', marker_color='#1a73e8', opacity=0.85))
                fig.add_trace(go.Bar(name='Match Win %', x=td_s['match_win_pct'], y=td_s['team'],
                                      orientation='h', marker_color='#f57c00', opacity=0.85))
                fig.update_layout(barmode='group', title='Toss Win% vs Match Win% by Team', **CHART_THEME, height=440)
                fig.update_yaxes(categoryorder='total ascending')
                st.plotly_chart(fig, use_container_width=True)

            section("Toss Decision by Season")
            dec_s = mid_df_f.groupby(['season_yr','toss_decision']).size().reset_index(name='count')
            if not dec_s.empty:
                fig = px.bar(dec_s, x='season_yr', y='count', color='toss_decision',
                              title='Field vs Bat per Season', barmode='stack',
                              color_discrete_map={'field':'#1a73e8','bat':'#f57c00'})
                fig.update_xaxes(type='category')
                apply_theme(fig, 300)
                st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: SEASON ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Season" in page:
    if no_sel:
        no_data_msg()
    else:
        ss = compute_season_summary(mid_df_all, d_all, sel_seasons)
        if ss.empty:
            no_data_msg("No season data available.")
        else:
            section("Season KPIs")
            cols = st.columns(4)
            with cols[0]: kpi("Most Sixes (Season)", f"{ss['Total Sixes'].max():,}",
                               f"IPL {ss.loc[ss['Total Sixes'].idxmax(),'Season']}", "#ff5722")
            with cols[1]: kpi("Most Runs (Season)",  f"{ss['Total Runs'].max():,}",
                               f"IPL {ss.loc[ss['Total Runs'].idxmax(),'Season']}", "#f57c00")
            with cols[2]: kpi("Highest Team Total",  f"{ss['High Total'].max()}",
                               "1st innings record", "#e91e63")
            with cols[3]: kpi("Highest Avg Score",   f"{ss['Avg 1st Inn'].max():.1f}",
                               f"IPL {ss.loc[ss['Avg 1st Inn'].idxmax(),'Season']}", "#9c27b0")

            tab1, tab2, tab3 = st.tabs(["📊 Runs & Wickets", "💥 Sixes & Fours", "🏆 Champions"])

            with tab1:
                c1, c2 = st.columns(2)
                with c1:
                    fig = go.Figure(go.Scatter(x=ss['Season'], y=ss['Total Runs'],
                                               mode='lines+markers', fill='tozeroy',
                                               line=dict(color='#f57c00',width=2),
                                               fillcolor='rgba(245,124,0,0.12)'))
                    fig.update_layout(title='Total Runs per Season', **CHART_THEME, height=300)
                    st.plotly_chart(fig, use_container_width=True)
                with c2:
                    fig = go.Figure(go.Scatter(x=ss['Season'], y=ss['Total Wickets'],
                                               mode='lines+markers', fill='tozeroy',
                                               line=dict(color='#9c27b0',width=2),
                                               fillcolor='rgba(156,39,176,0.12)'))
                    fig.update_layout(title='Total Wickets per Season', **CHART_THEME, height=300)
                    st.plotly_chart(fig, use_container_width=True)
                fig2 = px.bar(ss, x='Season', y='Avg 1st Inn', title='Avg 1st Innings Score',
                              color='Avg 1st Inn', color_continuous_scale='Viridis',
                              text='Avg 1st Inn')
                fig2.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                fig2.update_xaxes(type='category')
                apply_theme(fig2, 280)
                st.plotly_chart(fig2, use_container_width=True)

            with tab2:
                c1, c2 = st.columns(2)
                with c1:
                    fig = go.Figure(go.Bar(x=ss['Season'].astype(str), y=ss['Total Sixes'],
                                           marker_color='#ff5722', text=ss['Total Sixes'],
                                           textposition='outside'))
                    fig.update_layout(title='Sixes per Season', **CHART_THEME, height=300)
                    st.plotly_chart(fig, use_container_width=True)
                with c2:
                    fig = go.Figure(go.Bar(x=ss['Season'].astype(str), y=ss['Total Fours'],
                                           marker_color='#1a73e8', text=ss['Total Fours'],
                                           textposition='outside'))
                    fig.update_layout(title='Fours per Season', **CHART_THEME, height=300)
                    st.plotly_chart(fig, use_container_width=True)

                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(x=ss['Season'], y=ss['Total Sixes'], name='Sixes',
                                           mode='lines+markers', line=dict(color='#ff5722',width=2)))
                fig3.add_trace(go.Scatter(x=ss['Season'], y=ss['Total Fours'], name='Fours',
                                           mode='lines+markers', line=dict(color='#1a73e8',width=2)))
                fig3.update_layout(title='Sixes vs Fours Trend', **CHART_THEME, height=280)
                st.plotly_chart(fig3, use_container_width=True)

            with tab3:
                # Show champions table filtered to selected seasons
                champ_f = CHAMP_DF[CHAMP_DF['Year'].isin(sel_seasons)]
                if not champ_f.empty:
                    rows_html = ""
                    for _, row in champ_f.iterrows():
                        cc = TEAM_COLORS.get(row['Champion'],'#ffd700')
                        rc = TEAM_COLORS.get(row['Runner-Up'],'#a0b8d0')
                        rows_html += f"""<tr>
                          <td><b>{int(row['Year'])}</b></td>
                          <td class="gold" style="color:{cc}">🏆 {row['Champion']}</td>
                          <td style="color:{rc}">{row['Runner-Up']}</td>
                          <td class="venue-cell">{row['Final Venue']}</td></tr>"""
                    st.markdown(f"""<table class="champ-table">
                      <thead><tr><th>Year</th><th>Champion</th><th>Runner-Up</th><th>Final Venue</th></tr></thead>
                      <tbody>{rows_html}</tbody></table>""", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(ss, use_container_width=True, height=500)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: PREDICTIVE ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif "Predict" in page:
    # lazy import sklearn
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
        from sklearn.preprocessing import LabelEncoder
        sklearn_ok = True
    except ImportError:
        sklearn_ok = False

    if not sklearn_ok:
        st.error("scikit-learn is not installed. Please run:\n```\npip install scikit-learn\n```")
        st.stop()

    @st.cache_data(show_spinner="Training ML models…")
    def train_models_cached(data_hash):
        complete = mid_df_all[(mid_df_all['result_type']=='complete') & mid_df_all['winner'].notna()].copy()
        complete['toss_won'] = (complete['toss_winner'] == complete['team1']).astype(int)
        complete['field']    = (complete['toss_decision'] == 'field').astype(int)

        le_team  = LabelEncoder()
        le_venue = LabelEncoder()
        le_team.fit(pd.concat([complete['team1'], complete['team2']]).unique())
        le_venue.fit(complete['venue'].unique())

        complete['t1e'] = le_team.transform(complete['team1'])
        complete['t2e'] = le_team.transform(complete['team2'])
        complete['ve']  = le_venue.transform(complete['venue'])
        complete['target'] = (complete['winner'] == complete['team1']).astype(int)

        X = complete[['t1e','t2e','ve','toss_won','field','season_yr']].fillna(0)
        y = complete['target']
        if len(y) < 20:
            return {}, le_team, le_venue

        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
        results = {}
        for name, clf in [
            ("Logistic Regression", LogisticRegression(max_iter=1000, random_state=42)),
            ("Random Forest",       RandomForestClassifier(n_estimators=100, random_state=42)),
        ]:
            clf.fit(X_tr, y_tr)
            pred = clf.predict(X_te)
            results[name] = {
                'model': clf,
                'acc':  round(accuracy_score(y_te, pred)*100, 1),
                'prec': round(precision_score(y_te, pred, zero_division=0)*100, 1),
                'rec':  round(recall_score(y_te, pred, zero_division=0)*100, 1),
                'cm':   confusion_matrix(y_te, pred),
            }
        try:
            from xgboost import XGBClassifier
            xgb = XGBClassifier(n_estimators=100, random_state=42,
                                  eval_metric='logloss', verbosity=0)
            xgb.fit(X_tr, y_tr)
            pred_x = xgb.predict(X_te)
            results['XGBoost'] = {
                'model': xgb,
                'acc':  round(accuracy_score(y_te, pred_x)*100, 1),
                'prec': round(precision_score(y_te, pred_x, zero_division=0)*100, 1),
                'rec':  round(recall_score(y_te, pred_x, zero_division=0)*100, 1),
                'cm':   confusion_matrix(y_te, pred_x),
            }
        except ImportError:
            pass
        return results, le_team, le_venue

    section("Predictive Analytics — Match Outcome Prediction")
    st.info("ML models are trained on all 1,243 real IPL matches (2008–2026). Features: Teams, Venue, Toss, Season.")

    results, le_team, le_venue = train_models_cached(len(mid_df_all))

    if not results:
        st.warning("Not enough data to train models.")
    else:
        section("Model Performance")
        cols = st.columns(len(results))
        for col, (name, r) in zip(cols, results.items()):
            with col:
                st.markdown(f"**{name}**")
                kpi("Accuracy",  f"{r['acc']}%",  "", "#4caf50")
                kpi("Precision", f"{r['prec']}%", "", "#1a73e8")
                kpi("Recall",    f"{r['rec']}%",  "", "#f57c00")

        section("Confusion Matrices")
        cols2 = st.columns(len(results))
        for col, (name, r) in zip(cols2, results.items()):
            with col:
                fig = px.imshow(r['cm'], text_auto=True,
                                x=['Pred: T2 Wins','Pred: T1 Wins'],
                                y=['Act: T2 Wins', 'Act: T1 Wins'],
                                color_continuous_scale='Blues', title=name)
                apply_theme(fig, 260)
                st.plotly_chart(fig, use_container_width=True)

        section("Algorithm Accuracy Comparison")
        acc_df = pd.DataFrame([{'Model':k,'Accuracy':v['acc']} for k,v in results.items()])
        fig = px.bar(acc_df, x='Model', y='Accuracy', text='Accuracy',
                     color='Accuracy', color_continuous_scale='Greens')
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        apply_theme(fig, 280)
        st.plotly_chart(fig, use_container_width=True)

        section("🎯 Live Match Predictor")
        known_teams  = sorted(le_team.classes_)
        known_venues = sorted(le_venue.classes_)

        col_a, col_b, col_c = st.columns(3)
        with col_a: team1  = st.selectbox("Team 1 (Batting First)", known_teams)
        with col_b: team2  = st.selectbox("Team 2 (Bowling First)", [t for t in known_teams if t != team1])
        with col_c: venue  = st.selectbox("Venue", known_venues)
        col_d, col_e, col_f = st.columns(3)
        with col_d: toss_w = st.radio("Toss Winner",   [team1, team2], horizontal=True)
        with col_e: toss_d = st.radio("Toss Decision", ["field","bat"], horizontal=True)
        with col_f: season = st.slider("Season", 2008, 2026, 2024)
        algo = st.selectbox("Algorithm", list(results.keys()))

        if st.button("🔮 Predict Winner", use_container_width=True):
            model  = results[algo]['model']
            t1e    = le_team.transform([team1])[0]
            t2e    = le_team.transform([team2])[0]
            ve     = le_venue.transform([venue])[0] if venue in le_venue.classes_ else 0
            tw     = 1 if toss_w == team1 else 0
            fd     = 1 if toss_d == 'field' else 0
            X_pred = pd.DataFrame([[t1e,t2e,ve,tw,fd,season]],
                                   columns=['t1e','t2e','ve','toss_won','field','season_yr'])
            prob   = model.predict_proba(X_pred)[0]
            t1p, t2p = prob[1]*100, prob[0]*100
            winner = team1 if t1p > t2p else team2
            wc     = TEAM_COLORS.get(winner,'#4caf50')

            st.markdown(f"""
            <div style="background:#111d2e;border:2px solid {wc};border-radius:12px;
                        padding:20px;margin:12px 0;text-align:center;">
              <div style="font-size:13px;color:#8ab4d8;margin-bottom:6px;">Predicted Winner</div>
              <div style="font-size:28px;font-weight:700;color:{wc};">🏆 {winner}</div>
              <div style="font-size:18px;color:#4caf50;margin-top:4px;">{max(t1p,t2p):.1f}% probability</div>
            </div>""", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            tc1 = TEAM_COLORS.get(team1,'#1a73e8')
            tc2 = TEAM_COLORS.get(team2,'#f57c00')
            with c1:
                fig = go.Figure(go.Bar(
                    x=[team1[:14], team2[:14]], y=[t1p, t2p],
                    marker_color=[tc1, tc2],
                    text=[f"{t1p:.1f}%", f"{t2p:.1f}%"]))
                fig.update_traces(textposition='outside', textfont_color='#fff')
                fig.update_layout(title='Win Probability', **CHART_THEME, height=300)
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig = go.Figure(go.Pie(
                    labels=[team1[:14], team2[:14]], values=[t1p, t2p],
                    hole=0.5, marker_colors=[tc1, tc2]))
                fig.update_layout(title='Probability Share', **CHART_THEME, height=300)
                st.plotly_chart(fig, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:20px 0 8px;color:#4a7090;font-size:12px;
            border-top:1px solid #1e3a5f;margin-top:30px;">
  IPL Analytics Dashboard &nbsp;&nbsp;
</div>
""", unsafe_allow_html=True)