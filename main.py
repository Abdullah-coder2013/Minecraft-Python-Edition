from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursina.shaders import basic_lighting_shader
import random
import sys
import math
import json
from ursina.prefabs.panel import Panel



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
# player.model = "assets/player.obj"
# player.texture = "textures/"
terrainblocks = []
player.scale = 1
player.y = 50
block_id = 1
o = Panel(scale=5)
o.visible = False
inventorytrue = "i"
bgmusic = [Audio("assets/music/calm1.ogg", loop=True, autoplay=False),
           Audio("assets/music/calm2.ogg", loop=True, autoplay=False),
           Audio("assets/music/calm3.ogg", loop=True, autoplay=False),
           Audio("assets/music/hal1.ogg", loop=True, autoplay=False),
           Audio("assets/music/hal3.ogg", loop=True, autoplay=False),
           Audio("assets/music/hal4.ogg", loop=True, autoplay=False),
           ]
bgumusic = random.choice(bgmusic)
bgumusic.play()
# bgmusic.autoplay = True
voxels = []
noise = PerlinNoise(octaves=3,seed=random.randint(1,1000000))

terrain = Entity(model=None,collider=None)

blocks = [
    ['leaves', "assets/leaves_block_tex.png", load_texture("assets/leaves_block_tex.png")],
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

with open("configuration.json", "r") as configuration:
    data = json.load(configuration)
    trees = data["trees"]
    inventory = data["showInventory"]
    sounds = data["sounds"]
    directionalshaders = data["directionalShaders"]
    treesCount = data["treesCount"]
    fps_counter_enabled = data["fps_counter_enabled"]
    
if fps_counter_enabled == False:
    window.fps_counter = False

def trunk(parent):
    for __z in range(1):
        for __x in range(1):
            for __y in range(3):
                voxel = Voxel(position=(__x, __y - 3, __z), texture=blocks[6][2])
                voxel.parent = parent

    for ___z in range(5):
        for ___x in range(5):
            for ___y in range(2):
                voxel = Voxel(position=(___x - 2, ___y, ___z - 2),
                              texture='assets/leaves_block_tex.png')
                voxel.parent = parent
                
    for ____z in range(3):
        for ____x in range(3):
            for ____y in range(2):
                voxel = Voxel(position=(____x - 1, ____y+2, ____z - 1),
                              texture='assets/leaves_block_tex.png')
                voxel.parent = parent

def plantTree(_x, _y, _z):
    tree = Entity(model=None, position=Vec3(_x, _y, _z))
    trunk(tree)
    tree.y = 3


def checkTree(_x, _y, _z):
    freq = 3
    amp = 80
    treeChance = ((noise([_x / freq, _z / freq])) * amp)
    if treeChance > 38:
        plantTree(_x, _y, _z)


def genTrees():
    for tree in range(treesCount):
        chosenblock = random.choice(terrainblocks)
        # terrainblocks.remove(chosenblock)
        randomcoordinates = (chosenblock.x,chosenblock.z,chosenblock.y)
        plantTree(_x=randomcoordinates[0], _z=randomcoordinates[1], _y=randomcoordinates[2]+1)

def findsoundbasedontexture(blockid, mode, block, blocklist=blocks):
    if mode == "default":
        if blocklist[blockid][0] in blocklist[blockid][1]:
            sound = Audio(f"assets/sounds/{blocklist[blockid][0]}/{blocklist[blockid][0]}{random.randint(1, 4)}", loop=False, autoplay=False)
            return sound
    elif mode == "already":
        for blockk in blocklist:
            if blockk[0] == block:
                soundd = Audio(f"assets/sounds/{block}/{block}{random.randint(1,4)}", loop=False, autoplay=False)
                return soundd
    
def whichblockami(block):
    for eachBlock in blocks:
        try:
            if f"assets/{block.texture.name}" in eachBlock[1]:
                print(eachBlock[0])
                return eachBlock[0]
        
        except:
            print(f"No texture on index")   
    
def update():
    global inventorytrue
    if held_keys['left mouse down'] or held_keys['right mouse down']:
        # punch_sound.play()
        hand.active()
    else:
        hand.passive()

    # if held_keys["e"]:
    #     application.pause()
    #     o.visible = True
    #     inventory.visible = True
    #     inventory.addslots()
    #     mouse.locked = False
    #     mouse.visible = True
    #     # inventorytrue = "o"
    if held_keys['escape']:
        sys.exit()
        
    selected.adjust_position()
        
    if held_keys["t"]:
        plantTree(round(player.x), round(player.y), round(player.z))
        
    if player.y < -100:
        Audio("assets/sounds/sh/die.ogg")
        player.y = 15
        player.x = 0
        player.z = 0
        Audio("assets/sounds/sh/spawn.ogg")

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture="assets/grass_block_tex.png", **kwargs):
        super().__init__(
            parent=scene,
            position=position,
            model="assets/block",
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=1,
            shader=basic_lighting_shader
        )
        
        self.block = whichblockami(self)

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                if sounds == True:
                   findsoundbasedontexture(blockid=block_id,mode="default",block=self.block).play()
                Voxel(position=self.position + mouse.normal,
                      texture=blocks[block_id][2])
            if key == 'left mouse down':
                if sounds is True:
                    findsoundbasedontexture(blockid=block_id,mode="already",block=self.block).play()
                destroy(self)
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
            scale=0.3,
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
        

class Item(Entity):
    def __init__(self,texture,position=(0,-0.42)):
        super().__init__(
            parent=camera.ui,
            model="assets/block",
            texture=texture,
            scale=0.04,
            position=Vec2(position),
            rotation=Vec3(-10,-35,-10),
            shader=basic_lighting_shader,
        )
        
class Selected(Entity):
    def __init__(self, position=(0, -0.4)):
        super().__init__(
            parent=camera.ui,
            model="quad",
            texture="textures/widgets/selected.png",
            scale=0.1,
            position=Vec2(position),
            # rotation=Vec3(-10, -35, -10),
            # shader=basic_lighting_shader,
        )
    
    def adjust_position(self):
        if block_id is 1:
            self.position = Vec2(-0.35,-0.4)
        if block_id is 2:
            self.position = Vec2(-0.26, -0.4)
        if block_id is 3:
            self.position = Vec2(-0.17, -0.4)
        if block_id is 4:
            self.position = Vec2(-0.08, -0.4)
        if block_id is 5:
            self.position = Vec2(0, -0.4)
        if block_id is 6:
            self.position = Vec2(0.08, -0.4)
        if block_id is 7:
            self.position = Vec2(0.17, -0.4)
        if block_id is 8:
            self.position = Vec2(0.26, -0.4)
        if block_id is 9:
            self.position = Vec2(0.35, -0.4)
        

class Hotbar(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='quad',
            scale=(0.8, 0.10, 0),
            position=Vec2(0, -0.4),
            texture='textures/widgets/hotbar.png'
        )
        
    def appendItems(self):
        grass = Item(blocks[1][2],(-0.35,-0.42))
        dirt = Item(blocks[2][2],(-0.26,-0.42))
        stone = Item(blocks[3][2],(-0.17, -0.42))
        cobblestone = Item(blocks[4][2],(-0.08,-0.42))
        sand = Item(blocks[5][2],(0,-0.42))
        oak = Item(blocks[6][2],(0.08,-0.42))
        planks = Item(blocks[7][2],(0.17,-0.42))
        obsidian = Item(blocks[8][2], (0.26, -0.42))
        ice = Item(blocks[9][2], (0.35, -0.42))

# for z in range(-20,20):
#     for x in range(-20,20):
#         y = noise([x * .02, z * .02])
#         y = math.floor(y * 7.5)
#         voxel = Voxel(position=(x,y,z))
#         voxel.texture = blocks[1][2]
#         voxel.parent = terrain
#         terrainblocks.append(voxel)
terrainWidth = 25
freq = 24
amp = 6
for i in range(terrainWidth*terrainWidth):
    voxel = Voxel(texture=blocks[1][2])
    voxel.x = floor(i/terrainWidth)
    voxel.z = floor(i % terrainWidth)
    voxel.y = floor((noise([voxel.x/freq, voxel.z/freq]))*amp)
    terrainblocks.append(voxel)
    
# for b in range(1):
# 	for i in range(terrainWidth*terrainWidth):
# 		voxel = Voxel(texture=blocks[2][2])
# 		voxel.x = floor(i/terrainWidth)
# 		voxel.z = floor(i % terrainWidth)
# 		voxel.y = floor(((noise([voxel.x/freq, voxel.z/freq]))*amp)-(b+1))
  
# for d in range(1):
# 	for i in range(terrainWidth*terrainWidth):
# 		voxel = Voxel(texture=blocks[3][2])
# 		voxel.x = floor(i/terrainWidth)
# 		voxel.z = floor(i % terrainWidth)
# 		voxel.y = floor(((noise([voxel.x/freq, voxel.z/freq]))*amp)-(d+2))

if trees is True:
    genTrees()
      
terrain.combine()
print("Mesh combined successfully")
terrain.collider = 'mesh'
terrain.texture = blocks[1][2]
        
if directionalshaders == True:
    DirectionalLight(parent=Voxel, y=2, z=3, shadows=True)

if inventory is True:
    hotbar = Hotbar()
    hotbar.appendItems()
    selected = Selected()
    # inventory = Inventory()
    # inventory.visible = False
    inventorytrue = "i"
hand = Hand()
# chunk = combine(terrainblocks)
app.run()