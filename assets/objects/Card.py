from assets.CubicEngineData import *
from assets.objects.CardUsingAnim import *

class Card(Entity):
    def __init__(self, cardType="organ", organType="heart", x=0, parent=Entity, isvisible=True):
        super().__init__()
        self.parent = parent
        self.cardType = cardType
        self.organType = organType
        self.model = "quad"
        self.scale = (1.2,2)
        self.position = (x, -4)
        self.visible = False
        self.quickDescription = Text(parent=self, scale=(25/1.2, 25/2), text="X", z=-.01, origin=(0,0))
        #So you can't see the opponent cards
        if isvisible:
            self.collider = "box"
            self.visible = True
        #Creating the info text
        self.infoText = Text(parent=self, text="Generic info. Please ignore", origin=(0,0), position=(0,1), scale=(20/1.2, 20/2))
        self.infoText.visible = False
        self.used = False
        #Visuals and that stuff
        if self.organType == "heart":
            self.color = color.red
        if self.organType == "bone":
            self.color = color.yellow
        if self.organType == "stomache":
            self.color = color.lime
        if self.organType == "brain":
            self.color = color.cyan

        self.infoText.text = f"{self.cardType.capitalize()}.\n Can be used on {self.organType}s."
        if self.cardType == "organ":
            self.infoText.text = f"{self.cardType.capitalize()}.\n More specifically a {self.organType}."
        self.on_click = self.useCard
        match self.cardType:
            case "organ":
                self.quickDescription.text = f"{self.organType.capitalize()[0:1]}"
            case "heal":
                self.quickDescription.text = "+"
            case "virus":
                self.quickDescription.text = "-"
            case _:
                pass

    def update(self):
        if self.hovered:
            self.y += (-1.5-self.y)/10
            self.infoText.visible = True
        else:
            self.y += (-2-self.y)/10
            self.infoText.visible = False

    def useCard(self):
        if self.visible:
            CardUsingAnim(position=self.position, mycolor=self.color, parent=self.parent, quickDescription=self.quickDescription.text)
        self.used = True