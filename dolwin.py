# Main script to start the emulator

import os
import sys
import time
import threading
import msvcrt
from jdi import JdiClient

dolwin = None
exitDebugThread = False

'''
    Entry point. Сreate an instance for communicating with JDI, load the specified 
    file, starts the polling thread for debug messages and waits for a command/quit.
'''
def Main(file):
    global dolwin
    global exitDebugThread

    dolwin = JdiClient("DolwinEmuForPlayground.dll")

    print ("Dolwin Python, emulator version: " + dolwin.GetVersion())
    print ("Press any key to enter command or Esc to quit...\n")

    dolwin.Load(file)
    dolwin.Run()

    debugThread = threading.Thread(target=DebugThread)
    debugThread.start()

    while True:
        ch = msvcrt.getch()
        if ch == b'\x1b':   # Esc
            break
        cmdline = input("(dolwin) ")
        if cmdline != "":
            if cmdline[0] == '%':
                ExecuteCustomCommand(cmdline.split(' ')[1:])
            else:
                dolwin.Execute(cmdline)
    
    exitDebugThread = True

    dolwin.Unload()

    print ("\nThank you for flying Dolwin airlines!")    


'''
    Debug messages polling thread
'''
def DebugThread():
    global dolwin
    global exitDebugThread

    while exitDebugThread == False:
        msgs = dolwin.QueryDebugMessages()
        for str in msgs:
            print (str)
        time.sleep(0.1)


'''
    Execute external script as custom command
'''
def ExecuteCustomCommand(args):
    global dolwin
    try:
        module = __import__("Scripts." + args[0], fromlist=['object'])
        module.do_command (dolwin, args[1:])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print ("Use: py -3 dolwin.py <file>")
    else:
        Main(sys.argv[1])
