from assets.CubicEngineData import *
from assets.objects.GameScene import *
from assets.scenes.VirusGame import *
from assets.scenes.EndScreen import *
from assets.scenes.MainMenu import *

def startup():
    global gameScene
    #Insert initialitation code here
    gameScene = GameScene(saves={}, ram={})
    pass

def keyDetect(key):
    #Enter something like
    #if key == "space":
    #   print("Space key pressed")
    pass

def gameLoop():
    global gameScene
    #Here enter the main loop of the game
    if gameScene.__class__ == GameScene:
        saves = gameScene.saves
        ram = gameScene.ram
        destroy(gameScene)
        gameScene = VirusGame(saves=saves, ram=ram)
    if gameScene.changeToScene == "endScreen":
        saves = gameScene.saves
        ram = gameScene.ram
        destroy(gameScene)
        gameScene = EndScreen(saves=saves, ram=ram)
    if gameScene.changeToScene == "mainMenu":
        saves = gameScene.saves
        ram = gameScene.ram
        destroy(gameScene)
        gameScene = MainMenu(saves=saves, ram=ram)
    if gameScene.changeToScene == "virusGame":
        saves = gameScene.saves
        ram = gameScene.ram
        destroy(gameScene)
        gameScene = VirusGame(saves=saves, ram=ram)
    pass