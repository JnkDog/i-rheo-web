import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from scipy.interpolate import interp1d
import pandas as pd
import math
from scipy import interpolate
import plotly.express as px
import base64
import io

from algorithm.read_data import generate_df

class Oversampling:
    def __init__(self, data):
        self.data = data
    #available after design g_0,g_dot_inf input label

    '''       
        def __init__(self,g0,ginf,InterpFunc,oversampling):    
            self.g0= g0
            self.ginf= ginf
            self.InterpFunc= InterpFunc
            self.oversampling= oversampling    #ntimes
    ''' 

    def OverSample(self):
        #,t,g,g0,ginf,InterpFunc):
        df_news = pd.read_table(self.data, header = None)
        t = df_news[0]
        g = df_news[1]
        oversampling=10   #input
        gi = interp1d(t,g,InterpFunc='cubic',fill_value='extrapolate')#InterpFunc need input
        t_new = np.logspace(min(np.log10(t)),max(np.log10(t)),len(t)*oversampling) #re-sample t in log space
        Gint_I = gi(t_new) # get new g(t) taken at log-space sampled t
        t_I = t_new
        '''
        t0 = 0   

        g0 = 1     #delet after design input label
        ginf = 0   #delet after design input label
        InterpFunc = "slinear"  #delet after design input label

        freqpoints = 200
        DIP = math.log10(len(t))/math.log10(t[-1]/t[0]);
        if DIP < 0.6:
            OverSample = int(10^(math.log10(t[-1]/t[0])))
            t_I = np.linspace(0,t[-1],OverSample)
            t1 = np.hstack((0,t))
            g1 = np.hstack((g0,g))
            f = interpolate.interp1d(t1, g1, InterpFunc)
            Gint_I = f(t_I)
        else:
            OverSample = int(len(t)*1e1)
            t_I = np.linspace(0,t[-1],OverSample)
            t1 = np.hstack((0,t))
            g1 = np.hstack((g0,g))
            f = interpolate.interp1d(t1, g1, "slinear")
            Gint_I = f(t_I)
        '''
        plt.plot(t_I, Gint_I, '-o', lw=3, color='royalblue', label='$G^{II}$')
        plt.xscale('log')
        plt.xlabel('Time (s)')
        plt.ylabel('G(t) (Pa)')
        plt.show()
    
    # @staticmethod
        option = 'cubic'
        InterpFunc = option
        oversampling=10
        gi = interp1d(t,g,InterpFunc,fill_value='extrapolate')
        t_new = np.logspace(min(np.log10(t)),max(np.log10(t)),len(t)*oversampling) #re-sample t in log space
        Gint_I = gi(t_new) # get new g(t) taken at log-space sampled t
        t_I = t_new
            
        '''
        DIP = math.log10(len(t))/math.log10(t[len(t)-1]/t[1])
        g0 = 1
            t_I = np.linspace(0, t.tail(1).item(), OverSample)
            t1 = np.hstack((0, t))
            g1 = np.hstack((g0, g))
            f = interpolate.interp1d(t1, g1, InterpFunc)
            Gint_I = f(t_I)
        else:
            OverSample = int(len(t) * 1e1)
            t_I = np.linspace(0, t.tail(1).item(), OverSample)
            t1 = np.hstack((0, t))
            g1 = np.hstack((g0, g))
            f = interpolate.interp1d(t1, g1, "slinear")
            Gint_I = f(t_I)
        '''
        return t_I, Gint_I

##zyy=oversampling("SingExp6_5.txt")
#zyy.OverSample()


# ========================= Useful Function =============================
def get_oversamping_data(content, ntimes):
    raw_data_df = generate_df(content)
    x, y = oversamping_process(raw_data_df[0], raw_data_df[1], ntimes)

    return x, y

def oversamping_process(t, g, ntimes):
    """
    t = values in x-axis
    g = values in y-axis
    ntimes = input number from component(id="oversamping-input") 
    """
    gi = interp1d(t, g, kind='cubic', fill_value='extrapolate')
    #re-sample t in log space
    t_new = np.logspace(min(np.log10(t)), max(np.log10(t)), len(t) * ntimes)
    # get new g(t) taken at log-space sampled t 
    Gint_I = gi(t_new) 
    t_I = t_new   

    return t_I.tolist(), Gint_I.tolist()