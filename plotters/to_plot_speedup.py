import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_speedup(precision: str, df1: pd.DataFrame, df2: pd.DataFrame, sys: str, dev: str) -> list:
    speedup = [{} for x in range(2, 11)]
    d1: pd.DataFrame = df1.copy()
    d2: pd.DataFrame = df2.copy()

    d1 = d1[d1['precision'] == precision]
    d2 = d2[d2['precision'] == precision]

    dimensions = ['5000x38', '16063x280', '3602x5888', '8555x5177', '54675x1973']
    dataset_tags = ['ALL-AML', 'Lung', 'TCGA', 'GTEX', 'ExpO']
    k = [x for x in range(2, 11)]

    for i, d in enumerate(dimensions):
        res1 = d1[d1['dimension'] == d].sort_values(by='k')
        res2 = d2[d2['dimension'] == d].sort_values(by='k')

        t1 = res1['time'].tolist()
        t2 = res2['time'].tolist()
        if len(t1) != len(t2):
            print(f'ERORR: {sys} in {dev} with size of {d}')
            continue

        for j, t in enumerate(t1):
            speedup[j][dataset_tags[i]] = t2[j]/t1[j]

    return pd.DataFrame(speedup, index=k)

if __name__ == '__main__':
    in_path: str = os.path.join('.', 'datawarehouse', 'system', 'system_times.csv')
    df = pd.read_csv(in_path, header=0)
    base = df[df['device']=='base_code']

    fig_system=['lab', 'lab', 'devcloud', 'devcloud', 'devcloud_dual', 'lab_hybrid', \
        'devcloud_openmp', 'devcloud_openmp', 'lab_openmp', 'lab_openmp']
    fig_dev=['cpu', 'igpu', 'cpu', 'igpu', 'dual_gpu', 'hybrid', 'cpu', 'gpu', 'cpu', 'gpu']
    title = ['Intel Core i7-10700 (oneAPI)', 'Intel UHD 630  (oneAPI)', \
        'Intel i9-10920X (oneAPI)', 'Intel Iris Xe DG1 (oneAPI)', \
        'Dual (Intel Iris Xe DG1)', 'i7-10700 + UHD 630', 'Intel i9-10920X (OpenMP)', \
        'Intel Iris Xe DG1 (OpenMP)', 'Intel Core i7-10700 (OpenMP)', 'Intel UHD 630  (OpenMP)']

    for i in range(len(fig_system)):
        sys = fig_system[i]
        base_sys = base[base['system'] == sys]
        dev = fig_dev[i]
        test = df[df['system']==sys]
        test = test[test['device']==dev]

        speedup = get_speedup('simple', test, base_sys, sys, dev)
        fig, ax = plt.subplots()

        speedup.plot(
            kind='bar',
            figsize=(10,10),
            color = ['#2196f3', '#ef553b', '#00cc96', '#636efa', '#ffa15a'],
            width=0.8,
            linewidth=10,
            ecolor='blue',
            ax = ax
        )
        ax.legend(loc='upper center', ncol=2, prop={"size":25})
        ax.grid(linestyle='-', color='#B0BEC5')

        ax.set_ylim(0,4)
        plt.title(title[i], loc='center', fontsize=40)
        plt.ylabel('Speedup', fontsize=30)
        ax.xaxis.label.set_size(30)
        ax.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3), useOffset=False)
        ax.tick_params(axis='both', which='major', labelsize=25)
        ax.plot([-0.5, 8.5], [1, 1], 'black',  linestyle='dashed', linewidth=3) # Linea de speedup 1
        fig.savefig('speedup_'+sys+'_'+dev+'.png', format='png')
