from scipy.interpolate import interp1d
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import multiprocessing

# this functino is used to draw the graph in web
# and have been tested work successfully
# later I put them into another way to print the graph
# def fttest():
#     df_news = pd.read_table("SingExp6_5.txt", header=None)
#     df_news = df_news
#     i = complex(0, 1)
#     time = np.linspace(1e-2, 1e2, 10000)
#     func = df_news[1]

#     layout = go.Layout(
#         title='ft graph',
#         yaxis={
#             'hoverformat': '.2f'  # 如果想显示小数点后两位'.2f'，显示百分比'.2%'
#         },
#         xaxis_type="log",
#         yaxis_type="log"
#     )

#     def manlio_ft(g, t, g_0=1, g_dot_inf=0, N_f=100, interpolate=True, oversampling=10):
#         g = np.array(g)
#         t = np.array(t)

#         if interpolate is True:
#             gi = interp1d(t, g, kind='cubic', fill_value='extrapolate')
#             t_new = np.logspace(min(np.log10(t)), max(np.log10(t)), len(t)*oversampling)  # re-sample t in log space
#             g = gi(t_new)  # get new g(t) taken at log-space sampled t
#             t = t_new
#         i = complex(0, 1)
#         min_omega = 1/max(t)
#         max_omega = 1/min(t)
#         N_t = len(t)
#         omega = np.logspace(np.log10(min_omega), np.log10(max_omega), N_f)
#         zero = i*omega*g_0 + (1-np.exp(-i*omega*t[1]))*((g[1]-g_0)/t[1])\
#             + g_dot_inf*np.exp(-i*omega*t[N_t-1])
#         res = np.zeros(len(omega), dtype=complex)
#         for w_i, w in enumerate(omega):
#             after = 0
#             for k in range(2, N_t):
#                 after += ((g[k] - g[k-1]) / (t[k] - t[k-1])) * (np.exp(-i * w * t[k-1])-np.exp(-i * w * t[k]))
#             res[w_i] = (zero[w_i]+after)
#         return omega, ((res)/(i*omega)**2)

#     omega, res_test = manlio_ft(func, time, 1, 0, N_f=100, interpolate=True)
#     g_p = np.real(res_test*omega*i)
#     g_pp = np.imag(res_test*omega*i)

#     # Add traces
#     trace1 = go.Scatter(
#         x=omega,
#         y=g_p,
#         mode="lines",
#         name="g_p"
#     )
#     trace2 = go.Scatter(
#         x=omega,
#         y=g_pp,
#         name="g_pp"
#     )
#     data = [trace1, trace2]
#     # print(go.Figure(data=data, layout=layout))
#     return go.Figure(
#         data=data,
#         layout=layout
#     )


def ftdata(df, gc_0, gc_inf, interpolate=False, oversampling=10):
    i = complex(0, 1)
    time = df[0]
    func = df[1]
    g_0 = gc_0
    g_dot_inf = gc_inf
    N_f = 100

    omega, res_test = manlio_ft(func, time, g_0, g_dot_inf, N_f, interpolate, oversampling)
    g_p = np.real(res_test*omega*i)
    g_pp = np.imag(res_test*omega*i)
    # print(g_p[0: 100])
    # print(g_pp[0: 100])
    return omega.tolist(), g_p.tolist(), g_pp.tolist()
 

def manlio_ft(g, t, g_0=1, g_dot_inf=0, N_f=100, interpolate=True, oversampling=10):
    g = np.array(g)
    t = np.array(t)

    if interpolate is True:
        gi = interp1d(t, g, kind='cubic', fill_value='extrapolate')
        # re-sample t in log space
        t_new = np.logspace(min(np.log10(t)), max(np.log10(t)), len(t)*oversampling)
        # get new g(t) taken at log-space sampled t
        g = gi(t_new)
        t = t_new
    i = complex(0, 1)
    min_omega = 1 / max(t)
    max_omega = 1 / min(t)
    N_t = len(t)
    omega = np.logspace(np.log10(min_omega), np.log10(max_omega), N_f)

    zero = i * omega * g_0 + (1-np.exp(-i*omega*t[1]))*((g[1]-g_0)/t[1]) \
           + g_dot_inf * np.exp(-i*omega*t[N_t-1])
    res = np.zeros(len(omega), dtype=complex)
    
    for w_i, w in enumerate(omega):
        after = 0
        for k in range(2, N_t):
            after += ((g[k] - g[k-1]) / (t[k] - t[k-1])) * (np.exp(-i * w * t[k-1])-np.exp(-i * w * t[k]))
        res[w_i] = (zero[w_i]+after)
    return omega, ((res)/(i*omega)**2)


"""
Using multi-processes to accelerate processing
"""
# Race condition --- lock
def calcu(N_t,g,t,i,w,w_i,lock,zero,res):
        after=0
        for k in range(2, N_t):
            after += ((g[k] - g[k - 1]) / (t[k] - t[k - 1])) * (np.exp(-i * w *t[k - 1]) - np.exp(-i * w * t[k]))
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
    for idx in range(N_f):
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
    # print("-----------------\n",res)
    # print(len(res))
    return omega, ((res) / (i * omega) ** 2)

def fast_ftdata(df, g_0, g_inf, N_f, interpolate=False, oversampling=10):
    i = complex(0, 1)
    time = df[0]
    func = df[1]

    omega, ft_result = fast_manlio_ft(func, time, g_0, g_inf, N_f, interpolate, oversampling)
    g_p = np.real(ft_result*omega*i)
    g_pp = np.imag(ft_result*omega*i)
    
    non_time_g_p = np.real(ft_result)
    non_time_g_pp = np.imag(ft_result)
    
    return omega.tolist(), g_p.tolist(), g_pp.tolist(), non_time_g_p.tolist(), non_time_g_pp.tolist()

