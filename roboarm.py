import serial
import time


def initRoboArm(comport="COM4"):
    arduino = serial.Serial(comport, 9600, timeout=.1)        
    return arduino
    

def runRoboArm(arduino, motorAngles):    
    counter=0
    result = ""
    for motorAngle in motorAngles :
        result += str(counter) + ":" + str(motorAngle)+"&"
        counter+=1

    print('Sending to arm: {}'.format(result))    
    arduino.write(result.encode())

    time.sleep(3)    
    messageFromArm = arduino.read_all()
    #print("-------Message from Arm-------")
    #print(messageFromArm)
    #print("-------Message from Arm-------")
    
    
    


#arduino = initRoboArm('COM3')
#for i in range(1, 170,20):    
#    runRoboArm(arduino,[i,0,0])




#print("Done!")