import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
import time
import threading
from multiprocessing import Process
from multiprocessing import Process, Queue,Lock
from multiprocessing import Pool
import multiprocessing
res = np.zeros(100, dtype=complex)

def manlio_ft(g, t, g_0=1, g_dot_inf=0, N_f=100, interpolate=True, oversampling=10):
    g = np.array(g)
    t = np.array(t)
    if interpolate is True:
        gi = interp1d(t, g, kind='cubic', fill_value='extrapolate')
        t_new = np.logspace(min(np.log10(t)), max(np.log10(t)), len(t) * oversampling)  # re-sample t in log space
        g = gi(t_new)  # get new g(t) taken at log-space sampled t
        t = t_new
    i = complex(0, 1)
    min_omega = 1 / max(t)
    max_omega = 1 / min(t)
    N_t = len(t)
    omega = np.logspace(np.log10(min_omega), np.log10(max_omega), N_f)

    zero = i * omega * g_0 + (1 - np.exp(-i * omega * t[1])) * ((g[1] - g_0) / t[1]) \
           + g_dot_inf * np.exp(-i * omega * t[N_t - 1])


    print(len(omega))
    print(N_t)
    res= multiprocessing.Manager().list()
    for xxx in range(100):
        res.append(i)
    lock=multiprocessing.Manager().Lock()
    pool = multiprocessing.Pool(processes = 5)
    for w_i, w in enumerate(omega):
        after = 0
        pool.apply_async(calcu, (N_t,g,t,i,w,w_i,lock,zero,res))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

        #res[w_i] = (zero[w_i] + after)
    pool.close()
    pool.join()
    print("-----------------\n",res)
    print(len(res))
    return omega, ((res) / (i * omega) ** 2)



def calcu(N_t,g,t,i,w,w_i,lock,zero,res):

        after=0
        for k in range(2, N_t):
            after += ((g[k] - g[k - 1]) / (t[k] - t[k - 1])) * (np.exp(-i * w *t[k - 1]) - np.exp(-i * w * t[k]))
        print(after)
        
        lock.acquire()
        res[w_i]=after+zero[w_i]
        lock.release()

        
        return after


def test():
    i = complex(0, 1)
    time = df_news[0]
    func = df_news[1]

    omega, res_test = manlio_ft(func, time, N_f=100, interpolate=True)
    
    g_p = np.real(res_test * omega * i)
    g_pp = np.imag(res_test * omega * i)
    fig = plt.figure(figsize=(6, 5))
    

    plt.loglog(omega, g_p, '-o', lw=3, color='red', label='$G^{I}$')
    plt.loglog(omega, g_pp, '-o', lw=3, color='royalblue', label='$G^{II}$')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Moduli (Pa)')
    plt.legend()
    plt.show()
    

if __name__ == '__main__':
    start=time.time()
    df_news = pd.read_table('SingExp6_5.txt', sep='\t', header=None)
    
    test()
    end=time.time()
    print("\ntime",end-start)
