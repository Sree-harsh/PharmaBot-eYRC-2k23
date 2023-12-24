# Pharma Robot - [eYantra Robotics Competition](https://www.e-yantra.org/eyrc) Team PB#1182 

## Overview

This repository contains the code and documentation for the Pharma Robot developed for the [eYantra](https://www.e-yantra.org/eyrc) Robotics Competition 2k23 at IIT Bombay by Team PB#1182. The Pharma Robot is designed to address the issue of efficient medicine delivery in a smart city setting. The competition aims to explore autonomous robotics solutions to enhance the delivery of medicine packets from pharmacies to designated locations within a smart city arena.
<p align="center">
<img width="550" alt="1" src="https://github.com/Sree-harsh/PharmaBot-eYRC-2k23/assets/98598677/b339a841-0978-489b-85ae-5bc6954491ba">
</p>   
<p align="center"><strong>#1182's Pharma Bot</strong></p>

| Coppeliasim Emulation | OverHead Camera Feed |
| :---:         |          :---: |
|<img width="550" alt="1" src="https://github.com/Sree-harsh/PharmaBot-eYRC-2k23/assets/98598677/1d7960b1-d372-44ec-879e-e2302250f8f3">   | <img width="400" alt="2" src="https://github.com/Sree-harsh/PharmaBot-eYRC-2k23/assets/98598677/25e6a877-376d-46a2-bce8-33d31d413294">     | 

<h1 align="center"><strong>Coppeliasim Emulation</strong></h1>

![gif](/assets/1.gif)

<h1 align="center"><strong>Node Detection on Rpi</strong></h1>

![gif](/assets/2.gif)





## Table of Contents
- [Code Structure](#code-structure)
- [Rulebook](#rule-book)
- [Challenges](#key-challenges)
- [Theme Run](#theme-run)
- [Acknowledgments](#acknowledgments)

## Code Structure

The Repository contains 5 well-commented and maintained files :-
1. [Theme_functions](/PB_1182_PB_theme_functions.py) - Contains all the functions used in the code base.
2. [Raspberrypicode](/PB_1182_Raspberrypicode.py) - Consists of the Node detection and line following logic running on the Raspberrypi 3B. 
3. [task_1b.py](/task_1b.py) - Contains aruco detection code blocks .
4. [task_6.py](/task_6.py) - The entire server side code base and logics used in the theme which were submitted in task 6 (last task before finale).
5. [task_6_scene.zip](/task_6_scene.zip):- Contains the Coppeliasim scene which the team presented in the Finals.

## Rule Book

The [Rulebook](assets/rulebook.pdf) contains all the guidelines and deliverables the robot had to perform at the finals @IIT-Bombay. It also contains an in-depth explanation of the theme. 


## Key Challenges

**1. Autonomous Navigation:** Participants are required to develop robots capable of autonomously navigating a 5x5 grid representing a smart city. The robot must move through the grid, avoiding       obstacles such as roads under construction and responding to traffic signals.
   
**2. Image Processing:** The competition involves extracting critical information from test images using OpenCV and Python. This includes identifying start and end nodes, locations of traffic        signals, details of medicine packages in medical shops, and roads under construction.

**3. Algorithm Building:** Teams need to build algorithms for tasks such as line following, path planning, and robotic navigation. Time is a crucial factor, and efficient algorithms are essential to complete assigned tasks quickly.

**4. CoppeliaSim Simulation:** The virtual representation of the arena in CoppeliaSim adds another layer of complexity. Teams must set up the virtual arena based on the extracted information from test images, incorporating 3D models for buildings, trees, traffic signals, and more.

**5. Robot Emulation:** The AlphaBot, equipped with a web camera and RGB LEDs, is used for line following and indicating package pickup and delivery. The robot's motions are emulated in CoppeliaSim, and teams must ensure synchronization between the real and virtual environments.

**6. Package Pickup and Delivery:** The robot must "pick up" medicine packages from medical shops and "deliver" them to specified locations. The pickup and delivery process is indicated using RGB LEDs, and the robot must adhere to the constraints of carrying a maximum of three packages at a time.

Overall, the Pharma Bot theme combines elements of image processing, algorithm development, simulation, and hardware integration to simulate a real-world scenario of autonomous medicine delivery in a smart city, emphasizing efficiency, accuracy, and creativity. The competition encourages participants to showcase their skills in robotics, computer vision, and algorithmic design.

## Theme Run 

Here is the [link](https://www.youtube.com/live/7L1HzlAIuvg?si=YzjcJKyt8zgEEI6j&t=21519) to the video of the final theme run performed at IIT-Bombay.

## Acknowledgments

Team Members - 
1. [Phanendra Sreeharsh Kowdodi](https://github.com/Sree-harsh)
2. [Sai Ram Senapati](https://github.com/Sai1Ram)
3. [Raj Pattnaik](https://github.com/Tannic-Paprika)
4. [Ashish Kumar Sahu](https://github.com/ashishedge)

The e-Yantra theme instructors, with their expertise, have been pivotal in resolving our queries, while the seniors' unwavering support has been a cornerstone in our progress throughout the competition.

