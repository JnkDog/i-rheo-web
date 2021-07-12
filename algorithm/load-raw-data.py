import pandas as pd

# generate dataframe
def generate_df(file_path):
    return pd.read_fwf(file_path)

