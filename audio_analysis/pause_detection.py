import audioop
import numpy as np
import constants as c
import os


def quiet_time():
    seconds = 0
    for chunk in c.frames:
        rms = audioop.rms(chunk, 2)
        if rms < c.quiet_threshold:
            seconds += c.chunk_duration
    return seconds