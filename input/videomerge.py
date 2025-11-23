from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioArrayClip, concatenate_audioclips
import numpy as np

def merge_video_audio(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Sync audio length with video
    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)
    elif audio.duration < video.duration:
        silence_duration = video.duration - audio.duration
        fps = 44100
        silence_array = np.zeros((int(silence_duration * fps), 1))
        silence_clip = AudioArrayClip(silence_array, fps=fps)
        audio = concatenate_audioclips([audio, silence_clip])

    final = video.with_audio(audio)
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )

    