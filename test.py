#%%
# read_csv support the txt 
# what if convert txt to csv during chang-time
# from os import sep
import pandas as pd
import base64
import io

from pandas.core.frame import DataFrame
# # y = pd.read_csv("./test.txt", sep=" ", header=None, names=["x", "y"])
# z = pd.read_fwf("./readtest.csv")

# # y.head()
# z.head()

#  base64 version
# y = "data:text/plain;base64,WAl5CjIJMQozCTIJCjQJMwo1CTQKNgk1CjcJNg=="
# y = y.split(",")[-1]

# decoded = base64.b64decode(y)

# df = pd.read_fwf(io.StringIO(decoded.decode("utf-8")))

# print(df[df.columns[0]])
# df.info()
# df = pd.read_fwf("./test.txt")

# df.info()

# print(x)
# print(df[x])

# df.apply(lambda x: x * 2)
# %%
