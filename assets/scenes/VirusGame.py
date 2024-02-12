from assets.CubicEngineData import *
from assets.objects.GameScene import *
from assets.objects.Card import *
from assets.objects.GenericVirusGame import *
from assets.objects.OpponentAi import *

class VirusGame(GameScene):
    def __init__(self, saves=..., ram=...):
        super().__init__(saves, ram)
        #Some ram setup
        self.ram["winner"] = "nobody"
        self.ram["moves"] = 0
        #Player setup
        self.cards = []
        self.giveRandomCard(-2, target=self)
        self.giveRandomCard(0, target=self)
        self.giveRandomCard(2, target=self)
        #More player setup, specifically the internal one
        self.organs = {"heart": None, "bone": None, "stomache": None, "brain": None}
        self.infectedOrgans = []
        self.inmunizedOrgans = []
        self.protectedOrgans = []
        self.cardsAreVisible = True
        #Opponent setup
        self.opponent = OpponentAi(parent=self)
        self.giveRandomCard(0, target=self.opponent, visibility=False)
        self.giveRandomCard(0, target=self.opponent, visibility=False)
        self.giveRandomCard(0, target=self.opponent, visibility=False)
        #Moves counter
        self.moves = 0
        self.movesCounterText = Text(parent=self, text="Moves: 0", position=(0,3), scale=(20,20), origin=(0,0), visible=False)

    def update(self):
        index = 0
        #Looks every card and checks if it has been used, if so, applies it
        for card in self.cards:
            if card.used:
                #Updates the moves counter
                self.moves += 1
                self.movesCounterText.text = f"Moves: {self.moves}"
                self.applyCardEffects(card, index, target=self)
                self.opponent.step(self.organs)
                self.applyCardEffects(self.opponent.cards[self.opponent.cardIdxUsed], target=self.opponent, isplayer=False)
            index += 1
        
        #Shaking visuals for infected organs
        for organ in self.infectedOrgans:
            if self.organs[organ] != None:
                self.organs[organ].x = random.randint(498,502)/100 #I don't know anything like a randfloat so i'll just divide by 100
        
        #Visuals for inmunized organs
        for organ in self.inmunizedOrgans:
            if self.organs[organ] != None:
                self.organs[organ].scale = (1.2, 1.2)

    def applyCardEffects(self, card=Card, index=0, target=GenericVirusGame(), isplayer=True):
        #Checks if you are the player for a silly reason
        if isplayer:
            pleaseDontCrash = self.cards[index].x
        else:
            pleaseDontCrash = 0

        #Calls function depending on the card type
        if card.cardType == "organ":
            #Adds organ if the target doesn't have it yet
            if target.organs[card.organType] == None:
                target.organs[card.organType] = Entity(parent=target, model="quad", color=card.color)
            #Places the organ visually
            target.placeOrgan(card.organType)
        if card.cardType == "heal":
            self.healOrgan(organType=card.organType, target=target, isplayer=isplayer)
        if card.cardType == "virus":
            if isplayer:
                self.infectOrgan(card.organType, target=self.opponent)
            else:
                self.infectOrgan(card.organType, target=self)
        #Stuff that does after using any card, such as checking if you won, removing the card from your inventory and giving you another
        self.checkIfWon()
        if self.ram["winner"] == "nobody":
            invoke(lambda: self.giveRandomCard(pleaseDontCrash, target=target, visibility=isplayer), delay=1)
        target.cards.pop(index)
        destroy(card)

    def checkIfWon(self):
        existing = 0
        #Looks at all organs, checking if they are infected or they exist
        for organ in self.organs.items():
            if organ[1] != None and organ[0] not in self.infectedOrgans:
                existing += 1
        #If the four organs pass the check, you win!
        if existing == 4:
            self.ram["winner"] = "player"
            self.ram["moves"] = self.moves
            self.changeToScene = "endScreen"
            return

        #Checking if the opponent won
        existing = 0
        for organ in self.opponent.organs.items():
            if organ[1] != None and organ[0] not in self.opponent.infectedOrgans:
                existing += 1
        #Again, four organs pass the test, it wins
        if existing == 4:
            self.ram["winner"] = "opponent"
            self.ram["moves"] = self.moves
            self.changeToScene = "endScreen"

    def placeOrgan(self, organType=str):
        #Nothing to say about
        if organType == "heart":
            self.organs[organType].position = (5, 3)
        if organType == "stomache":
            self.organs[organType].position = (5, 1)
        if organType == "bone":
            self.organs[organType].position = (5, -1)
        if organType == "brain":
            self.organs[organType].position = (5, -3)

    def giveRandomCard(self, cardx=0, target=GenericVirusGame(), visibility=True):
        #Making a list of the organs, you can edit it if you want, you will just have to add a few stuff on the "Card" class
        possibleOrgans = ["heart", "stomache", "bone", "brain"]
        #And these are the card types. Of course you will have to add a behaviour if you add more card types. A card without a behaviour will just be discarded
        possibleTypes = ["organ", "virus", "heal"]
        #Chooses a organ and a card type from the previous lists
        selectedOrgan = possibleOrgans[random.randint(0,len(possibleOrgans)-1)]
        selectedType = possibleTypes[random.randint(0,len(possibleTypes)-1)]
        if self.ram["winner"] == "nobody":
            target.cards.append(Card(cardType=selectedType, organType=selectedOrgan, x=cardx, parent=self, isvisible=visibility))

    def healOrgan(self, organType=str, target=GenericVirusGame(), isplayer=True):
        #Sorry for this messy code, i didn't knew the list.index function
        index = 0
        for organ in target.infectedOrgans:
            if organ == organType:
                target.infectedOrgans.pop(index)
                if isplayer:
                    target.organs[organType].x = 5
                else:
                    target.organs[organType].x = -5
                return
            index += 1
        #This code inmunizes and protects the organs. I don't think you need to change anything from here
        if target.organs[organType] != None:
            if organType in target.protectedOrgans and not organType in target.inmunizedOrgans:
                target.protectedOrgans.pop(target.protectedOrgans.index(organType))
                target.inmunizedOrgans.append(organType)
            elif not organType in self.inmunizedOrgans:
                target.protectedOrgans.append(organType)
                target.organs[organType].rotation_z = 45

    def infectOrgan(self, organType=str, target=GenericVirusGame()):
        #This is what happens when your opponent uses a virus against you
        if target.organs[organType] != None:
            #If the organ is infected
            if organType in target.infectedOrgans:
                destroy(target.organs[organType])
                target.organs[organType] = None
                target.infectedOrgans.pop(target.infectedOrgans.index(organType))
            #If the target isn't inmunized
            elif not organType in target.inmunizedOrgans:
                #If the organ is protected
                if organType in target.protectedOrgans:
                    target.protectedOrgans.pop(target.protectedOrgans.index(organType))
                    target.organs[organType].rotation_z = 90
                #If the organ just exists
                else:
                    target.infectedOrgans.append(organType)

    def input(self, key):
        #Debug keys
        if key == "f":
            self.ram["winner"] = "debug"
            self.changeToScene = "endScreen"
        if key == "r":
            print_on_screen(text="Player cards re-sorted", origin=(0,0), scale=2)
            for card in self.cards:
                destroy(card)
            self.cards = []
            self.giveRandomCard(-2, target=self)
            self.giveRandomCard(0, target=self)
            self.giveRandomCard(2, target=self)
        if key == "h":
            print_on_screen(text="Healed all organs", origin=(0,0), scale=2)
            for organ in self.organs.items():
                if organ[1] != None:
                    self.healOrgan(organType=organ[0], target=self, isplayer=True)
        if key == "m":
            print_on_screen(text="Activated moves counter", origin=(0,0), scale=2)
            self.movesCounterText.visible = True