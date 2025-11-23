from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

def merge_video_audio(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)  # WAV file

    final = video.set_audio(audio)
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

    