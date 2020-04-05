# Hospital Environment mobile robot simulation using Coppelia Robotics (VREP) Simulator 

This repository is a bootstrap project to use Coppelia Robotics simulator (previously known as VREP) for simulating a mobile robot, *Pioneer P3-DX* , moving within a hopsital environment with a camera and ultrasonic sensors installed on it.

![](.\img\sim.jpg)

# Preparation

This project is based on **Coppelia Robotics Simulator V4** (Previously known as v-rep simulator).

All simulation has been run on Windows.

First you need to download latest version of CRS (CoppeliaRoboticsSimulator).

For this project we used following version, however you can check their website for latest version, and make sure take a look at updating CoppeliaSim section at end of this document.

https://www.coppeliarobotics.com/files/CoppeliaSim_Edu_V4_0_0_Setup.exe



- Install CRS v4 EDU Version using aforementioned link or updated version from its website
- Clone this repository to your a directory
  - Open CMD or Powershell
  - Change directory to your desired directory
    - `cd E:\Projects\CRSim\`
  - Clone this repository
    - `git clone https://github.com/HamedJafarzadeh/CoppeliaRoboticsPythonMobileRobotBootstrap`
- Open `Hospital.ttt` file with CRS and you would be able to see the hospital environment
- Click on `Start Simulation` button in toolbar and you should be able to see everything starts moving
- In the text box in bottom of CRS write following code to start remoteServer, so then we can connect our python code to CRS
  - `simRemoteApi.start(2323)`
  - Then you should be able to see a `1` printed in the console which means server started
- Make sure that your simulation is running and open `simpleTest.py` file and run it (In VSCode or any other IDE or CMD)
- You should be able to see camera output on the robot and robot should have started to go forward

