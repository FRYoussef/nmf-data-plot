import os
import pandas as pd
import plotly.graph_objects as go


def get_speedup(precision: str, df1: pd.DataFrame, df2: pd.DataFrame) -> list:
    speedup = []
    d1: pd.DataFrame = df1.copy()
    d2: pd.DataFrame = df2.copy()

    d1 = d1[d1['precision'] == precision]
    d2 = d2[d2['precision'] == precision]

    #dimensions = ['5000x38', '16063x280', '54675x1973', '3602x5888', '8555x5177']
    dimensions = ['5000x38', '16063x280', '3602x5888']

    for d in dimensions:
        res1 = d1[d1['dimension'] == d].sort_values(by='k')
        res2 = d2[d2['dimension'] == d].sort_values(by='k')

        spds = []
        k = []
        t1 = res1['time'].tolist()
        t2 = res2['time'].tolist()
        if len(t1) != len(t2):
            print(f'ERORR in: {d}')
            print(f'{t1}\n')
            print(f'{t2}\n')
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
    fig.add_hline(y=1, line_dash="dash", opacity=1)

    # Add traces
    colors = ['#2196f3', '#ef553b', '#00cc96', '#636efa', '#ffa15a']
    for i, s in enumerate(speedup):
        fig.add_trace(
            go.Bar(x=s['k'], y=s['speedup'], name=s['dimension'], marker_color=colors[i])
        )

    # Add figure title
    fig.update_layout(
        legend={
            'orientation': 'v', 
            'x': 1, 
            'y': 0.5,
            'font': {'size': 44},
            'bordercolor': "Black",
            'borderwidth': 2,
            'itemsizing': 'constant'},
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
            'tickfont': {'size': 40},
        },
        yaxis={
            'showgrid': True,
            'gridwidth': 0.5,
            'gridcolor': '#B0BEC5',
            'tick0': 0,
            'dtick': 0.25,
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
            'tickfont': {'size': 40},
        },
        title=plot_title,
        plot_bgcolor="white",
        barmode='group',
    )
    fig.update_xaxes(
        title_text = "Factorization rank (k)",
        title_font = {"size": 50},
        title_standoff = 25)

    fig.update_yaxes(
        title_text = "Times faster than BLAS implementation",
        title_font = {"size": 50},
        title_standoff = 25)

    fig.show()


if __name__ == '__main__':
    computer = 'devcloud_openmp'
    df: pd.DataFrame = pd.read_csv(os.path.join(f'{computer}_results.csv'), header=0)
    #cpu  = df[df['device'] == 'cpu']
    igpu = df[df['device'] == 'igpu']
    base = df[df['device'] == 'openmp_gpu']

    speedup: list = get_speedup('simple', igpu, base)
    plot(speedup=speedup, plot_title=f'Speedup SYCL GPU / OpenMP GPU')
    
    #speedup: list = get_speedup('simple', cpu, base)
    #plot(speedup=speedup, plot_title=f'Speedup SYCL CPU / CPU Base code (single precision; {computer})')

    #speedup: list = get_speedup('simple', igpu, base)
    #plot(speedup=speedup, plot_title=f'Speedup SYCL iGPU / CPU Base code (single precision; {computer})')

    #speedup: list = get_speedup('simple', igpu, cpu)
    #plot(speedup=speedup, plot_title=f'Speedup SYCL iGPU / SYCL CPU (simple precision; {computer})')

    # speedup: list = get_speedup('double', cpu, base)
    # plot(speedup=speedup, plot_title=f'Speedup SYCL CPU / CPU Base code (double precision; {computer})')

    # speedup: list = get_speedup('double', igpu, base)
    # plot(speedup=speedup, plot_title=f'Speedup SYCL iGPU / CPU Base code (double precision; {computer})')

    # speedup: list = get_speedup('double', igpu, cpu)
    # plot(speedup=speedup, plot_title=f'Speedup SYCL iGPU / SYCL CPU (double precision; {computer})')
