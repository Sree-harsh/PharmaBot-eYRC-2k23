'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 6 of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 1182 ]
# Author List:		[ Phanendra Sreeharsh Kowdodi , Sai Ram Senapati , Ashish Kumar Sahu , Raj Pattnaik ]
# Filename:			task_6.py
# Functions:		
# 					[ task_6_implementation , go_to_shop_read_qr , main_logic ]

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
import random
from threading import Thread
##############################################################

## Import PB_theme_functions code
try:
	pb_theme = __import__('PB_theme_functions')

except ImportError:
	print('\n[ERROR] PB_theme_functions.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure PB_theme_functions.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your PB_theme_functions.py throwed an Exception, kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()

def task_6_implementation(sim):
	"""
	Purpose:
	---
	This function contains the implementation logic for task 6 

	Input Arguments:
	---
    `sim` : [ object ]
            ZeroMQ RemoteAPI object

	Returns:
	---
	NA

	Logic :
	--- 
	- This Function is responsible for running two threads 1) Main Thread performing coppeliasim emulation
														   2) Thread t1 executing the main logic via socket communication

	- The Main Thread of emulation is executed untill thread t1 is alive i.e till the main logic is executing.
														   
	Example call:
	---
	task_6_implementation(sim)
	"""

	##################	ADD YOUR CODE HERE	##################
	shops = {"Shop_1":[] , "Shop_2":[] ,"Shop_3":[] ,"Shop_4":[] ,"Shop_5":[]  }

	for package in medicine_package_details:  #Segregating Packages according to their respective shops
		
		if package[0] == "Shop_1":
			shops["Shop_1"] += [package[1]+"_"+package[2]]
		
		elif package[0] == "Shop_2":
			shops["Shop_2"] += [package[1]+"_"+package[2]]

		elif package[0] == "Shop_3":
			shops["Shop_3"] += [package[1]+"_"+package[2]]

		elif package[0] == "Shop_4":
			shops["Shop_4"] += [package[1]+"_"+package[2]]  

		elif package[0] == "Shop_5":
			shops["Shop_5"] += [package[1]+"_"+package[2]]  
	
	packages_on_bot_data = {} 

	for shop in shops: #Activating all Qr-Codes
		
		shop_no = int(shop[5])
			
		if len(shops[shop]) > 0:
			qr_handle = sim.getObject('/qr_plane_'+str(shop_no))	
			sim.setObjectInt32Param(qr_handle,10,1)

	def go_to_shop_read_qr(sim,shop_no,current_node,facing,packages_on_bot_data,led_data):
		"""
		Function Name: go_to_shop_qr

		Input: 
		---
		`sim` : [ object ]
            	ZeroMQ RemoteAPI object
		'Shop_no' : [ int ] -- Shop number to which the robot has to reach to scan QR at PN.
		
		'current_node' : [ int ] -- The Node at which the robot is present during function call. 

		'facing' : [ string ] -- The facing of the Robot w.r.t the top of arena (One of "Up" , "Down" , "Left" , "Right").

		'packages_on_bot_data' : [ dictionary ] -- Information regarding packages present on Robot (Eg - {"Orange_cone":"F5","Pink_cube":"F4"}). 

		'led_data' : [ dictionary ] -- Information of Leds ON at the current time (Eg - {"1":"Orange","2":"Pink}).

		Output: 
		---
		'current_node' = [ string ] -- The Node at which the robot is present after the completion of this function.

		'facing' = [ string ] -- The facing of the robot w.r.t the top of arena after the completion of this function.

	    Logic:-- The Robot goes to the PN of the Shop number provided as input argument and picks up the packages 
	    	  -- If the number of packages picked up are less that 3 then it would move to the PN of the next Shop to pick packages
		      -- After Picking up 3 packages , the robot would then drop them to their drop locations as scanned from the QR code at their respective PNs
		      
		      *** The core concept used here is - Recursion ***

		---      
		Example Call: 
		
		go_to_shop_read_qr(sim,2,"B6","Up",{"Orange_cone":"F5","Pink_cube":"F4"},{"1":"Orange","2":"Pink}):

		"""

		shop_name = "Shop_"+str(shop_no)
		
		if len(shops[shop_name]) == 0:
			pass

		else:
			packages_in_shop = shops[shop_name]
			qr_message = None 
			package_handles_list = []
			go_to_node = chr(shop_no+65)+"2" 
			detected_arena_parameters = pb_theme.detect_arena_parameters(config_img)	
			paths = detected_arena_parameters['paths']
			backtrace_path = pb_theme.path_planning(paths,current_node,go_to_node)
			list_moves = pb_theme.paths_to_moves(backtrace_path,traffic_signals)
			original_command = list_moves[0]
			correction = pb_theme.path_correction(facing,original_command)
			list_moves[0]=correction

			i = 1 #Variable to help printing node names when reached

			for move in list_moves: # Sending Commands to Raspberrypi
				
				pb_theme.send_message_via_socket(connection_2,move)
				if move == "WAIT_5":
					statement = "WAIT AT " + backtrace_path[i-1]
					print(statement)
					pb_theme.send_message_via_socket(connection_1,statement)

				while True:
					message = pb_theme.receive_message_via_socket(connection_2)
					if message == "DONE" and move == "WAIT_5":
						break

					elif message == "DONE" :
						statement = "ARRIVED AT " + backtrace_path[i]
						print(statement)
						pb_theme.send_message_via_socket(connection_1,statement)
						i+=1
						break

			facing = pb_theme.get_facing(backtrace_path[-1],backtrace_path[-2]) # Getting facing after reaching PN
			current_node = backtrace_path[-1]

			# print(facing , "Is is new facing at PN")
			# print("Reached PN , Reading Qr")

			while qr_message is None: #Reading the qr using a correction algo to account for the errors in emulation

				try :
					time.sleep(1)
					visionSensorHandle = sim.getObject("/alpha_bot/Vision_sensor")
					img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)  #Capturing image from vision sensor
					img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)		
					img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0) 
					barcodes = decode(img)
					bdata= barcodes[0].data.decode("utf-8")
					qr_message= f"{bdata}"
					# print(qr_message)

				except  :

					# print("Please place qr properly")
					
					pb_theme.send_message_via_socket(connection_2,'CORRECT_BACK')
					while True:
						message = pb_theme.receive_message_via_socket(connection_2)
						if message == "DONE" :
							break

				
			qr_data = eval(qr_message)
			# drop_data.update(qr_data)


			colours_list = ["Orange", "Skyblue", "Green", "Pink"]
			shapes_list = ["cone","cylinder","cube"]

			package_tray_handle = sim.getObject('/alpha_bot/tray_joint/package_tray')

			package_no = len(packages_on_bot_data)+1 #Initializing a variable for number of packages
				
			#Package pickup in coppeliasim

			for package in qr_data.keys():  

				for i in range(len(package)): #Extracting package colour from qr data
					sub_string = package[0:i]
					if(sub_string in colours_list):
						package_colour = sub_string
						break
				
				for i in range(len(package)): #Extracting package shape from qr data
					sub_string = package[-(i+1):]
					if(sub_string in shapes_list):
						package_shape = sub_string
						break

				# print(package_colour, "is colour")
				# print(package_shape, "is shape")

				led_message = "LED_"+str(package_no)+"_"+package_colour # Creating a custom message to help pi light the LEDs
				# print(led_message,"is message sent to led to light ",package)
				pb_theme.send_message_via_socket(connection_2, led_message)
				led_data[package_no] = package_colour
				# print(led_data)

				package_handle = sim.getObjectHandle(package)
				sim.setObjectParent(package_handle,package_tray_handle,False)
				# package_handles_list += package_handle

				if package_no == 1:
					#Topleft
					x = 0.001089
					y = 0.019800
					sim.setObjectPosition(package_handle, package_tray_handle,[x,y,-0.019800])
					sim.setObjectOrientation(package_handle,-1,[0,0,-1.57])
					print("PICKED UP:",package_colour,"," ,package_shape,",", qr_data[package])
					packages_in_shop.remove(package_colour+"_"+package_shape)
					pass
				elif package_no == 2 :
					#TopRight
					x = 0.001089
					y = -0.019800
					sim.setObjectPosition(package_handle, package_tray_handle,[x,y,-0.019800])
					sim.setObjectOrientation(package_handle,-1,[0,0,-1.57])
					print("PICKED UP:",package_colour,",",package_shape,",", qr_data[package])
					packages_in_shop.remove(package_colour+"_"+package_shape)
					pass
				else:
					#Between
					x = 0.0010890
					y = 0.00000027537
					sim.setObjectPosition(package_handle, package_tray_handle,[x,y,+0.019796])
					sim.setObjectOrientation(package_handle,-1,[0,0,-1.57])
					print("PICKED UP:",package_colour,",",package_shape,",", qr_data[package])
					packages_in_shop.remove(package_colour+"_"+package_shape)
					pass

				package_no += 1

			packages_on_bot_data.update(qr_data)
			shops[shop_name] = packages_in_shop
			# print(shops)
			
			# Condition to recursion by checking whether there are 3 packages on robot or not . If not , the same function is called again by an increment in shop number

			if len(packages_on_bot_data) < 3 :
				current_node , facing = go_to_shop_read_qr(sim,shop_no+1,current_node,facing,packages_on_bot_data,led_data)
			else:

				# Dropping all 3 packages at once

				packages_dropped = 0
				packages_on_bot_data = {k: v for k, v in sorted(packages_on_bot_data.items(), key=lambda item: item[1])}

				for package in packages_on_bot_data.keys():
					

					for i in range(len(package)): #Extracting package colour from qr data
						sub_string = package[0:i+1]
						if(sub_string in colours_list):
							package_colour = sub_string
							break

					for i in range(len(package)): #Extracting package shape from qr data
						sub_string = package[-(i+1):]
						if(sub_string in shapes_list):
							package_shape = sub_string
							break

					drop_node = packages_on_bot_data[package]
					detected_arena_parameters = pb_theme.detect_arena_parameters(config_img)	
					paths = detected_arena_parameters['paths']
					backtrace_path = pb_theme.path_planning(paths,current_node,drop_node)
					list_moves = pb_theme.paths_to_moves(backtrace_path,traffic_signals)
					original_command = list_moves[0]
					correction = pb_theme.path_correction(facing,original_command)
					list_moves[0]=correction

					# print(list_moves)
					# print(backtrace_path,"is path to drop location")

					i = 1

					for move in list_moves: # Sending Commands to the Raspberrypi
						
						pb_theme.send_message_via_socket(connection_2,move)
						if move == "WAIT_5":
							statement = "WAIT AT " + backtrace_path[i-1]
							print(statement)
							pb_theme.send_message_via_socket(connection_1,statement)

						while True:
							message = pb_theme.receive_message_via_socket(connection_2)
							if message == "DONE" and move == "WAIT_5":
								break

							elif message == "DONE" :
								statement = "ARRIVED AT " + backtrace_path[i]
								print(statement)
								pb_theme.send_message_via_socket(connection_1,statement)
								i+=1
								break
					
					# print("Reached drop location , Dropping package")

					facing = pb_theme.get_facing(backtrace_path[-1],backtrace_path[-2])
					current_node = backtrace_path[-1]
					# print(facing , "Is is new facing at drop location")
					package_handle = sim.getObjectHandle(package)
					package_handles_list = [package_handle]
					sim.setObjectParent(package_handle,sim.getObjectHandle('Arena'),False)
					pb_theme.drop_packages(sim,package_handles_list,facing,drop_node)
					sim.setObjectOrientation(package_handle,-1,[0,0,-1.57])
					packages_dropped+=1

					for led_no in led_data:  # Turning off the led of the dropped package 
						colour = led_data[led_no]
						if colour == package_colour:
							led_number_to_off = led_no
							break
					
					pb_theme.send_message_via_socket(connection_2, "LED_"+str(led_number_to_off)+"_Off")
					led_data.pop(led_number_to_off)
					# print(led_data , "after turning off an led")
					print("DELIVERED:",package_colour,",",package_shape,", PACKAGE AT",packages_on_bot_data[package])
					
				packages_on_bot_data = {}
				pass

			
			return current_node , facing		
		return current_node , facing


	def main_logic(): #Function for socket communication

		"""
		Function Name: main_logic
		Input: 
		---
		NA

		Output: 
		---
		NA

	    Logic:-- The function go_to_shop_read_qr is recursively called untill all the packages are picked up and dropped smartly.
	    	  -- After dropping all packages, the robot plans its path to the end node.
		      -- Upon reaching ,  End of Task is indicated by lighting all 3 LEDs as White.
		      
		---      
		Example Call: 
		
		main_logic()

		"""
		
		coppelia_client1 = RemoteAPIClient()
		sim1 = coppelia_client1.getObject('sim')

		current_node = start_node
		facing = "Up"

		packages_on_bot_data = {}
		led_data = {}

		for shop in shops:
			shop_no = int(shop[5])
			current_node , facing = go_to_shop_read_qr(sim1,shop_no,current_node,facing,packages_on_bot_data,led_data)

		detected_arena_parameters = pb_theme.detect_arena_parameters(config_img)	
		paths = detected_arena_parameters['paths']
		backtrace_path = pb_theme.path_planning(paths,current_node,end_node)
		list_moves = pb_theme.paths_to_moves(backtrace_path,traffic_signals)
		original_command = list_moves[0]
		correction = pb_theme.path_correction(facing,original_command)
		list_moves[0]=correction

		# print(list_moves)
		# print(backtrace_path,"is path to the end node")

		i = 1

		for move in list_moves: # Sending Commands to the Raspberrypi
			
			pb_theme.send_message_via_socket(connection_2,move)
			if move == "WAIT_5":
				statement = "WAIT AT " + backtrace_path[i-1]
				print(statement)
				pb_theme.send_message_via_socket(connection_1,statement)

			while True:
				message = pb_theme.receive_message_via_socket(connection_2)
				if message == "DONE" and move == "WAIT_5":
					break

				elif message == "DONE" :
					statement = "ARRIVED AT " + backtrace_path[i]
					print(statement)
					pb_theme.send_message_via_socket(connection_1,statement)
					i+=1
					break
		# print("Reached End Node")

		pb_theme.send_message_via_socket(connection_2, "LED_1_White")
		time.sleep(0.1)
		pb_theme.send_message_via_socket(connection_2, "LED_2_White")
		time.sleep(0.1)
		pb_theme.send_message_via_socket(connection_2, "LED_3_White")
		time.sleep(2)
		print("End of Task")

	##### Main Tread implementing the coppeliasim emulation #####

	task_1b = __import__('task_1b')
	video = cv2.VideoCapture(0)	
	
	# Giving Inputs of the coordinates of corners as recieved from another script 
	top_left , top_right , bottom_left , bottom_right = [[1,2],1] , [[1,2],1] , [[1,2],1] ,[[1,2],1] # Giving Garbage Values to define lists
	top_left[0][0] = 136 #-20
	top_left[0][1] = 67 #- 20

	top_right[0][0] = 487 #+ 20
	top_right[0][1] = 33  #- 20

	bottom_left[0][0] = 173 #- 20
	bottom_left[0][1] = 422 #+ 20

	bottom_right[0][0] = 523 #+ 20
	bottom_right[0][1] = 382 #+ 20

	
	t1 = Thread(target=main_logic) #Starting the thread for socket communication
	t1.start()

	while True : #The Coppeliasim Emulation Code

		ret,frame = video.read()	
		warped_image = pb_theme.perspective_transform(frame,top_left,top_right,bottom_left,bottom_right)	
		scene_parameters = pb_theme.transform_values(warped_image)	
		# print(scene_parameters)
		pb_theme.set_values(scene_parameters,sim)
		# print("Emulating")

		cv2.imshow("Frame",warped_image)

		if cv2.waitKey(1) == ord('q'):
			break
		if not t1.is_alive(): # Checking if the main logic has completed or not 
			#pb_theme.send_message_via_socket(connection_2, "END")
			break
	

	pb_theme.send_message_via_socket(connection_2, "END")
	cv2.destroyAllWindows()

	##########################################################

if __name__ == "__main__":
	
	host = ''
	port = 5050


	## Set up new socket server
	try:
		server = pb_theme.setup_server(host, port)
		print("Socket Server successfully created")

		# print(type(server))

	except socket.error as error:
		print("Error in setting up server")
		print(error)
		sys.exit()


	## Set up new connection with a socket client (PB_task3d_socket.exe)
	try:
		print("\nPlease run PB_socket.exe program to connect to PB_socket client")
		connection_1, address_1 = pb_theme.setup_connection(server)
		print("Connected to: " + address_1[0] + ":" + str(address_1[1]))

	except KeyboardInterrupt:
		sys.exit()


	# ## Set up new connection with a socket client (socket_client_rgb.py)
	try:
		print("\nPlease connect to Raspberry pi client")
		connection_2, address_2 = pb_theme.setup_connection(server)
		print("Connected to: " + address_2[0] + ":" + str(address_2[1]))

	except KeyboardInterrupt:
		sys.exit()

	## Send setup message to PB_socket
	pb_theme.send_message_via_socket(connection_1, "SETUP")

	message = pb_theme.receive_message_via_socket(connection_1)
	## Loop infinitely until SETUP_DONE message is received
	while True:
		if message == "SETUP_DONE":
			break
		else:
			print("Cannot proceed further until SETUP command is received")
			message = pb_theme.receive_message_via_socket(connection_1)


	try:
		
		# obtain required arena parameters
		image_filename = os.path.join(os.getcwd(), "config_image.png")
		config_img = cv2.imread(image_filename)
		detected_arena_parameters = pb_theme.detect_arena_parameters(config_img)			
		medicine_package_details = detected_arena_parameters["medicine_packages"]
		traffic_signals = detected_arena_parameters['traffic_signals']
		start_node = detected_arena_parameters['start_node']
		end_node = detected_arena_parameters['end_node']
		horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
		vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction']

		# print("Medicine Packages: ", medicine_package_details)
		# print("Traffic Signals: ", traffic_signals)
		# print("Start Node: ", start_node)
		# print("End Node: ", end_node)
		# print("Horizontal Roads under Construction: ", horizontal_roads_under_construction)
		# print("Vertical Roads under Construction: ", vertical_roads_under_construction)
		# print("\n\n")

	except Exception as e:
		print('Your task_1a.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	try:

		## Connect to CoppeliaSim arena
		coppelia_client = RemoteAPIClient()
		sim = coppelia_client.getObject('sim')

		## Define all models
		all_models = []

		## Setting up coppeliasim scene
		print("[1] Setting up the scene in CoppeliaSim")
		all_models = pb_theme.place_packages(medicine_package_details, sim, all_models)
		all_models = pb_theme.place_traffic_signals(traffic_signals, sim, all_models)
		all_models = pb_theme.place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
		all_models = pb_theme.place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
		all_models = pb_theme.place_start_end_nodes(start_node, end_node, sim, all_models)
		print("[2] Completed setting up the scene in CoppeliaSim")
		print("[3] Checking arena configuration in CoppeliaSim")

	except Exception as e:
		print('Your task_4a.py throwed an Exception, kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	pb_theme.send_message_via_socket(connection_1, "CHECK_ARENA")

	## Check if arena setup is ok or not
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)

		if message == "ARENA_SETUP_OK":
			print("[4] Arena was properly setup in CoppeliaSim")
			break
		elif message == "ARENA_SETUP_NOT_OK":
			print("[4] Arena was not properly setup in CoppeliaSim")
			connection_1.close()
			# connection_2.close()
			server.close()
			sys.exit()
		else:
			pass

	## Send Start Simulation Command to PB_Socket
	pb_theme.send_message_via_socket(connection_1, "SIMULATION_START")
	
	## Check if simulation started correctly
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)

		if message == "SIMULATION_STARTED_CORRECTLY":
			print("[5] Simulation was started in CoppeliaSim")
			break

		if message == "SIMULATION_NOT_STARTED_CORRECTLY":
			print("[5] Simulation was not started in CoppeliaSim")
			sys.exit()

	# send_message_via_socket(connection_2, "START")

	task_6_implementation(sim)


	## Send Stop Simulation Command to PB_Socket
	pb_theme.send_message_via_socket(connection_1, "SIMULATION_STOP")

	## Check if simulation started correctly
	message = pb_theme.receive_message_via_socket(connection_1)
	while True:
		# message = pb_theme.receive_message_via_socket(connection_1)

		if message == "SIMULATION_STOPPED_CORRECTLY":
			print("[6] Simulation was stopped in CoppeliaSim")
			break

		if message == "SIMULATION_NOT_STOPPED_CORRECTLY":
			print("[6] Simulation was not stopped in CoppeliaSim")
			sys.exit()