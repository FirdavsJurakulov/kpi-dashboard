# app.py
import streamlit as st
import pandas as pd
from analysis import compute_kpis
from charts import line_chart_with_forecast, distribution_chart, bar_chart
from narrative import generate_narrative

st.set_page_config(
    page_title="AI KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Powered KPI Dashboard")
st.caption("Upload your CSV → Get charts + an AI executive summary instantly")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    uploaded = st.file_uploader("Upload CSV", type=['csv'])
    st.markdown("---")
    st.markdown("**Sample dataset:** [Superstore Sales](https://bit.ly/superstore-csv)")

if uploaded is None:
    st.info("👈 Upload a CSV file to get started, or use the sample dataset.")
    st.stop()

# --- Load Data ---
try:
    df = pd.read_csv(uploaded, encoding='utf-8')
except UnicodeDecodeError:
    uploaded.seek(0)  # reset file pointer after failed read
    df = pd.read_csv(uploaded, encoding='latin-1')
st.success(f"Loaded **{len(df):,} rows** and **{len(df.columns)} columns**")

col1, col2 = st.columns(2)
with col1:
    date_col = st.selectbox("📅 Select date column", df.columns.tolist())
with col2:
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    value_col = st.selectbox("💰 Select metric to analyze", numeric_cols)

if st.button("🚀 Generate Dashboard", type="primary", use_container_width=True):
    with st.spinner("Crunching numbers..."):
        stats = compute_kpis(df, date_col, value_col)
        monthly_df = stats.pop('monthly_data')

    # --- KPI Cards ---
    st.markdown("### Key Metrics")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total", f"{stats['total']:,.0f}")
    k2.metric("Monthly Avg", f"{stats['mean']:,.0f}")
    k3.metric("MoM Change", f"{stats['mom_change_pct']}%",
              delta=stats['mom_change_pct'])
    k4.metric("Trend", stats.get('trend_direction', 'N/A').capitalize())

    # --- Charts ---
    st.markdown("### Visualizations")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            line_chart_with_forecast(monthly_df, stats['forecast_3m'], value_col),
            use_container_width=True
        )
    with c2:
        st.plotly_chart(bar_chart(monthly_df, value_col), use_container_width=True)

    st.plotly_chart(distribution_chart(monthly_df, value_col), use_container_width=True)

    # --- AI Narrative ---
    st.markdown("### 🤖 AI Executive Summary")
    with st.spinner("Generating AI insights..."):
        narrative = generate_narrative(stats, value_col)

    st.info(narrative)
    st.download_button(
        "📥 Download Summary",
        data=narrative,
        file_name="executive_summary.txt",
        mime="text/plain"
    )