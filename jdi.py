# Binding with an emulator

import ctypes
from ctypes import *
import pathlib

class JdiClient:

    dll = None


    def __init__(self, dllname):
        fullpath = str(pathlib.Path().absolute() / dllname)
        self.dll = ctypes.CDLL(fullpath)


    def __exec(self, str):
        self.dll.CallJdiNoReturn(str.encode("ascii"))


    def __execReturnStr(self, str):
        self.dll.CallJdiReturnString.argtypes = [c_char_p, POINTER(c_char), c_int]
        result = ctypes.create_string_buffer(1024)
        self.dll.CallJdiReturnString (str.encode("ascii"), result, 1024)
        return result.value.decode("ascii")


    def GetVersion(self):
        return self.__execReturnStr("GetVersion")


    def Load(self, file):
        self.__exec("load " + file)


    def Unload(self):
        self.__exec("unload")


    def Run(self):
        self.__exec("run")


    def Help(self):
        self.__exec("help")


    def QueryDebugMessages(self):
        #self.dll.CallJdiReturnJson.argtypes = [c_char_p, POINTER(c_char), c_int]
        #self.dll.CallJdiReturnJson.restype = None
        result = (c_char * 256)()
        self.dll.CallJdiReturnJson("qd", result, 256)
        print (result);
        return []
