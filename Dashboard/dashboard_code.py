import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
import numpy as np

# --------------------------
# LOAD DATA (SAFE PATH)
# --------------------------
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "..", "Data", "cleaned_data.csv")

df = pd.read_csv(file_path)

# Numeric data
numeric_df = df.select_dtypes(include='number')

# KPIs
avg_prod = round(df['productivity'].mean(), 2)
avg_study = round(df['study'].mean(), 2)
avg_sleep = round(df['sleep'].mean(), 2)

# --------------------------
# CREATE LAYOUT
# --------------------------
fig = make_subplots(
    rows=2, cols=2,
    vertical_spacing=0.12,
    horizontal_spacing=0.08,
    subplot_titles=(
        "Instagram vs Productivity",
        "Study vs Productivity",
        "Sleep vs Productivity",
        "Correlation Matrix"
    )
)

# --------------------------
# 1. Instagram vs Productivity
# --------------------------
fig.add_trace(
    go.Scatter(
        x=df["instagram"],
        y=df["productivity"],
        mode='markers',
        marker=dict(
            color=df["productivity"],
            colorscale="Reds",
            size=9,
            opacity=0.7,
            showscale=False
        )
    ),
    row=1, col=1
)

# --------------------------
# 2. Study vs Productivity + TREND LINE
# --------------------------
fig.add_trace(
    go.Scatter(
        x=df["study"],
        y=df["productivity"],
        mode='markers',
        marker=dict(
            color="#27ae60",
            size=9,
            opacity=0.6,
            showscale=False
        )
    ),
    row=1, col=2
)

# Trend line
z = np.polyfit(df["study"], df["productivity"], 1)
p = np.poly1d(z)

fig.add_trace(
    go.Scatter(
        x=df["study"],
        y=p(df["study"]),
        mode='lines',
        line=dict(color='darkgreen'),
        showlegend=False,
    ),
    row=1, col=2
)

# --------------------------
# 3. Sleep vs Productivity
# --------------------------
fig.add_trace(
    go.Scatter(
        x=df["sleep"],
        y=df["productivity"],
        mode='markers',
        marker=dict(
            color="#2980b9",
            size=9,
            opacity=0.6,
            showscale=False
        )
    ),
    row=2, col=1
)

# --------------------------
# 4. HEATMAP
# --------------------------
corr = numeric_df.corr()

fig.add_trace(
    go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        text=corr.values,
        texttemplate="%{text:.2f}",
        colorscale="RdBu",
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Correlation",len=0.6)
    ),
    row=2, col=2
)

# --------------------------
# INSIGHT BOX
# --------------------------
fig.add_annotation(
    text=(
        "<b>Key Insights</b><br>"
        "Instagram ↓ Productivity | Study ↑ Productivity | Sleep helps performance"
    ),
    x=0.5, y=-0.12,
    xref="paper", yref="paper",
    showarrow=False,
    align="center",
    font=dict(size=12)
)

# --------------------------
# FINAL LAYOUT
# --------------------------
fig.update_layout(
    height=750,
    autosize=True,

    margin=dict(l=60, r=60, t=100, b=100),

    paper_bgcolor="#eef2f7",
    plot_bgcolor="#ffffff",

    title={
        'text': "<b>📊 Student Productivity Dashboard</b><br>"
                f"<span style='font-size:14px;'>Avg Productivity: {avg_prod} | Study: {avg_study} hrs | Sleep: {avg_sleep} hrs</span>",
        'x': 0.5,
        'xanchor': 'center',
        'font': dict(size=26)
    },

    font=dict(family="Arial", size=12),
    showlegend=False
)

# Grid
fig.update_xaxes(showgrid=True, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridcolor='lightgray')

# --------------------------
# SHOW
# --------------------------
fig.show(config={'responsive': True})