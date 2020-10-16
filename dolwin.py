# Main script to start the emulator

import sys
import ctypes
import pathlib

import jdi

def Main(file):
    print ("Loading " + file)
    MainLoop()

def MainLoop():
    return

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print ("Use: py -3 dolwin.py <file>")
        sys.exit(0)
    Main(sys.argv[1])
