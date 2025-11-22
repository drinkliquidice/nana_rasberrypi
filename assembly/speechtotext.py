
import assemblyai as aai
import constants
import os
import json

with open('data.json') as f:
    aai.settings.api_key = json.load(f)['api_key']

def transcribe_audio(audio_file):
    transcriber = aai.Transcriber(config=constants.config)
    transcript = transcriber.transcribe(audio_file)
    if transcript.status == "completed":
        file_name = os.path.join(constants.transcription_result_folder, constants.transcription_name)
        paragraphs = transcript.get_paragraphs()
        with open(file_name, "w") as f:
            for paragraph in paragraphs:
                f.write(paragraph.text + "\n\n")
        print("Finished")
    elif transcript.status == "error":
        print("Error: ", transcript.error)

