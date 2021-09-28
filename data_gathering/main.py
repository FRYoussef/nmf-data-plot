import os
import pandas as pd
from typing import Any, List, Dict

def extract_data_from(root: str, system: str) -> pd.DataFrame:
    tests: List[Dict[str, Any]] = list()
    path: str = os.path.join(root, system)
    files: List[str] = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in files:
        params = f.split('.')
        d = dict(
            system=params[1],
            device=params[2],
            version=params[3],
            precision=params[4],
            dimension=f'{params[5]}x{params[6]}',
            k=params[7],
        )

        with open(os.path.join(path, f), 'r') as fin:
            content: str = fin.read()
            content = content.split('100%')[1].split(' EXEC TIME')[0].strip() #clean non-kernels content
            lines: List[str] = content.split('\n')

        for line in lines:
            name: str = line.split('time =')[0].strip()
            time: int = float(line.split('=')[1].split('(us)')[0].strip())
            time = time / 1000000 # us -> s
            d['kernel'] = name
            d['time'] = time
            aux: Dict = d.copy()
            tests.append(aux)

    return pd.DataFrame(tests)


if __name__ == '__main__':
    df: pd.DataFrame = pd.DataFrame()
    path: str = os.path.join('.', 'datawarehouse', 'system')
    systems: List[str] = [s for s in os.listdir(path) if os.path.isdir(os.path.join(path, s))]

    for s in systems:
        df = df.append(extract_data_from(path, s))

    out: str = os.path.join(path, 'system_times.csv')
    df.to_csv(out, index=False)
