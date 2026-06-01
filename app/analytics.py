import pandas as pd
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CSV_FILE = os.path.join(
    BASE_DIR,
    "data",
    "Brigade_Bangalore_10_April_26 (1)bc6219c.csv"
)


def load_transactions():

    df = pd.read_csv(
        CSV_FILE,
        low_memory=False
    )

    print(df.columns.tolist())

    return df