#!/usr/bin/env python

import read_sbus_from_GPIO
import time

import os

class Kill():
    def __init__(self, pin:int)-> None:
        self.SBUS_PIN = pin #pin where sbus wire is plugged in

        reader = read_sbus_from_GPIO.SbusReader(self.SBUS_PIN)
        reader.begin_listen()

        #wait until connection is established
        while(not reader.is_connected()):
            time.sleep(.2)

        #Note that there will be nonsense data for the first 10ms or so of connection
        #until the first packet comes in.
        time.sleep(.1)

    def listen()-> None:
        try:
            is_connected = reader.is_connected()
            packet_age = reader.get_latest_packet_age() #milliseconds

            #returns list of length 16, so -1 from channel num to get index
            channel_data = reader.translate_latest_packet()
            
            #
            #Do something with data here!
            #ex:print(f'{channel_data[0]}')
            #
            
            nodes = os.popen("rosnode list").readlines()
            for i in range(len(nodes)):
                nodes[i] = nodes[i].replace("\n","")

            for node in nodes:
                os.system("rosnode kill "+ node)
                
            reader.pi.set_servo_pulsewidth(12,0)
            reader.pi.set_servo_pulsewidth(13,0)
            
            
            
        except KeyboardInterrupt:
            #cleanup cleanly after ctrl-c
            reader.end_listen()
            exit()
        except:
            #cleanup cleanly after error
            reader.end_listen()
            raise

