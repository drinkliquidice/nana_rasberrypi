import pygame
import asyncio

async def play_audio(file_path):
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    except pygame.error as e:
        print(f"Could not initialize mixer: {e}")
        return

    try:
        sound_effect = pygame.mixer.Sound(file_path)
    except pygame.error as e:
        print(f"Could not load sound file: {e}")
        return

    channel = sound_effect.play()

    # Non-blocking wait
    while channel.get_busy():
        await asyncio.sleep(0.1)

    print("Playback finished.")
