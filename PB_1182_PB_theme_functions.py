'''
*****************************************************************************************
*
*        		     ===============================================
*           		       Pharma Bot (PB) Theme (eYRC 2022-23)
*        		     ===============================================
*
*  This script contains all the past implemented functions of Pharma Bot (PB) Theme 
*  (eYRC 2022-23).
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 1182 ]
# Author List:		[ Phanendra Sreeharsh Kowdodi , Ashish Kumar Sahu ,  Sai Ram Senapati , Raj Pattnaik]
# Filename:			PB_theme_functions.py
# Functions:		
# 					[setup_server,
# 					setup_connection
#  					receive_message_via_socket
#					send_message_via_socket
# 					read_qr_code
# 					detect_paths_to_graph				
# 					detect_all_nodes
# 					detect_horizontal_roads_under_construction
# 					detect_vertical_roads_under_construction
# 					detect_medicine_packages
# 					detect_arena_parameters
# 					place_packages
# 					place_traffic_signals
# 					place_start_end_nodes
# 					place_horizontal_barricade
# 					path_planning					
# 					paths_to_moves
# 					perspective_transform
# 					transform_values
# 					set_values
# 					path_correction
# 					get_facing
# 					drop_packages]
####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import socket
import time
import os, sys
from zmqRemoteApi import RemoteAPIClient
import traceback
import zmq
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import json
##############################################################
task_1b = __import__('task_1b')
################# ADD UTILITY FUNCTIONS HERE #################


##############################################################


################## ADD SOCKET COMMUNICATION ##################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 3D for setting up a Socket
Communication Server in this section
"""

def setup_server(host, port):

	"""
	Purpose:
	---
	This function creates a new socket server and then binds it 
	to a host and port specified by user.

	Input Arguments:
	---
	`host` :	[ string ]
			host name or ip address for the server

	`port` : [ string ]
			integer value specifying port name
	Returns:

	`server` : [ socket object ]
	---

	
	Example call:
	---
	server = setupServer(host, port)
	""" 

	server = None

	##################	ADD YOUR CODE HERE	##################
	server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((host,port))

	##########################################################

	return server

def setup_connection(server):
	"""
	Purpose:
	---
	This function listens for an incoming socket client and
	accepts the connection request

	Input Arguments:
	---
	`server` :	[ socket object ]
			socket object created by setupServer() function
	Returns:
	---
	`server` : [ socket object ]
	
	Example call:
	---
	connection = setupConnection(server)
	"""
	connection = None
	address = None

	##################	ADD YOUR CODE HERE	##################
	server.listen(10)

	connection,address= server.accept()	

	##########################################################

	return connection, address

def receive_message_via_socket(connection):
	"""
	Purpose:
	---
	This function listens for a message from the specified
	socket connection and returns the message when received.

	Input Arguments:
	---
	`connection` :	[ connection object ]
			connection object created by setupConnection() function
	Returns:
	---
	`message` : [ string ]
			message received through socket communication
	
	Example call:
	---
	message = receive_message_via_socket(connection)
	"""

	message = None

	##################	ADD YOUR CODE HERE	##################
	message = connection.recv(1024)
	message_decode = message.decode()

	##########################################################

	return message_decode

def send_message_via_socket(connection, message):
	"""
	Purpose:
	---
	This function sends a message over the specified socket connection

	Input Arguments:
	---
	`connection` :	[ connection object ]
			connection object created by setupConnection() function

	`message` : [ string ]
			message sent through socket communication

	Returns:
	---
	None
	
	Example call:
	---
	send_message_via_socket(connection, message)
	"""

	##################	ADD YOUR CODE HERE	##################
	message_encode= message.encode(encoding = 'UTF-8')
	connection.send(message_encode)

	##########################################################

##############################################################
##############################################################

######################### ADD TASK 2B ########################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 2B for reading QR code from
CoppeliaSim arena in this section
"""

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the CoppeliaSim vision sensor's 
	field of view and returns the message encoded into it.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	`qr_message`   :    [ string ]
		QR message retrieved from reading QR code

	Example call:
	---
	control_logic(sim)
	"""
	qr_message = None
	
	##############  ADD YOUR CODE HERE  ##############
	def get_vision_data(sim):

		visionSensorHandle = sim.getObjectHandle('Vision_sensor')
		img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)  #Capturing image from sensor
		img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)		
		img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0) 
		return img
	img= get_vision_data(sim)
	cv2.imwrite("qr_miage.jpg",img)
	#cv2.waitKey(0)
	
	barcodes = decode(img)
	bdata= barcodes[0].data.decode("utf-8")
	qr_message= f"{bdata}"
	# print(qr_message,"Is the message")

	##################################################

	return qr_message

##############################################################
##############################################################

############### ADD ARENA PARAMETER DETECTION ################


def detect_paths_to_graph(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary of the
	connect path from a node to other nodes and will be used for path planning

	HINT: Check for the road besides the nodes for connectivity 

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`paths` : { dictionary }
			Every node's connection to other node and set it's value as edge value 
			Eg. : { "D3":{"C3":1, "E3":1, "D2":1, "D4":1}, 
					"D5":{"C5":1, "D2":1, "D6":1 }  }

			Why edge value 1? -->> since every road is equal

	Example call:
	---
	paths = detect_paths_to_graph(maze_image)
	"""    

	paths = {}

	##############	ADD YOUR CODE HERE	##############
	traffic_signals , start_node , end_node = detect_all_nodes(image)

	for px in range(100,700,100):

		for py in range(100,700,100):

			intensity = image[py,px]
			intensity_right = image[py,px+15]
			intensity_left = image[py,px-15]
			intensity_below = image[py+15,px]
			intensity_above = image[py-15,px]

			black = np.array([0,0,0])

			position = str(chr(int((px/100) + 64)) + str(int(py/100)))
			
			position_list={}
			

			if (intensity_right == black).all() :
				position_right = str(chr(int((px/100) + 64 + 1)) + str(int(py/100)))

				if position_right in traffic_signals:
					position_list[position_right] = 9
				else :
					position_list[position_right] = 4

			if (intensity_left == black).all() :
				position_left = str(chr(int((px/100) + 64 - 1)) + str(int(py/100)))
				if position_left in traffic_signals:
					position_list[position_left] = 9
				else :
					position_list[position_left] = 4
				
			
			if (intensity_above == black).all() :
				position_above = str(chr(int((px/100) + 64 )) + str(int(py/100)-1))
				if position_above in traffic_signals:
					position_list[position_above] = 9
				else :
					position_list[position_above] = 4

			if (intensity_below == black).all() :
				position_below = str(chr(int((px/100) + 64 )) + str(int(py/100)+1))
				position_list[position_below] = 1
				if position_below in traffic_signals:
					position_list[position_below] = 9
				else :
					position_list[position_below] = 4
			# position = str(chr(int((px/100) + 64)) + str(int(py/100)))
			paths[position]=position_list
	# print(paths)
	##################################################

	return paths

####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 1A and 3A for detecting arena parameters
from configuration image in this section
"""

def detect_all_nodes(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals, start_node and end_node are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals, start_node, end_node` : [ list ], str, str
			list containing nodes in which traffic signals are present, start and end node too
	
	Example call:
	---
	traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
	"""    
	traffic_signals = []
	start_node = ""
	end_node = ""

    ##############	ADD YOUR CODE HERE	##############
	for px in range(100,700,100):

		for py in range(100,700,100):

			intensity = image[py,px]
			red = np.array([0,0,255])
			green = np.array([0,255,0])
			purple = np.array([189,43,105])

			if (intensity == green).all():
				start_node = str(chr(int((px/100) + 64)) + str(int(py/100)))

			if (intensity == purple).all():
				end_node = str(chr(int((px/100) + 64)) + str(int(py/100)))

			if (intensity == red).all() :

				position = str(chr(int((px/100) + 64)) + str(int(py/100)))
				traffic_signals += [position]

    ##################################################

	return traffic_signals, start_node, end_node

def detect_horizontal_roads_under_construction(image):	
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing horizontal links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links
	
	Example call:
	---
	horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
	"""    
	horizontal_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	for px in range(150,650,100):

		for py in range(100,700,100):

			intensity = image[py,px]
			white = np.array([255,255,255])

			if (white == intensity).all() :

				left_end = str(chr(int((px-50)/100) + 64) + str(int(py/100)))
				right_end = str(chr(int((px+50)/100) + 64) + str(int(py/100)))
				horizontal_roads_under_construction += [left_end + "-" + right_end]

	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing vertical links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links
	
	Example call:
	---
	vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
	"""    
	vertical_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	for px in range(100,700,100):

		for py in range(150,650,100):

			intensity = image[py,px]
			white = np.array([255,255,255])

			if (white == intensity).all() :

				upper_end = str(chr(int((px)/100) + 64) + str(int((py-50)/100)))
				lower_end = str(chr(int((px)/100) + 64) + str(int((py+50)/100)))
				vertical_roads_under_construction += [upper_end + "-" + lower_end]
	
	##################################################
	
	return vertical_roads_under_construction

def detect_medicine_packages(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a nested list of
	details of the medicine packages placed in different shops

	** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
	   as well as in the alphabetical order of colors.
	   For example, the list should first have the packages of shop_1 listed. 
	   For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`medicine_packages` : [ list ]
			nested list containing details of the medicine packages present.
			Each element of this list will contain 
			- Shop number as Shop_n
			- Color of the package as a string
			- Shape of the package as a string
			- Centroid co-ordinates of the package
	Example call:
	---
	medicine_packages = detect_medicine_packages(maze_image)
	"""    
	medicine_packages = []

	##############	ADD YOUR CODE HERE	##############
	def shape_detection(No_of_sides): 

		if No_of_sides == 3 :
			return "cone"
		elif No_of_sides == 4 :
			return "cube"
		else:
			return "cylinder"


	def detect_colour(pixel_value):

		Green = np.array([0,255,0])
		Pink = np.array([180,0,255])
		Skyblue = np.array([255 ,255,0])
		Orange = np.array([0,127,255])
		if (pixel_value == Green).all() :
			return "Green"
		elif (pixel_value == Pink).all() :
			return "Pink"
		elif (pixel_value == Orange).all() :
			return "Orange"
		elif (pixel_value == Skyblue).all() :
			return "Skyblue"
		
	for px1 in range(105,605,100): #Accessing a particular shop

		shop_no = "Shop_" + str(int((px1-5)/100))
		shop_crop = image[105:195 , px1:(px1+90)]
		gray = cv2.cvtColor(shop_crop, cv2.COLOR_BGR2GRAY)
		_,thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
		contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
		shop_detail = []
		contours = list(contours)
		if len(contours) != 1: #Rejecting the empty shops
			
			contours.pop(0)  #Removing the boundary of cropped image contour

			for contour in contours: #INSIDE A SHAPE

				shape_detail = [] #All Info of a particular shape
				approx = cv2.approxPolyDP(contour,0.02*cv2.arcLength(contour,True),True)
				shape = shape_detection(len(approx))
				M = cv2.moments(contour)
				if M['m00'] != 0:
					cx = int(M['m10']/M['m00']) 
					cy = int(M['m01']/M['m00'])
				shape_detail += [shop_no , detect_colour(shop_crop[cy,cx]) , shape , [cx + px1 ,cy + 105]]
				shop_detail += [shape_detail]
			shop_detail.sort(key = lambda x : x[1]) #Sorting as per Colour

		medicine_packages += shop_detail

	##################################################

	return medicine_packages

def detect_arena_parameters(maze_image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) start_node : Start node which is mark in light green
	iii) end_node : End node which is mark in Purple
	iv) paths : list containing paths

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)

	Eg. arena_parameters={"traffic_signals":[], 
	                      "start_node": "E4", 
	                      "end_node":"A3", 
	                      "paths": {}}
	"""    
	arena_parameters = {}

    ##############	ADD YOUR CODE HERE	##############
	arena_parameters["traffic_signals"] , arena_parameters["start_node"] , arena_parameters["end_node"] = detect_all_nodes(maze_image)

	arena_parameters["paths"]=detect_paths_to_graph(maze_image)

	arena_parameters["horizontal_roads_under_construction"] = detect_horizontal_roads_under_construction(maze_image)
	
	arena_parameters["vertical_roads_under_construction"] = detect_vertical_roads_under_construction(maze_image)

	arena_parameters["medicine_packages"] = detect_medicine_packages(maze_image)

    ##################################################

	return arena_parameters

##############################################################
##############################################################

####################### ADD ARENA SETUP ######################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 4A for setting up the CoppeliaSim
Arena according to the configuration image in this section
"""

def place_packages(medicine_package_details, sim, all_models):
    """
	Purpose:
	---
	This function takes details (colour, shape and shop) of the packages present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The packages should be inserted only into the 
    designated areas in each shop as mentioned in the Task document.

    Functions from Regular API References should be used to set the position of the 
    packages.

	Input Arguments:
	---
	`medicine_package_details` :	[ list ]
                                nested list containing details of the medicine packages present.
                                Each element of this list will contain 
                                - Shop number as Shop_n
                                - Color of the package as a string
                                - Shape of the package as a string
                                - Centroid co-ordinates of the package			

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	
	Example call:
	---
	all_models = place_packages(medicine_package_details, sim, all_models)
	"""
    models_directory = os.getcwd()
    packages_models_directory = os.path.join(models_directory, "package_models")
    arena = sim.getObject('/Arena')    

####################### ADD YOUR CODE HERE #########################

    shops = {"Shop_1":[] , "Shop_2":[] ,"Shop_3":[] ,"Shop_4":[] ,"Shop_5":[]  }
    
    for package in medicine_package_details:
        
        if package[0] == "Shop_1":
            shops["Shop_1"] += [package]
        
        elif package[0] == "Shop_2":
            shops["Shop_2"] += [package]

        elif package[0] == "Shop_3":
            shops["Shop_3"] += [package]

        elif package[0] == "Shop_4":
            shops["Shop_4"] += [package]  

        elif package[0] == "Shop_5":
            shops["Shop_5"] += [package]  


    y_shop = -0.695
    ######  SHOP 1 ######  
    # x_shop = 0.84
    z = 0.015
    if len(shops["Shop_1"]) != 0:

        package_no = 1
        for package in shops["Shop_1"]:
            # print(package)
            x_shop = 0.84 - (package_no-1)*(0.08)
            package_no+=1
            package_name = package[1]+"_" + package[2]
            package_path = packages_models_directory+ "\\" + package_name+".ttm" 
            # print(package_path)
            # print(x_shop,"is x of shop")
            objectHandle = sim.loadModel(package_path)
            sim.setObjectParent(objectHandle,arena,False)
            sim.setObjectAlias(objectHandle,package_name)
            sim.setObjectPosition(objectHandle,-1,[x_shop,y_shop,z])
            all_models+=[objectHandle]

    ######  SHOP 2 ######
    if len(shops["Shop_2"]) != 0:
        package_no = 1
        for package in shops["Shop_2"]:
            # print(package)
            x_shop = 0.48 - (package_no-1)*(0.08)
            package_no+=1
            package_name = package[1]+"_" + package[2]
            package_path = packages_models_directory+ "\\" + package_name+".ttm" 
            # print(package_path)
            # print(x_shop,"is x of shop")
            objectHandle = sim.loadModel(package_path)
            sim.setObjectParent(objectHandle,arena,False)
            sim.setObjectAlias(objectHandle,package_name)
            sim.setObjectPosition(objectHandle,-1,[x_shop,y_shop,z])
            all_models+=[objectHandle]

    ###### SHOP 3 ######
    if len(shops["Shop_3"]) != 0:
        package_no = 1
        for package in shops["Shop_3"]:
            # print(package)
            x_shop = 0.12 - (package_no-1)*(0.08)
            package_no+=1
            package_name = package[1]+"_" + package[2]
            package_path = packages_models_directory+ "\\" + package_name+".ttm" 
            # print(package_path)
            # print(x_shop,"is x of shop")
            objectHandle = sim.loadModel(package_path)
            sim.setObjectParent(objectHandle,arena,False)
            sim.setObjectAlias(objectHandle,package_name)
            sim.setObjectPosition(objectHandle,-1,[x_shop,y_shop,z])
            all_models+=[objectHandle]

    ###### SHOP 4 ######
    if len(shops["Shop_4"]) != 0:
        package_no = 1
        for package in shops["Shop_4"]:
            # print(package)
            x_shop = -0.24 - (package_no-1)*(0.08)
            package_no+=1
            package_name = package[1]+"_" + package[2]
            package_path = packages_models_directory+ "\\" + package_name+".ttm" 
            # print(package_path)
            # print(x_shop,"is x of shop")
            objectHandle = sim.loadModel(package_path)
            sim.setObjectParent(objectHandle,arena,False)
            sim.setObjectAlias(objectHandle,package_name)
            sim.setObjectPosition(objectHandle,-1,[x_shop,y_shop,z])
            all_models+=[objectHandle]

    ###### SHOP 5 ######
    if len(shops["Shop_5"]) != 0:
        package_no = 1
        for package in shops["Shop_5"]:
            # print(package)
            x_shop = -0.60 - (package_no-1)*(0.08)
            package_no+=1
            package_name = package[1]+"_" + package[2]
            package_path = packages_models_directory+ "\\" + package_name+".ttm" 
            # print(package_path)
            # print(x_shop,"is x of shop")
            objectHandle = sim.loadModel(package_path)
            sim.setObjectParent(objectHandle,arena,False)
            sim.setObjectAlias(objectHandle,package_name)
            sim.setObjectPosition(objectHandle,-1,[x_shop,y_shop,z])
            all_models+=[objectHandle]

####################################################################

    return all_models

def place_traffic_signals(traffic_signals, sim, all_models):
    """
	Purpose:
	---
	This function takes position of the traffic signals present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The signal should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    signals.

	Input Arguments:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	None
	
	Example call:
	---
	all_models = place_traffic_signals(traffic_signals, sim, all_models)
	"""
    models_directory = os.getcwd()
    traffic_sig_model = os.path.join(models_directory, "signals", "traffic_signal.ttm" )
    arena = sim.getObject('/Arena')

####################### ADD YOUR CODE HERE #########################
    
    for signal in traffic_signals:
        
        x = 0.90 - (ord(signal[0])-65)*0.36
        y = -0.90 + (int(signal[1])-1)*0.36
        objectHandle = sim.loadModel(traffic_sig_model)
        sim.setObjectParent(objectHandle,arena,False)
        sim.setObjectAlias(objectHandle,"Signal_"+signal)
        sim.setObjectPosition(objectHandle,-1,[x,y,0.15588])
        all_models+=[objectHandle]

####################################################################

    return all_models

def place_start_end_nodes(start_node, end_node, sim, all_models):
    """
	Purpose:
	---
	This function takes position of start and end nodes present in 
    the arena and places them on the virtual arena. 
    The models should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    start and end nodes.

	Input Arguments:
	---
	`start_node` : [ string ]
    `end_node` : [ string ]
					

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
	"""
    models_directory = os.getcwd()
    start_node_model = os.path.join(models_directory, "signals", "start_node.ttm" )
    end_node_model = os.path.join(models_directory, "signals", "end_node.ttm" )
    arena = sim.getObject('/Arena')   

####################### ADD YOUR CODE HERE #########################
	# print(start_node , "is start node")
    # print(end_node , "is end node")

    x_start = 0.90 - (ord(start_node[0])-65)*0.36
    y_start = -0.90 + (int(start_node[1])-1)*0.36

    x_end = 0.90 - (ord(end_node[0])-65)*0.36
    y_end = -0.90 + (int(end_node[1])-1)*0.36

    objectHandle_start = sim.loadModel(start_node_model)
    sim.setObjectParent(objectHandle_start,arena,False)
    sim.setObjectAlias(objectHandle_start,"Start_Node")

    objectHandle_end = sim.loadModel(end_node_model)
    sim.setObjectParent(objectHandle_end,arena,False)
    sim.setObjectAlias(objectHandle_end,"End_Node")


    sim.setObjectPosition(objectHandle_start,-1,[x_start,y_start,0.15588])
    all_models+=[objectHandle_start]

    sim.setObjectPosition(objectHandle_end,-1,[x_end,y_end,0.15588])
    all_models+=[objectHandle_end]
    

####################################################################

    return all_models

def place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing horizontal roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    horizontal barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    horizontal barricades.

	Input Arguments:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    horiz_barricade_model = os.path.join(models_directory, "barricades", "horizontal_barricade.ttm" )
    arena = sim.getObject('/Arena')  

####################### ADD YOUR CODE HERE #########################
	# print(horizontal_roads_under_construction)
    for road in horizontal_roads_under_construction:

        barri_x = ord(road[0])
        barri_x = 0.72 - (barri_x-65)*0.36
        # print(barri_x-65)
        
        barri_y = -0.90 + (int(road[1])-1)*0.36

        # print(barri_x,"is x")
        # print(barri_y,"is y")
#  Horizontal_missing_node_D5_E5
        objectHandle_barri = sim.loadModel(horiz_barricade_model)
        sim.setObjectParent(objectHandle_barri,arena,False)
        sim.setObjectAlias(objectHandle_barri,"Horizontal_missing_road_"+road)

        sim.setObjectPosition(objectHandle_barri,-1,[barri_x,barri_y,0.024])

        all_models+=[objectHandle_barri]


####################################################################

    return all_models


def place_vertical_barricade(vertical_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing vertical roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    vertical barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    vertical barricades.

	Input Arguments:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    vert_barricade_model = os.path.join(models_directory, "barricades", "vertical_barricade.ttm" )
    arena = sim.getObject('/Arena')

####################### ADD YOUR CODE HERE #########################
	 # print(vertical_roads_under_construction)
    for road in vertical_roads_under_construction:

        barri_x = 0.90 - (ord(road[0])-65)*0.36
        
        # barri_x = 0.72 - (barri_x-65)*0.36
        # print(barri_x-65)
        barri_y = int(road[4])
        barri_y = -0.72 + (barri_y -2)*0.36

        # print(barri_x,"is x")
        # print(barri_y,"is y")

        objectHandle_barri = sim.loadModel(vert_barricade_model)
        sim.setObjectParent(objectHandle_barri,arena,False)
        sim.setObjectAlias(objectHandle_barri,"Vertical_missing_road_"+road)

        sim.setObjectPosition(objectHandle_barri,-1,[barri_x,barri_y,0.024])
        
        all_models+=[objectHandle_barri]

####################################################################

    return all_models

##############################################################
##############################################################

def path_planning(graph, start, end):

	"""
	Purpose:
	---
	This function takes the graph(dict), start and end node for planning the shortest path

	** Note: You can use any path planning algorithm for this but need to produce the path in the form of 
	list given below **

	Input Arguments:
	---
	`graph` :	{ dictionary }
			dict of all connecting path
	`start` :	str
			name of start node
	`end` :		str
			name of end node


	Returns:
	---
	`backtrace_path` : [ list of nodes ]
			list of nodes, produced using path planning algorithm

		eg.: ['C6', 'C5', 'B5', 'B4', 'B3']
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    

	backtrace_path=[]

	##############	ADD YOUR CODE HERE	##############
	# print(graph)
	def dijkshtra_algo(graph,start,goal):
		current_shortest_distance = {}
		track_predecessor = {}
		unseenNodes = graph
		infinity = 100000 
		

		for node in unseenNodes:
			current_shortest_distance[node] = infinity
		current_shortest_distance[start] = 0
		
		while unseenNodes:
			min_dist_to_node = None 

			for node in unseenNodes :
				# print(node)
				if min_dist_to_node is None:
					min_dist_to_node = node
				elif current_shortest_distance[node] < current_shortest_distance[min_dist_to_node]:
					min_dist_to_node = node

			path_options = graph[min_dist_to_node].items()

			for child_node , length in path_options:

				if length + current_shortest_distance[min_dist_to_node] < current_shortest_distance[child_node]:
					current_shortest_distance[child_node] = length + current_shortest_distance[min_dist_to_node]
					track_predecessor[child_node] = min_dist_to_node
			
			unseenNodes.pop(min_dist_to_node)

		currentNode = goal

		while currentNode != start :
			try:
				backtrace_path.insert(0,currentNode)
				currentNode = track_predecessor[currentNode]
			except KeyError:
				break
		backtrace_path.insert(0,start)
		return backtrace_path


	backtrace_path=dijkshtra_algo(graph,start,end)
	##################################################


	return backtrace_path


def paths_to_moves(paths, traffic_signal):

	"""
	Purpose:
	---
	This function takes the list of all nodes produces from the path planning algorithm
	and connecting both start and end nodes

	Input Arguments:
	---
	`paths` :	[ list of all nodes ]
			list of all nodes connecting both start and end nodes (SHORTEST PATH)
	`traffic_signal` : [ list of all traffic signals ]
			list of all traffic signals
	---
	`moves` : [ list of moves from start to end nodes ]
			list containing moves for the bot to move from start to end

			Eg. : ['UP', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN']
	
	Example call:
	---
	moves = paths_to_moves(paths, traffic_signal)
	"""    
	
	list_moves=[]

	##############	ADD YOUR CODE HERE	##############
	facing = "up"
	for i in range(len(paths)-1) :
		
		current_node = paths[i]
		next_node = paths[i+1]

		current_node_letter = str(current_node[0])
		next_node_letter = str(next_node[0])

		current_node_number = int(current_node[1])
		next_node_number = int(next_node[1])


		if current_node in traffic_signal:
			list_moves += ["WAIT_5"]
		
		if current_node_letter != next_node_letter:
			
			if ord(next_node_letter) - ord(current_node_letter) > 0:
				if facing == "up":
					list_moves += ["RIGHT"]
					
				elif facing == "right":
					list_moves += ["STRAIGHT"]
					
				elif facing == "left":
					list_moves += ["REVERSE"]
				
				elif facing == "down":
					list_moves += ["LEFT"]
				
				facing = "right"

			else:
				if facing == "up":
					list_moves += ["LEFT"]
					
				elif facing == "right":
					list_moves += ["REVERSE"]
					
				elif facing == "left":
					list_moves += ["STRAIGHT"]
				
				elif facing == "down":
					list_moves += ["RIGHT"]
				
				facing = "left"
		
		elif current_node_number > next_node_number :
			if facing == "up":
				list_moves += ["STRAIGHT"]
					
			elif facing == "right":
				list_moves += ["LEFT"]
				
			elif facing == "left":
				list_moves += ["RIGHT"]
			
			elif facing == "down":
				list_moves += ["REVERSE"]
			
			facing = "up"
		else:
			
			if facing == "up":
				list_moves += ["REVERSE"]
				
			elif facing == "right":
				list_moves += ["RIGHT"]
				
			elif facing == "left":
				list_moves += ["LEFT"]
			
			elif facing == "down":
				list_moves += ["STRAIGHT"]
			
			facing = "down"
	
	##################################################

	return list_moves

def perspective_transform(image,top_left,top_right,bottom_left,bottom_right):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array
    
    Example call:
    ---
    warped_image = perspective_transform(image)
    """   
    warped_image = [] 
#################################  ADD YOUR CODE HERE  ###############################
    detect_aruco = task_1b.detect_ArUco_details(image)
    #print(detect_aruco[0])
    if len(detect_aruco[0]) > 0:
    
        # top_left = detect_aruco[0][3]
        # top_right = detect_aruco[0][4]
        # bottom_left = detect_aruco[0][2]
        # bottom_right = detect_aruco[0][1]
            
        # top_left[0][0] = top_left[0][0] - 20
        # top_left[0][1] = top_left[0][1] - 20

        # top_right[0][0] = top_right[0][0] + 20
        # top_right[0][1] = top_right[0][1] - 20 

        # bottom_left[0][0] = bottom_left[0][0] - 20
        # bottom_left[0][1] = bottom_left[0][1] + 20

        # bottom_right[0][0] = bottom_right[0][0] + 20
        # bottom_right[0][1] = bottom_right[0][1] + 20 
            
        srcpts = np.array([bottom_left[0], top_left[0], top_right[0], bottom_right[0]] , np.float32)
        destpts = np.array([[0, 512], [0, 0], [512, 0], [512, 512]] , np.float32)

        resmatrix = cv2.getPerspectiveTransform(srcpts, destpts)
        warped_image = cv2.warpPerspective(image, resmatrix, (512, 512))
       # cv2.imshow("Warped Image" , warped_image)
    else :
        # print("Continue")
        return False
    # print("Continue")
    # return False
   
######################################################################################

    return warped_image


def transform_values(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]
    
    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.
    
    Example call:
    ---
    scene_parameters = transform_values(image)
    """   
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ###############################
    if image is not False:
        detect_aruco = task_1b.detect_ArUco_details(image)
        # print(detect_aruco[0])
        if 5 in detect_aruco[0].keys() :


            #print("Emulating")
            items_dictionary = detect_aruco[0]
            
            old_x = items_dictionary[5][0][0]
            old_y = items_dictionary[5][0][1]
            old_angle = items_dictionary[5][1]
            old_angle_abs = abs(old_angle)

            if old_angle > 0:
                coppelia_angle = -(180 - old_angle_abs)

            else :
                coppelia_angle = 180 - old_angle_abs

            new_x = -(old_x - 256)
            new_y = old_y - 256

            coppelia_x = (new_x*0.955/256)
            coppelia_y = (new_y*0.955/256)

        # print("Old coordinates were :", old_x , old_y)
        # print("Old angle", old_angle)
        # print("New angle", coppelia_angle)
        # print("New coordinates are :", new_x , new_y)
        # print("Transformed coordinates are :", coppelia_x , coppelia_y)

            scene_parameters += [coppelia_x,coppelia_y,coppelia_angle]
        else :
            scene_parameters=[]

    else:
        scene_parameters=[]
######################################################################################

    return scene_parameters

def set_values(scene_parameters,sim):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.

    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.
    
    Example call:
    ---
    set_values(scene_parameters)
    """   
    aruco_handle = sim.getObject('/alpha_bot')
    # cone_handle = sim.getObject('/Green_cone')
    package_tray_handle = sim.getObject('/tray_joint')
    # +5.1040e-02
#################################  ADD YOUR CODE HERE  ###############################
    if len(scene_parameters)!=0:
        # print("reached copp")
        coordiante_x = scene_parameters[0]
        coordiante_y = scene_parameters[1]

        angle = scene_parameters[2]
        
        sim.setObjectPosition(aruco_handle,-1,[coordiante_x,coordiante_y,0.0324])
        # sim.setObjectPosition(cone_handle,package_tray_handle,[0.0011001,0.02,-0.02])
        
        sim.setObjectOrientation(aruco_handle,-1,[1.57,(angle*2*3.14)/360,1.57])
        #(angle*2*3.14)/360
######################################################################################

    return None


def path_correction(facing , command):
    """
    Input:
    ---
    Takes facing and command as input arguments. Initially assuming that the facing of the bot is Up, a correction of the command
	given by the path planning algorithm is done using this function as the real time facing of the Alphabot may not be Up all the time.
    
	Returns:
    ---
    Returns the movement direction as per the command provided.
    
    Example call:
    ---
    path_correction(facing, command)
    
    """   
    if facing =="Up":
        return command
    elif facing == "Right":
        
        if command == "STRAIGHT":
            return "LEFT"
        
        if command == "LEFT":
            return "REVERSE"
        
        if command == "REVERSE":
            return "RIGHT"
        
        if command == "RIGHT":
            return "STRAIGHT"
        
    elif facing == "Left":
        
        if command == "STRAIGHT":
            return "RIGHT"
        
        if command == "LEFT":
            return "STRAIGHT"
        
        if command == "REVERSE":
            return "LEFT"
        
        if command == "RIGHT":
            return "REVERSE"
        
    elif facing == "Down":
        
        if command == "STRAIGHT":
            return "REVERSE"
        
        if command == "LEFT":
            return "RIGHT"
        
        if command == "REVERSE":
            return "STRAIGHT"
        
        if command == "RIGHT":
            return "LEFT"
	
def get_facing(last_node , second_last_node):
    """
    Input:
    ---
    Takes the last node and second last node as input arguments as strings.
    
    Returns:
    ---
    returns the current direction of the Alphabot.

    Example call:
    ---
    get_facing(last_node,second_last_node)
    """ 
    if(last_node[1]==second_last_node[1]):
        #x-axis
        if(ord(last_node[0])<ord(second_last_node[0])):
            facing = "Left"
        else:
            facing = "Right"
    elif (int(last_node[1])>int(second_last_node[1])):
        facing = "Down"
    else:
        facing = "Up"   

    # print(facing)
    return facing

def drop_packages(sim,package_handles_list,facing,drop_node):
	"""
    Input:
    ---
    `sim` : [ object ]
        ZeroMQ RemoteAPI object
	
	'package_handles_list': [ list ]
		List of handles of all the pckages to be dropped.

	'facing': [String]
		Shows the direction the bot is currently facing.

	'drop_node': [String]
		Basically an alphanumeric string e.g., B3, D5,etc. 
  
    Returns:
    ---
    Doesn't return anything specific but drops the packages to their drop locations.

    Example call:
    ---
    drop_packages(sim,package_handles_list,facing,drop_node)
    """ 
	node_x = 0.90 - (ord(drop_node[0])-65)*0.36
	node_y = -0.90 + (int(drop_node[1])-1)*0.36
	no_of_packages = len(package_handles_list)

	for i in range(no_of_packages):
		package_handle = package_handles_list[i]
		if(facing=="Right"):
			package_drop_x = node_x - 0.085
			package_drop_y = node_y - 0.225 + (0.03*i)
			sim.setObjectPosition(package_handle,-1,[package_drop_x,package_drop_y,0.015])


		if(facing=="Left"):
			package_drop_x = node_x + 0.085
			package_drop_y = node_y + 0.225 - (0.03*i)
			sim.setObjectPosition(package_handle,-1,[package_drop_x,package_drop_y,0.015])

			
		# print(facing)
		if(facing=="Up"):
			package_drop_x = node_x + 0.225 - (0.03*i)
			package_drop_y = node_y - 0.085
			sim.setObjectPosition(package_handle,-1,[package_drop_x,package_drop_y,0.015])


		if(facing=="Down"):
			package_drop_x = node_x - 0.225 + (0.03*i)
			package_drop_y = node_y + 0.085
			sim.setObjectPosition(package_handle,-1,[package_drop_x,package_drop_y,0.015])

			