from assets.CubicEngineData import *
from assets.objects.GameScene import *

class MainMenu(GameScene):
    def __init__(self, saves=..., ram=...):
        super().__init__(saves, ram)