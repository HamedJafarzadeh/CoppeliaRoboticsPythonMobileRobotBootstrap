# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import sim
    import numpy as np
    import matplotlib.pyplot as mpl
    import time
    import math
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time

print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',2323,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:
    print ('Connected to remote API server')

    # Now try to retrieve data in a blocking fashion (i.e. a service call):
    res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)

    # Get Camera Handle
    errorCode,visionSensorHandle = sim.simxGetObjectHandle(clientID,'vcam',sim.simx_opmode_oneshot_wait)

    # Get Motors Handle
    errorCode,leftMotorHandle = sim.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',sim.simx_opmode_oneshot_wait)
    errorCode,rightMotorHandle = sim.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',sim.simx_opmode_oneshot_wait)


    if res==sim.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
    else:
        print ('Remote API function call returned with error code: ',res)

    # Now retrieve streaming data (i.e. in a non-blocking fashion):
    startTime=time.time()
    sim.simxGetIntegerParameter(clientID,sim.sim_intparam_mouse_x,sim.simx_opmode_streaming) # Initialize streaming
    while time.time()-startTime < 20:

        #Get the image of vision sensor
        errprCode,resolution,image = sim.simxGetVisionSensorImage(clientID,visionSensorHandle,0,sim.simx_opmode_streaming)
        time.sleep(0.1)
        errprCode,resolution,image = sim.simxGetVisionSensorImage(clientID,visionSensorHandle,0,sim.simx_opmode_buffer)
        
        #Process the image to the format (512,512,3)
        sensorImage = []
        sensorImage = np.array(image,dtype = np.uint8)
        sensorImage.resize([resolution[0],resolution[1],3])
        
        #Use matplotlib.imshow to show the image
        mpl.imshow(sensorImage,origin='lower')
        mpl.pause(0.05)
        
        #Set Motors Speed
        sim.simxSetJointTargetVelocity(clientID,leftMotorHandle,3,sim.simx_opmode_oneshot) # Speed is Deg/Sec
        sim.simxSetJointTargetVelocity(clientID,rightMotorHandle,3,sim.simx_opmode_oneshot) # Speed is Deg/Sec

        returnCode,data=sim.simxGetIntegerParameter(clientID,sim.sim_intparam_mouse_x,sim.simx_opmode_buffer) # Try to retrieve the streamed data
        if returnCode==sim.simx_return_ok: # After initialization of streaming, it will take a few ms before the first value arrives, so check the return code
            print ('Mouse position x: ',data) # Mouse position x is actualized when the cursor is over CoppeliaSim's window
        time.sleep(0.005)

    # Now send some data to CoppeliaSim in a non-blocking fashion:
    sim.simxAddStatusbarMessage(clientID,'Hello CoppeliaSim!',sim.simx_opmode_oneshot)

    # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(clientID)

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
