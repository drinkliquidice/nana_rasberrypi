import assemblyai as aai
import constants as c
import os
import json

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