# charts.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def line_chart_with_forecast(monthly_df, forecast_values, value_col):
    fig = go.Figure()

    # Actual line
    fig.add_trace(go.Scatter(
        x=monthly_df['month_str'], y=monthly_df[value_col],
        name='Actual', line=dict(color='#2563EB', width=2.5)
    ))

    # Forecast extension
    if forecast_values:
        last_month = monthly_df['month_str'].iloc[-1]
        period = pd.Period(last_month, 'M')
        future_months = [(period + i).strftime('%Y-%m') for i in range(1, 4)]
        fig.add_trace(go.Scatter(
            x=future_months, y=forecast_values,
            name='Forecast', line=dict(color='#F59E0B', width=2, dash='dash'),
            mode='lines+markers'
        ))

    fig.update_layout(
        title='Monthly Trend + 3-Month Forecast',
        xaxis_title='Month', yaxis_title=value_col,
        template='plotly_white', height=400
    )
    return fig

def distribution_chart(monthly_df, value_col):
    fig = px.histogram(monthly_df, x=value_col, nbins=15,
                       title='Value Distribution',
                       color_discrete_sequence=['#2563EB'])
    fig.update_layout(template='plotly_white', height=350)
    return fig

def bar_chart(monthly_df, value_col):
    fig = px.bar(monthly_df, x='month_str', y=value_col,
                 title='Monthly Breakdown',
                 color_discrete_sequence=['#7C3AED'])
    fig.update_layout(template='plotly_white', height=350, xaxis_tickangle=-45)
    return fig