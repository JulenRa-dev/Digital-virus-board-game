from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

def randomCol():
    return random.randint(0,255)

def prefabWorld(tilesTexture="grass"):
    worldTiles = []
    important = {}
    worldMesh = {}
    for x in range(20):
        for z in range(20):
            bud = Entity(model="plane",texture=tilesTexture,x=x,z=z,collider="box")
            worldTiles.append(bud)
    bud = FirstPersonController(x=10,y=1,z=10,collider="box")
    important["player"] = bud
    worldMesh = {"worldTiles": worldTiles,"important": important}
    return worldMesh

class CubicEntity(Entity):
    '''
    This instances a entity with physics functions
    and some other usefull stuff

    Functions:
    applyXForce(force) default force: 0
    applyYForce(force) default force: 0
    applyZForce(force) default force: 0
    '''
    def __init__(self, model=None, position=(0,0,0), texture=None, rotation=(0,0,0)):
        super().__init__()
        self.position = position
        self.model = model
        self.texture = texture
        self.rotation = rotation
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0

    def applyXForce(self,force=0):
        self.speed_x += 0.9 * force
        self.speed_x = 0.9 * self.speed_x
        self.x += self.speed_x
    
    def applyYForce(self,force=0):
        self.speed_y += 0.9 * force
        self.speed_y = 0.9 * self.speed_y
        self.y += self.speed_y

    def applyZForce(self,force=0):
        self.speed_z += 0.9 * force
        self.speed_z = 0.9 * self.speed_z
        self.z += self.speed_z

class Platformer2dController(CubicEntity):
    def __init__(self, position=(0,0,0), texture=None, model=None, collider="box"):
        super().__init__(
            position = position,
            texture = texture,
            model = model,
            collider = collider,
            jumpForce = 150,
            colliderZone = scene,
            gravity = -2.98,
            speed = 1,
        )
    def input(self, key):
        if key == "space":
            self.applyYForce(force=self.jumpForce)
    
    def update(self):
        ground = raycast(origin=self.position,direction=self.down,traverse_target=self.colliderZone,distance=.5,debug=False)
        if not ground.hit:
            self.applyYForce(force=self.gravity)

        self.applyXForce(force=held_keys["d"]-held_keys["a"]*self.speed)