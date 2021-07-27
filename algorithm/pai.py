
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
df_news = pd.read_table('data.txt',sep=' ',header = None)
pai = []
pai = 1 - df_news[1]
plt.plot(df_news[0],pai,'-o', lw=3, color='royalblue',label='$G^{II}$')
plt.xscale('log')
plt.xlabel('t (sec)')
plt.ylabel('Π(t)')
plt.show()
'''
输入只有file
在gamma位置输出
'''



