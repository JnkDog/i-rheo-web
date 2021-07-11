from matplotlib import pyplot as plt
import pandas as pd


class sigma:
    def __init__(self, data):
        self.data=data
    def sigma_print(self):
        df_news = pd.read_table(self.data,header = None)
        plt.plot(df_news[0],df_news[1],'-o', lw=3, color='royalblue',label='$G^{II}$')
        plt.xscale('log')
        plt.xlabel('Time (s)')
        plt.ylabel('G(t) (Pa)')
        plt.show()    


#zyy=sigma("SingExp6_5.txt")
#zyy.sigma_print()