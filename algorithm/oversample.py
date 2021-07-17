
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
import math
from scipy import interpolate

class oversampling:
    def __init__(self, data):
        self.data=data
    #available after design g_0,g_dot_inf input label
    '''       
    def __init__(self,g0,ginf,oversampling):    
        self.g0 = g0
        self.ginf = ginf
        self.oversampling = oversampling  #times
    ''' 
    
    def OverSample(self):
         #,t,g,g0,ginf,InterpFunc):

        df_news = pd.read_table(self.data,header = None)
        t = df_news[0]
        g = df_news[1]
        oversampling=10
        gi = interp1d(t,g,InterpFunc='cubic',fill_value='extrapolate')
        t_new = np.logspace(min(np.log10(t)),max(np.log10(t)),len(t)*oversampling) #re-sample t in log space
        Gint_I = gi(t_new) # get new g(t) taken at log-space sampled t
        t_I = t_new
        '''
        InterpFunc = "slinear"#delet after design input label
        freqpoints = 200
        DIP = math.log10(len(t))/math.log10(t[len(t)-1]/t[1]);
        if DIP < 0.6:
            OverSample = int(10^(math.log10(t[len(t)-1]/t[1])))
            t_I = np.linspace(0,t[len(t)-1],OverSample)
            t1 = np.hstack((0,t))
            g1 = np.hstack((g0,g))
            f = interpolate.interp1d(t1,g1,InterpFunc)
            Gint_I=f(t_I)
        else:
            OverSample = int(len(t)*1e1)
            t_I = np.linspace(0,t[len(t)-1],OverSample)
            t1 = np.hstack((0,t))
            g1 = np.hstack((g0,g))
            f = interpolate.interp1d(t1,g1,"slinear")
            Gint_I=f(t_I)
        '''
        plt.plot(t_I,Gint_I,'-o', lw=3, color='royalblue',label='$G^{II}$')
        plt.xscale('log')
        plt.xlabel('Time (s)')
        plt.ylabel('G(t) (Pa)')
        plt.show()
    
        

##zyy=oversampling("SingExp6_5.txt")
#zyy.OverSample()

          