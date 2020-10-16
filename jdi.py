# Binding with an emulator

import ctypes
from ctypes import *
import pathlib

class JdiClient:

    dll = None

    '''
        Make friends with the emulator
    '''
    def __init__(self, dllname):
        fullpath = str(pathlib.Path().absolute() / dllname)
        self.dll = ctypes.CDLL(fullpath)

    '''
        Get emulator version
    '''
    def GetVersion(self):
        self.dll.CallJdiReturnString.argtypes = [c_char_p, POINTER(c_char), c_int]
        result = ctypes.create_string_buffer(32)
        self.dll.CallJdiReturnString ("GetVersion".encode("ascii"), result, 32)
        return result.value.decode("ascii")

    def Help(self):
        self.dll.CallJdiNoReturn("help")

    def QueryDebugMessages(self):
        #self.dll.CallJdiReturnJson.argtypes = [c_char_p, POINTER(c_char), c_int]
        #self.dll.CallJdiReturnJson.restype = None
        result = (c_char * 256)()
        self.dll.CallJdiReturnJson("qd", result, 256)
        print (result);
        return []
