# Main script to start the emulator

import sys
from jdi import JdiClient

jdi = None

'''
    Entry point. Сreate an instance for communicating with JDI, load the specified 
    file and go to the main loop.
'''
def Main(file):
    jdi = JdiClient("DolwinEmuForPlayground.dll")

    print ("Dolwin Version: " + jdi.GetVersion())

    #jdi.Help()
    #msgs = jdi.QueryDebugMessages()

    MainLoop()

'''
    The main loop polls and displays debug messages from the emulator.
    Exit occurs by pressing the button.
'''
def MainLoop():
    return

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print ("Use: py -3 dolwin.py <file>")
        sys.exit(0)
    Main(sys.argv[1])
