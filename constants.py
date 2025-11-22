import assemblyai as aai
import pyaudio

# AssemblyAI Constants
speech_model = aai.SpeechModel.nano
config = aai.TranscriptionConfig(speech_model=speech_model, disfluencies=True)
audiofile = "https://assembly.ai/wildfires.mp3"
transcription_result_folder = "outputs"
transcription_name = "transcriptions.txt"

# Audio Constants
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100 
chunk_duration = chunk/fs                        
interval = 1                      
file_folder = "outputs"
name = "speaking.wav"
quiet_threshold = 20