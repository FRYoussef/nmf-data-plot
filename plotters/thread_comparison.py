import os
from typing import List, Tuple
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def extract_data_from(root: str, files: List[str]) -> Tuple[List[str], List[float]]:
    threads: List[int] = list()
    times: List[float] = list()

    for file in files:
        with open(os.path.join(root, file), 'r') as fin:
            content: List[str] = fin.read()

        time: float = float(content.split(' EXEC TIME ')[1].split('.')[0].strip())
        time = float(time / 1000000) # us -> s
        thread: int = int(file.split('.')[2])

        threads.append(thread)
        times.append(time)

    return (threads, times)


if __name__ == '__main__':
    data_path: str = os.path.join('.', 'datawarehouse', 'thread_comparison')
    sycl_files: List[str] = ['nmf.sycl.1', 'nmf.sycl.2']
    openmp_files: List[str] = ['nmf.openmp.1', 'nmf.openmp.2']

    sycl: Tuple[List[str], List[float]] = extract_data_from(data_path, sycl_files)
    openmp: Tuple[List[str], List[float]] = extract_data_from(data_path, openmp_files)

    version: List[str] = ['SYCL']*len(sycl[0]) + ['OpenMP']*len(openmp[0])
    rows: List = zip(version, sycl[0]+openmp[0], sycl[1]+openmp[1])
    headers: List = ['version', 'threads', 'time']
    df: pd.DataFrame = pd.DataFrame(rows, columns=headers)
    
    fig, ax = plt.subplots(figsize=(10,10))

    versions = df['version'].drop_duplicates()
    colors: List[str] = ['#2196f3', '#ef553b']
    index = np.arange(start=1, stop=len(versions)+1, step=1)
    bar_width: float = 0.35
    acc_width: float = 0

    for i, version in enumerate(versions):
        v = df[df['version'] == version]
        plt.bar(
                x=index + acc_width, 
                height=v['time'].tolist(), 
                color=colors[i], 
                label=version,
                width=bar_width,
        )
        acc_width += bar_width
    
    plt.legend(loc='upper left', ncol=2, prop={"size":18})
    plt.grid(linestyle='-', color='#B0BEC5', axis='y')

    plt.ylabel('Seconds', fontsize=20)
    plt.xlabel('Threads per core', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=18)
    plt.xticks(index + (bar_width/2), index, rotation=0)
    y_limit = 8
    ax.set_ylim(0, y_limit)
    plt.yticks(np.arange(0, y_limit, 0.5))

    # time text
    ax.text(0.93, 5.6, '5.5s', fontsize=16)
    ax.text(1.28, 5.9, '5.8s', fontsize=16)

    ax.text(1.92, 7.2, '7.1s', fontsize=16)
    ax.text(2.28, 7, '6.9s', fontsize=16)

    out: str = os.path.join(data_path, 'thread_comparison.eps')
    plt.savefig(out, format='eps', bbox_inches='tight')