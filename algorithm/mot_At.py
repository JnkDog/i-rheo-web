from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def at_test():
    '''
    输入只有file
    在sigma位置输出
    '''
    df_news = pd.read_table('data.txt',sep=' ',header = None)
    plt.plot(df_news[0],df_news[1],'-o', lw=3, color='royalblue',label='$G^{II}$')
    plt.xscale('log')
    plt.xlabel('t (sec)')
    plt.ylabel('A(t)')
    plt.show()

# at_test()
