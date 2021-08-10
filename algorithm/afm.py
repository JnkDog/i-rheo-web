def oversample_function(df, ntimes):
    # used for test
    return df[0], df[1], df[2]

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
import time
import threading
from multiprocessing import Process
from multiprocessing import Process, Queue, Lock
from multiprocessing import Pool
import multiprocessing
import math
res = np.zeros(100, dtype=complex)


def manlio_ft(g, t, g_0=1, g_dot_inf=0, N_f=100, interpolate=True, oversampling=10):
    g = np.array(g)
    t = np.array(t)
    epsilon = 1e-5

    if interpolate is True:
        gi = interp1d(t, g, kind='cubic', fill_value='extrapolate')
        t_new = np.logspace(min(np.log10(t+epsilon)), max(np.log10(t+epsilon)), len(t) * oversampling)  # re-sample t in log space
        g = gi(t_new)  # get new g(t) taken at log-space sampled t
        t = t_new

    i = complex(0, 1)
    min_omega = 1 / max(t)
    max_omega = 1 / min(t)
    N_t = len(t)

    omega = np.logspace(np.log10(min_omega), np.log10(max_omega), N_f)

    zero = i * omega * g_0 + (1 - np.exp(-i * omega * t[1])) * ((g[1] - g_0) / t[1]) \
           + g_dot_inf * np.exp(-i * omega * t[N_t - 1])
    
    res = multiprocessing.Manager().list()

    for xxx in range(N_f):
        res.append(i)

    lock = multiprocessing.Manager().Lock()
    pool = multiprocessing.Pool(processes=5)

    for w_i, w in enumerate(omega):
        after = 0
        pool.apply_async(calcu, (N_t,g,t,i,w,w_i,lock,zero,res))  

        # res[w_i] = (zero[w_i] + after)
    pool.close()
    pool.join()
    # print("-----------------\n",res)
    # print(len(res))
    return omega, ((res) / (i * omega) ** 2)


def calcu(N_t, g, t, i, w, w_i, lock, zero,  res):
        after = 0
        for k in range(2, N_t):
            after += ((g[k] - g[k - 1]) / (t[k] - t[k - 1])) * (np.exp(-i * w *t[k - 1]) - np.exp(-i * w * t[k]))
        # print(after)
        
        lock.acquire()
        res[w_i] = after+zero[w_i]
        lock.release()
    
        return after


def afm_moduli_process(df, radius=20, v=0.5, load0=1, loadinf=0, ind0=1, indinf=0, N_f=100, interpolate=False, ntimes=10):
    i = complex(0, 1)  # 这行有用嘛？
    times = df[0]
    force = df[1]
    inden = df[2]
    # N_f = 100
    At = ((8*(radius**(1/2)))/(3*(1-v)))*(inden**(3/2))

    omega1, res_test1 = manlio_ft(force, times, load0, loadinf, N_f, interpolate, ntimes)
    omega2, res_test2 = manlio_ft(At, times, ind0, indinf, N_f, interpolate, ntimes)
    G_star = res_test1/res_test2
    # print("get result")
    g_p = np.real(G_star)
    g_pp = np.imag(G_star)

    return omega1, g_p, g_pp


# if __name__ == '__main__':
#     
#     df_news = pd.read_table('Agarose gel.txt',sep='	',header = None)
#     test()
#     
