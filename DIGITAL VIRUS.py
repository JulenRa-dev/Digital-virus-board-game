import os
try:
    os.system("pip install ursina")
    from assets.CubicEngineData import *
except:
    os.system("py -m pip install ursina")
    from assets.CubicEngineData import *
from assets.mainGame import *

app = Ursina(development_mode=False, borderless=False, title="DIGITAL VIRUS")

window.color = color.gray
window.borderless = False
window.fullscreen = False

startup()

def input(key):
    keyDetect(key)

def update():
    gameLoop()


app.run()