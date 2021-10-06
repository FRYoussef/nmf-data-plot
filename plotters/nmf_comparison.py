import os
from typing import List
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot(out_path: str, df: pd.DataFrame) -> None:
    df['device'] = df['device'].str.upper()
    df.loc[(df.device == 'IGPU'), 'device'] = 'iGPU'

    df['system'] = df['system'].str.capitalize()

    df['version'] = df['version'].str.upper()
    df.loc[(df.version == 'OPENMP'), 'version'] = 'OpenMP'
    df.loc[(df.version == 'BASE_CODE'), 'version'] = 'BLAS base version'

    df['name'] = df["system"] + ' ' + df["device"] + ' (' + df['version'] + ')'
    
    fig, ax = plt.subplots(figsize=(10,10))

    kernels = df['kernel'].drop_duplicates()
    margin = np.zeros(len(df['name'].drop_duplicates()))
    colors: List[str] = ['#ffa15a', '#2196f3', '#ef553b', '#636efa']
    df = df.sort_values(by=['name'], ascending=False)

    for i, kernel in enumerate(kernels):
        values = list(df[df['kernel'] == kernel].loc[:, 'time'])
        df[df['kernel'] == kernel].plot.barh('name', 'time', ax=ax, 
            left=margin, color=colors[i], label=kernel)
        
        margin += values

    # bar texture
    bars = ax.patches
    start = 0
    for _ in range(4):
        bs = bars[start:start+10]
        start += 10
        for i, b in enumerate(bs):
            if i < 5:
                b.set_hatch('x')
            else:
                b.set_hatch('//')
    

    #legend
    legend = plt.legend(loc='lower right', ncol=1, prop={"size":16})
    handles = legend.legendHandles
    for h in handles:
        h.set_hatch('')

    plt.grid(linestyle='-', color='#B0BEC5', axis='x')

    plt.xlabel('Seconds', fontsize=20)
    plt.ylabel('')
    ax.tick_params(axis='both', which='major', labelsize=14)
    x_limit = 32
    ax.set_xlim(0, x_limit)
    plt.xticks(np.arange(0, x_limit, 2))

    plt.savefig(out_path, format='eps', bbox_inches='tight')


if __name__ == '__main__':
    data_path: str = os.path.join('.', 'datawarehouse', 'system')
    infile_path: str = os.path.join(data_path, 'system_times.csv')
    df: pd.DataFrame = pd.read_csv(infile_path, header=0)

    # filter by dataset
    df1: pd.DataFrame = df[df['matrix_size'] == '5000x38']
    df2: pd.DataFrame = df[df['matrix_size'] == '16063x280']
    df3: pd.DataFrame = df[df['matrix_size'] == '54675x1973']
    
    #plot(out_path=os.path.join(data_path, '5000x38x4_nmf_comparison.eps'), df=df1)
    plot(out_path=os.path.join(data_path, '16063x280x4_nmf_comparison.eps'), df=df2)
    #plot(out_path=os.path.join(data_path, '54675x1973x4_nmf_comparison.eps'), df=df3)
