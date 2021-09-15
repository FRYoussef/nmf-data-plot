import os
from typing import Dict, List, Tuple
import pandas as pd
import matplotlib.pyplot as plt

def extract_data_from(root: str, file) -> Tuple[List[str], List[int]]:
    names: List[str] = list()
    times: List[int] = list()

    with open(os.path.join(root, file), 'r') as fin:
        lines: List[str] = fin.readlines()

    for i in range(5, 9):
        names.append(lines[i].split('time')[0].strip()) #name of function
        times.append(int(float(lines[i].split('=')[1].split('(us)')[0].strip())))

    return (names, times)


if __name__ == '__main__':
    data_path: str = os.path.join('.', 'datawarehouse', 'base_comparison')
    base_times: Tuple[List[str], List[int]] = extract_data_from(data_path, 'base_code_test.txt')
    gemm_times: Tuple[List[str], List[int]] = extract_data_from(data_path, 'sgemm_code_test.txt')

    labels: List[str] = base_times[0]
    

    title: str = 'Base NMF vs SGEMM NMF'
    fig, ax = plt.subplots()

    ax.bar(labels, men_means, width, yerr=men_std, label='Men')
    ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
       label='Women')

    base_times.plot(
        kind='bar',
        figsize=(10,10),
        color = ['#2196f3', '#ef553b', '#00cc96', '#636efa'],
        width=0.8,
        linewidth=10,
        ecolor='blue',
        ax = ax
    )
    plt.legend(loc='upper center', ncol=2, prop={"size":25})
    plt.grid(linestyle='-', color='#B0BEC5')

    # ax.set_ylim(0,4)
    # plt.title(title, loc='center', fontsize=40)
    # plt.ylabel('Time in us', fontsize=30)
    # ax.xaxis.label.set_size(30)
    # ax.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3), useOffset=False)
    # ax.tick_params(axis='both', which='major', labelsize=25)
    # ax.plot([-0.5, 8.5], [1, 1], 'black',  linestyle='dashed', linewidth=3) # Linea de speedup 1
    out: str = os.path.join(data_path, 'base_comparison.png')
    plt.savefig(out, format='png')