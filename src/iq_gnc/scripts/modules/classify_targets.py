import cv2
from modules.target import Target
import math
import matplotlib.pyplot as plt
import numpy as np
import os

def edge_detect(mask):
    '''
    Detects the edges in an input greyscale image
    In this case, we are passing a mask of 0s and 255s
    It will return a 0s and 255s numpy array of edges or non-edge pixels
    '''
    edges = cv2.Canny(mask, threshold1=40, threshold2=60)
    #print("edges shape:", edges.shape)
    return edges


def find_targets(frame,
                 H_UPPER_LIMIT = 200,H_LOWER_LIMIT = 30,
                 W_UPPER_LIMIT = 200,W_LOWER_LIMIT = 30,
                 DISTANCE_THRES = 300):
    '''
    limits for the target size
    :param DISTANCE_THRES: threshold in pixels for eliminating multiple bboxes on one target
    :return: target_list, a list of Target objects found in frame
    '''
    (thresh, im_bw) = cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    target_list = []
    for i in contours:
        x, y, w, h = cv2.boundingRect(i)
        same_target = False
        if target_list:
            for target in target_list:
                same_target = math.sqrt((x - target.get_x()) ** 2 + (y - target.get_y()) ** 2) < DISTANCE_THRES
        if H_LOWER_LIMIT < h < H_UPPER_LIMIT and W_LOWER_LIMIT < w < W_UPPER_LIMIT and not same_target:
            target_list.append(Target(frame[y: y + h, x: x + h], x + w // 2, y + h // 2, (x,y,w,h)))

    return target_list


if __name__ == "__main__":
    LOCATION = r"C:\Users\Shen\Documents\GitHub\RiceUAV\vision\modules\testimg\sshtesthigh5.jpg"
    
    DetectorScript = r"C:\Users\Shen\Documents\GitHub\RiceUAV\vision\modules\edgeFinder\edge_detector.py"

    ScriptFirst = "python " + DetectorScript + " --input "

    ScriptSecond = " --prototxt vision/modules/edgeFinder/deploy.prototxt --caffemodel vision/modules/edgeFinder/hed_pretrained_bsds.caffemodel"
    #tile length is a 6th of length, 6th of height
    # 250 by 250
    # 6 tiles down, 12 across
    frame1 = cv2.imread(LOCATION)
    #frame = cv2.fastNlMeansDenoisingColored(frame1,None,10,10,7,21)
    cropped = frame1[1000:2500,3000:6000]
    
    # saves cropped image and references the saved image
    cv2.imwrite("croppedtest2.jpg", cropped)
    scriptFull = ScriptFirst + "croppedtest2.jpg" + ScriptSecond
    
    # loads model and runs inference on the saved cropped image
    os.system(scriptFull)
    
    # crops background image
    backgroundImg = cropped[0:250,0:250]
    
    
    for rows in range(6):
        for cols in range(12):
            #print(cropped.shape)
            lowerR = (rows)*250
            upperR = (rows+1)*250
            lowerC = (cols)*250
            upperC = (cols+1)*250
            tilePre = cropped[lowerR:upperR,lowerC:upperC]
            tile = cv2.subtract(backgroundImg, tilePre)
            tile2 = cv2.subtract(tilePre, backgroundImg)
            (thresh, blackAndWhiteImage) = cv2.threshold(tile, 30, 255, cv2.THRESH_BINARY)

            #cv2.imshow("tile", tile)
            #cv2.waitKey(0)
            
            # save the tile after preprocessing
            cv2.imwrite("input.jpg", tilePre)
            script = ScriptFirst + "input.jpg" + ScriptSecond
            
            # runs inference on the tile, outputs to out.jpg
            os.system(script)
            
            # loads out.jpg and finds targets
            tilePost = cv2.imread("out.jpg", cv2.IMREAD_GRAYSCALE)
            targets = find_targets(tilePost)
            #targets2 = find_targets(tile2)
            #edges = cv2.Canny(tile, 40, 60)
            
            # draws boundary box for any targets in the tile 
            for target in targets:
                x, y, w, h = target.get_bbox()
                cv2.rectangle(tilePre, (x, y), (x + w, y + h), (255, 255, 0), 4)
                print("I drew a rect!")
            #for target in targets2:
            #x, y, w, h = target.get_bbox()
            #cv2.rectangle(tilePre, (x, y), (x + w, y + h), (0, 255, 255), 4)

  
            # saves the tile with bbox drawn and the processed tile with edges
            #print("I drew a rect!")
            #image[rows][cols] = tile  
            cv2.imwrite("AtileTest" + str(rows) + str(cols) + ".jpg", tilePre)
            cv2.imwrite("AtilePOST" + str(rows) + str(cols) + ".jpg", tilePost)
            #cv2.imwrite("edgesTest" + str(rows) + str(cols) + ".jpg", edges)
            #cv2.imwrite("tile2Test" + str(rows) + str(cols) + ".jpg", tile2)

'''
    #edges = cv2.Canny(cropped, 60, 120)
    for x in range(10):
        edges = cv2.Canny(cropped, 40, (x*10)+50)
        cv2.imwrite("croppedEdges30to" + str((x*10)+50) + ".jpg",edges)
    cv2.imshow("cropped",cropped)
    cv2.imshow("edges", edges)
    cv2.imwrite("croppededgestest2.jpg", edges)
    #  scaling stuff
    #scaleX is scale factor in x direction
    #scaleY is scale factor in y direction
    scaleX = 0.6
    scaleY = 0.6
    scaleUp = cv2.resize(cropped, None, fx= scaleX*3, fy= scaleY*3, interpolation= cv2.INTER_LINEAR)

    #cv2.imshow("Scaled Up", scaleUp)

    plt.subplot(121),plt.imshow(cropped,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    #plt.show()
    targets = find_targets(cropped)
    print(len(targets))
    for target in targets:
        x, y, w, h = target.get_bbox()
        cv2.rectangle(cropped, (x, y), (x + w, y + h), (255, 0, 0), 4)
    #cv2.imshow('frame',frame)
    cv2.imwrite('frametest3.jpg', cropped)
    cv2.waitKey(0)
    #cv2.destroyAllWindows()
'''