# Main script to start the emulator

import os
import sys
import time
import threading
import msvcrt
from jdi import JdiClient

dolwin = None
exitDebugThread = False
autorunScript = None

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

    dolwin.Execute("load " + file)
    dolwin.Execute("run")

    debugThread = threading.Thread(target=DebugThread)
    debugThread.start()

    RunAutorun()

    while True:
        ch = msvcrt.getch()
        if ch == b'\x1b':   # Esc
            break
        try:
            cmdline = input("(dolwin) ")
            if cmdline != "":
                if cmdline[0] == '%':
                    ExecuteCustomCommand(cmdline.split(' ')[1:])
                else:
                    dolwin.Execute(cmdline)
        except Exception as e:
            print(e)
    
    exitDebugThread = True

    dolwin.Execute("unload")

    print ("\nThank you for flying Dolwin airlines!")    


'''
    Debug messages polling thread
'''
def DebugThread():
    while exitDebugThread == False:
        msgs = dolwin.QueryDebugMessages()
        for str in msgs:
            print (str)
        time.sleep(0.1)


'''
    Execute external script as custom command
'''
def ExecuteCustomCommand(args):
    try:
        module = __import__("Scripts." + args[0], fromlist=['object'])
        module.do_command (dolwin, args[1:])
    except Exception as e:
        print(e)


'''
    Run autorun after emulation started
'''
def RunAutorun():
    if not autorunScript:
        return
    with open(autorunScript, "r") as f:
        for line in f:
            cmdline = line.replace("\n", "")
            if not cmdline:
                continue
            if cmdline[0] == '#':
                continue
            if cmdline[0] == '%':
                ExecuteCustomCommand(cmdline.split(' ')[1:])
            else:
                dolwin.Execute(cmdline)


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print ("Use: py -3 dolwin.py <file> [autorun.txt]")
    else:
        if len(sys.argv) >= 3:
            autorunScript = sys.argv[2]
        Main(sys.argv[1])
