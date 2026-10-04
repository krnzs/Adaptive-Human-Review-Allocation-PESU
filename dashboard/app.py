import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Reliability Intelligence",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# PATHS
# ============================================================

BASE = Path(__file__).resolve().parent.parent

# ============================================================
# LOAD RESULTS
# ============================================================

summary = pd.read_csv(
    BASE / "results" / "final_experiment_summary.csv"
)

drift = pd.read_csv(
    BASE / "results" / "drift_results.csv"
)

models = pd.read_csv(
    BASE / "results" / "model_comparison.csv"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(70, 100, 255, 0.14), transparent 28%),
        radial-gradient(circle at 90% 5%, rgba(150, 70, 255, 0.10), transparent 25%),
        #08090d;
    color: #f5f5f7;
}

.block-container {
    max-width: 1450px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* HERO */

.hero-title {
    font-size: 4rem;
    font-weight: 700;
    line-height: 0.98;
    letter-spacing: -0.065em;
    color: #f5f5f7;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.15rem;
    line-height: 1.6;
    color: #92929c;
    max-width: 850px;
    margin-bottom: 1.8rem;
}

/* PILLS */

.pill {
    display: inline-block;
    padding: 8px 14px;
    margin-right: 6px;
    margin-bottom: 6px;
    border-radius: 999px;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.075);
    color: #aaaab4;
    font-size: 12px;
}

/* METRIC CARDS */

.metric-card {
    min-height: 145px;
    padding: 25px;
    border-radius: 25px;
    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.075),
        rgba(255,255,255,0.025)
    );
    border: 1px solid rgba(255,255,255,0.075);
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
}

.metric-label {
    color: #92929c;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.04em;
}

.metric-value {
    color: #f5f5f7;
    font-size: 38px;
    font-weight: 700;
    letter-spacing: -0.055em;
    margin-top: 12px;
}

.metric-caption {
    color: #666670;
    font-size: 12px;
    margin-top: 8px;
}

/* HIGHLIGHT */

.highlight-card {
    margin-top: 28px;
    padding: 32px;
    border-radius: 30px;
    background:
        radial-gradient(
            circle at 10% 20%,
            rgba(70,110,255,0.20),
            transparent 45%
        ),
        linear-gradient(
            135deg,
            rgba(55,80,190,0.18),
            rgba(130,70,220,0.08)
        );
    border: 1px solid rgba(100,120,255,0.20);
    box-shadow: 0 25px 80px rgba(0,0,0,0.25);
}

.highlight-label {
    color: #aeb5ff;
    font-size: 13px;
    font-weight: 600;
}

.highlight-number {
    color: #ffffff;
    font-size: 58px;
    font-weight: 700;
    letter-spacing: -0.065em;
    margin-top: 5px;
}

.highlight-description {
    color: #9696a2;
    font-size: 14px;
    line-height: 1.6;
    max-width: 750px;
}

/* SECTION */

.section-title {
    color: #f5f5f7;
    font-size: 22px;
    font-weight: 600;
    letter-spacing: -0.035em;
    margin-top: 45px;
    margin-bottom: 12px;
}

/* DIVIDER */

hr {
    border-color: rgba(255,255,255,0.06);
}

/* SELECTOR */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
}

/* SLIDER LABEL */

.stSelectSlider label {
    color: #8f8f99 !important;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

/* FOOTER */

.dashboard-footer {
    text-align: center;
    color: #555660;
    font-size: 11px;
    padding: 25px;
}
</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# PLOTLY STYLE
# ============================================================

def style_chart(fig, height=430):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(
            l=15,
            r=15,
            t=60,
            b=25
        ),
        font=dict(
            family="Inter, Arial, sans-serif",
            color="#A0A0AA"
        ),
        title_font=dict(
            size=18,
            color="#F5F5F7"
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#A0A0AA"
            )
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color="#777780"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.055)",
            zeroline=False,
            color="#777780"
        )
    )

    return fig


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero-title">Reliability<br>Intelligence.</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Adaptive human-review allocation for reliable machine learning '
    'under distribution shift.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<span class="pill">BIGFLOW-NIDS</span>'
    '<span class="pill">66.9M benchmark records</span>'
    '<span class="pill">Temporal evaluation</span>'
    '<span class="pill">Human-review simulation</span>',
    unsafe_allow_html=True
)

# ============================================================
# TOP METRICS
# ============================================================

st.markdown(
    '<div style="height:28px;"></div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        '<div class="metric-card">'
        '<div class="metric-label">EVALUATION SET</div>'
        '<div class="metric-value">75K</div>'
        '<div class="metric-caption">temporal shifted predictions</div>'
        '</div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        '<div class="metric-card">'
        '<div class="metric-label">PREDICTION ERRORS</div>'
        '<div class="metric-value">3,427</div>'
        '<div class="metric-caption">4.57% error rate</div>'
        '</div>',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        '<div class="metric-card">'
        '<div class="metric-label">FEATURES</div>'
        '<div class="metric-value">49</div>'
        '<div class="metric-caption">network-flow attributes</div>'
        '</div>',
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        '<div class="metric-card">'
        '<div class="metric-label">REVIEW BUDGETS</div>'
        '<div class="metric-value">4</div>'
        '<div class="metric-caption">1% · 2% · 5% · 10%</div>'
        '</div>',
        unsafe_allow_html=True
    )

# ============================================================
# MAIN INSIGHT
# ============================================================

st.markdown(
    '<div class="highlight-card">'
    '<div class="highlight-label">ADAPTIVE REVIEW ALLOCATION</div>'
    '<div class="highlight-number">15.6%</div>'
    '<div class="highlight-description">'
    'Errors captured when only 1% of shifted-test predictions '
    'were allocated to simulated human review.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# REVIEW STRATEGY
# ============================================================

st.markdown(
    '<div class="section-title">Review Strategy</div>',
    unsafe_allow_html=True
)

budget = st.select_slider(
    "Human review capacity",
    options=[1, 2, 5, 10],
    value=1,
    format_func=lambda x: f"{x}%"
)

selected = summary[
    summary["review_budget_percent"] == budget
].copy()

selected = selected.sort_values(
    "error_capture_percent",
    ascending=True
)

# ============================================================
# ERROR CAPTURE CHART
# ============================================================

fig = go.Figure()

for _, row in selected.iterrows():

    strategy = row["strategy"]

    if strategy == "Dynamic_Adaptive":
        bar_color = "#4C78FF"
    elif strategy == "Confidence":
        bar_color = "#8B8B96"
    elif strategy == "Static_MultiFactor":
        bar_color = "#74747F"
    elif strategy == "Random":
        bar_color = "#4E4E58"
    else:
        bar_color = "#3A3A43"

    fig.add_trace(
        go.Bar(
            x=[row["error_capture_percent"]],
            y=[strategy],
            orientation="h",
            name=strategy,
            marker=dict(
                color=bar_color
            ),
            text=[
                f'{row["error_capture_percent"]:.1f}%'
            ],
            textposition="outside",
            hovertemplate=(
                f"<b>{strategy}</b><br>"
                f"Errors captured: "
                f"{row['error_capture_percent']:.2f}%"
                "<extra></extra>"
            ),
            showlegend=False
        )
    )

fig.update_layout(
    title=f"Errors captured at {budget}% review capacity",
    xaxis=dict(
        title="Errors captured (%)",
        range=[0, 100]
    ),
    yaxis=dict(
        title=""
    )
)

style_chart(fig, 430)

st.plotly_chart(
    fig,
    width="stretch",
    config={
        "displayModeBar": False
    }
)

# ============================================================
# TWO COLUMN SECTION
# ============================================================

left, right = st.columns(2)

# ============================================================
# REVIEW EFFICIENCY
# ============================================================

with left:

    st.markdown(
        '<div class="section-title">Review Efficiency</div>',
        unsafe_allow_html=True
    )

    fig = go.Figure()

    strategies = summary["strategy"].unique()

    for strategy in strategies:

        d = summary[
            summary["strategy"] == strategy
        ].sort_values(
            "review_budget_percent"
        )

        is_adaptive = strategy == "Dynamic_Adaptive"

        fig.add_trace(
            go.Scatter(
                x=d["review_budget_percent"],
                y=d["errors_per_1000_reviews"],
                mode="lines+markers",
                name=strategy,
                line=dict(
                    width=3 if is_adaptive else 1.5
                ),
                marker=dict(
                    size=8
                ),
                opacity=1 if is_adaptive else 0.55
            )
        )

    fig.update_layout(
        title="Errors caught per 1,000 reviews",
        xaxis_title="Review budget (%)",
        yaxis_title="Errors / 1,000 reviews"
    )

    style_chart(fig, 430)

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )

# ============================================================
# DISTRIBUTION SHIFT
# ============================================================

with right:

    st.markdown(
        '<div class="section-title">Distribution Shift</div>',
        unsafe_allow_html=True
    )

    top_drift = (
        drift
        .sort_values(
            "psi",
            ascending=False
        )
        .head(8)
        .sort_values(
            "psi",
            ascending=True
        )
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=top_drift["psi"],
            y=top_drift["feature"],
            orientation="h",
            marker=dict(
                color="#8B5CF6"
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "PSI: %{x:.3f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title="Features with strongest distribution shift",
        xaxis_title="Population Stability Index",
        yaxis_title=""
    )

    style_chart(fig, 430)

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )

# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">Prediction Engine</div>',
    unsafe_allow_html=True
)

fig = go.Figure()

metrics = [
    "Precision",
    "Recall",
    "F1",
    "ROC_AUC"
]

for metric in metrics:

    fig.add_trace(
        go.Bar(
            name=metric,
            x=models["Model"],
            y=models[metric]
        )
    )

fig.update_layout(
    title="Base model performance",
    barmode="group",
    yaxis=dict(
        range=[0, 1]
    )
)

style_chart(fig, 430)

st.plotly_chart(
    fig,
    width="stretch",
    config={
        "displayModeBar": False
    }
)

# ============================================================
# EXPERIMENT TABLE
# ============================================================

st.markdown(
    '<div class="section-title">Experiment Detail</div>',
    unsafe_allow_html=True
)

display_df = selected[
    [
        "strategy",
        "reviews",
        "errors_caught",
        "error_capture_percent",
        "errors_per_1000_reviews"
    ]
].copy()

display_df.columns = [
    "Strategy",
    "Reviews",
    "Errors Caught",
    "Capture (%)",
    "Errors / 1K Reviews"
]

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

# ============================================================
# METHODOLOGY
# ============================================================

st.markdown(
    '<div class="highlight-card">'
    '<div class="highlight-label">EVALUATION METHOD</div>'
    '<div class="highlight-description">'
    'Human review is simulated using fixed review budgets. '
    'Ground-truth labels are used only to measure how many '
    'actual prediction errors would have been caught. '
    'Shifted-test labels are not used to rank the predictions.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="dashboard-footer">'
    'ADAPTIVE HUMAN-REVIEW ALLOCATION · CAPSTONE RESEARCH'
    '</div>',
    unsafe_allow_html=True
)