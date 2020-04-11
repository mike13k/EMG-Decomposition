import numpy as np
from scipy import signal
from scipy.signal import iirfilter, iirnotch, lfilter, butter, filtfilt
import matplotlib.pyplot as plt

def read_file(file_name):
    lines = [line.rstrip('\n') for line in open(file_name)]
    return np.array(lines).astype(np.float)

original_signal = read_file('Data.txt')
