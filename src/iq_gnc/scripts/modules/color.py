import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import PIL
from sklearn.cluster import KMeans
from collections import Counter
import math
import colorsys
KMeans.n_init = 5
"""
# colors include:
white
black
grey
red
blue
green
yellow
purple
brown
orange
n=10 colors
maybe add terrain?
"""
#  compute distance between color 1 and color 2
#  not used anymore :)
clr_ctrs = {}
clr_ctrs["red"] = (237,55,55)
clr_ctrs["white"] = (255,255,255)
clr_ctrs["black"] = (0,0,0)
clr_ctrs["grey"] = (220,220,200)
clr_ctrs["blue"] = (30,30,230)
clr_ctrs["green"] = (55,237,55)
clr_ctrs["yellow"] = (255,255,0)
clr_ctrs["purple"] = (93, 63, 211)
clr_ctrs["brown"] = (150, 75, 0)
clr_ctrs["orange"] = (250, 150, 5)
"""
input: color 1 and color 2
returns the euclidean distance between the two colors
"""
#clr_ctrs["terrain"] = (190,174,163)
def colorDist(color1, color2):
    dist = math.sqrt((color1[0]-color2[0])**2+(color1[1]-color2[1])**2+(color1[2]-color2[2])**2)
    #print("This DIST IS: ")
    #print(dist)
    return dist
"""
input: color1, a color in form (R,G,B)
output: the color in clr_ctrs that it is closest to
"""
def find_best_match(color1):
    min_dist = 100000000
    ret_clr = "null"
    for color,centroid in clr_ctrs.items():    
        #print(color, centroid)
        #if centroid == clr_ctrs["terrain"]:
            #continue
        this_dist = colorDist(color1, centroid)
        #print(this_dist, color, centroid)
        #print("THIS DIST IS :")
        #print(this_dist)
        if this_dist < min_dist:
            min_dist = this_dist
            ret_clr = color
    return ret_clr
"""
A method to show the target image, the color palette, and our color guess
"""
def show_img_compar(img_1, img_2, colorGuess):
    f, ax = plt.subplots(1, 2, figsize=(10,10))
    plt.text(90,30, colorGuess, fontsize=20)
    ax[0].imshow(img_1)
    ax[1].imshow(img_2)
    ax[0].axis('off') #hide the axis
    ax[1].axis('off')
    f.tight_layout()
    plt.show()

def palette(clusters):
    width=300
    palette = np.zeros((50, width, 3), np.uint8)
    steps = width/clusters.cluster_centers_.shape[0]
    for idx, centers in enumerate(clusters.cluster_centers_): 
        palette[:, int(idx*steps):(int((idx+1)*steps)), :] = centers
    return palette
"""
input: k_cluster
output: palette, a proportional palette of the colors of a k_cluster that is the clusters of colors in an img
color_2_pct, a dictionary that maps RGB values to their prevalence in the image

"""
def palette_perc(k_cluster):
    width = 300
    palette = np.zeros((50, width, 3), np.uint8)
    
    n_pixels = len(k_cluster.labels_)
    counter = Counter(k_cluster.labels_) # count how many pixels per cluster
    perc = {}
    for i in counter:
        perc[i] = np.round(counter[i]/n_pixels, 2)
    perc = dict(sorted(perc.items()))
    
    #for logging purposes
    #print(perc)
    #print("these are cluster centers: ")
    #print(k_cluster.cluster_centers_)
    cluster_centers = k_cluster.cluster_centers_.tolist()
    #print(perc)
    #print(cluster_centers)
    # my code: !
    color_2_pct = {}
    for i in range(2):
        color_2_pct[tuple(cluster_centers[i])] = perc[i]
    #print("DICT IS : ")
    #print(color_2_pct)
    step = 0
    
    for idx, centers in enumerate(k_cluster.cluster_centers_): 
        palette[:, step:int(step + perc[idx]*width+1), :] = centers
        step += int(perc[idx]*width+1)
        
    return palette, color_2_pct
# goal: find most prevalent color that is not the terrain color
# input: a map of colors in an image to their prevalence in the image
def find_best_nottrn(color_2_pct):
    max_pct_nottrn = 0
    ret_color = "null"
    for color, pct in color_2_pct.items():
        this_color = find_best_match(color)
        
        #print("THE COLOR IS : ")
        #print(this_color)
        if (this_color != "terrain") and (pct > max_pct_nottrn):
            
            
            max_pct_nottrn = pct
            ret_color = this_color
    return ret_color
"""
input: a dictionary that maps rgb values to percentage of prescence in a picture
returns: the rgb value in the form (0,0,0) that takes up the most space
"""
def find_terrain_ctr(color_2_pct):
    max_pct = 0
    retVal = (0,0,0)
    for rgb, pct in color_2_pct.items():
        if pct > max_pct:
            max_pct = pct
            retVal = rgb
    return retVal
"""
input: a list of colors: to Match, and a color2: to go far away from
returns the rgb value in the form (r,g,b) of the color in to Match furthest away from color2
"""
def find_best_chance(colors_2_pcts, color2):
    retClr = (0,0,0)
    min_pct = min(colors_2_pcts.values())
    print(min_pct)
    min_dist = 0
    for colors, pcts in colors_2_pcts.items():
        this_dist = colorDist(colors, color2)
        if ((this_dist > min_dist) & (pcts > min_pct)).all():
            min_dist = this_dist
            retClr = colors
    return retClr
"""
Input: Hue, Saturation, Lumniance (Float values)

Using if statements guess the color
"""
def hsl_to_color(hue, s, l):
    hue = hue*360
    s = s*-100
    l = l-100
    hsl = (": " + str(math.floor(hue)) + ", " + str(math.floor(s)) + ", " + str(math.floor(l)))
    
        
    if (l > 98):
        return "white" + hsl
    if (l < 2):
        return ("black" + hsl)
    if (0 < s < 10):
        return "grey"
    if ((0 < hue < 17) or (319 < hue < 361)):
        return "red" + hsl
    if (16 < hue < 50):
        return "orange" + hsl
    if (49 < hue < 73):
        return "yellow" + hsl
    if (72 < hue < 160):
        return "green" + hsl
    if (159 < hue < 255):
        return "blue" + hsl
    if (254 < hue < 320):
        return "purple" + hsl
    else:
        return ("damn idk dawg " + str(math.floor(hue)) + ", " + str(math.floor(s)) + ", " + str(math.floor(l)))

#clt = KMeans(n_clusters=5)
#clt_3 = KMeans(n_clusters=3)
#clt_3.fit(img_2.reshape(-1, 3))
#show_img_compar(img_2, palette(clt_3))
#clt_2 = clt.fit(img_2.reshape(-1, 3))
#palette1, color_2_pct = palette_perc(clt_2)
#show_img_compar(img_2, palette1)
#print(find_best_nottrn(color_2_pct))
#print("BETTER BE WHITE : ")
#print(find_best_match((0,0,0)))

"""
Overall Process:
Get the image
Sort the colors into 2 clusters 
Get how prevalent each of those 2 cluster colors are in the image
The less prevalent color is (assumed to be) the color of the target itself
Convert that color's RGB value to HSL (Hue, Saturation, Luminance)
Using a bunch of if statements, convert that HSL to one of the ten possible colors (brown not possible rn)
Display the Target Image, the 2 Color Clusters, and the Guess for the Color
All that 500 times
"""
def classify_color(img) -> str:
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    clt = KMeans(n_clusters=2)
    clt_here = clt.fit(img.reshape(-1,3))
    palette_here, color_dict = palette_perc(clt_here)
    colorBest = min(color_dict, key=color_dict.get)
    r, g, b = colorBest[0], colorBest[1], colorBest[2]
    hue, l, s = colorsys.rgb_to_hls(r,g,b)
    actualColor = hsl_to_color(hue, s, l)
    return actualColor
    
if __name__ == "__main__":
    for i in range(500):       
        img = cv.imread("./training_data/shapes/circle/circle" + str(i) + ".jpg")
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        clt = KMeans(n_clusters=2)
        clt_here = clt.fit(img.reshape(-1,3))
        palette_here, color_dict = palette_perc(clt_here)
        colorBest = min(color_dict, key=color_dict.get)
        r, g, b = colorBest[0], colorBest[1], colorBest[2]
        print(str(r)+", " + str(g) + ", " + str(b))
        hue, l, s = colorsys.rgb_to_hls(r,g,b)
        print(color_dict)
        #clr_ctrs["terrain"] = find_terrain_ctr(color_dict)
        #bestChance = find_best_chance(color_dict, clr_ctrs["terrain"])
        #guess = find_best_match(colorBest)
        #hue, s, l = rgb_to_hsl(colorBest)
        print(str(hue)+", " + str(s) + ", " + str(l))
        actualColor = hsl_to_color(hue, s, l)
        #print(guess)
        show_img_compar(img, palette_here, actualColor)
