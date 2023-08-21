import pickle
from pathlib import Path
import os 

username = os.getlogin()


ROOM_SIZE = 450
coin_multi = 1
button_width_height = (100, 30)

PATH = rf'C:\Users\{username}\AppData\Local\VampireAbyss\SaveFiles'


try:
    Path(PATH).mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(e)
    
PATH = Path(PATH)
