
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd

class mtfourier:
    def __init__(self, data):
        self.data = data

# available after design g_0,g_dot_inf input label
    
    # invoking test function to print G' and G"
    def test(self):
        df_news = pd.read_table(self.data,header = None)
        i = complex(0,1)
        time=np.linspace(1e-2,1e2,10000) 
        func = df_news[1]
        omega,res_test = mtfourier.manlio_ft(self,func,time,N_f=100,interpolate=True)
        g_p = np.real(res_test*omega*i)
        g_pp = np.imag(res_test*omega*i)
        fig = plt.figure(figsize=(6,5))
        plt.loglog(omega,g_p, '-o', lw=3, color='red',label='$G^{I}$') 
        plt.loglog(omega,g_pp, '-o', lw=3, color='royalblue',label='$G^{II}$')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Moduli (Pa)')
        plt.legend()
        plt.show()
    
    def manlio_ft(self,g,t,g_0=1,g_dot_inf=0,N_f=100,interpolate=True,oversampling=10):
    
        g = np.array(g)
        t = np.array(t)
    
        if interpolate is True:
            gi = interp1d(t,g,kind='cubic',fill_value='extrapolate')
            t_new = np.logspace(min(np.log10(t)),max(np.log10(t)),len(t)*oversampling) #re-sample t in log space
            g = gi(t_new) # get new g(t) taken at log-space sampled t
            t = t_new
        i = complex(0,1)
        min_omega = 1/max(t)
        max_omega = 1/min(t)
        N_t = len(t)
        omega = np.logspace(np.log10(min_omega),np.log10(max_omega),N_f)
        zero = i*omega*g_0 + (1-np.exp(-i*omega*t[1]))*((g[1]-g_0)/t[1])\
                + g_dot_inf*np.exp(-i*omega*t[N_t-1]) 
        res = np.zeros(len(omega),dtype=complex)
        for w_i, w in enumerate(omega):
            after = 0
            for k in range(2,N_t):
                after+=((g[k] - g[k-1]) / (t[k] - t[k-1])) * (np.exp(-i * w *
                t[k-1])-np.exp(-i * w * t[k]))
            res[w_i]=(zero[w_i]+after)
        return omega, ((res)/(i*omega)**2)


zyy = mtfourier("SingExp6_5.txt")
zyy.test()
    