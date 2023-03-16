from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursina.shaders import basic_lighting_shader
import random
import sys
import math



app = Ursina()

player = FirstPersonController()

window.exit_button.visible = False
window.fullscreen = True
window.borderless = False
window.color = color.rgb(0,181,226)
window.show_ursina_splash = True
window.title = "Minecraft Python Edition"
player.height = 2
player.gravity = 0.5
player.y = 50
block_id = 1
bgmusic = [Audio("assets/music/calm1.ogg", loop=True, autoplay=False),
           Audio("assets/music/calm2.ogg", loop=True, autoplay=False),
           Audio("assets/music/calm3.ogg", loop=True, autoplay=False),
           Audio("assets/music/hal1.ogg", loop=True, autoplay=False),
           Audio("assets/music/hal3.ogg", loop=True, autoplay=False),
           Audio("assets/music/hal4.ogg", loop=True, autoplay=False),
           ]
bgumusic = random.choice(bgmusic)
# bgmusic.autoplay = True
voxels = []
noise = PerlinNoise(octaves=3,seed=random.randint(1,1000000))

blocks = [
    ['hello', "hello", "hello"],
    ["grass", "assets/grass_block_tex.png", load_texture("assets/grass_block_tex.png")],
    ["dirt", "assets/dirt_block_tex.png", load_texture("assets/dirt_block_tex.png")],
    ["stone", "assets/stone_block_tex.png", load_texture("assets/stone_block_tex.png")],
    ["cobblestone", "assets/cobblestone_block_tex.png", load_texture("assets/cobblestone_block_tex.png")],
    ["sand", "assets/sand_block_tex.png", load_texture("assets/sand_block_tex.png")],
    ["oak", "assets/oak_block_tex.png", load_texture("assets/oak_block_tex.png")],
    ["planks", "assets/planks_block_tex.png", load_texture("assets/planks_block_tex.png")],
    ["obsidian", "assets/obsidian_block_tex.png", load_texture("assets/obsidian_block_tex.png")],
    ["ice", "assets/ice_block_tex.png", load_texture("assets/ice_block_tex.png")]
]

def findsoundbasedontexture(blockid,blocklist=blocks):
    if blocklist[blockid][0] in blocklist[blockid][1]:
        sound = Audio(f"assets/sounds/{blocklist[blockid][0]}/{blocklist[blockid][0]}{random.randint(1, 4)}", loop=False, autoplay=False)
        return sound
    
# def whichblockami(block):
#     for eachBlock in blocks:
#         if block.texture in eachBlock[1]:
#             print(eachBlock[0])
        
        
    
def update():
    if held_keys['left mouse down'] or held_keys['right mouse down']:
        # punch_sound.play()
        hand.active()
    else:
        hand.passive()

    if held_keys['escape']:
        sys.exit()
        
    if player.y < -110:
        Audio("assets/sounds/sh/die.ogg")
        player.y = 15
        player.x = 0
        player.z = 0
        Audio("assets/sounds/sh/spawn.ogg")
        
        
class Side(Entity):
    def __init__(self, x, y, z):
        super().__init__(
            parent=scene,
            position=(x, y, z),
            model="quad",
            scale=(16, 1, 16),
            texture=None,

        )


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture="assets/grass_block_tex.png"):
        super().__init__(
            parent=scene,
            position=position,
            model="assets/block",
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=1,
            shader=basic_lighting_shader,
            # block=whichblockami(self)
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                findsoundbasedontexture(blockid=block_id).play()
                Voxel(position=self.position + mouse.normal,
                      texture=blocks[block_id][2])
            if key == 'left mouse down':
                findsoundbasedontexture(blockid=block_id).play()
                destroy(self)

    def create_sides(self, direction, x, y, z):
        if direction == "north":
            plane = Side(x=x+15, y=y, z=z)
            plane.texture = "textures/grass_block_side.png"
        if direction == "south":
            plane = Side(x=x-15, y=y, z=z)
            plane.texture = "textures/grass_block_side.png"
        if direction == "west":
            plane = Side(x=x, y=y, z=z+15)
            plane.texture = "textures/grass_block_side.png"
        if direction == "east":
            plane = Side(x=x, y=y, z=z-15)
            plane.texture = "textures/grass_block_side.png"
        if direction == "up":
            plane = Side(x=x, y=y+15, z=z)
            plane.texture = "textures/grass_block_top.png"
        if direction == "down":
            plane = Side(x=x, y=y-15, z=z)
            plane.texture = "textures/dirt.png"



        


def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        hand.texture = blocks[block_id][2]
        

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/block',
            texture=blocks[block_id][2],
            scale=0.4,
            shader=basic_lighting_shader,
            rotation=Vec3(-10, -10, 10),
            position=Vec2(-0.6, -0.6)
        )

    @staticmethod
    def active():
        hand.position = Vec2(0.4, -0.5)

    @staticmethod
    def passive():
        hand.position = Vec2(0.6, -0.6)

for z in range(-10,10):
    for x in range(-10,10):
        y = noise([x * .02, z * .02])
        y = math.floor(y * 7.5)
        voxel = Voxel(position=(x,y,z))
        # voxels.append(voxel)
        
hand = Hand()

app.run()


