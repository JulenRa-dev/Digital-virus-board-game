from assets.CubicEngineData import *

class CardUsingAnim(Entity):
    def __init__(self, position=(0,-2), mycolor=color.red, parent=Entity, target=(0,1), quickDescription="X"):
        super().__init__()
        self.parent = parent
        self.model = "quad"
        self.scale = (1.2,2)
        self.position = position
        self.color = mycolor
        self.doingAnimation = False
        self.target = target
        self.quickDescription = Text(parent=self, scale=(25/1.2, 25/2), text=quickDescription, z=-.01, origin=(0,0))

    def update(self):
        self.y += (self.target[1]-self.y)/10
        self.x += (self.target[0]-self.x)/10
        if self.y > self.target[1]-.1 and (self.x > self.target[0]-.1 and self.x < self.target[0]+.1) and not self.doingAnimation:
            self.animate_color(color.rgba(self.color.r, self.color.g, self.color.b, 0), duration=1)
            self.quickDescription.animate_color(color.rgba(255, 255, 255, 0), duration=1)
            invoke(lambda: destroy(self), delay=2.5)
            self.doingAnimation = True