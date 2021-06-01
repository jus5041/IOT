import pyaudio
import numpy as np
import time
import wave
import matplotlib.pyplot as plt
from scipy import signal
import librosa


# open stream
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

CHUNK = 2048 # RATE / number of updates per second

RECORD_SECONDS = 20


# use a Blackman window
window = np.blackman(CHUNK)

x = 0

def soundPlot(stream, stream2, stream3):
    t1=time.time()
 
    data = stream.read(CHUNK, exception_on_overflow=False)
    waveData = wave.struct.unpack("%dh"%(CHUNK), data)
    npArrayData = np.array(waveData)
    indata = npArrayData*window
    #Plot time domain
    ax1.cla()
    ax1.plot(indata)
    ax1.grid()
    ax1.axis([0,CHUNK,-5000,5000])
    ax1.set_title("Mic_1")

    data2 = stream2.read(CHUNK, exception_on_overflow=False)
    waveData2 = wave.struct.unpack("%dh"%(CHUNK), data2)
    npArrayData2 = np.array(waveData2)
    indata2 = npArrayData2*window
    #Plot time domain
    ax2.cla()
    ax2.plot(indata2)
    ax2.grid()
    ax2.axis([0,CHUNK,-5000,5000])
    ax2.set_title("Mic_2")


    data3 = stream3.read(CHUNK, exception_on_overflow=False)
    waveData3 = wave.struct.unpack("%dh"%(CHUNK), data3)
    npArrayData3 = np.array(waveData3)
    indata3 = npArrayData3*window
    
    #Plot time domain
    ax3.cla()
    ax3.plot(indata3)
    ax3.grid()
    ax3.axis([0,CHUNK,-5000,5000])
    ax3.set_title("Mic_3")

    delay_1 , delay_arr_1, corr_1  = cal_delay(indata, indata2, RATE)

    #Plot time domain
    ax4.cla()
    
    ax4.plot(delay_arr_1, corr_1)
    ax4.grid()
    ax4.axis([-1, 1,-1,1])
    ax4.set_title("Mic_1 and Mic_2 Delay")

    delay_2 , delay_arr_2, corr_2  = cal_delay(indata2, indata3, RATE)

    #Plot time domain
    ax5.cla()
    ax5.plot(delay_arr_2, corr_2)
    ax5.grid()
    ax5.axis([-1, 1,-1,1])
    ax5.set_title("Mic_2 and Mic_3 Delay")

    delay_3 , delay_arr_3, corr_3  = cal_delay(indata, indata3, RATE)

    #Plot time domain
    ax6.cla()
    ax6.plot(delay_arr_3, corr_3)
    ax6.grid()
    ax6.axis([-1, 1,-1,1])
    ax6.set_title("Mic_1 and Mic_3 Delay")

    
    ax7.cla()

    if abs(delay_1) < 0.00025 :
        ax7.scatter(1,1)
    elif abs(delay_2) < 0.00025 :
        ax7.scatter(-1,1)
    elif abs(delay_3) < 0.00025 :
        ax7.scatter(0,1)
    else : ax7.scatter(0,0)

    ax7.grid()
    ax7.axis([-2, 2, -2, 2])
    ax7.set_title("Location_Detection")
    

    plt.pause(0.0001)



def cal_delay(y1, y2, sr):
    n = len(y1)

    corr = signal.correlate(y2, y1, mode='same') / np.sqrt(signal.correlate(y1, y1, mode='same')[int(n/2)] * signal.correlate(y2, y2, mode='same')[int(n/2)])

    delay_arr = np.linspace(-0.5*n/sr, 0.5*n/sr, n)
    delay = delay_arr[np.argmax(corr)]
    #delay = str(delay)
    return delay , delay_arr, corr

def angle(d1,d2,d3):
    if abs(d1) < 0.00025 :
        return 1
    elif abs(d2) < 0.00025 :
        return 2
    elif abs(d3) < 0.00025 :
        return 3

def location_detection(angle):
    if angle == 1:
        (x,y) = (1,1)
    elif angle ==2:
        (x,y) = (0,1)
    elif angle ==2:
        (x,y) = (-1,1)
    ax7.cla()
    ax7.plot(x, y)
    ax7.grid()
    ax7.axis([-2, 2, -2, 2])
    ax7.set_title("Mic_1 and Mic_3 Delay")


if __name__=="__main__":
    p=pyaudio.PyAudio()

    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  input_device_index=1,frames_per_buffer=CHUNK)
    stream2=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  input_device_index=2,frames_per_buffer=CHUNK)
    stream3=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  input_device_index=3,frames_per_buffer=CHUNK)
    
    plt.ion()
    fig = plt.figure(figsize=(10,10))
    ax1 = fig.add_subplot(331)
    ax2 = fig.add_subplot(332)
    ax3 = fig.add_subplot(333)
    ax4 = fig.add_subplot(334)
    ax5 = fig.add_subplot(335)
    ax6 = fig.add_subplot(336)
    ax7 = fig.add_subplot(337)

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        soundPlot(stream, stream2, stream3)
 

    stream.stop_stream()
    stream.close()
    p.terminate()
 