from plotly import graph_objects as go
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

import scipy.stats as st
import pandas as pd
import numpy as np

from src.constants import *



PROD_INDICS_COLORS = {
    'P10': CHART_COLORS[1],
    'P50': CHART_COLORS[2],
    'P90': CHART_COLORS[3],

}

def plot_vars_distribution(stat_data: pd.DataFrame) -> go.Figure:
    fig = make_subplots(rows=1, cols=len(stat_data.columns))
    for var, i in zip(stat_data.columns, range(1,len(stat_data.columns))):
        fig.add_trace(
            go.Histogram(x=stat_data[var], nbinsx=14), row=1, col=i)
    fig.update_xaxes(rangemode='tozero')

    return fig


def plot_tornado(df_affection: pd.DataFrame) -> go.Figure:
    fig = make_subplots(rows=1,cols=2)
    fig.add_trace(
        go.Bar(
            x=df_affection['kmin'],
            y=df_affection.index,
            orientation='h',
            # name='Влияние в меньшую сторону',
            name='',
            marker_color=CHART_COLORS[0],
            ),
        row=1,
        col=1
    )
    fig.add_trace(
        go.Bar(
            x=df_affection['kmax'],
            y=df_affection.index,
            orientation='h',
            # name='Влияние в большую сторону',
            name='',
            marker_color=CHART_COLORS[1],
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


def plot_ecdf_indicators(vars: pd.DataFrame, title: str) -> go.Figure:

    fig = px.ecdf(vars, title=title, color_discrete_sequence=CHART_COLORS)
    # indicators = st.scoreatpercentile(vars, [10, 50, 90])
    indicators = np.percentile(vars, [10, 50, 90])
    fig.add_trace(
        go.Scatter(
            x=indicators, 
            y=[0.1, 0.5, 0.9], 
            mode='markers', 
            marker_size=20,
            marker_color=CHART_COLORS[1],
        )
    )
    fig.add_annotation(x=indicators[0],
                       y=0.1,
                       text=f'P90 = {indicators[0]:.0f} млн. м3',
                       showarrow=True,
                       arrowhead=2,
                       font=dict(size=18),
                       align='center',
                       bordercolor='#000000',
                       bgcolor='#ffffff')
    
    fig.add_annotation(x=indicators[1],
                       y=0.5,
                       text=f'P50 = {indicators[1]:.0f} млн. м3',
                       showarrow=True,
                       arrowhead=2,
                       font=dict(size=18),
                       align='center',
                       bordercolor='#000000',
                       bgcolor='#ffffff')
    
    fig.add_annotation(x=indicators[2],
                       y=0.9,
                       text=f'P10 = {indicators[2]:.0f} млн. м3',
                       showarrow=True,
                       arrowhead=2,
                       font=dict(size=18),
                       align='center',
                       bordercolor='#000000',
                       bgcolor='#ffffff')
    
    fig.update_layout(
        height=500,
        legend=dict(
            visible=False
        ),
        xaxis=dict(
            tickformat=".0f",  # Full Format
            title=dict(text=title)
        ),
        yaxis = {
            'title': {
                'text': 'Вероятность'
            }
        },
    )
    fig.update_traces(hovertemplate=f'{title}'+': %{x}', selector={'name': '0'})
    return fig

def plot_pdf_indicators(vars: pd.DataFrame, title: str) -> go.Figure:

    if np.allclose(vars, vars[0]):
        vars += np.random.normal(loc=0, scale=1e-8, size=len(vars))
    fig = ff.create_distplot([vars], [title], bin_size=0.01, show_hist=False, show_rug=False, colors=CHART_COLORS)

    indicators = np.percentile(vars, [10, 50, 90])
    ys: list
    kde = st.gaussian_kde(vars)
    ys = kde.pdf(indicators)

    fig.add_trace(
        go.Scatter(
            x=indicators, 
            y=ys, 
            mode='markers', 
            marker_size=20,
            marker_color=CHART_COLORS[1],
        )
    )
    
    fig.add_annotation(x=indicators[0],
                       y=ys[0],
                       text=f'P90 = {indicators[0]:.0f} млн. м3',
                       showarrow=True,
                       arrowhead=2,
                       font=dict(size=18),
                       align='center',
                       bordercolor='#000000',
                       bgcolor='#ffffff')
    fig.add_annotation(x=indicators[1],
                       y=ys[1],
                       text=f'P50 = {indicators[1]:.0f} млн. м3',
                       showarrow=True,
                       arrowhead=2,
                       font=dict(size=18),
                       align='center',
                       bordercolor='#000000',
                       bgcolor='#ffffff')
    fig.add_annotation(x=indicators[2],
                       y=ys[2],
                       text=f'P10 = {indicators[2]:.0f} млн. м3',
                       showarrow=True,
                       arrowhead=2,
                       font=dict(size=18),
                       align='center',
                       bordercolor='#000000',
                       bgcolor='#ffffff')

    fig.update_layout(
        height=500,
        xaxis=dict(
            tickformat=".0f",  # Full Format
            title=dict(text=title)
        ),
        legend=dict(
            visible=False
        ),
    )

    return fig


def plot_pressure_on_production_stages(pressure_vals: pd.DataFrame, name: str) -> go.Figure:
    fig = go.Figure()
    for pressure, color_id in zip(pressure_vals.columns, range(4)):
        fig.add_trace(go.Scatter(name=DISPLAY_VARNAMES_INDICATORS[pressure],
                                 x=pressure_vals.index.values.tolist(),
                                 y=pressure_vals[pressure],
                                 mode="lines+markers",
                                 line=dict(color=CHART_COLORS[color_id]),
                                 marker=dict(color=CHART_COLORS[color_id]), ))
    fig.update_layout(
        title=dict(text=name)
    )
    fig.update_xaxes(rangemode='tozero')
    return fig


def plot_united_pressures(charts: list[go.Figure]) -> go.Figure:
    fig = make_subplots(rows=3,
                        cols=1,
                        vertical_spacing=0.1,
                        subplot_titles=('Вариант P10', 'Вариант P50', 'Вариант P90' ))
    for chart, i in zip(charts, range(3)):
        for trace in chart.data:
            trace.legendgroup = f"group{i+1}"
            fig.add_trace(trace, row=i+1, col=1)

    for i in range(1, 4):
        fig.update_xaxes(title_text='Годы', col=1, row=i, rangemode='tozero')
        fig.update_yaxes(title_text='Давление, МПа', col=1, row=i)

    fig.update_xaxes(matches='x')

    fig.update_layout(
        height=1000,
        legend=dict(
            tracegroupgap=222,
            itemsizing='trace',
            groupclick='toggleitem',
        )
    )
    return fig


def plot_summary_chart(fig: go.Figure, df_prod_kig: pd.DataFrame, prod_indic: str) -> go.Figure:
    if fig is None:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=df_prod_kig.index.values.tolist(), 
            y=df_prod_kig["annual_production"], 
            mode="lines+markers", 
            name="Qt_"+prod_indic,
            customdata=df_prod_kig,
            hovertemplate=
                '<br>Годовой отбор: %{y}<br>'+
                'Количество скважин: %{customdata[2]}',
            line=dict(color=PROD_INDICS_COLORS[prod_indic])
        ), secondary_y = False)
    
    fig.add_trace(
        go.Scatter(
            x=df_prod_kig.index.values.tolist(), 
            y=df_prod_kig["kig"], 
            mode="lines+markers", 
            name="КИГ_"+prod_indic,
            customdata=df_prod_kig,
            hovertemplate=
                '<br>КИГ: %{y:.2f}<br>',
            line=dict(color=PROD_INDICS_COLORS[prod_indic])
        ), secondary_y = True)

    fig.update_layout(
        hovermode='x',
        xaxis=dict(
            title=dict(
                text='Год'
            ),
            rangemode='tozero'
        ),
    )
    fig.update_yaxes(title_text=DISPLAY_VARNAMES_INDICATORS['annual_production'], secondary_y=False)
    fig.update_yaxes(title_text=DISPLAY_VARNAMES_INDICATORS['kig'], secondary_y=True)
    return fig


def make_bubble_charts(values: pd.DataFrame,
                       y: str) -> go.Figure:

    fig = go.Figure()
    max_acc_prod = values.max(axis=1).loc[VARNAMES_ANALYSIS['accumulated_production']]
    coef = 1 / max_acc_prod
    max_bubble_size = 70
    min_bubble_size = 10
    for field, field_id in zip(values.columns, range(len(values.columns))):
        fig.add_trace(
            go.Scatter(
                x=[values.loc[VARNAMES['geo_gas_reserves'], field]],
                y=[values.loc[VARNAMES_ANALYSIS[y], field]],
                mode='markers',
                name=field,
                marker_size=values.loc[VARNAMES_ANALYSIS['accumulated_production'], field] * coef * max_bubble_size + min_bubble_size,
                marker_color=CHART_COLORS[field_id % len(CHART_COLORS)],
            )
        )

    fig.update_layout(
        xaxis=dict(
            tickformat=".0f",  # Full Format
            title=dict(text=VARNAMES['geo_gas_reserves'])
        ),
        yaxis=dict(
            title=VARNAMES_ANALYSIS[y]
        )
    )

    return fig
