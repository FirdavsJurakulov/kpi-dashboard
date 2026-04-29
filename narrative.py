# narrative.py
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_narrative(stats: dict, metric_name: str) -> str:
    mom = stats.get('mom_change_pct')
    anomalies = stats.get('anomalies', [])
    forecast = stats.get('forecast_3m', [])

    prompt = f"""You are a senior business analyst writing for a non-technical executive.
Analyze these KPI statistics and write a concise executive briefing.

Metric analyzed: {metric_name}
- Total: {stats['total']:,.2f}
- Monthly average: {stats['mean']:,.2f}
- Best month: {stats['max']:,.2f}
- Worst month: {stats['min']:,.2f}
- Month-over-month change: {mom}%
- Overall trend: {stats.get('trend_direction', 'unknown')}
- Anomaly months: {', '.join(anomalies) if anomalies else 'None detected'}
- 3-month forecast: {[round(v,2) for v in forecast]}

Write exactly 5 bullet points:
- Key performance summary (1 sentence)
- Trend assessment (1 sentence)
- Notable anomalies or risks (1 sentence)
- Forecast outlook (1 sentence)
- Recommended action (1 sentence)

Use plain English. Be specific with numbers. No fluff."""

    response = model.generate_content(prompt)
    return response.text