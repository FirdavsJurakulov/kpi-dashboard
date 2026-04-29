# narrative.py
import anthropic

client = anthropic.Anthropic()

def generate_narrative(stats: dict, metric_name: str) -> str:
    trend = stats.get('trend_direction', 'unknown')
    mom = stats.get('mom_change_pct')
    anomalies = stats.get('anomalies', [])
    forecast = stats.get('forecast_3m', [])

    summary_prompt = f"""You are a senior business analyst writing for a non-technical executive.
Analyze these KPI statistics and write a concise executive briefing.

Metric analyzed: {metric_name}
- Total: {stats['total']:,.2f}
- Monthly average: {stats['mean']:,.2f}
- Best month: {stats['max']:,.2f}
- Worst month: {stats['min']:,.2f}
- Month-over-month change: {mom}%
- Overall trend: {trend}
- Anomaly months (unusual spikes/dips): {', '.join(anomalies) if anomalies else 'None detected'}
- 3-month forecast: {[round(v,2) for v in forecast]}

Write exactly 5 bullet points:
- Key performance summary (1 sentence)
- Trend assessment (1 sentence)  
- Notable anomalies or risks (1 sentence)
- Forecast outlook (1 sentence)
- Recommended action (1 sentence)

Use plain English. Be specific with numbers. No fluff."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=400,
        messages=[{"role": "user", "content": summary_prompt}]
    )
    return message.content[0].text