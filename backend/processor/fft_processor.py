import numpy as np

def compute_fft(signal, fs):
    # simple FFT wrapper returning freq and magnitude
    N = len(signal)
    yf = np.fft.rfft(signal)
    xf = np.fft.rfftfreq(N, 1.0/fs)
    mag = np.abs(yf) / N
    return xf, mag
