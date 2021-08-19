from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import math
df_news = pd.read_table('PI130k-02_-30C_SR01_CP10H_gt.txt',sep='	',header = None)


plt.plot(df_news[0],df_news[1],'-o', lw=3, color='royalblue',label='$G^{II}$')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Time(s)')
plt.ylabel('Stress[Pa]')
plt.show()