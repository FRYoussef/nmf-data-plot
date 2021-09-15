import os
import pandas as pd
import plotly.graph_objects as go


def get_speedup(df1: pd.DataFrame, df2: pd.DataFrame) -> list:
    speedup = []
    d1: pd.DataFrame = df1.copy()
    d2: pd.DataFrame = df2.copy()

    dimensions = ['5000x38', '16063x280', '3602x5888', '54675x1973', '8555x5177']

    for d in dimensions:
        res1 = d1[d1['dimension'] == d].sort_values(by='k')
        res2 = d2[d2['dimension'] == d].sort_values(by='k')

        spds = []
        k = []
        t1 = res1['time'].tolist()
        t2 = res2['time'].tolist()
        if len(t1) != len(t2):
            print(f'ERORR in: {d}')
            continue

        for i, t in enumerate(t1):
            spds.append(t2[i]/t1[i])
            k.append(i+2)

        speedup.append({
            'k': k,
            'dimension': d,
            'speedup': spds,
        })

    return speedup


def plot(speedup: list, plot_title: str) -> None:
    fig = go.Figure()
    # Add traces
    for s in speedup:
        fig.add_trace(
            go.Bar(x=s['k'], y=s['speedup'], name=s['dimension'])
        )

    # Add figure title
    fig.update_layout(
        #legend={'orientation': 'h', 'x': 0, 'y': 1.1, 'font': {'size': 28}},
        xaxis={
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
            'showgrid': True,
            'gridwidth': 0.5,
            'gridcolor': '#B0BEC5',
            'tickfont': {'size': 28},
        },
        yaxis={
            'showgrid': True,
            'gridwidth': 0.5,
            'gridcolor': '#B0BEC5',
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
            'tickfont': {'size': 28},
        },
        title=plot_title,
        plot_bgcolor="white",
        barmode='group',
    )

    fig.show()


if __name__ == '__main__':
    computer = 'devcloud'
    df: pd.DataFrame = pd.read_csv(os.path.join(f'{computer}_results.csv'), header=0)
    igpu = df[df['device'] == 'igpu']
    igpu = igpu[igpu['precision'] == 'simple']
    df1: pd.DataFrame = pd.read_csv(os.path.join(f'{computer}_for_results.csv'), header=0)
    df1 = df1[df1['device'] == 'igpu']
    df1 = df1[df1['precision'] == 'simple']

    speedup: list = get_speedup(igpu, df1)
    plot(speedup=speedup, plot_title=f'Diferencia entre oneAPI 2021.1 y 2021.2({computer})')