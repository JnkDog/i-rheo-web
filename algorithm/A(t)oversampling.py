
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
import math
from scipy import interpolate

df_news = pd.read_table('data.txt',sep=' ',header = None)
t = df_news[0]
g = df_news[1]
oversampling=10  #输入赋值=次数
gi = interp1d(t,g,kind='cubic',fill_value='extrapolate')
t_new = np.logspace(min(np.log10(t)),max(np.log10(t)),len(t)*oversampling) #re-sample t in log space
Gint_I = gi(t_new) # get new g(t) taken at log-space sampled t
t_I = t_new
plt.plot(t_I,Gint_I,'-o', lw=3, color='royalblue',label='$G^{II}$')
plt.xscale('log')
plt.xlabel('t (sec)')
plt.ylabel('A(t)')
plt.show()

'''
输入过采样次数
'''
    
        



          