
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
df_news = pd.read_table('C0500_NVT_450K_1atm.txt',sep='	', header = None)
for i in df_news[1]:
    if i<0:
        print(i)
plt.plot(df_news[0],df_news[1],'-o', lw=3, color='royalblue',label='$G^{II}$')
plt.xscale('log')
plt.xlabel('Time (s)')
plt.ylabel('G(t) (Pa)')

plt.show()



