import pandas as pd
import base64
import io

# generate dataframe
def generate_df(content):
    decoded_content = parse_contents(content)
    # read seprate includes space and tab (delim_whitespace=True)
    df = pd.read_table(io.StringIO(decoded_content.decode("utf-8")), header=None, delim_whitespace=True)

    return df
    
def parse_contents(content):
    content = content.split(",")[-1]
    decoded_content = base64.b64decode(content)

    return decoded_content

def generate_df_from_local(path):
    df = pd.read_table(path, header=None, delim_whitespace=True)

    return df

def convert_lists_to_df(data):
    x = data.get("x")
    y = data.get("y")
    if data.get("z"):
        z = data.get("z")
        return pd.DataFrame(list(zip(x, y, z)))

    df = pd.DataFrame(list(zip(x, y)))

    return df
    
# replace the dict's value
def replace_dict_value(dict, replacement, replacement_keys):
    idx = 0
    for key in dict:
        dict[key] = replacement[idx] if key in replacement_keys else dict[key]
        idx = idx + 1 if key in replacement_keys else idx

    return dict