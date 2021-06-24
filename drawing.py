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