from assets.CubicEngineData import *
from assets.objects.GameScene import *

class EndScreen(GameScene):
    def __init__(self, saves=..., ram=...):
        super().__init__(saves, ram)
        self.endText = Text(parent=self, text="End Screen", origin=(0,0), scale=(20,20))
        self.movesCounterText = Text(parent=self, text=f"Moves: {self.ram['moves']}", origin=(0,0), scale=(20,20), position=(0,-2))
        match self.ram["winner"]:
            case "player":
                self.endText.text = "You win!"
            case "opponent":
                self.endText.text = "You lost..."
            case "debug":
                self.endText.text = "Warped here with debug keys"
            case _:
                self.endText.text = "Wait, what the fuck?!"

        self.goToMainScreen = Button(parent=self, text="Replay", scale=(2.8,1), position=(0, -1), on_click=self.mainScreenFunction) #I'm not gonna make the main menu yet

    def mainScreenFunction(self):
        self.changeToScene = "virusGame" #Will soon send to main menu