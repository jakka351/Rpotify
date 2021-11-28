#!/usr/bin/python3
# can0swc fg falcon swc-can adapter
# https://github.com/jakka351/FG-Falcon | https://github.com/jakka351/can0swc
# assumes ms-can is up on can0
# buffers several CAN IDS, then matches byte specific data
# this version rigged up to work with raspotify - control spotify connect via canbus
############################
# Import modules
############################
import can
import time
import os
import sys
import queue
from threading import Thread
c                      = ''
count                  = 0  
# CAN Id's
SWC                    = 0x2F2 
SWM                    = 0x2EC
ICC                    = 0x2FC 
# SWC Button CAN Data
SWC_SEEK               = (0x08, 0x09, 0x0C, 0x0D)  # seek button on bit [7] of id 0x2f2
SWC_VOLUP              = (0x10, 0x11, 0x14, 0x15)  # volume + button on bit [7] of id 0x2f2
SWC_VOLDOWN            = (0x18, 0x19, 0x1C, 0x1D)  # volume - button on bit [7] of id 0x2f2
SWC_PHONE              = (0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, )  # phone button on bit [6] of id 0x2f2
SWC_MODE               = (0x10)
AuxillaryMode          = (0x41, 0xC1)
RadioPhoneMode         = (0x43, 0x44, 0x45, 0x47, 0x48, 0xC3, 0xC4, 0xC5, 0xC7, 0xC8)
modeswap = 0
counter = 0
def scroll():
    #prints logo to console
        print('  ')
        print('''  
             ,777I77II??~++++=~::,,,,::::::::::~~~==+~                                        
           ,IIIIII,IIII+~R,:A, S,,P:~O:,T..I.,F,,Y:::~+?+?=                                    
         :=I7777I=IIIIII~...:===,:,=~:,,,,,,::=,,,:::~~:=?===                                 
      ~=,?I?777II7IIIII=~,.,,,,,,,,,,,:,,,,,,::,,,,~:~~~~:~+:~:~                              
      I=I?IIIIII~IIIIIII+:..,,,,,,,,,,,,.,.,,::.,,,,:::~~=~:=+~?~~                            
      I77?+?IIIIIIIII7I7=~,.,,,..,,,,.,.,.......,.,.,.,..,,,:~=~:==~~                         
     +=I7777I?+???IIIIII+=:..,,,,,,,,,,,...,,,,,,,,,,,,..,,,:..:?I7+...,,                     
     +=+=I7777I=~~+~:~IIII~,..,,,,,,,,,,..,,,,,...~+II?I?+?IIHECTICII77I7=.....                
      ==++++III=~~~::~+I:+?~:.........:+IIIIIIII+=?IIJACK????????????III7II7I....             
     ?+=  ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████++++???II?III....         
     ?+= ██ C    ██ A ██ ████ N ██ ██B ████ ██ U    ██     ██ ██   S ======++?II?+7II.         
     ??+ ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██     ~~~~======+???++II.       
     ??+ ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██     ~~~~~~~~~===++++=II,      
     I??  ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████:::~~~~~~~~~====+==I,     
      ?I+=~~fg+falcon+swc+adapter+??++++===~:~~~~~~~=???=?:=H~~~~~::::::::~~~~~~~~~~=~=+?7~:    
       ?+=~~~~=++~~~~~+???~=?7II??+++++++==~~:~~~~~~:~~???=+:I~~~~~~:::::::::~~~~=++:,.,+=,,   
        =?I+~~~==++~~:+??~====+I?+===+++++==~~~::::::::::~????T~~~~~:::::~:~==+:,,,,?..::+=:   
          =?I=~~~==++=+++~==:,~~=+====+++++:,,...:,::~:::::~~~~E~:~~:~~==,.,,.?I~,..::~~=,:   
           ~=+I?=~~=~+++~~=...,~:=+====++?:~+=?I~,I=I??..~III7I:=F=~,.,,.,,.,,,...::~~++~:~:   
              ~?I+=~~~~+~~~.:+,,,:=+===+++~+==~=+:III=?I?LOL77I~~~O===,,,,.,.,,~~~~=+=~::,,:   
                ~?I+=:~~~~~~,,+:,,+==~+++++,:~~:==,??,:,,=??I++,,,: R===,,,::~~=++=:::~=..,,   
             ,,,,:=+?==~~~~.=:~~,..,=+++++=~:=+=~:.,:,,,,::?=I=:::::+~D====++++=~:::?I+?,..,   
              :,,,,~+====~:,,,:=,.,,,~~===~~~,:==~~~~~~:..,,,,,,..,,,~==S+++~:,~++I++II?...    
               :,,,,,,+==+,:..:==.:,,~:~~~~~:,,,,:~~~~~~~~=========~++++~,M....II+II+?...,:    
                 ,,,,,,,++.,,.,,,,=:,,~:::~:::,,,,,,,,,::~~~=====~====~......E.?I=I.....,:~    
                   ::,,,,,,:~::,~+I+,..~::::::,,,,,,,,,,,,,,,,,~==~~~.........+L....L..S:,,    ''')
        
def setup():
    global bus
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        sys.exit() # quits if there is no canbus interface
    print("                      ")
    print("        CANbus active on", bus)   
    print("        waiting for matching can frame...")     #this line gets replaced by the next matching can frame
    print("        Raspotify Control via CAN...")             # this line gets replaced by the button in the car that is pushed
    
def msgbuffer():
    global message, q, SWC
    while True:
        message = bus.recv()          # if recieving can frames then put these can arb id's into a queue
        if message.arbitration_id == SWC:                        
            q.put(message)
        #if message.arbitration_id == SWM:                        
        #   q.put(message)
        #if message.arbitration_id == ICC:                        
        #    q.put(message)
def main(): 
    global message, bus, q, SWC, SWC_SEEK, SWC_VOLUP, SWC_VOLDOWN, SWC_PHONE, AuxillaryMode, RadioPhoneMode, counter, modeswap
    try:
        while True:
            for i in range(8):
                while(q.empty() == True):                               # wait for messages to queue
                    pass
                message = q.get()   
                c = '{0:f},{1:d},'.format(message.timestamp,count)
              

                if message.arbitration_id == SWC and message.data[7] in SWC_SEEK:
                    os.system("./rpotify.sh next")
                    print("SWCSeekBtn pushed @", message.timestamp)
                    time.sleep(0.5)
                                                  
                elif message.arbitration_id == SWC and message.data[7] in SWC_VOLUP:
                    os.system("./rpotify.sh up")
                    print("SWCVolUpBtn pushed @", message.timestamp)
                    time.sleep(0.5)
                        
                elif message.arbitration_id == SWC and message.data[7] in SWC_VOLDOWN:  
                    os.system("./rpotify.sh down") 
                    print("SWCVolDownBtn pushed @", message.timestamp)
                    time.sleep(0.5)
                    
                elif message.arbitration_id == SWC and message.data[6] in SWC_PHONE:
                    os.system("./rpotify.sh play")
                    os.system("./rpotify.sh status")
                    print("SWCPhoneBtn pushed @", message.timestamp)                    
                    time.sleep(0.5)

                elif message.arbitration_id == SWC and message.data[6] in AuxillaryMode:
                    modeswap = 0
                    if counter == 0:
                        os.system("./rpotify.sh play")
                        print("AuxillaryMode Active @", message.timestamp) 
                        time.sleep(1)
                        counter = counter + 1
                    elif counter >= 1:            
                        pass

                elif message.arbitration_id == SWC and message.data[6] in RadioPhoneMode:
                    counter = 0
                    if modeswap == 0:
                        os.system("./rpotify.sh stop")
                        print("FM Radio or Phone Call Active @", message.timestamp) 
                        time.sleep(1)
                        modeswap = modeswap + 1
                    elif modeswap == 1:
                        pass                   
                else:
                    pass        
                                                                           
    except KeyboardInterrupt:
        sys.exit(0)                                              # quit if ctl + c is hit
    except Exception:
        sys.exit()
    except OSError:
        sys.exit()                                               # quit if there is a system issue
############################
# can0swc 
############################
if __name__ == "__main__":
    q                      = queue.Queue()                       #
    rx                     = Thread(target = msgbuffer)          #
    scroll()                                                     # scroll out fancy logo text
    setup()                                                      # set the can interface
    rx.start()                                                   # start the rx thread and queue msgs
    main()                                                       
    spotStart()
    spotDevices()
    
k
