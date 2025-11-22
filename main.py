import audio_analysis.audiorecord as ar
import assembly.speechtotext as stt
import audio_analysis.pause_detection as pd
import constants as c
import os

file_name = os.path.join(c.file_folder, c.name)
ar.record_audio(file_name)
stt.transcribe_audio("./" + file_name)  
