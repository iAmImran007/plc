#from connect.connection import DATA 
import asyncio
import random
import threading
import time
import pygame
import os

DATA = {}
PLAYING_SOUNDS = {}


async def dummy_plc():

    while True:
        
        DATA["Emergency_Stop"] = random.choice([True, False])
        DATA["Pressure_High"] = random.choice([True, False])
        DATA["Temperature_High"] = random.choice([True, False])
        DATA["Pressure_Low"] = random.choice([True, False])
        DATA["Temperature_Low"] = random.choice([True, False])

        print("\n--- PLC DATA UPDATE ---")
        print(DATA)

        await asyncio.sleep(3)




def get_audio_path(audio_file):
    audio_path = os.path.join(os.getcwd(), "audio", audio_file)
    return audio_path
    


        
def audio_manager_thread():

  pygame.mixer.init()

  sound_files = {
      "Emergency_Stop": get_audio_path("Emergency_Stop.mp3"),
      "Pressure_High": get_audio_path("Pressure_High.mp3"),
      "Temperature_High": get_audio_path("Temperature_High.mp3"),
      "Pressure_Low": get_audio_path("Pressure_Low.mp3"),
      "Temperature_Low": get_audio_path("Temperature_Low.mp3")
  }

  loaded_sounds = {}
  for key, file_path in sound_files.items():
    try:
      loaded_sounds[key] = pygame.mixer.Sound(file_path)
    except Exception as e:
      print(f"Could not load {file_path}: {e}")

  while True:
    for key, active in list(DATA.items()):

      if active and key not in PLAYING_SOUNDS:
        if key in loaded_sounds:
          # loops=-1 plays infinitely
          PLAYING_SOUNDS[key] = loaded_sounds[key].play(loops=-1)
          print(f"Started alarm: {key}")

      elif not active and key in PLAYING_SOUNDS:
        PLAYING_SOUNDS[key].stop()
        del PLAYING_SOUNDS[key]
        print(f"Stopped alarm: {key}")
    time.sleep(0.5)
