import assemblyai as aai
import pyaudio

result_folder = "outputs"

# AssemblyAI Constants
speech_model = aai.SpeechModel.nano
config = aai.TranscriptionConfig(speech_model=speech_model, disfluencies=True, entity_detection=True, speaker_labels=True)
audiofile = "https://assembly.ai/wildfires.mp3"
transcription_name = "transcriptions.txt"
entity_name = "entities.json"
stutter_name = "stutters.json"
speaker_name = "speakersep.json"

# Audio Constants
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100 
chunk_duration = chunk/fs                        
interval = 1                      
audio = "speaking.wav"
quiet_threshold = 20

# Recording Constants
recording_file = "questions"
