import pyaudio
import wave
import numpy as np
import time
import os
import constants as c
import json

frames = []

def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return (in_data, pyaudio.paContinue)


def record_audio(file_name):
    shouldrun = True
    p = pyaudio.PyAudio()

    print("Recording...")

    stream = p.open(format = c.sample_format,
                    channels = c.channels,
                    rate = c.fs,
                    frames_per_buffer = c.chunk,
                    input = True,
                    stream_callback=callback)

    stream.start_stream()

    seconds = 0
    while(shouldrun):
        time.sleep(0.1)
        seconds += 0.1
        text = input("Stop recording?:")
        if(text.lower() == "s" or seconds >= 10):
            shouldrun = False

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Recording Stop")
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(c.channels)
    wf.setsampwidth(p.get_sample_size(c.sample_format))
    wf.setframerate(c.fs)
    wf.writeframes(b''.join(frames))
    wf.close()
