import os
from typing import List
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == '__main__':
    data_path: str = os.path.join('.', 'datawarehouse', 'memory_comparison')
    file: str = os.path.join(data_path, 'mem_time.csv')
    df: pd.DataFrame = pd.read_csv(file, header=0)
    
    fig, ax = plt.subplots(figsize=(10,10))

    memory_types = df['memory_type'].drop_duplicates()
    n_devices = len(df['device'].drop_duplicates())
    colors: List[str] = ['#ffa15a', '#636efa']
    index = np.arange(start=1, stop=n_devices+1, step=1)
    bar_width: float = 0.35
    acc_width: float = 0

    for i, memory_type in enumerate(memory_types):
        v = df[df['memory_type'] == memory_type]
        plt.bar(
                x=index + acc_width, 
                height=v['time'].tolist(), 
                color=colors[i], 
                label=memory_type,
                width=bar_width,
        )
        acc_width += bar_width
    
    plt.legend(loc='upper left', ncol=2, prop={"size":18})
    plt.grid(linestyle='-', color='#B0BEC5', axis='y')

    plt.ylabel('Seconds', fontsize=20)
    plt.xlabel('')
    plt.xticks(index + (bar_width/2), df['device'].drop_duplicates().to_list(), fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=18)
    y_limit = 14
    ax.set_ylim(0, y_limit)
    plt.yticks(np.arange(0, y_limit, 2))

    # time text
    ax.text(0.84, 8.1, '7.9s', fontsize=16)
    ax.text(1.2, 10.6, '10.4s', fontsize=16)
    
    ax.text(1.88, 6.1, '5.9s', fontsize=16)
    ax.text(2.23, 7.6, '7.4s', fontsize=16)

    ax.text(2.85, 11.5, '11.3s', fontsize=16)
    ax.text(3.2, 12.4, '12.2s', fontsize=16)

    ax.text(3.87, 2.1, '1.9s', fontsize=16)
    ax.text(4.2, 2.7, '2.5s', fontsize=16)

    out: str = os.path.join(data_path, 'mem_comparison.pdf')
    plt.savefig(out, format='pdf', bbox_inches='tight')