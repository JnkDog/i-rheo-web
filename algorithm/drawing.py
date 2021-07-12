import base64
import io

import numpy as np
import plotly.express as px
import pandas as pd

def drawing(contents, value=1):
    # print(type(value))
    # print(type(contents))  
    fig = px.scatter()

    if contents is not None:
        contents = contents.split(",")[-1]
        decoded = base64.b64decode(contents)
        df = pd.read_fwf(io.StringIO(decoded.decode("utf-8")))
        points = df.apply(lambda x: x * value)
        # print(df)
        fig = px.scatter(x=points[points.columns[0]], y=points[points.columns[1]])
    

    return fig

def drawing_demo_data():
    df = pd.read_table("./example_data/SingExp6_5.txt",header=None)
    df.columns = ["Time (s)", "G(t) (Pa)"]

    fig = px.line(data_frame=df, x="Time (s)", y="G(t) (Pa)", log_x=True, range_y=[0, 1])
    return fig
