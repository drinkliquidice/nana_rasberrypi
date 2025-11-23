from gpiozero import LED
from gpiozero import TonalBuzzer
from gpiozero import Button
from gpiozero.tones import Tone
import time
import random

LED_PINS = [12, 13, 14, 15]
BUTTON_PINS = [11, 10, 9, 8]
BUZZER_PIN = 6

leds = [LED(pin) for pin in LED_PINS]
buttons = [Button(pin, pull_up=True) for pin in BUTTON_PINS]
buzzer = TonalBuzzer(BUZZER_PIN)

FREQUENCIES = [440, 494, 523, 587]

sequence = []
user_input = []

def play_tone(frequency):
    buzzer.play(Tone(frequency))
    time.sleep(0.2)
    buzzer.stop()

def light_led(index):
    leds[index].on()
    play_tone(FREQUENCIES[index])
    time.sleep(0.2)
    leds[index].off()
    time.sleep(0.2)

def flash_button(index):
    leds[index].on()
    play_tone(FREQUENCIES[index])
    time.sleep(0.05)
    leds[index].off()

def get_user_input():
    global user_input
    user_input = []

    while len(user_input) < len(sequence):
        for i, button in enumerate(buttons):
            if button.is_pressed:
                flash_button(i)
                user_input.append(i)

                if user_input[-1] != sequence[len(user_input) - 1]:
                    return False

                time.sleep(0.2)
                while button.is_pressed:
                    time.sleep(0.1)

    return True

def idle_mode():
    while True:
        for i in range(len(leds)):
            leds[i].on()
            time.sleep(0.1)
            leds[i].off()
            time.sleep(0.1)

        if any(button.is_pressed for button in buttons):
            return

def game_over():
    for _ in range(3):
        for led in leds:
            led.on()
        play_tone(300)
        time.sleep(0.5)
        for led in leds:
            led.off()
        time.sleep(0.5)

def play_game():
    global sequence
    sequence = []
    score = 0

    while True:
        next_led = random.randint(0, 3)
        sequence.append(next_led)

        for led_index in sequence:
            light_led(led_index)
            time.sleep(0.2)

        if not get_user_input():
            print("Game Over! You failed.")
            game_over()
            return score

        score += 1
        print("Correct! Next round.")

