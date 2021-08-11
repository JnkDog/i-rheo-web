import pandas as pd
import numpy as np

i = complex(0, 1)

"""
Combine the real_list and imag_list to complex_ndarray
"""
def combine_as_complex(real, imaginary):
    real_nd  = np.asarray(real)
    imaginary_nd = np.asarray(imaginary)

    # combine as complex with the real and imag
    complex = np.array(real_nd, dtype=np.complex128)
    complex.imag = imaginary_nd

    return complex.tolist()

"""
Formating saving data as six decimal place 
"""
def six_decimal_saving(data):
    for key, item in data.items():
        data[key] = np.around(item, decimals=6)

    return data