import os
import pandas as pd
from typing import List, Dict

def extract_data_from(root: str, system: str) -> pd.DataFrame:
    tests: List[Dict[str, str]] = []
    path: str = os.path.join(root, system, 'OUT')
    files: List[str] = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in files:
        params = f.split('.')
        d = {
            'system': system,
            'k': params[5],
            'device': params[1],
            'precision': params[2],
            'dimension': f'{params[3]}x{params[4]}',
        }
        fin = open(os.path.join(path, f), 'r')
        content: str = fin.read()
        fin.close()
        try:
            d['time'] = content.split(' EXEC TIME ')[1].split('.')[0]
            tests.append(d)
        except:
            print(f'ERROR: System = {system}, file = {f}')

    return pd.DataFrame(tests)


if __name__ == '__main__':
    df: pd.DataFrame = pd.DataFrame()
    path: str = os.path.join('.', 'datawarehouse', 'system')
    systems: List[str] = [s for s in os.listdir(path) if os.path.isdir(os.path.join(path, s))]

    for s in systems:
        df.append(extract_data_from(path, s), ignore_index=True)

    out: str = os.path.join(path, 'system_times.csv')
    df.to_csv(out, index=False)
