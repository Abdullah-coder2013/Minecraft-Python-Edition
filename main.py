from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursina.shaders import lit_with_shadows_shader
import random
import json
import psutil
from ursina.prefabs.panel import Panel

#Initializing Game Object
app = Ursina()

#Creating the Player Object
player = FirstPersonController()
player.height = 2
player.cursor = Entity(parent=camera.ui, model='quad',color=color.light_gray, scale=.008, rotation_z=45)
player.gravity = 1
player.jump_height = 1
player.fall_after = .30
# player.model = "assets/player.obj"
# player.texture = "textures/"

# Window Settings
window.title = "Minecraft Python Edition"
window.exit_button.visible = False
window.fullscreen = True
window.vsync = False
window.borderless = False
window.color = color.rgb(0, 181, 226)
window.show_ursina_splash = True

# Init Variables
terrainblocks = []
button_font = "font/minecraft.ttf"
pressed = False
block_id = 1
bgmusic = [Audio("assets/music/calm1.ogg", loop=True, autoplay=False),
           Audio("assets/music/calm2.ogg", loop=True, autoplay=False),
           Audio("assets/music/calm3.ogg", loop=True, autoplay=False),
           Audio("assets/music/hal1.ogg", loop=True, autoplay=False),
           Audio("assets/music/hal3.ogg", loop=True, autoplay=False),
           Audio("assets/music/hal4.ogg", loop=True, autoplay=False),
           ]
bgumusic = random.choice(bgmusic)
bgumusic.play()
noise = PerlinNoise(octaves=3,seed=random.randint(1,1000000))
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

# Variables for F3 debug screen
debugscreen = Entity(model=None, parent=camera.ui)
debugscreen.visible = False
coordinates = Text(position=Vec3(-.87, 0.44, 0),
                   font=button_font, parent=debugscreen)
cpu_panel = Text(position=Vec3(-.87, 0.40, 0),
                 parent=debugscreen, font=button_font)

#Importing Json
with open("configuration.json", "r") as configuration:
    data = json.load(configuration)
    trees = data["trees"]
    inventory = data["showInventory"]
    sounds = data["sounds"]
    directionalshaders = data["directionalShaders"]
    treesCount = data["treesCount"]
    fps_counter_enabled = data["fps_counter_enabled"]
    parkour = data["parkour_mode"]
    landsize = data["land_size"]
    world_type = data["world_type"]
    
if fps_counter_enabled == False:
    window.fps_counter = False

#----------------------------------------------Function Space---------------------------------------------------

#Defining Tree Structure
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

def genTrees():
    for tree in range(treesCount):
        chosenblock = random.choice(terrainblocks)
        # terrainblocks.remove(chosenblock)
        randomcoordinates = (chosenblock.x,chosenblock.z,chosenblock.y)
        plantTree(_x=randomcoordinates[0], _z=randomcoordinates[1], _y=randomcoordinates[2]+1)

# Finding about the blocks
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


# Sneaking           
def sneak():
    player.scale_y  = 0.90
    player.speed = 1
    
# Sprinting
def sprint():
    camera.fov = 100
    player.speed = 10
    player.jumping = True
    
# Zooming
def zoom():
    camera.fov = 70

# Default Function
def default():
    player.speed = 5
    camera.fov = 90
    player.scale_y = 1
            
#------------------------------------End of Function Space-------------------------------------------

# Task Update  
def update():
    global inventorytrue, pressed, items
    if held_keys['left mouse down'] or held_keys['right mouse down']:
        # punch_sound.play()
        hand.active()
    else:
        hand.passive()
    
    if held_keys["shift"]:
        sneak()
        
    elif held_keys["control"] and held_keys["w"]:
        sprint()
    
    elif held_keys["c"]:
        zoom()
        
    else:
        default()

    if held_keys['escape']:
        sys.exit()
        
    if held_keys['f3']:
        if pressed == False:
            debugscreen.visible = True
            pressed = True
        elif pressed == True:
            debugscreen.visible = False
            pressed = False
        
    selected.adjust_position()
        
    if held_keys["t"]:
        plantTree(round(player.x), round(player.y), round(player.z))
        
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    coordinates.text = f'Position: {round(player.x)},{round(player.y)},{round(player.z)}'
    pid = os.getpid()
    python_process = psutil.Process(pid)
    memoryUse = python_process.memory_info()[0]/2.**30

    cpu_panel.text = f'CPU: {cpu}% / RAM: {ram}% / Memory use: {round(memoryUse,2)} GB'
    
    if player.y < -100:
        Audio("assets/sounds/sh/die.ogg")
        player.y = 15
        player.x = 0
        player.z = 0
        Audio("assets/sounds/sh/spawn.ogg")
        
    # if player.y < -100:
    #     Audio("assets/sounds/sh/die.ogg")
    #     application.pause()
    #     o.visible = True
    #     dietext.visible = True
    #     items = False
    #     hotbar.destroyItems()
    #     hotbar.visible = False
    #     hand.visible = False
    #     selected.visible = False
    #     respawn_button = RespawnButton()
    #     respawn_button.text_entity.font = button_font
    #     mouse.locked = False

# Defining Voxel
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
            shader=lit_with_shadows_shader
        )
        
        self.block = whichblockami(self)

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                if sounds == True:
                   findsoundbasedontexture(blockid=block_id,mode="default",block=self.block).play()
                voxel = Voxel(position=self.position + mouse.normal,
                      texture=blocks[block_id][2])
                terrainblocks.append(voxel)
            if key == 'left mouse down':
                if sounds == True:
                    findsoundbasedontexture(blockid=block_id,mode="already",block=self.block).play()
                destroy(self)
                
# Changing hand texture
def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        hand.texture = blocks[block_id][2]
        
# Death Screen
o = Panel(scale=4, color=color.rgba(255, 0, 0, 200))
o.visible = False
items = True
dietext = Text(font=button_font, text="You Died!",
               position=Vec2(-0.1, 0.2), color=color.white, scale=2)
dietext.visible = False
class RespawnButton(Button):
    def __init__(self):
        super().__init__(
            text="Respawn", 
            parent=camera.ui, 
            model="quad",
            texture="textures/widgets/button.png", 
            color=color.color(0, 0, random.uniform(0.9, 1)), 
            scale=(0.5, 0.1)
        )
        
    def input(self, key):
        if self.hovered:
            self.texture = "textures/widgets/button_selected.png"
            if key == "left mouse down":
                dietext.visible = False
                application.resume()
                player.y = 15
                player.x = 0
                player.z = 0
                Audio("assets/sounds/sh/spawn.ogg")
                destroy(self)
        
# Defining Hand
class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/block',
            texture=blocks[block_id][2],
            scale=0.3,
            shader=lit_with_shadows_shader,
            rotation=Vec3(-10, -10, 10),
            position=Vec2(-0.6, -0.6)
        )

    @staticmethod
    def active():
        hand.position = Vec2(0.4, -0.5)

    @staticmethod
    def passive():
        hand.position = Vec2(0.6, -0.6)
        
#----------------------------------------------Inventory Zone-----------------------------------------

class Item(Entity):
    def __init__(self,texture,position=(0,-0.42)):
        super().__init__(
            parent=camera.ui,
            model="assets/block",
            texture=texture,
            scale=0.04,
            position=Vec2(position),
            rotation=Vec3(-10,-35,-10),
            shader=lit_with_shadows_shader,
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
        if block_id == 1:
            self.position = Vec2(-0.35,-0.4)
        if block_id == 2:
            self.position = Vec2(-0.26, -0.4)
        if block_id == 3:
            self.position = Vec2(-0.17, -0.4)
        if block_id == 4:
            self.position = Vec2(-0.08, -0.4)
        if block_id == 5:
            self.position = Vec2(0, -0.4)
        if block_id == 6:
            self.position = Vec2(0.08, -0.4)
        if block_id == 7:
            self.position = Vec2(0.17, -0.4)
        if block_id == 8:
            self.position = Vec2(0.26, -0.4)
        if block_id == 9:
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
        self.grass = Item(blocks[1][2],(-0.35,-0.42))
        self.dirt = Item(blocks[2][2],(-0.26,-0.42))
        self.stone = Item(blocks[3][2],(-0.17, -0.42))
        self.cobblestone = Item(blocks[4][2],(-0.08,-0.42))
        self.sand = Item(blocks[5][2],(0,-0.42))
        self.oak = Item(blocks[6][2],(0.08,-0.42))
        self.planks = Item(blocks[7][2],(0.17,-0.42))
        self.obsidian = Item(blocks[8][2], (0.26, -0.42))
        self.ice = Item(blocks[9][2], (0.35, -0.42))

    def destroyItems(self):
        if items == False:
            self.grass.visible = False
            self.dirt.visible = False
            self.stone.visible = False
            self.cobblestone.visible = False
            self.sand.visible = False
            self.oak.visible = False
            self.planks.visible = False
            self.obsidian.visible = False
            self.ice.visible = False
#-------------------------------------End of Inventory Zone-------------------------------------------

# Terrain Generation
terrainWidth = landsize
freq = 24
if parkour == True:
    amp = 100
else:
    amp = 5
    
if world_type == "super_flat":
    amp = 0
else:
    amp = 5
for i in range(terrainWidth*terrainWidth):
    voxel = Voxel(texture=blocks[1][2])
    voxel.x = floor(i/terrainWidth)
    voxel.z = floor(i % terrainWidth)
    voxel.y = floor((noise([voxel.x/freq, voxel.z/freq]))*amp)
    # voxel.parent = terrain
    terrainblocks.append(voxel)

if trees == True:
    genTrees()
       
if directionalshaders == True:
    DirectionalLight(parent=Voxel, y=2, z=3, shadows=True)

hand = Hand()
hotbar = Hotbar()
selected = Selected()
hotbar.appendItems()
app.run()