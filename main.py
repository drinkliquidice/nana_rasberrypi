import input.audiorecord as ar
import assembly.text_analysis as sta
import input.pause_detection as pd
import constants as c
import os

audio = os.path.join(c.result_folder, c.audio)
input("Press ENTER to start the code...")
# Your code begins here after Enter is pressed
ar.record_audio(audio)
transcription = sta.transcribe_audio("./" + audio)  
silence_info = pd.analyze_silence(audio)
print(silence_info["silent_segments"])
sta.entity_analysis(transcription)
sta.stutter_count(transcription)
sta.speaker_seperation(transcription)
