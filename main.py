import serial
import binascii
from CalcLidarData import CalcLidarData
import matplotlib.pyplot as plt
import math

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='polar')
ax.set_title('lidar (exit: Key E)',fontsize=18)


plt.connect('key_press_event', lambda event: exit(1) if event.key == 'e' else None)

ser = serial.Serial(port='/dev/tty.usbserial-0001',
                    baudrate=230400,
                    timeout=5.0,
                    bytesize=8,
                    parity='N',
                    stopbits=1)

tmpString = ""
lines = list()
angles = list()
distances = list()

i = 0
while True:
    loopFlag = True
    flag2c = False

    if(i % 40 == 39):
        if('line' in locals()):
            line.remove()
        line = ax.scatter(angles, distances, c="pink", s=5)

        ax.set_theta_offset(math.pi / 2)
        plt.pause(0.01)
        angles.clear()
        distances.clear()
        i = 0
        
        # get the furthest points and their angles within 90 degrees from 0 degrees
        max_angle = -math.pi/2
        min_angle = math.pi/2
        max_distance = 0

        for j in range(len(angles)):
            if angles[j] > math.pi/2 or angles[j] < -math.pi/2:
                continue

            if distances[j] > max_distance:
                max_distance = distances[j]
                max_angle = angles[j]
            
            if angles[j] > 0 and angles[j] < min_angle:
                min_angle = angles[j]
            elif angles[j] < 0 and angles[j] > max_angle:
                max_angle = angles[j]

        plt.text(0,0,"Furthest points within 180 degrees:\nMax distance:, {max_distance}, at angle, {max_angle}*180/math.pi, degrees", fontsize=12)
        # print("Furthest points within 180 degrees:")
        # print("Max distance:", max_distance, "at angle", max_angle*180/math.pi, "degrees")
        # print("Min angle:", min_angle*180/math.pi, "degrees")
        # print("Max angle:", max_angle*180/math.pi, "degrees")

    while loopFlag:
        b = ser.read()
        tmpInt = int.from_bytes(b, 'big')
        
        if (tmpInt == 0x54):
            tmpString +=  b.hex()+" "
            flag2c = True
            continue
        
        elif(tmpInt == 0x2c and flag2c):
            tmpString += b.hex()

            if(not len(tmpString[0:-5].replace(' ','')) == 90 ):
                tmpString = ""
                loopFlag = False
                flag2c = False
                continue

            lidarData = CalcLidarData(tmpString[0:-5])
            angles.extend(lidarData.Angle_i)
            distances.extend(lidarData.Distance_i)
                
            tmpString = ""
            loopFlag = False
        else:
            tmpString += b.hex()+" "
        
        flag2c = False
    
    i +=1

ser.close()

