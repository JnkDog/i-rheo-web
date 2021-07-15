import pandas as pd
import base64
import io

# generate dataframe
def generate_df(content):
    decoded_content = parse_contents(content)
    df = pd.read_table(io.StringIO(decoded_content.decode("utf-8")), header=None)

    return df
    
def parse_contents(content):
    content = content.split(",")[-1]
    decoded_content = base64.b64decode(content)

    return decoded_content
