from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def pai_test():
    '''
    输入只有file
    在gamma位置输出
    '''
    df_news = pd.read_table('data.txt',sep=' ',header = None)
    pai = []
    pai = 1 - df_news[1]
    df_news[1] = df_news[1].apply(lambda x: 1-x)
    print(df_news[1])
    print(pai)

    plt.plot(df_news[0], df_news[1], '-o', lw=3, color='royalblue',label='$G^{II}$')
    plt.xscale('log')
    plt.xlabel('t (sec)')
    plt.ylabel('Π(t)')
    plt.show()

# pai_test()

def pai_processing(df):
    df["pai"] = df[1].apply(lambda x: 1-x)
    return df
