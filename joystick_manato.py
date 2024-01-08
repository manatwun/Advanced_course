# Copyright (c) 2021 Takenoshin
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import time
import threading 
import socket
import sys
from decimal import Decimal
import pygame
import csv
import datetime

#Create a UDP socket
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1' , 8889)

#command-mode : 'command'
socket.sendto('command'.encode('utf-8'),tello_address)
print ('start')
 
socket.sendto('takeoff'.encode('utf-8'),tello_address)
print ('takeoff')
# socket.sendto('left 20'.encode('utf-8'),tello_address)
# time.sleep(5)
# socket.sendto('forward 20'.encode('utf-8'),tello_address)
# time.sleep(5)
# socket.sendto('flip l'.encode('utf-8'),tello_address)
# time.sleep(5)

def main():
    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    try:
        

        dt_now = datetime.datetime.now()
        csvname = 'controller-{date}.csv'.format(date = dt_now)

        with open(csvname, 'w') as csv_file:
            fieldnames = ['LEFT Y', 'RIGHT X', 'RIGHT Y', 'L1', 'R1']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

        n_axe = joy.get_numaxes()
        print("Joystick Name: " + joy.get_name())
        print("Number of Axis : " + str(n_axe))

        pygame.event.get()
        s_axe = [0.0] * n_axe

        with open(csvname, 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            while True:
                # Axes
                for i in range(n_axe):
                    #s_axe[i] = round(joy.get_axis(i), 2)
                    s_axe[i] = float(Decimal(joy.get_axis(i)).quantize(Decimal('0.01')))
                print("Axe", end="")
                print(s_axe)
                pygame.event.get()
                
                # s_axe = [左ステX,左ステY,右ステX,右ステY,ZL(defaul:-1.0),ZR(defaul:-1.0)]
                if s_axe[1] < -0.2:
                    text = 'speed {up_value}'.format(up_value = int(s_axe[1] * -10+10))
                    socket.sendto(text.encode('utf-8'),tello_address)
                    socket.sendto('up 5'.encode('utf-8'),tello_address)
                    print(text)
                    print('up')
                elif s_axe[1] > 0.2:
                    text = 'speed {down_value}'.format(down_value = int(s_axe[1] * 10+10))
                    socket.sendto(text.encode('utf-8'),tello_address)
                    socket.sendto('down 5'.encode('utf-8'),tello_address)
                    print(text)
                    print('down')
                
                if s_axe[2] > 0.2:
                    text = 'speed {right_value}'.format(right_value = int(s_axe[2] * 10+10))
                    socket.sendto(text.encode('utf-8'),tello_address)
                    socket.sendto('right 5'.encode('utf-8'),tello_address)
                    print(text)
                    print('right')
                elif s_axe[2] < -0.2:
                    text = 'speed {left_value}'.format(left_value = int(s_axe[2] * -10+10))
                    socket.sendto(text.encode('utf-8'),tello_address)
                    socket.sendto('left 5'.encode('utf-8'),tello_address)
                    print(text)
                    print('left')

                if s_axe[3] < -0.2:
                    text = 'speed {forward_value}'.format(forward_value = int(s_axe[3] * -10+10))
                    socket.sendto(text.encode('utf-8'),tello_address)
                    socket.sendto('forward 5'.encode('utf-8'),tello_address)
                    print(text)
                    print('forward')
                elif s_axe[3] > 0.2:
                    text = 'speed {back_value}'.format(back_value = int(s_axe[3] * 10+10))
                    socket.sendto(text.encode('utf-8'),tello_address)
                    socket.sendto('back 5'.encode('utf-8'),tello_address)
                    print(text)
                    print('back')

                if s_axe[4] == 1:
                    socket.sendto('takeoff'.encode('utf-8'),tello_address)

                if s_axe[5] == 1:
                    socket.sendto('land'.encode('utf-8'),tello_address)

                # memo: fieldnames = ['左ステX', '左ステY', '右ステX', '右ステY']
                writer.writerow({'LEFT Y': s_axe[1], 'RIGHT X': s_axe[2], 'RIGHT Y': s_axe[3], 'L1': s_axe[4], 'R1': s_axe[5]})

                time.sleep(0.1)
    except( KeyboardInterrupt, SystemExit): # Exit with Ctrl-C
        print("Exit")
        socket.sendto('land'.encode('utf-8'),tello_address)
        print ('land')

if __name__ == "__main__":
    main()
