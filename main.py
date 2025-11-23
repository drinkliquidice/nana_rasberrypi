import input.audiorecord as ar
import assembly.text_analysis as sta
import input.pause_detection as pd
import constants as c
from playsound import playsound
import json
import os

def question_protocol(question):
    playsound("questions/" + question + ".mp3")
    audio_file = question +".wav"
    ar.record_audio(os.path.join(c.result_folder, audio_file))
    transcription = sta.transcribe_audio(os.path.join(c.result_folder, audio_file), question)
    sta.entity_analysis(transcription, os.path.join(c.result_folder, question))
    sta.stutter_count(transcription, os.path.join(c.result_folder, question))

# input("Press ENTER to start the code...")
# question_protocol("name_dob")
# question_protocol("why_in_hospital")
# question_protocol("address")
# question_protocol("how_is_day")

data = os.path.join(c.result_folder, "results.json")
name = json.load(open("outputs/name_dob_entity.json"))[0]
dob = json.load(open("outputs/name_dob_entity.json"))[1]
why_in_hospital = json.load(open("outputs/why_in_hospital_entity.json"))[2]
address = json.load(open("outputs/address_entity.json"))[3]
pause_data = pd.analyze_silence("outputs/how_is_day.wav")
dicdata = {"What is your name?": name['text'], "What is your date of birth?": dob['text'], "Why are you in the hospital?": why_in_hospital['text'], "What is your address?": address['text'], "How long where they thinking when asked about their day?": pause_data['silence_percentage']} 
with open(data, 'w') as f:
    json.dump(dicdata, f, indent=4)