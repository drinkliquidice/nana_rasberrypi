import input.audiorecord as ar
import assembly.text_analysis as sta
import input.pause_detection as pd
import input.playaudio as pa
import input.videorecord as vr
import input.videomerge as mav
import constants as c
import json
import os
import sys
import asyncio

async def wait_for_stop(stop_event: asyncio.Event):
    loop = asyncio.get_running_loop()
    print("Type 's' then press ENTER to stop recording...")

    while not stop_event.is_set():
        text = await loop.run_in_executor(None, sys.stdin.readline)
        if text.strip().lower() == 's':
            stop_event.set()
            print("Stopping recording...")
            break

async def process_transcription(audio_file, question):
    loop = asyncio.get_running_loop()

    # Run blocking functions in a separate thread
    transcription = await asyncio.to_thread(
        sta.transcribe_audio,
        os.path.join(c.result_folder, audio_file),
        question
    )

    num = None
    if question != "how_is_day":
        num = await asyncio.to_thread(
            sta.entity_analysis,
            transcription,
            os.path.join(c.result_folder, question)
        )

    await asyncio.to_thread(
        sta.stutter_count,
        transcription,
        os.path.join(c.result_folder, question)
    )

    return num, transcription

async def question_protocol(question):
    loop = asyncio.get_running_loop()

    await pa.play_audio(os.path.join(c.question_folder, question + ".mp3"))

    print(f"Press 's' then Enter to START recording for question: {question}")
    while True:
        text = await loop.run_in_executor(None, input)
        if text.strip().lower() == 's':
            break

    print(f"Recording started for question: {question}")
    stop_event = asyncio.Event()

    video_file = os.path.join(c.result_folder, question + ".mp4")
    audio_file = os.path.join(c.result_folder, question + ".wav")

    async def stop_listener():
        print(f"Press 'd' then Enter to STOP recording for question: {question}")
        while not stop_event.is_set():
            t = await loop.run_in_executor(None, input)
            if t.strip().lower() == 'd':
                stop_event.set()
                print("Stopping recording...")
                break

    wait_task = asyncio.create_task(stop_listener())

    vr_task = asyncio.create_task(vr.record_video(video_file, stop_event))
    ar_task = asyncio.create_task(ar.record_audio(audio_file, stop_event))

    await asyncio.gather(vr_task, ar_task, wait_task)

    print(f"Recording finished for question: {question}")

    num, transcription = await process_transcription(question + ".wav", question)

    return num

async def main():
    input("Press ENTER to start the code...")

    await question_protocol("name_dob")
    await question_protocol("why_in_hospital")
    a = await question_protocol("address")
    await question_protocol("how_is_day")

    data = os.path.join(c.result_folder, "results.json")

    if a >= 4:
        name = json.load(open("outputs/name_dob_entity.json"))[0]
        dob = json.load(open("outputs/name_dob_entity.json"))[1]
        why_in_hospital = json.load(open("outputs/why_in_hospital_entity.json"))[2]
        address = json.load(open("outputs/address_entity.json"))[3]

        pause_data = pd.analyze_silence("outputs/how_is_day.wav")
        stutter_data = json.load(open("outputs/how_is_day_stutter.json"))

        dicdata = {
            "questions": {
                "What is your name?": name['text'],
                "What is your date of birth?": dob['text'],
                "Why are you in the hospital?": why_in_hospital['text'],
                "What is your address?": address['text']
            },
            "pauses": pause_data['silence_percentage'],
            "Stutter Data": stutter_data
        }

        with open(data, 'w') as f:
            json.dump(dicdata, f, indent=4)

    else:
        with open(data, 'w') as f:
            json.dump({"error": "Not enough entities found"}, f, indent=4)

    mav.merge_video_audio("outputs/name_dob.mp4",
                          "outputs/name_dob.wav",
                          "outputs/name_dob.mp4")
    mav.merge_video_audio("outputs/why_in_hospital.mp4",
                          "outputs/why_in_hospital.wav",
                          "outputs/why_in_hospital.mp4")
    mav.merge_video_audio("outputs/address.mp4",
                          "outputs/address.wav",
                          "outputs/address.mp4")
    mav.merge_video_audio("outputs/how_is_day.mp4",
                          "outputs/how_is_day.wav",
                          "outputs/how_is_day.mp4")
    
    
if __name__ == "__main__":
    asyncio.run(main())
