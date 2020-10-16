# Main script to start the emulator

import os
import sys
import time
import threading
import msvcrt
from jdi import JdiClient

jdi = None
exitDebugThread = False

'''
    Entry point. Сreate an instance for communicating with JDI, load the specified 
    file, starts the polling thread for debug messages and waits for a button press.
'''
def Main(file):
    global exitDebugThread
    jdi = JdiClient("DolwinEmuForPlayground.dll")

    print ("Dolwin Python, emulator version: " + jdi.GetVersion())
    print ("Press any key to stop emulation...\n")

    jdi.Load(file)
    jdi.Run()

    debugThread = threading.Thread(target=DebugThread)
    debugThread.start()

    msvcrt.getch()
    exitDebugThread = True

    jdi.Unload()

    print ("\nThank you for flying Dolwin airlines!")    


'''
    Debug messages polling thread
'''
def DebugThread():

    #jdi.Help()
    #msgs = jdi.QueryDebugMessages()

    while exitDebugThread == False:
        #print ("Wait")
        time.sleep(0.1)


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print ("Use: py -3 dolwin.py <file>")
        sys.exit(0)
    Main(sys.argv[1])
