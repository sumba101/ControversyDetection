import pandas as pd
import os
from tqdm import tqdm

def joinFiles(dir):
    files = os.listdir(dir)
    final = pd.DataFrame()

    for file in tqdm(files):
        df = pd.read_csv(dir+file)
        final = final.append(df)

    final.to_csv('./output_data/'+'compiled_v1.csv', index=False)


if __name__ == '__main__':
    DIR = './intermediate_data/'
    joinFiles(DIR)