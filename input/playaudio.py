import pygame

def play_audio(file_path):
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    except pygame.error as e:
        print(f"Could not initialize mixer: {e}")
        exit()
    
    try:
        sound_effect = pygame.mixer.Sound(file_path)
    except pygame.error as e:
        print(f"Could not load sound file: {e}")
        exit()

    playing = sound_effect.play()
    
    while playing.get_busy():
        pygame.time.delay(100)
        
    print("Playback finished.")