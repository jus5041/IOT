import pyaudio
import numpy as np
import time
import wave
import matplotlib.pyplot as plt


# open stream
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

CHUNK = 2048 # RATE / number of updates per second

RECORD_SECONDS = 5


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

    data2 = stream2.read(CHUNK, exception_on_overflow=False)
    waveData2 = wave.struct.unpack("%dh"%(CHUNK), data2)
    npArrayData2 = np.array(waveData2)
    indata2 = npArrayData2*window
    #Plot time domain
    ax2.cla()
    ax2.plot(indata2)
    ax2.grid()
    ax2.axis([0,CHUNK,-5000,5000])

    data3 = stream3.read(CHUNK, exception_on_overflow=False)
    waveData3 = wave.struct.unpack("%dh"%(CHUNK), data3)
    npArrayData3 = np.array(waveData3)
    indata3 = npArrayData3*window
    #Plot time domain
    ax3.cla()
    ax3.plot(indata3)
    ax3.grid()
    ax3.axis([0,CHUNK,-5000,5000])

    plt.pause(0.0001)


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
    fig = plt.figure(figsize=(10,20))
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        soundPlot(stream, stream2, stream3)
 

    stream.stop_stream()
    stream.close()
    p.terminate()
 