import streamlit.components.v1 as components
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import plotly.express as px
import pandas as pd
from euroleague_api.game_stats import GameStats as gs
from euroleague_api.team_stats import TeamStats as ts
from euroleague_api.standings import Standings as s
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title='EuroLeague · Team Dashboard',
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state='collapsed'
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #F7F8FA;
    --surface:   #FFFFFF;
    --border:    #E8ECF0;
    --text-primary:   #0D1117;
    --text-secondary: #6B7280;
    --accent:    #0055FF;
    --accent-light: #EEF3FF;
    --win:       #16A34A;
    --win-bg:    #DCFCE7;
    --loss:      #DC2626;
    --loss-bg:   #FEE2E2;
    --radius:    12px;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem 4rem 3rem !important;
    max-width: 1280px;
}

/* ── Top header bar ── */
.dash-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1.5px solid var(--border);
}
.dash-header h1 {
    font-size: 1.45rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin: 0;
}
.dash-header span {
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: 400;
}

/* ── Section label ── */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
}

/* ── Card ── */
.card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}

/* ── Stat pill row ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
    margin-bottom: 1.4rem;
}
.stat-pill {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 14px 12px;
    text-align: center;
}
.stat-pill .val {
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.04em;
    line-height: 1;
    font-family: 'DM Mono', monospace;
}
.stat-pill .lbl {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-top: 5px;
}

/* ── Selectbox ── */
div[data-testid="stSelectbox"] > div > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    color: var(--text-primary) !important;
    box-shadow: none !important;
}
div[data-testid="stSelectbox"] label {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}

/* ── Slider ── */
div[data-testid="stSlider"] > div > div > div > div {
    background: var(--accent) !important;
}
div[data-testid="stSlider"] label {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
}

/* ── Dataframe ── */
div[data-testid="stDataFrame"] {
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden;
}
div[data-testid="stDataFrame"] table {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}
div[data-testid="stDataFrame"] th {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
    border-bottom: 1.5px solid var(--border) !important;
    padding: 10px 14px !important;
}
div[data-testid="stDataFrame"] td {
    padding: 9px 14px !important;
    border-bottom: 1px solid var(--border) !important;
}

/* ── Team logo container ── */
.team-logo-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 1.4rem 1rem;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    margin-bottom: 1rem;
}
.team-name {
    font-size: 0.9rem;
    font-weight: 600;
    text-align: center;
    color: var(--text-primary);
}

/* ── W/L badge inline ── */
.badge-w {
    background: var(--win-bg);
    color: var(--win);
    font-weight: 700;
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 99px;
    display: inline-block;
}
.badge-l {
    background: var(--loss-bg);
    color: var(--loss);
    font-weight: 700;
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 99px;
    display: inline-block;
}

/* ── Divider ── */
.divider {
    height: 1.5px;
    background: var(--border);
    border: none;
    margin: 1.6rem 0;
}

/* ── Chart wrapper ── */
.chart-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem 0.8rem 1.6rem;
    margin-bottom: 1.2rem;
}
.chart-title {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 0.8rem;
}

/* ── Streamlit columns spacing ── */
div[data-testid="column"] {
    padding: 0 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
    <div>
        <h1>🏀 EuroLeague Team Dashboard</h1>
        <span>Performance analytics · Game-by-game breakdown</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CONTROLS ROW
# ─────────────────────────────────────────────
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 2, 3])

with ctrl_col1:
    sezon = st.selectbox(
        'Season',
        [2025,2024,2023,2022,2021,2020,2019,2018,2017,2016,2015,2014],
        key='season_select'
    )

# ─────────────────────────────────────────────
#  DATA LOAD
# ─────────────────────────────────────────────
df_stats = pd.DataFrame()
df_stats2 = pd.DataFrame()

try:
    euro_img = 'https://media-cdn.incrowdsports.com/23610a1b-1c2e-4d2a-8fe4-ac2f8e400632.svg'
except:
    pass

standinga = s("E")
df_clubs = standinga.get_standings(season=sezon, round_number=1, endpoint='basicstandings')
df_clubs = df_clubs[['club.name','club.editorialName','club.images.crest','club.tvCode','club.code']].copy()
df_clubs = df_clubs.sort_values(by='club.name', ascending=True)
box1 = df_clubs['club.name'].values.tolist()

with ctrl_col2:
    option = st.selectbox('Team', (box1), key='team_select', index=None)

with ctrl_col3:
    value1 = st.slider(
        label='Last N Games',
        min_value=1, max_value=38, step=1, key="games_slider"
    )
    game_label = f'Showing last **{value1}** {"game" if value1 == 1 else "games"}'
    st.caption(game_label)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN CONTENT
# ─────────────────────────────────────────────
if option is not None:

    takm1 = df_clubs.loc[df_clubs['club.name'] == option, 'club.code'].values[0]
    resm  = df_clubs.loc[df_clubs['club.name'] == option, 'club.images.crest'].values[0]

    # ── Left sidebar: team identity + avg stats
    left_col, right_col = st.columns([1, 3])

    # ── Fetch game codes
    team_stats  = ts("E")
    game_stats  = gs("E")
    df_results_all = team_stats.get_gamecodes_season(season=sezon)
    df_results1 = df_results_all.loc[df_results_all['homecode'] == takm1].copy()
    df_results2 = df_results_all.loc[df_results_all['awaycode'] == takm1].copy()
    df_results_team1 = pd.concat([df_results1, df_results2])
    df_results_team1 = df_results_team1.sort_values(by='gameCode', ascending=False)

    df_results_team1.loc[df_results_team1['homecode'] == takm1, 'saha'] = 'H'
    df_results_team1.loc[df_results_team1['homecode'] != takm1, 'saha'] = 'A'
    df_results_team1.loc[(df_results_team1['homecode'] == takm1) & (df_results_team1['homescore'] > df_results_team1['awayscore']), 'W/L'] = '1'
    df_results_team1.loc[(df_results_team1['homecode'] == takm1) & (df_results_team1['homescore'] < df_results_team1['awayscore']), 'W/L'] = '0'
    df_results_team1.loc[(df_results_team1['homecode'] != takm1) & (df_results_team1['homescore'] > df_results_team1['awayscore']), 'W/L'] = '0'
    df_results_team1.loc[(df_results_team1['homecode'] != takm1) & (df_results_team1['homescore'] < df_results_team1['awayscore']), 'W/L'] = '1'
    df_results_team1.loc[df_results_team1['saha'] == 'H', 'P+'] = df_results_team1['homescore']
    df_results_team1.loc[df_results_team1['saha'] == 'A', 'P+'] = df_results_team1['awayscore']
    df_results_team1.loc[df_results_team1['saha'] == 'H', 'P-'] = df_results_team1['awayscore']
    df_results_team1.loc[df_results_team1['saha'] == 'A', 'P-'] = df_results_team1['homescore']

    uzunluk = len(df_results_team1)
    if value1 <= uzunluk:
        uzunluk = value1

    df_results_team1 = df_results_team1.head(uzunluk)
    game_codes  = df_results_team1['gameCode'].values.tolist()
    durum       = df_results_team1['W/L'].values.tolist()
    saha        = df_results_team1['saha'].values.tolist()
    round_list  = df_results_team1['Round'].values.tolist()
    points_eks  = df_results_team1['P-'].values.tolist()
    mimle = 0

    for r in game_codes:
        df2 = game_stats.get_game_stats(season=sezon, game_code=r)
        if saha[mimle] == 'H':
            df2 = df2[['local.total.points','local.total.accuracyMade','local.total.accuracyAttempted',
                        'local.total.totalRebounds','local.total.assistances','local.total.turnovers']].copy()
        else:
            df2 = df2[['road.total.points','road.total.accuracyMade','road.total.accuracyAttempted',
                        'road.total.totalRebounds','road.total.assistances','road.total.turnovers']].copy()
        df2.columns = ['Points','Accuracy Made','Accuracy Attempted','Rebounds','Assists','Turnovers']
        df2['Points-']   = points_eks[mimle]
        df2['W/L']       = durum[mimle]
        df2['H/A']       = saha[mimle]
        df2['%Accuracy'] = df2['Accuracy Made'] / df2['Accuracy Attempted']
        df2['Round']     = round_list[mimle]
        df_stats = pd.concat([df2, df_stats])
        mimle += 1

    df_stats.loc[df_stats['W/L'] == '1', '-W/L-'] = 'W'
    df_stats.loc[df_stats['W/L'] == '0', '-W/L-'] = 'L'

    # ── Averages
    df_team1 = df_stats.copy()
    df_team1['All'] = 'All'
    df_team1 = pd.pivot_table(
        df_team1,
        values=['Points','Points-','Accuracy Attempted','Rebounds','Assists','Turnovers'],
        index=['All'], aggfunc="sum"
    ).reset_index().drop(['All'], axis=1)
    df_team1 = df_team1[['Points','Points-','Assists','Rebounds','Turnovers','Accuracy Attempted']].copy()
    df_team1.columns = ['Points','Points-','Assists','Rebounds','Turnovers','ScoreAttempt']
    for col in df_team1.columns:
        df_team1[col] = (df_team1[col] / uzunluk).round(1)

    df_team1_orj = df_team1.copy()
    df_team1_orj['Off. Accuracy'] = (df_team1_orj['Points'] / df_team1_orj['ScoreAttempt'] * 100).round(1)
    df_team1_orj['Off. Accuracy'] = df_team1_orj['Off. Accuracy'].astype(str) + '%'

    # ── Left column: team card + averages
    with left_col:
        st.markdown(f"""
        <div class="team-logo-wrap">
            <img src="{resm}" width="90" style="object-fit:contain;">
            <div class="team-name">{option}</div>
        </div>
        """, unsafe_allow_html=True)

        # Averages table
        avg_data = {
            'Metric': ['Pts For', 'Pts Agst', 'Assists', 'Rebounds', 'Turnovers', 'Off. Acc.'],
            'Avg': [
                df_team1_orj['Points'].values[0],
                df_team1_orj['Points-'].values[0],
                df_team1_orj['Assists'].values[0],
                df_team1_orj['Rebounds'].values[0],
                df_team1_orj['Turnovers'].values[0],
                df_team1_orj['Off. Accuracy'].values[0],
            ]
        }
        st.markdown('<p class="section-label">Per-game averages</p>', unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(avg_data),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Metric": st.column_config.TextColumn("Metric"),
                "Avg": st.column_config.TextColumn("Avg"),
            }
        )

    # ── Right column: charts
    with right_col:

        # ── Color helpers
        results   = df_stats['-W/L-'].tolist()
        rounds    = df_stats['Round'].tolist()
        home_away = df_stats['H/A'].tolist()

        WIN_COLOR  = '#16A34A'
        LOSS_COLOR = '#DC2626'
        WIN_FILL   = 'rgba(22,163,74,0.12)'
        LOSS_FILL  = 'rgba(220,38,38,0.12)'
        ACCENT     = '#0055FF'
        GRID_COLOR = '#E8ECF0'
        BG         = '#FFFFFF'

        marker_colors = [WIN_COLOR if r == 'W' else LOSS_COLOR for r in results]

        # ────────────────────────────────
        # CHART 1 — Match results timeline
        # ────────────────────────────────
        st.markdown('<div class="chart-card"><p class="chart-title">Match Results Timeline</p>', unsafe_allow_html=True)

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=rounds,
            y=[1] * len(rounds),
            mode='markers+text',
            marker=dict(
                symbol='circle',
                size=30,
                color=marker_colors,
                opacity=1,
                line=dict(color='white', width=2),
            ),
            text=home_away,
            textposition='middle center',
            textfont=dict(family='DM Sans, sans-serif', size=10, color='white'),
            hovertemplate='<b>Round %{x}</b><br>Result: %{customdata[0]}<br>%{customdata[1]}<extra></extra>',
            customdata=list(zip(results, home_away)),
        ))

        # W / L legend annotations
        fig1.add_annotation(x=1, y=1, xref='paper', yref='paper',
            text='<span style="color:#16A34A;">●</span> Win  <span style="color:#DC2626;">●</span> Loss',
            showarrow=False, font=dict(size=11, family='DM Sans'), xanchor='right', yanchor='bottom')

        fig1.update_layout(
            xaxis=dict(
                title=dict(text='Round', font=dict(family='DM Sans', size=12, color='#6B7280')),
                tickmode='array', tickvals=rounds, ticktext=[str(r) for r in rounds],
                tickfont=dict(family='DM Mono', size=11, color='#6B7280'),
                showgrid=False, zeroline=False,
            ),
            yaxis=dict(visible=False, range=[0.4, 1.6]),
            plot_bgcolor=BG, paper_bgcolor=BG,
            height=130,
            margin=dict(l=10, r=10, t=10, b=40),
            showlegend=False,
        )
        st.plotly_chart(fig1, use_container_width=True, config={'staticPlot': True})
        st.markdown('</div>', unsafe_allow_html=True)

        # ────────────────────────────────
        # CHART 2 — Shooting Accuracy
        # ────────────────────────────────
        st.markdown('<div class="chart-card"><p class="chart-title">Shooting Accuracy per Game</p>', unsafe_allow_html=True)

        df_acc = df_stats[['Round', '-W/L-', '%Accuracy']].copy()
        acc_colors = [WIN_COLOR if r == 'W' else LOSS_COLOR for r in df_acc['-W/L-']]

        fig2 = go.Figure()

        # Shaded area
        fig2.add_trace(go.Scatter(
            x=df_acc['Round'], y=df_acc['%Accuracy'],
            fill='tozeroy',
            fillcolor='rgba(0,85,255,0.06)',
            mode='none', showlegend=False,
        ))
        # Line
        fig2.add_trace(go.Scatter(
            x=df_acc['Round'], y=df_acc['%Accuracy'],
            mode='lines',
            line=dict(color='#CBD5E1', width=1.5, dash='dot'),
            showlegend=False,
        ))
        # Dots
        fig2.add_trace(go.Scatter(
            x=df_acc['Round'], y=df_acc['%Accuracy'],
            mode='markers',
            marker=dict(color=acc_colors, size=10, line=dict(color='white', width=1.5)),
            hovertemplate='Round %{x}<br>Accuracy: %{y:.1%}<extra></extra>',
            showlegend=False,
        ))
        # 50% reference line
        fig2.add_hline(
            y=0.50,
            line=dict(color='#94A3B8', width=1, dash='dash'),
            annotation_text='50%',
            annotation_position='left',
            annotation_font=dict(size=10, color='#94A3B8', family='DM Mono'),
        )
        # Legend markers
        fig2.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
            marker=dict(color=WIN_COLOR, size=9), name='Win'))
        fig2.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
            marker=dict(color=LOSS_COLOR, size=9), name='Loss'))

        fig2.update_layout(
            xaxis=dict(
                title=dict(text='Round', font=dict(family='DM Sans', size=12, color='#6B7280')),
                tickmode='array', tickvals=df_acc['Round'].tolist(),
                tickfont=dict(family='DM Mono', size=11, color='#6B7280'),
                showgrid=False, zeroline=False,
            ),
            yaxis=dict(
                title=dict(text='Accuracy', font=dict(family='DM Sans', size=12, color='#6B7280')),
                tickformat='.0%',
                tickfont=dict(family='DM Mono', size=11, color='#6B7280'),
                showgrid=True,
                gridcolor=GRID_COLOR,
                gridwidth=1,
                zeroline=False,
                range=[0.30, 0.70],
            ),
            plot_bgcolor=BG,
            paper_bgcolor=BG,
            height=300,
            margin=dict(l=50, r=20, t=10, b=40),
            legend=dict(
                orientation='h', yanchor='bottom', y=1.02,
                xanchor='right', x=1,
                font=dict(family='DM Sans', size=11, color='#6B7280'),
                bgcolor='rgba(0,0,0,0)',
            ),
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ────────────────────────────────
        # CHART 3 — Points For vs Against
        # ────────────────────────────────
        st.markdown('<div class="chart-card"><p class="chart-title">Points Scored vs Conceded</p>', unsafe_allow_html=True)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=df_stats['Round'], y=df_stats['Points'],
            name='Points For',
            marker_color=ACCENT,
            opacity=0.85,
            hovertemplate='Round %{x}<br>Scored: %{y}<extra></extra>',
        ))
        fig3.add_trace(go.Bar(
            x=df_stats['Round'], y=df_stats['Points-'],
            name='Points Against',
            marker_color='#E2E8F0',
            hovertemplate='Round %{x}<br>Conceded: %{y}<extra></extra>',
        ))
        fig3.update_layout(
            barmode='group',
            bargap=0.3,
            bargroupgap=0.05,
            xaxis=dict(
                title=dict(text='Round', font=dict(family='DM Sans', size=12, color='#6B7280')),
                tickmode='array', tickvals=df_stats['Round'].tolist(),
                tickfont=dict(family='DM Mono', size=11, color='#6B7280'),
                showgrid=False, zeroline=False,
            ),
            yaxis=dict(
                title=dict(text='Points', font=dict(family='DM Sans', size=12, color='#6B7280')),
                tickfont=dict(family='DM Mono', size=11, color='#6B7280'),
                showgrid=True, gridcolor=GRID_COLOR, gridwidth=1, zeroline=False,
            ),
            plot_bgcolor=BG, paper_bgcolor=BG,
            height=280,
            margin=dict(l=50, r=20, t=10, b=40),
            legend=dict(
                orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(family='DM Sans', size=11, color='#6B7280'),
                bgcolor='rgba(0,0,0,0)',
            ),
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Full-width game log table
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Game Log</p>', unsafe_allow_html=True)

    display_df = df_stats[['Round','H/A','-W/L-','Points','Points-','Assists','Rebounds','Turnovers','%Accuracy']].copy()
    display_df['%Accuracy'] = (display_df['%Accuracy'] * 100).round(1).astype(str) + '%'
    display_df.columns = ['Round','H/A','Result','Pts For','Pts Agst','Assists','Rebounds','Turnovers','Accuracy']
    display_df = display_df.reset_index(drop=True)

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Result": st.column_config.TextColumn("Result"),
            "Pts For": st.column_config.NumberColumn("Pts For", format="%d"),
            "Pts Agst": st.column_config.NumberColumn("Pts Agst", format="%d"),
            "Assists": st.column_config.NumberColumn("Assists", format="%d"),
            "Rebounds": st.column_config.NumberColumn("Rebounds", format="%d"),
            "Turnovers": st.column_config.NumberColumn("Turnovers", format="%d"),
        }
    )

else:
    # ── Empty state
    st.markdown("""
    <div style="
        text-align:center;
        padding: 5rem 2rem;
        color: #9CA3AF;
        font-family: 'DM Sans', sans-serif;
    ">
        <div style="font-size:3rem; margin-bottom:1rem;">🏀</div>
        <div style="font-size:1.1rem; font-weight:600; color:#374151;">Select a team to get started</div>
        <div style="font-size:0.88rem; margin-top:0.5rem;">Choose a season and team from the controls above</div>
    </div>
    """, unsafe_allow_html=True)
