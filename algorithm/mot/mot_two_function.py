import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import multiprocessing
from scipy.interpolate import interp1d

"""
Using multi-processes to accelerate processing
"""
i = complex(0, 1)

# Race condition --- lock
def calcu(N_t,g,t,i,w,w_i,lock,zero,res):
        after=0
        for k in range(2, N_t):
            after += ((g[k] - g[k - 1]) / (t[k] - t[k - 1])) \
                     * (np.exp(-i * w *t[k - 1]) - np.exp(-i * w * t[k]))
        # print(after)
        
        lock.acquire()
        res[w_i] = after + zero[w_i]
        lock.release()

        return after

def fast_manlio_ft(g, t, g_0=1, g_dot_inf=0, N_f=100, interpolate=True, oversampling=10):
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

    res = multiprocessing.Manager().list()
    for idx in range(100):
        res.append(i)

    # setting a lock
    lock = multiprocessing.Manager().Lock()
    # seting a resource pool
    pool = multiprocessing.Pool(processes = 5)
    for w_i, w in enumerate(omega):
        #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
        pool.apply_async(calcu, (N_t, g, t, i, w, w_i, lock, zero, res))   

    pool.close()
    pool.join()

    return omega, ((res) / (i * omega) ** 2)

def pai_t_G_star_processing(k, a, omega, ft_result):
    G_start = (k/(6 * math.pi * a))*(1/(i * omega * ft_result) - 1)
    return G_start

def a_t_G_star_processing(k, a, omega, ft_result):
    G_star = (k/(6 * math.pi * a))*(1/(1 - i * omega * ft_result) - 1)
    return G_star

def mot_integrated_processing(df, k, a, g_0, g_dot_inf,interpolate=False, n_times=10):
    # The input value is k, a, g_0, g_dot_inf
    x = df[0]
    y = df[1]

    omega, ft_result = fast_manlio_ft(y, x, g_0, g_dot_inf, interpolate=interpolate, oversampling=n_times)
    # k a only works in g_p g_pp 
    pai_t_G_star = pai_t_G_star_processing(k, a, omega, ft_result)
    a_t_G_start = a_t_G_star_processing(k, a, omega, ft_result)
    
    # Due to the complex is tuple, it cannot be serilized, it needs sliced to real and imag
    pai_g_p, a_t_g_p, ft_result_real   = list(map(np.real, [pai_t_G_star, a_t_G_start, ft_result]))
    pai_g_pp, a_t_g_pp, ft_result_imag = list(map(np.imag, [pai_t_G_star, a_t_G_start, ft_result]))
    
    return omega.tolist(), pai_g_p.tolist(), pai_g_pp.tolist(),\
            a_t_g_p.tolist(), a_t_g_pp.tolist(), \
            ft_result_real.tolist(), ft_result_imag.tolist()

"""
k, a only influence the gp gpp not the FT 
"""
def chenged_G_start_to_g(k, a, data):
    ft_complex = combine_as_complex(data)
    omega = np.asarray(data["x"]) 

    # k a only works in g_p g_pp 
    pai_t_G_star = pai_t_G_star_processing(k, a, omega, ft_complex)
    a_t_G_start = a_t_G_star_processing(k, a, omega, ft_complex)

    pai_g_p, a_t_g_p = list(map(np.real, [pai_t_G_star, a_t_G_start]))
    pai_g_pp, a_t_g_pp = list(map(np.imag, [pai_t_G_star, a_t_G_start]))

    return  pai_g_p.tolist(), pai_g_pp.tolist(), a_t_g_p.tolist(), a_t_g_pp.tolist()


"""
Combine the real_list and imag_list to complex_ndarray
"""
def combine_as_complex(data):
    ft_real  = data["ft_real"] 
    ft_image = data["ft_imag"]

    # combine as complex with the real and imag
    ft_complex = np.array(ft_real, dtype=complex)
    ft_complex.imag = ft_image

    return ft_complex