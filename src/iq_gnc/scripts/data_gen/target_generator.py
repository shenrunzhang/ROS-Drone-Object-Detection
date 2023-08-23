from PIL import Image, ImageDraw, ImageFont,ImageFilter
import random
import numpy as np
from skimage import util
import os
import math
import argparse
from math import * 

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument('-a','--all', action="store_true", help="generate all shapes")
group.add_argument('-s','--shape',type=str, help= "what shape to generate?")
parser.add_argument('-n','--num_pics', type=int, default=500, help="how many pics per shape to generate?")
parser.add_argument('-bp', '--background_path', type=str,default="vision/texture_concrete.jpg",
                    help="image for background")
parser.add_argument('-sp','--save_path',type=str, default="training_data", help="path to folder where data will be saved")
parser.add_argument('--final_pic_size', type=int, default=120, help="size of images to be generated")
parser.add_argument('-b','--blur',type=float, default=2.5, help="how much to blur shape")
parser.add_argument('--block_size',type=int, default=60, 
                    help="(leave this) size of individual blocks of background img to randomly shuffle")
parser.add_argument('--num_blocks', type=int, default=2, 
                    help="(leave this) the num of blocks of background img that will fit along the side of the final image")
parser.add_argument('-ss', '--shape_scale', type=float, default=1, help= "(leave this) how much to scale the size if the shape. Set to \
    < 1 to shrink the shape relative to the image, and > 1 to increase the shape size. Default is 1.")

args = parser.parse_args()



# Functions randomPatch & quilt for background texture generation
def randomPatch(texture, block_size=0):
    h, w, _ = texture.shape

    i = np.random.randint(0,h - block_size)
    j = np.random.randint(0,w - block_size)

    return texture[i:i+block_size, j:j+block_size]

def quilt(image_path, block_size, num_block, final_block_size):
    texture = Image.open(image_path)
    texture = util.img_as_float(texture)
    
    # crops out a random patch from larger image to do random shuffling
    h, w, _ = texture.shape    
    i = np.random.randint(h-final_block_size)
    j = np.random.randint(w-final_block_size)
    texture = texture[i:i+final_block_size, j:j+final_block_size]
    

    overlap = block_size // 6
    num_blockHigh, num_blockWide = num_block

    h = (num_blockHigh * block_size) - (num_blockHigh - 1) * overlap
    w = (num_blockWide * block_size) - (num_blockWide - 1) * overlap

    res = np.zeros((h, w, texture.shape[2]))

    for i in range(num_blockHigh):
        for j in range(num_blockWide):            
            y = i * (block_size - overlap)
            x = j * (block_size - overlap)
            patch = randomPatch(texture, block_size)
            res[y:y+block_size, x:x+block_size] = patch

    image = Image.fromarray((res * 255).astype(np.uint8))
    
    image = image.resize((final_block_size,final_block_size))
    return image

# Generate a number of random shapes
# SAVE_PATH refers to the higher directory in which all generated images will be stored
def generate_shape(shape: str, num_pics: int, BACKGROUND_PATH="vision/modules/texture_original.jpg", SAVE_PATH="training_data",
                   final_pic_size=120, shape_blur=2.5, block_size=60, num_blocks=2, shape_scale= 1):
    shape_function = shape
    SAVE_PATH = SAVE_PATH + "/shapes/" + shape_function
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    block_size = block_size
    num_blocks = num_blocks
    final_block_size = final_pic_size
    num_pics = num_pics
    blur = shape_blur

    # Font for text
    font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', int(20 * sqrt(shape_scale)))

    width, height = final_block_size, final_block_size

    # Generating random attributes    
    def randLetter():
        return random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

    def randomColor():
        return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    def randomCoords():
        return (random.randint(int(width * 0.40), int(width * 0.60)), random.randint(int(height * 0.40), int(height * 0.60)))

    def randomCircle():
        return (randomCoords(), int(random.randint(30,35) * shape_scale))

    # Functions for drawing shapes 
    def drawCircle():
        x, y = randomCoords()
        
        r = int(random.randint(25,35) * shape_scale)
        coordinates = [(x - r, y - r), (x + r, y + r)]
        draw.ellipse(coordinates, fill = randomColor())
        draw.text((x-7,y-10),randLetter(), font=font)
        return
    
    def drawTriangle():
        (x, y), r = randomCircle()
        draw.regular_polygon(((x,y),r), n_sides = 3, fill=randomColor(),
                            rotation=random.randint(0,180))
        
        draw.text((x-7,y-10),randLetter(), font=font)
        return
    
    def drawSquare():
        (x, y), r = randomCircle()
        draw.regular_polygon(((x,y),r), n_sides=4, fill=randomColor(),
                            rotation=random.randint(0,180))
        
        draw.text((x-7,y-10),randLetter(), font=font)
        return
    
    def drawPentagon():
        (x, y), r = randomCircle()
        draw.regular_polygon(((x,y),r), n_sides=5, fill=randomColor(),
                            rotation=random.randint(0,180))
        
        draw.text((x-7,y-10),randLetter(), font=font)
        return
    
    def drawHexagon():
        (x, y), r = randomCircle()
        draw.regular_polygon(((x,y),r), n_sides=6, fill=randomColor(),
                            rotation=random.randint(0,180))
        
        draw.text((x-7,y-10),randLetter(), font=font)
        return
    
    def drawHeptagon():
        (x, y), r = randomCircle()
        draw.regular_polygon(((x,y),r), n_sides=7, fill=randomColor(),
                            rotation=random.randint(0,180))
        
        draw.text((x-7,y-10),randLetter(), font=font)
        return
    
    def drawOctagon():
        (x, y), r = randomCircle()
        draw.regular_polygon(((x,y),r), n_sides=8, fill=randomColor(),
                            rotation=random.randint(0,180))
        
        draw.text((x-7,y-10),randLetter(), font=font)
        return
    
    def drawSemicircle():
        x, y = randomCoords()
        r = int(random.randint(25,30) * shape_scale)
        y -= r // 2
        coordinates = [(x - r, y - r), (x + r, y + r)]
        draw.pieslice(coordinates, start =0, end=180, fill = randomColor())
        draw.text((x-7,y), randLetter(), font=font)
        return
    
    def drawQuartercircle():
        x, y = randomCoords()
        
        r = int(random.randint(40,50) * shape_scale)
        x -= r // 2
        y -= r // 2
        coordinates = [(x - r, y - r), (x + r, y + r)]
        draw.pieslice(coordinates, start =0, end=90, fill = randomColor())
        draw.text((x + 7,y + 3), randLetter(), font=font)
        return
    
    def drawTrapezoid():
        x, y = randomCoords()
        randomUpperHeight =int(random.randint(10,15) * shape_scale)
        randomLowerHeight =int(random.randint(15,25) * shape_scale)
        randomUpperWidth = int((random.randint(30,35) // 2) * shape_scale)
        randomLowerWidth = int((random.randint(45,55) // 2) * shape_scale)
        
        coordinates = [(x-randomLowerWidth, y-randomLowerHeight),
                    (x+randomLowerWidth, y-randomLowerHeight),
                    (x+randomUpperWidth, y+randomUpperHeight),
                    (x-randomUpperWidth, y+randomUpperHeight)]
        draw.polygon(coordinates, fill=randomColor())
        draw.text((x-7,y-10),randLetter(), font=font)
        return

    def drawStar():
        num_points = 5
        x, y = randomCoords()
        outer_angles = [2*math.pi*i/num_points for i in range(num_points)]
        inner_angles = [2*math.pi*i/num_points + 2*math.pi/2/num_points for i in range(num_points)]
        
        r = int(random.randint(10,15) * shape_scale)
        R = int(random.randint(30,40) * shape_scale)
        
        list_vertices = []
        for i in range(num_points):
            list_vertices.append((R*math.cos(outer_angles[i]), R*math.sin(outer_angles[i])))
            list_vertices.append((r*math.cos(inner_angles[i]), r*math.sin(inner_angles[i])))
        
        list_vertices = [(int(x_coord + x), int(y_coord + y)) for (x_coord, y_coord) in list_vertices]
        draw.polygon(list_vertices, fill=randomColor())
        draw.text((x-7,y-10),randLetter(), font=font)
        return

    def drawCross():    
        x, y = randomCoords()
        
        long = int(random.randint(30, 35) * shape_scale)
        short =int(random.randint(7,12) * shape_scale)
        
        coords_1 = [(x-short, y-long), (x+short, y+long)]
        coords_2 = [(x-long, y-short), (x+long, y+short)]
        color = randomColor()
        draw.rectangle(coords_1, fill=color)
        draw.rectangle(coords_2, fill=color)    
        draw.text((x-7,y-10),randLetter(), font=font)
        return

    def drawRectangle():
        
        x, y = randomCoords()
        
        long =  int(random.randint(30, 35) * shape_scale)
        short = int(random.randint(10,15) * shape_scale)
        
        coords_1 = [(x-short, y-long), (x+short, y+long)]
        color = randomColor()
        draw.rectangle(coords_1, fill=color)
        
        draw.text((x-7,y-10),randLetter(), font=font)
        return
        

    shapes = {"circle": drawCircle, "triangle": drawTriangle, "square": drawSquare,
            "pentagon": drawPentagon, "hexagon": drawHexagon, "heptagon": drawHeptagon, 
            "octagon": drawOctagon, "semicircle": drawSemicircle, 
            "quartercircle": drawQuartercircle, "trapezoid": drawTrapezoid, "star": drawStar,
            "cross": drawCross, "rectangle": drawRectangle}

    for pic in range(num_pics):
        # Generates new background
        img = quilt(BACKGROUND_PATH, block_size, (num_blocks,num_blocks), final_block_size)
        
        # Load a blank transparent image to draw shape
        target = Image.new('RGBa', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(target)
        
        # Draws shape
        shapes[shape_function]()

        # Adds random rotation
        target=target.rotate(random.randint(0,180))
        
        # Blurs shape
        target = target.filter(ImageFilter.GaussianBlur(blur)).convert("RGBA")

        # Pastes shape onto background
        img.paste(target, (0,0), mask=target)
        
        # Saves image
        filename = SAVE_PATH + "/" + shape_function + str(pic) + ".jpg"
        
        img.save(filename)
    print("Finish generating new " + shape + " images at " + SAVE_PATH)

all_shapes = ["circle", "triangle", "square",
            "pentagon", "hexagon", "heptagon", 
            "octagon", "semicircle", 
            "quartercircle", "trapezoid", "star",
            "cross", "rectangle"]

# Functionalities for argsparse
if args.all:
    for shape in all_shapes:
        generate_shape(shape, num_pics=args.num_pics, BACKGROUND_PATH= args.background_path,
                       SAVE_PATH=args.save_path, final_pic_size=args.final_pic_size, 
                       shape_blur=args.blur, block_size=args.block_size, num_blocks=args.num_blocks, shape_scale = args.shape_scale)
else:
    generate_shape(shape=args.shape, num_pics=args.num_pics, BACKGROUND_PATH= args.background_path,
                       SAVE_PATH=args.save_path, final_pic_size=args.final_pic_size, 
                       shape_blur=args.blur, block_size=args.block_size, num_blocks=args.num_blocks, shape_scale = args.shape_scale)