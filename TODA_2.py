import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import librosa


def cal_delay(y1, y2, sr):
    n = len(y1)

    corr = signal.correlate(y2, y1, mode='same') / np.sqrt(signal.correlate(y1, y1, mode='same')[int(n/2)] * signal.correlate(y2, y2, mode='same')[int(n/2)])

    delay_arr = np.linspace(-0.5*n/sr, 0.5*n/sr, n)
    delay = delay_arr[np.argmax(corr)]
    delay = str(delay)
    return delay

def Angle(d1,d2,d3):
    if abs(d1) < 0.00025 :
        return 1
    elif abs(d2) < 0.00025 :
        return 2
    elif abs(d3) < 0.00025 :
        return 3

# Sine sample with some noise and copy to y1 and y2 with a 1-second lag

audio_path_1st = '1.wav'
A, sr = librosa.load(audio_path_1st)
audio_path_2nd = '2.wav'
B, sr = librosa.load(audio_path_2nd)
audio_path_3rd = '3.wav'
C, sr = librosa.load(audio_path_3rd)

delay_1 = cal_delay(A, B, sr)
delay_2 = cal_delay(A, C, sr)
delay_3 = cal_delay(B, C, sr)