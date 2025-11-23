import pyaudio
import wave
import asyncio
import constants as c

# Make frames local to each recording to avoid accumulation
async def record_audio(file_name, stop_event: asyncio.Event):
    frames = []

    def callback(in_data, frame_count, time_info, status):
        frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    p = pyaudio.PyAudio()
    print("Audio recording started...")

    stream = p.open(
        format=c.sample_format,
        channels=c.channels,
        rate=c.fs,
        frames_per_buffer=c.chunk,
        input=True,
        stream_callback=callback
    )

    stream.start_stream()

    # Poll stop_event so recording stops when triggered
    while not stop_event.is_set():
        await asyncio.sleep(0.01)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Audio recording stopped")

    # Save to file
    with wave.open(file_name, 'wb') as wf:
        wf.setnchannels(c.channels)
        wf.setsampwidth(p.get_sample_size(c.sample_format))
        wf.setframerate(c.fs)
        wf.writeframes(b''.join(frames))
