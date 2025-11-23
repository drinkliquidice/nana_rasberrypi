import assemblyai as aai
import constants as c
import os
import json

with open('data.json') as f:
    aai.settings.api_key = json.load(f)['aai_api_key']


def transcribe_audio(audio_file, file):
    transcriber = aai.Transcriber(config=c.config)
    transcript = transcriber.transcribe(audio_file)
    if transcript.status == "completed":
        file_name = os.path.join(c.result_folder, file + ".txt")
        paragraphs = transcript.get_paragraphs()
        with open(file_name, "w") as f:
            for paragraph in paragraphs:
                f.write(paragraph.text + "\n\n")
        print("Finished")
    elif transcript.status == "error":
        print("Error: ", transcript.error)
    return transcript

def entity_analysis(transcript, output_filename):
    entities_data = [
        {
            "text": entity.text,
            "entity_type": entity.entity_type,
            "start": entity.start,
            "end": entity.end
        }
        for entity in transcript.entities
    ]
    count = 0
    for entity in entities_data:
        count += 1
    with open(output_filename + "_entity.json", 'w') as f:
            json.dump(entities_data, f, indent=4)
    entities_data.clear()
    print("Entities found!")
    return count

def stutter_count(transcript, output_filename):
    words = ["uh", "um", "mm"]
    stutter_data = [
        {
            "text": match.text,
            "count": match.count
        }
        for match in transcript.word_search(words)
    ]
    with open(output_filename + "_stutter.json", 'w') as f:
        json.dump(stutter_data, f, indent=4)
    stutter_data.clear()
    print("Stutter Data Finished!")