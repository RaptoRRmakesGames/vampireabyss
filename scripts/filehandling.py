import pickle
from pathlib import Path

from scripts.settings import *



def savevar(path, var):
    global PATH
    file_path = PATH / path
    with file_path.open(mode='wb') as f:
        pickle.dump(var, f)
        
def loadvar( filename):
    global PATH
    file_path = PATH / filename
    with file_path.open(mode='rb') as f:
        return pickle.load(f)

