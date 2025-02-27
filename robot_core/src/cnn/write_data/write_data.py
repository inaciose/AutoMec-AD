#!/usr/bin/env python3

# Imports
import signal
import sys
import cv2
from csv import writer
import copy
import numpy as np
from numpy.lib.function_base import angle
import rospy
from geometry_msgs.msg._Twist import Twist
from sensor_msgs.msg._Image import Image
from cv_bridge.core import CvBridge
from datetime import datetime
import pandas as pd
import datetime 
from PIL import Image as Image_pil

# Global Variables
global angular
global linear
global bridge
global begin_cmd
global begin_img
global img_rbg
global driving_log


# Calback Function to receive the cmd values
def messageReceivedCallback(message):

    global angular
    global linear
    global begin_cmd

    angular = float(message.angular.z)
    linear = float(message.linear.x)

    begin_cmd = True

# Callback function to receive image
def message_RGB_ReceivedCallback(message):
    
    global img_rbg
    global bridge
    global begin_img


    img_rbg = bridge.imgmsg_to_cv2(message, "bgr8")

    begin_img = True

    
def signal_handler(sig, frame):
    global driving_log
    print('You pressed Ctrl+C!')
    driving_log.to_csv('../data/driving_log.csv',mode='a',index=False,header=False)
    sys.exit(0)

    

def main():

    # Global variables
    global angular
    global linear
    global bridge
    global img_rbg
    global begin_cmd
    global begin_img
    global driving_log

    # Initial Value
    begin_cmd = False
    begin_img = False
    first_time = True

    # Init Node
    rospy.init_node('write_data', anonymous=False)

    # Subscribe topics
    rospy.Subscriber('robot/cmd_vel', Twist, messageReceivedCallback)
    rospy.Subscriber('/robot/camera/rgb/image_raw', Image, message_RGB_ReceivedCallback)
    
    # Create an object of the CvBridge class
    bridge = CvBridge()

    # Create pandas dataframe
    driving_log = pd.DataFrame(columns=['image','angle'])
  
   
    rate = rospy.Rate(10)


    signal.signal(signal.SIGINT, signal_handler)

    while  True:
        
        if begin_cmd==False or begin_img==False:
            continue


        curr_time = datetime.datetime.now()
        image_name = str(curr_time.year) + '_' + str(curr_time.month) + '_' + str(curr_time.day)+ '__' + str(curr_time.hour)+ '_' + str(curr_time.minute)+ '_' + str(curr_time.second)+ '__' + str(curr_time.microsecond)
        
        # add image and angle to the driving_log pandas
        row  = pd.DataFrame([[image_name,angular]],columns=['image','angle'])
        driving_log=driving_log.append(row,ignore_index=True)
        

        # save image

        width = 320
        height = 160
        dim = (width, height)
        img_rbg = cv2.resize(img_rbg, dim, interpolation = cv2.INTER_AREA)
        image_saved = Image_pil.fromarray(img_rbg)
        image_saved.save('../data/IMG/' + image_name + '.jpg')
        print('Image Saved')

        
        rate.sleep()
    



    
    


if __name__ == '__main__':
    main()