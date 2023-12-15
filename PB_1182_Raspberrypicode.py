'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 4B-Part 1 of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 1182 ]
# Author List:		[ Phanendra Sreeharsh Kowdodi , Raj Pattnaik , Sai Ram Senapati , Ashish Kumar Sahu  ]
# Filename:			task_4b_1.py
# Functions:		control_logic, 
#                   move_bot,
#                   motor_pin_setup
#                   forward
#                   backward
#                   motor_pause
#                   stop
#                   setup_client
#                   receive_message_via_socket
#                   send_message_via_socket
#                   control_logic
#                   get_count_right
#                   get_count_left
#                   forward_to_goal
#                   correct_back
#                   right_turn
#                   right_turn_back
#                   left_turn
#                   STRAIGHT
#                   WAIT_5
#                   LEFT
#                   RIGHT
#                   REVERSE
#                   CORRECT_BACK	
# Global Variables: count_left , count_right, goal_forward , goal_turn			

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section.   ##
## You have to implement this task with the available modules ##
##############################################################
import socket
import time
import os,sys
import numpy as np
import cv2
import time
import RPi.GPIO as GPIO
import sys
import datetime
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
from threading import Thread
from picamera.array import PiRGBArray
from picamera import PiCamera

########### ADD YOUR UTILITY FUNCTIONS HERE ##################
L_PWM_PIN1 = 38
L_PWM_PIN2 = 40
R_PWM_PIN2 = 32
R_PWM_PIN1 = 33
R_PWM_ENA=31
L_PWM_ENB=37
sensor_1= 24 #24
sensor_2= 26 #26
redPin_1 = 16
gndPin_1 = 18
greenPin_1 = 12
bluePin_1 = 29
redPin_2 = 36
greenPin_2 = 15
bluePin_2 = 13
redPin_3 = 22
greenPin_3 = 11
bluePin_3 = 35

def motor_pin_setup():
    """
    Purpose:
    ---
    This function is suppose to define the pins of Motors and LEDs used in the Alphabot.

    Example call:
    ---
    motor_pin_setup()
    """    
    global L_MOTOR1, L_MOTOR2, R_MOTOR1, R_MOTOR2, R_PWM_ENA, L_PWM_ENB
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(R_PWM_PIN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(R_PWM_PIN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(L_PWM_PIN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(L_PWM_PIN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(R_PWM_ENA, GPIO.OUT, initial= GPIO.HIGH)
    GPIO.setup(L_PWM_ENB, GPIO.OUT, initial= GPIO.HIGH)

    # setting initial PWM frequency for all 4 pins
    L_MOTOR1 = GPIO.PWM(L_PWM_PIN1, 100) 
    R_MOTOR1 = GPIO.PWM(R_PWM_PIN1, 100)
    L_MOTOR2 = GPIO.PWM(L_PWM_PIN2, 100)
    R_MOTOR2 = GPIO.PWM(R_PWM_PIN2, 100) 
    
    # setting initial speed (duty cycle) for each pin as 0
    L_MOTOR1.start(0)
    R_MOTOR1.start(0)
    L_MOTOR2.start(0)
    R_MOTOR2.start(0)
    
    # setting up encoders
    GPIO.setup(sensor_1, GPIO.IN)
    GPIO.setup(sensor_2, GPIO.IN)
    
    # led
    GPIO.setup(redPin_1,GPIO.OUT)
    GPIO.setup(bluePin_1,GPIO.OUT)
    GPIO.setup(gndPin_1,GPIO.OUT)
    GPIO.setup(greenPin_1,GPIO.OUT)
    GPIO.setup(redPin_2,GPIO.OUT)
    GPIO.setup(bluePin_2,GPIO.OUT)
    GPIO.setup(greenPin_2,GPIO.OUT)
    GPIO.setup(redPin_3,GPIO.OUT)
    GPIO.setup(bluePin_3,GPIO.OUT)
    GPIO.setup(greenPin_3,GPIO.OUT)
    
    
    
def forward(left, right):
    """
    Purpose:
    ---
    This function is suppose to move the motors in forward direction as per the speed inputs.

    Example call:
    ---
    forward(left, right)
    """    
    L_MOTOR1.ChangeDutyCycle(left)
    R_MOTOR1.ChangeDutyCycle(right)
    
def backward(left, right):
    """
    Purpose:
    ---
    This function is suppose to move the motors in backward direction as per the speed inputs.

    Example call:
    ---
    forward(left, right)
    """    
    L_MOTOR2.ChangeDutyCycle(left)
    R_MOTOR2.ChangeDutyCycle(right)
    
def motor_pause(secs):
    """
    Purpose:
    ---
    This function is suppose to stop the motors as per the given time input.

    Example call:
    ---
    motor_pause(secs)
    """    
    L_MOTOR1.ChangeDutyCycle(0)
    R_MOTOR1.ChangeDutyCycle(0)
    L_MOTOR2.ChangeDutyCycle(0)
    R_MOTOR2.ChangeDutyCycle(0)
    time.sleep(secs)
    
def stop():
    """
    Purpose:
    ---
    This function is suppose to stop the motors after the execution of the program.

    Example call:
    ---
    stop()
    """  
    L_MOTOR1.stop()
    R_MOTOR1.stop()
    L_MOTOR2.stop()
    R_MOTOR2.stop()
    GPIO.cleanup()
      
##############################################################
    
def setup_client(host, port):

	##################	ADD YOUR CODE HERE	##################
	
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((host,port))

	##########################################################
	

	return client

def receive_message_via_socket(client):

	message = None

	##################	ADD YOUR CODE HERE	##################
	message = client.recv(1024)
	message_decode = message.decode()

	##########################################################
	

	return message_decode

def send_message_via_socket(client, message):
	
	##################	ADD YOUR CODE HERE	##################
    
	message_encode = message.encode(encoding = 'UTF-8')
	client.send(message_encode)

	##########################################################
	
def control_logic():

    """
    Purpose:
    ---
    This function is suppose to process the frames from the PiCamera and
    check for the error using image processing and with respect to error
    it should correct itself using PID controller.

    >> Process the Frame from PiCamera 
    >> Check for the error in line following and node detection
    >> PID controller

    Returns:
    ---
    [string] -- calculated error through image processing to give input for PID of line following.

    Example call:
    ---
    control_logic()
    """    

    ##################	ADD YOUR CODE HERE	##################
    
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    stream = camera.capture_continuous(rawCapture,format="bgr", use_video_port=True)
    
    
    
    hue_min = 76
    hue_max = 179
    sat_min = 95
    sat_max = 255
    val_min = 50
    val_max = 255
    line_threshold = 92
    
    lower = np.array([hue_min,sat_min,val_min])
    upper = np.array([hue_max,sat_max,val_max])
    
    for frame in stream:
        
        image = frame.array
        #blurred = cv2.medianBlur(image,3)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        
        mask = cv2.inRange(hsv , lower , upper)
        #img = cv2.bitwise_and(image,image,mask=mask)
        #print("HI")
        cv2.imshow("masked", mask)
        
        key = cv2.waitKey(1) & 0xFF         
            
            # if the `q` key was pressed, break from the loop and close display window
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
        
        
        
        for x in range(0,640):
            
            pix = mask[240,x]
        
            if pix >  0:
                #print(x)
                rawCapture.truncate(0)
                camera.close()
                #cv2.destroyAllWindows()
                return "Reached Node"
        
        ret,thresh1 = cv2.threshold(gray,line_threshold,255,cv2.THRESH_BINARY) 
        #edged = cv2.Canny(thresh1,85,200)
        contours,hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            
        if(len(contours)) > 0:
            
            c = max(contours, key = cv2.contourArea)
            M = cv2.moments(c)
            
            if M["m00"] != 0:
                cx = int(M['m10']/M['m00'])
                error = cx - 370
        
                move_bot(error)
                rawCapture.truncate(0)
        rawCapture.truncate(0)      

    ##########################################################

prev_error = 0
def move_bot(error):
    """
    Purpose:
    ---
    This function is suppose to move the bot

    Input Arguments:
    ---
    [float]--Error calculated through image processing 

    Example call:
    ---
    move_bot()
    """    

    ##################	ADD YOUR CODE HERE	##################
    global prev_error
    kp = 0.0055
    kd = 0.0079
    error = kp*error + kd*(error-prev_error)
    base = 43
    forward(base - error , base + error)
    prev_error = error
    ##########################################################



################# ADD UTILITY FUNCTIONS HERE #################

global count_left , count_right
global goal_forward , goal_turn
goal_forward = 8
goal_turn = 19
count_right = 0
count_left = 0

def get_count_right(c):
    """
    Purpose:
    ---
    This is a callback function which gives the motor Encoder output of the right wheel in the form of integer variables.

    Example call:
    ---
    get_count_right(c)
    """    
    global count_right
    count_right+=1
    #print(count_right)

def get_count_left(c):
    """
    Purpose:
    ---
    This is a callback function which gives the motor Encoder output of the left wheel in the form of integer variables.

    Example call:
    ---
    get_count_left(c)
    """ 
    global count_left
    count_left+=1
    #print(count_left)

def forward_to_goal(goal_forward):
    """
    Purpose:
    ---
    This is a function which moves the robot in the forward direction for distance entered given as motor Encoder pulse level changes(LOW to HIGH).
    
    Input Arguments:
    ---
    [int]--Number of motor encoder pulse changes.

    Example call:
    
    forward_to_goal(goal_forward)
    """ 
    #count_left = 0
    global count_left
    while count_left <= goal_forward:
        forward(47,45)
        #print(count_left)
    motor_pause(0.15)

def correct_back():
    """
    Purpose:
    ---
    This is a function which moves the robot in the backward direction as a part of the correction algorithm while reading QR Codes.
    
    Example call:
    
    correct_back()
    """ 
    #count_left = 0
    global count_left
    while count_left <= 2:
        backward(58,53)
        #print(count_left)
    motor_pause(0.15)
    
def right_turn(goal_turn):
    """
    Purpose:
    ---
    This is a function which moves the left motor of the robot in the forward direction for distance entered given as motor Encoder pulse level changes(LOW to HIGH).
    
    Example call:
    
    right_turn(goal_turn)
    """ 
    #count_left = 0
    global count_left
    while count_left <= goal_turn :
        forward(70,0)
    motor_pause(0.15)

def right_turn_back(goal_turn):
    """
    Purpose:
    ---
    This is a function which moves the right motor of the robot in the backward direction for distance entered given as motor Encoder pulse level changes(LOW to HIGH).
    
    Example call:
    
    right_turn_back(goal_turn)
    """ 
    #count_left = 0
    global count_right
    while count_right <= goal_turn :
        backward(0,60)
    motor_pause(0.15)

    
def left_turn(goal_turn):
    """
    Purpose:
    ---
    This is a function which moves the right motor of the robot in the forward direction for distance entered given as motor Encoder pulse level changes(LOW to HIGH).
    
    Example call:
    
    left_turn(goal_turn)
    """ 
    #count_right = 0
    #global count_right
    global count_right
    while count_right <= goal_turn :
        forward(0,60)
        #print(count_right)
    motor_pause(0.15)
##############################################################

def STRAIGHT():
    """
    Purpose:
    ---
    This is a function which moves the robot from one node to the other in straight direction using Image Processing.
    
    Example call:
    
    STRAIGHT()
    """ 
    global count_left
    count_left = 0
    forward_to_goal(goal_forward)
    
    #print("RUnning")
    status = control_logic()
    #print(status)
    motor_pause(0.5)
    
def WAIT_5():
    """
    Purpose:
    ---
    This is a function which makes the robot wait for five seconds in real time.
    
    Example call:
    
    WAIT_5()
    """ 

    motor_pause(5)
    
def LEFT():
    """
    Purpose:
    ---
    This is a function which first takes a left turn and then moves the robot from one node to the other in straight direction using Image Processing.
    
    Example call:
    
    LEFT()
    """ 
    global count_left
    count_left = 0
    forward_to_goal(goal_forward)
    global count_right
    count_right = 0
    left_turn(goal_turn)
    status = control_logic()
    #print(status)
    motor_pause(0.5)

def RIGHT():
    """
    Purpose:
    ---
    This is a function which first takes a right turn and then moves the robot from one node to the other in straight direction using Image Processing.
    
    Example call:
    
    RIGHT()
    """ 
    global count_left
    count_left = 0
    forward_to_goal(goal_forward)
    #global count_left
    count_left = 0
    right_turn(goal_turn)
    status = control_logic()
    #print(status)
    motor_pause(0.5)
    
def REVERSE():
    """
    Purpose:
    ---
    This is a function which rotates the robot turn 180 degrees.
    
    Example call:
    
    REVERSE()
    """ 
    global count_left
    count_left = 0
    forward_to_goal(20)
    global count_right
    count_right = 0
    right_turn_back(goal_turn)
    count_left=0
    right_turn(goal_turn+1)
    status = control_logic()
    #print(status)
    motor_pause(0.5)

def CORRECT_BACK():
    """
    Purpose:
    ---
    This is a function which implements the correction algorithm at PN of shops.
    
    Example call:
    
    CORRECT_BACK()
    """ 
    global count_left
    count_left = 0
    correct_back()
    
    




##############################################################
    
if __name__ == "__main__":

    """
    The goal of the this task is to move the robot through a predefied 
    path which includes straight road traversals and taking turns at 
    nodes. 

    This script is to be run on Raspberry Pi and it will 
    do the following task.
 
    >> Stream the frames from PiCamera
    >> Process the frame, do the line following and node detection
    >> Move the bot using control logic

    The overall task should be executed here, plan accordingly. 
    """    

    ##################	ADD YOUR CODE HERE	##################
    
    host = '192.168.189.138'
    port = 5050

    motor_pin_setup()
    
    global RED,BLUE,GREEN
    RED_1 = GPIO.PWM(redPin_1,250)
    BLUE_1 = GPIO.PWM(bluePin_1,250)
    GREEN_1 = GPIO.PWM(greenPin_1,250)
    RED_2 = GPIO.PWM(redPin_2,250)
    BLUE_2 = GPIO.PWM(bluePin_2,250)
    GREEN_2 = GPIO.PWM(greenPin_2,250)
    RED_3 = GPIO.PWM(redPin_3,250)
    BLUE_3 = GPIO.PWM(bluePin_3,250)
    GREEN_3 = GPIO.PWM(greenPin_3,250)
    
    RED_1.start(0)
    GREEN_1.start(0)
    BLUE_1.start(0)
    RED_2.start(0)
    GREEN_2.start(0)
    BLUE_2.start(0)
    RED_3.start(0)
    GREEN_3.start(0)
    BLUE_3.start(0)
    
    GPIO.add_event_detect(sensor_1, GPIO.RISING, callback=get_count_left)
    GPIO.add_event_detect(sensor_2, GPIO.RISING, callback=get_count_right)
    

    ################################################################################
    '''camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    stream = camera.capture_continuous(rawCapture,format="bgr", use_video_port=True)'''
    ################################################################################
    
    #key = cv2.waitKey(1) & 0xFF
    #rawCapture.truncate(0)
    
    try:
        client = setup_client(host, port)


    except socket.error as error:
        print("Error in setting up client")
        print(error)
        sys.exit()
    
    Green= [0,100,0]
    SkyBlue= [0,100,100]
    Pink= [100,0,100]
    Orange= [100,20,0]
    White= [100,100,100]
    Off = [0, 0, 0]
    colour = None
    while True:    
        message = receive_message_via_socket(client)
        
        if message == "STRAIGHT" or message == "LEFT" or message == "RIGHT" or message == "WAIT_5" or message == "REVERSE" or message == "CORRECT_BACK": 
            #print(message)
            if message == "STRAIGHT" :
                STRAIGHT()
            elif message == "LEFT":
                LEFT()
            elif message == "RIGHT":
                RIGHT()
            elif message == "WAIT_5":
                WAIT_5()
            elif message == "REVERSE":
                REVERSE()
            elif message == "CORRECT_BACK":
                CORRECT_BACK()
                
            send_message_via_socket(client,"DONE")
        
        elif message[0:3] == "LED":
            
            if(message[6:] == "Orange"):
                colour = Orange
            elif(message[6:] == "Skyblue"):
                colour = SkyBlue
            elif(message[6:] == "Green"):
                colour = Green
            elif(message[6:] == "Pink"):
                colour = Pink
            elif(message[6:] == "White"):
                colour = White
            elif(message[6:] == "Off"):
                colour = Off
            
            
            if(message[4:5] == "1"):
                RED_1.ChangeDutyCycle(colour[0])
                GREEN_1.ChangeDutyCycle(colour[1])
                BLUE_1.ChangeDutyCycle(colour[2])
                
            elif(message[4:5] == "2"):   
                RED_2.ChangeDutyCycle(colour[0])
                GREEN_2.ChangeDutyCycle(colour[1])
                BLUE_2.ChangeDutyCycle(colour[2])
            elif(message[4:5] == "3"):              
                RED_3.ChangeDutyCycle(colour[0])
                GREEN_3.ChangeDutyCycle(colour[1])
                BLUE_3.ChangeDutyCycle(colour[2])
            
            
            
            
            
            
        elif message =="END":
            #print("ENDING")
            
            break
       
           
    #STRAIGHT()
    #LEFT()
    #STRAIGHT()
    #REVERSE()
    #RIGHT()
    #print("out")
    #CORRECT_BACK()
    
    #RIGHT()
    #LEFT()
    

    #REVERSE()
    stop()
    cv2.destroyAllWindows()
    
    
   
    
    # if the `q` key was pressed, break from the loop and close display window

    #STRAIGHT()
    #LEFT()
    #STRAIGHT()
    #RIGHT()
    #stop()
    #cv2.destroyAllWindows()'''
    
    
    ##########################################################

    pass
