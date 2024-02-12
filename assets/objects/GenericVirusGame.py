#This is made for helping me making the game. This scene won't be used in any part of the game(unless you are very dumb and actually make so you can access it)

from assets.CubicEngineData import *
from assets.objects.GameScene import *
from assets.objects.Card import *

class GenericVirusGame(GameScene):
    def __init__(self, saves=..., ram=...):
        super().__init__(saves, ram)
        self.cards = []
        self.giveRandomCard(-2)
        self.giveRandomCard(0)
        self.giveRandomCard(2)
        self.organs = {"heart": None, "bone": None, "stomache": None, "brain": None}
        self.infectedOrgans = []
        self.inmunizedOrgans = []
        self.protectedOrgans = []
        self.cardsAreVisible = True

    def update(self):
        pass

    def applyCardEffects(self, target, card=Card, index=0):
        pass

    def checkIfWon(self):
        pass

    def placeOrgan(self, organType=str):
        pass

    def giveRandomCard(self, target, cardx=0):
        pass

    def healOrgan(self, target, organType=str):
        pass

    def infectOrgan(self, target, organType=str):
        pass