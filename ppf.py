import cProfile 
from app import Game

game = Game()

cProfile.run("game.run()", sort="cumtime")