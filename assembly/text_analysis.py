import assemblyai as aai
import constants as c
import os
import json
import requests
import time 

with open('data.json') as f:
    aai.settings.api_key = json.load(f)['aai_api_key']


def transcribe_audio(audio_file):
    transcriber = aai.Transcriber(config=c.config)
    transcript = transcriber.transcribe(audio_file)
    if transcript.status == "completed":
        file_name = os.path.join(c.result_folder, c.transcription_name)
        paragraphs = transcript.get_paragraphs()
        with open(file_name, "w") as f:
            for paragraph in paragraphs:
                f.write(paragraph.text + "\n\n")
        print("Finished")
    elif transcript.status == "error":
        print("Error: ", transcript.error)
    return transcript

def entity_analysis(transcript):
    output_filename = os.path.join(c.result_folder, c.entity_name)
    entities_data = [
        {
            "text": entity.text,
            "entity_type": entity.entity_type,
            "start": entity.start,
            "end": entity.end
        }
        for entity in transcript.entities
    ]
    with open(output_filename, 'w') as f:
            json.dump(entities_data, f, indent=4)

    print("Entities found!")

def stutter_count(transcript):
    output_filename = os.path.join(c.result_folder, c.stutter_name)
    words = ["uh", "um", "mm"]
    stutter_data = [
        {
            "text": match.text,
            "count": match.count
        }
        for match in transcript.word_search(words)
    ]
    with open(output_filename, 'w') as f:
        json.dump(stutter_data, f, indent=4)

    print("Stutter Data Finished!")

def speaker_seperation(transcript):
    output_filename = os.path.join(c.result_folder, c.speaker_name)

    speaker_data = [
        {
            "speaker": utterance.speaker,
            "text": utterance.text,
            "start": utterance.start,
            "end": utterance.end
        }
        for utterance in transcript.utterances
    ]

    with open(output_filename, 'w') as f:
        json.dump(speaker_data, f, indent=4)

    print("Speaker separation data finished!")