import os
from typing import List, Tuple
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def extract_data_from(root: str, file) -> Tuple[List[str], List[int]]:
    names: List[str] = list()
    times: List[int] = list()

    with open(os.path.join(root, file), 'r') as fin:
        lines: List[str] = fin.readlines()

    for i in range(5, 9):
        names.append(lines[i].split('time')[0].strip()) #name of function
        time: int = int(float(lines[i].split('=')[1].split('(us)')[0].strip()))
        time = int(time / 1000000) # us -> s
        times.append(time)

    return (names, times)


if __name__ == '__main__':
    data_path: str = os.path.join('.', 'datawarehouse', 'base_comparison')
    base_times: Tuple[List[str], List[int]] = extract_data_from(data_path, 'base_code_test.txt')
    gemm_times: Tuple[List[str], List[int]] = extract_data_from(data_path, 'sgemm_code_test.txt')

    versions: List[str] = ['Base Code']*len(base_times[0]) + ['SGEMM code']*len(gemm_times[0])
    rows: List = zip(versions, base_times[0]+gemm_times[0], base_times[1]+gemm_times[1])
    headers: List = ['version', 'foo', 'time']
    df: pd.DataFrame = pd.DataFrame(rows, columns=headers)
    
    fig, ax = plt.subplots(figsize=(10,10))
    foos = df['foo'].drop_duplicates()
    margin_bottom = np.zeros(len(df['version'].drop_duplicates()))
    colors: List[str] = ['#ffa15a', '#2196f3', '#ef553b', '#636efa']

    for i, foo in enumerate(foos):
        values = list(df[df['foo'] == foo].loc[:, 'time'])
        df[df['foo'] == foo].plot.bar(x='version', y='time', ax=ax, stacked=True, 
            bottom=margin_bottom, color=colors[i], label=foo)
        
        margin_bottom += values
    
    plt.legend(loc='upper right', ncol=1, prop={"size":18})
    plt.grid(linestyle='-', color='#B0BEC5', axis='y')

    plt.ylabel('Seconds', fontsize=20)
    plt.xlabel('')
    ax.tick_params(axis='both', which='major', labelsize=18)
    plt.xticks(rotation=0)
    y_limit = 125
    ax.set_ylim(0, y_limit)
    plt.yticks(np.arange(0, y_limit, 10))

    #text
    ax.text(-0.1, 116, '115s', fontsize=18)
    ax.text(0.9, 22.3, '22.5s', fontsize=18)
    ax.annotate('', xy=(0, 115), xytext=(0.97, 25.5), size=40, arrowprops=dict(facecolor='black', arrowstyle='<|-|>', lw=2.5))
    ax.text(0.36, 63, 'x5.1 faster', fontsize=18, fontfamily='sans-serif', fontweight='bold', rotation=302)

    out: str = os.path.join(data_path, 'base_comparison.pdf')
    plt.savefig(out, format='pdf', bbox_inches='tight')