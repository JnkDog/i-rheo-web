import math
import multiprocessing
import threading
import time
from multiprocessing import Lock, Pool, Process, Queue

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

i = complex(0, 1)

def manlio_ft(g, t, stress_0, stress_dot_inf, strain_0, strain_dot_inf, 
            gg, ggg,  N_f=100, interpolate=False, oversampling=10):
    g = np.array(g)
    gg = np.array(gg)
    ggg = np.array(ggg)
    t = np.array(t)
    if interpolate is True:
        gi = interp1d(t, g, kind='cubic', fill_value='extrapolate')
        ggi = interp1d(t, gg, kind='cubic', fill_value='extrapolate')
        gggi = interp1d(t, ggg, kind='cubic', fill_value='extrapolate')
        t_new = np.logspace(min(np.log10(t)), max(np.log10(t)), len(t) * oversampling)  # re-sample t in log space
        g = gi(t_new)  # get new g(t) taken at log-space sampled t
        gg = ggi(t_new)
        ggg = gggi(t_new)
        t = t_new

    min_omega = 1 / max(t)
    max_omega = 1 / min(t)
    N_t = len(t)
    omega = np.logspace(np.log10(min_omega), np.log10(max_omega), N_f)

    zero = i * omega * stress_0 + (1 - np.exp(-i * omega * t[1])) * ((g[1] - stress_0) / t[1]) \
           + stress_dot_inf * np.exp(-i * omega * t[N_t - 1])

    zerooo = i * omega * strain_0 + (1 - np.exp(-i * omega * t[1])) * ((ggg[1] - strain_0) / t[1]) \
           + strain_dot_inf * np.exp(-i * omega * t[N_t - 1])

    res= multiprocessing.Manager().list()
    for xxx in range(N_f):
        res.append(i)
    lock=multiprocessing.Manager().Lock()
    pool = multiprocessing.Pool(processes = 5)
    for w_i, w in enumerate(omega):
        pool.apply_async(calcu, (N_t,g,t,i,w,w_i,lock,zero,res))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    pool.close()
    pool.join()
    
    ress= multiprocessing.Manager().list()
    for xxx in range(N_f):
        ress.append(i)
    lock = multiprocessing.Manager().Lock()
    pool = multiprocessing.Pool(processes = 5)
    for q_i, q in enumerate(omega):
        pool.apply_async(calcu, (N_t,gg,t,i,q,q_i,lock,zero,ress))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    pool.close()
    pool.join()
    
    resss= multiprocessing.Manager().list()
    for xxx in range(N_f):
        resss.append(i)
    lock = multiprocessing.Manager().Lock()
    pool = multiprocessing.Pool(processes = 5)
    for p_i, p in enumerate(omega):
        pool.apply_async(calcu, (N_t,ggg,t,i,p,p_i,lock,zerooo,resss))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    pool.close()
    pool.join()

    ressss= multiprocessing.Manager().list()
    for xxx in range(N_f):
        ressss.append(i)
    
    lock = multiprocessing.Manager().Lock()
    pool = multiprocessing.Pool(processes = 5)
    for p_i, p in enumerate(omega):
        pool.apply_async(calcu, (N_t,gg,t,i,p,p_i,lock,zerooo,ressss))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    pool.close()
    pool.join()

    return omega, ((res) / (i * omega) ** 2), ((ress) / (i * omega) ** 2), ((resss) / (i * omega) ** 2), ((ressss) / (i * omega) ** 2)

def calcu(N_t,g,t,i,w,w_i,lock,zero,res):

        after=0
        for k in range(2, N_t):
            after += ((g[k] - g[k - 1]) / (t[k] - t[k - 1])) * (np.exp(-i * w *t[k - 1]) - np.exp(-i * w * t[k]))
        lock.acquire()
        res[w_i]=after+zero[w_i]
        lock.release()

        return after

def bulk_ft(df, stress_0, stress_dot_inf,strain_0, strain_dot_inf, 
            interpolate, N_f, oversampling=10):
    funcc = df[2]
    func = df[1] 
    time = df[0]
    func = func/funcc
    funccc = df[1]

    omega, res_test, ress_test, resss_test, ressss_test = \
        manlio_ft(func, time, stress_0, stress_dot_inf, 
                  strain_0, strain_dot_inf, funcc, funccc, 
                  N_f, interpolate, oversampling)

    G1  = (res_test * omega * i)
    G2  = (ress_test * omega * i)
    G22 = (ressss_test * omega * i)
    G3  = (resss_test * omega * i)
    G4  = (G1/G2)
    G5  = (G3/G22)

    g_p = np.real(G5)
    g_pp = np.imag(G4)

    y1 = g_p*10**5
    y2 = g_pp*10**6

    return omega.tolist(), y1.tolist(), y2.tolist()