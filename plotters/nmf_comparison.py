import os
from typing import List
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot(out_path: str, df: pd.DataFrame) -> None:
    #ordering
    df.loc[(df.device == 'i7-10700'), 'device'] = '1'
    df.loc[(df.device == 'i9-10920X'), 'device'] = '2'
    df.loc[(df.device == 'gold'), 'device'] = '3'
    df.loc[(df.device == 'uhd630'), 'device'] = '4'
    df.loc[(df.device == 'dg1'), 'device'] = '5'
    df.loc[(df.device == 'ats'), 'device'] = '6'
    df.loc[(df.device == 'rtx3090'), 'device'] = '7'
    df = df.sort_values(by=['system', 'device', 'version'], ascending=False)

    df.loc[(df.device == '1'), 'device'] = 'i7-10700'
    df.loc[(df.device == '2'), 'device'] = 'i9-10920X'
    df.loc[(df.device == '3'), 'device'] = 'Xeon Gold 6336Y'
    df.loc[(df.device == '4'), 'device'] = 'UHD 630'
    df.loc[(df.device == '5'), 'device'] = 'Iris Xe MAX DG1'
    df.loc[(df.device == '6'), 'device'] = 'Xe HP Artic Sound'
    df.loc[(df.device == '7'), 'device'] = 'RTX 3090'

    cpu: List[str] = ['i7-10700', 'i9-10920X', 'Xeon Gold 6336Y']
    # gpu: List[str] = ['UHD 630', 'Xe DG1', 'Xe HP Artic Sound', 'GT 1030', 'RTX 3090']
    gpu: List[str] = ['Iris Xe MAX DG1', 'RTX 3090']

    #filter by cpu or gpu
    df = df[df['device'].isin(cpu)]

    df['system'] = df['system'].str.capitalize()

    df['version'] = df['version'].str.upper()
    df.loc[(df.version == 'OPENMP'), 'version'] = 'OpenMP'
    df.loc[(df.version == 'BASE_CODE'), 'version'] = 'BLAS base'

    df['name'] = df["device"] + ' (' + df['version'] + ')'
    
    fig, ax = plt.subplots(figsize=(10,10))

    kernels = df['kernel'].drop_duplicates()
    margin = np.zeros(len(df['name'].drop_duplicates()))
    colors: List[str] = ['#ffa15a', '#2196f3', '#ef553b', '#636efa']

    for i, kernel in enumerate(kernels):
        values = list(df[df['kernel'] == kernel].loc[:, 'time'])
        df[df['kernel'] == kernel].plot.barh('name', 'time', ax=ax, 
            left=margin, color=colors[i], label=kernel)
        
        margin += values

    # # bar texture
    # bars = ax.patches
    # start = 0
    # for _ in range(4):
    #     bs = bars[start:start+10]
    #     start += 10
    #     for i, b in enumerate(bs):
    #         if i < 5:
    #             b.set_hatch('x')
    #         else:
    #             b.set_hatch('//')
    

    #legend
    legend = plt.legend(loc='lower right', ncol=1, prop={"size":16})
    handles = legend.legendHandles
    for h in handles:
        h.set_hatch('')

    plt.grid(linestyle='-', color='#B0BEC5', axis='x')

    plt.xlabel('Seconds', fontsize=20)
    plt.ylabel('')
    ax.tick_params(axis='both', which='major', labelsize=15)
    x_limit = 23
    ax.set_xlim(0, x_limit)
    plt.xticks(np.arange(0, x_limit, 2))
    # ax.set_xscale('log')

    plt.savefig(out_path, format='pdf', bbox_inches='tight')


if __name__ == '__main__':
    data_path: str = os.path.join('.', 'datawarehouse', 'system')
    infile_path: str = os.path.join(data_path, 'system_times.csv')
    df: pd.DataFrame = pd.read_csv(infile_path, header=0)

    # filter by dataset
    df1: pd.DataFrame = df[df['matrix_size'] == '5000x38']
    df2: pd.DataFrame = df[df['matrix_size'] == '16063x280']
    df3: pd.DataFrame = df[df['matrix_size'] == '54675x1973']
    
    #plot(out_path=os.path.join(data_path, '5000x38x4_nmf_comparison.eps'), df=df1)
    plot(out_path=os.path.join(data_path, '16063x280x4_nmf_comparison.pdf'), df=df2)
    # plot(out_path=os.path.join(data_path, '54675x1973x4_nmf_comparison.pdf'), df=df3)
