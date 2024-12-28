from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import scipy.stats as st


def plot_vars_distribution(stat_data: pd.DataFrame) -> go.Figure:
    fig = make_subplots(rows=1, cols=len(stat_data.columns))
    for var, i in zip(stat_data.columns, range(1,len(stat_data.columns))):
        fig.add_trace(
            go.Histogram(x=stat_data[var], nbinsx=14), row=1, col=i)

    return fig


def plot_tornado(df_affection: pd.DataFrame) -> go.Figure:
    fig = make_subplots(rows=1,cols=2)
    fig.add_trace(
        go.Bar(
            x=df_affection['kmin'],
            y=df_affection.index,
            orientation='h',
            name='Влияние в меньшую сторону',
            ),
        row=1,
        col=1
    )
    fig.add_trace(
        go.Bar(
            x=df_affection['kmax'],
            y=df_affection.index,
            orientation='h',
            name='Влияние в большую сторону',
            ),
        row=1,
        col=2
    )

    fig.update_layout(
        xaxis=dict(
            domain=[0.0, 0.5],
            autorange="reversed"
        ),
        xaxis2=dict(domain=[0.5, 1]),
        yaxis=dict(ticklabelstandoff=15),
        yaxis2=dict(visible=False),
        legend=dict(
            orientation='h',
            xanchor='center',
            x=0.5
        )
    )


    annotations=[]

    # Adding labels
    for ykmin, ykmax, xd in zip(df_affection['kmin'], df_affection['kmax'], df_affection.index):
        # labeling the bar net worth
        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=ykmin+0.03,
                                text=str(np.round(ykmin*100, 1)) + '%',
                                showarrow=False))
        annotations.append(dict(xref='x2', yref='y2',
                                y=xd, x=ykmax+0.03,
                                text=str(np.round(ykmax*100, 1)) + '%',
                                showarrow=False))

    fig.update_layout(annotations=annotations)
    return fig



def plot_indicators(vars: pd.DataFrame) -> go.Figure:
    fig = px.ecdf(vars)
    indicators = st.scoreatpercentile(vars, [10, 50, 90])
    fig.add_trace(go.Scatter(x=indicators, y=[0.1, 0.5, 0.9], mode='markers', marker_size=20))
    return fig


def plot_pressure_on_production_stages(pressureVals: pd.DataFrame, name: str) -> go.Figure:
    fig = go.Figure()
    for pressure in pressureVals.columns:
        fig.add_trace(go.Scatter(x=pressureVals.index.values.tolist(), y=pressureVals[pressure], mode="lines+markers", name=pressure))
    fig.update_layout(
        title=dict(text=name)
    )
    return fig

def plot_prod_kig(fig: go.Figure, df_prod_kig: pd.DataFrame, Pind: str) -> go.Figure:
    if fig is None:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df_prod_kig.index.values.tolist(), y=df_prod_kig["annual_production"], mode="lines+markers", name="Qt_"+Pind), secondary_y = False)
    fig.add_trace(go.Scatter(x=df_prod_kig.index.values.tolist(), y=df_prod_kig["kig"], mode="lines+markers", name="КИГ_"+Pind), secondary_y = True)
    return fig