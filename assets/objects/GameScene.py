from assets.CubicEngineData import *

class GameScene(Entity):
    def __init__(self, saves={}, ram={}):
        super().__init__()
        self.changeToScene = "nothing"
        self.saves = saves
        self.ram = ram