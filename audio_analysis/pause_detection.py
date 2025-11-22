from pydub import AudioSegment
from pydub.silence import detect_silence

def analyze_silence_pydub(wav_file, silence_thresh=-40, min_silence_len=500):
    audio = AudioSegment.from_wav(wav_file)
    
    # Detect silent segments
    silent_ranges = detect_silence(audio, 
                                   min_silence_len=min_silence_len,
                                   silence_thresh=silence_thresh)
    
    silent_segments = []
    for start_ms, end_ms in silent_ranges:
        silent_segments.append({
            'start_time': start_ms / 1000,
            'end_time': end_ms / 1000,
            'duration': (end_ms - start_ms) / 1000
        })
    
    total_duration = len(audio) / 1000  # Convert to seconds
    total_silence = sum(end - start for start, end in silent_ranges) / 1000
    silence_percentage = (total_silence / total_duration) * 100
    
    return {
        'total_duration_seconds': total_duration,
        'silence_duration_seconds': total_silence,
        'silence_percentage': silence_percentage,
        'num_silent_segments': len(silent_ranges),
        'silent_segments': silent_segments
    }