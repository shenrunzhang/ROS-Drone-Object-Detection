#! /usr/bin/env python
# Import ROS.
import rospy
# Import the API.
from iq_gnc.py_gnc_functions import *
# To print colours (optional).
from iq_gnc.PrintColours import *
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from pipeline import get_target_list
from collections import deque

bridge = CvBridge()

image_queue = deque()

last_image = None

def capture_image():
    global last_image
    # Create a subscriber for the camera topic
    image_sub = rospy.Subscriber('/webcam/image_raw', Image, callback)
    
    # Wait for image to arrive
    while not last_image:
        rospy.sleep(0.1)
    
    image = last_image
    
    # Convert to cv image
    cv_image = bridge.imgmsg_to_cv2(image)
    
    # # Display the captured image
    # cv2.imshow("", cv_image)
    # cv2.waitKey(0)
    
    return cv_image

def callback(data):
    global last_image
    # Store most recent image
    last_image = data


def main():
    # Initializing ROS node.
    rospy.init_node("drone_controller", anonymous=True)

    # Create an object for the API.
    drone = gnc_api()
    # Wait for FCU connection.
    drone.wait4connect()
    # Wait for the mode to be switched.
    drone.wait4start()

    # Create local reference frame.
    drone.initialize_local_frame()
    # Request takeoff with an altitude of 3m.
    drone.takeoff(3)

    # Specify control loop rate. We recommend a low frequency to not over load the FCU with messages. Too many messages will cause the drone to be sluggish.
    rate = rospy.Rate(3)
    
    # How many pictures to take:
    n_pics = 4

    # Declare length of the runway in meters 
    len_runway = 40

    # Declare flight altitude
    height = 20

    # Create waypoints
    goals = []

    for y in range(0, len_runway, len_runway // (n_pics + 2)):
        goals.append([0, y, height, 0])
    
    i = 0

    text = ""

    while i < len(goals):
        drone.set_destination(
            x=goals[i][0], y=goals[i][1], z=goals[i][2], psi=goals[i][3])
        rate.sleep()

        
        if drone.check_waypoint_reached():
            # Record locations
            text += str(drone.get_current_location()) + "\n"
            
            if i != 0 and i != len(goals) - 1:
                # Take pictures at middle waypoints
                img = capture_image()
                image_queue.append(img)

            i += 1

            
    # Land after all waypoints is reached.
    drone.land()
    rospy.loginfo(CGREEN2 + "All waypoints reached landing now." + CEND)
    
    
    # Saves images and logs targets
    
    n_targets = len(image_queue)
    
    for i in range(n_targets):
        text += "-" * 20 + " Image " + str(i) + " " + "-" * 20 + "\n"
        
        img = image_queue.popleft()

        cv2.imwrite('pic%s.jpg'%i, img)
        
        target_list = get_target_list(img)
        
        for target in target_list:
            # Get the coordinates of the target
            c_x, c_y = target.get_x(), target.get_y()
            
            # Get bounding box coordinates of target
            x, y, w, h = target.get_bbox()
            
            # Get the shape of the target
            shape = target.get_shape()
            
            # Get the color of the target
            color = target.get_color()
            
            # Draw bounding box onto image and save image
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.imwrite("view_" + str(i) + ".jpg",img)
            
            text += "Coordinates: (%s,%s) | Shape: %s | Color: %s \n" %(c_x, c_y, shape, color) 

    with open("log.txt", "w+") as f:
        f.write(text)
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
