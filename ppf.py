import cProfile 
from app import Game
print(dir(cProfile))

game = Game()

cProfile.run("game.run()", sort="cumtime")