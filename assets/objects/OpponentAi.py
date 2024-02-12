from assets.CubicEngineData import *
from assets.objects.CardUsingAnim import *

class OpponentAi(Entity):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.cards = []
        self.organs = {"heart": None, "bone": None, "stomache": None, "brain": None}
        self.infectedOrgans = []
        self.inmunizedOrgans = []
        self.protectedOrgans = []
        self.cardsAreVisible = False
        self.cardIdxUsed = -1

    def placeOrgan(self, organType=str):
        if organType == "heart":
            self.organs[organType].position = (-5, 3)
        if organType == "stomache":
            self.organs[organType].position = (-5, 1)
        if organType == "bone":
            self.organs[organType].position = (-5, -1)
        if organType == "brain":
            self.organs[organType].position = (-5, -3)

    def step(self, playerOrgans={}):
        cardTypes = []
        for card in self.cards:
            cardTypes.append(card.cardType)
        if "organ" in cardTypes:
            self.cardIdxUsed = cardTypes.index("organ")
            CardUsingAnim(position=(-6,1), mycolor=self.cards[self.cardIdxUsed].color, parent=self.parent, target=(-2, 1), quickDescription=self.cards[self.cardIdxUsed].quickDescription.text)
            return
        if "virus" in cardTypes:
            if playerOrgans[self.cards[cardTypes.index("virus")].organType] != None:
                self.cardIdxUsed = cardTypes.index("virus")
                CardUsingAnim(position=(-6,1), mycolor=self.cards[self.cardIdxUsed].color, parent=self.parent, target=(-2, 1), quickDescription=self.cards[self.cardIdxUsed].quickDescription.text)
                return
        if "heal" in cardTypes:
            if self.organs[self.cards[cardTypes.index("heal")].organType] != None:
                self.cardIdxUsed = cardTypes.index("heal")
                CardUsingAnim(position=(-6,1), mycolor=self.cards[self.cardIdxUsed].color, parent=self.parent, target=(-2, 1), quickDescription=self.cards[self.cardIdxUsed].quickDescription.text)
                return
        self.cardIdxUsed = random.randint(0,len(self.cards)-1)
        CardUsingAnim(position=(-6,1), mycolor=self.cards[self.cardIdxUsed].color, parent=self.parent, target=(-2, 1), quickDescription=self.cards[self.cardIdxUsed].quickDescription.text)

    def createVisualCard(self, organType=str):
        cardColor = color.rgb(255,255,255)
        match organType:
            case "heart":
                cardColor = color.red
            case "bone":
                cardColor = color.yellow
            case "stomache":
                cardColor = color.lime
            case "brain":
                cardColor = color.cyan
            case _:
                print_on_screen(text="Oops, something went wrong...", origin=(0,0), scale=2, duration=3)
        CardUsingAnim(position=(-6,1), mycolor=cardColor, parent=self.parent, target=(-2, 1))

    #Yeah, copypasta time!
    def update(self):
        for organ in self.infectedOrgans:
            if self.organs[organ] != None:
                self.organs[organ].x = random.randint(498,502)/100 * -1 #I don't know anything like a randfloat so i'll just divide by 100
        
        for organ in self.inmunizedOrgans:
            if self.organs[organ] != None:
                self.organs[organ].scale = (1.2, 1.2)