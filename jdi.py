# Binding with an emulator

import ctypes
from ctypes import *
import pathlib
import json

class JdiClient:

    dll = None


    def __init__(self, dllname):
        fullpath = str(pathlib.Path().absolute() / dllname)
        self.dll = ctypes.CDLL(fullpath)


    def __exec(self, str):
        self.dll.CallJdiNoReturn(str.encode("ascii"))


    def __execReturnStr(self, str, size):
        self.dll.CallJdiReturnString.argtypes = [c_char_p, POINTER(c_char), c_int]
        result = ctypes.create_string_buffer(size)
        self.dll.CallJdiReturnString (str.encode("ascii"), result, size)
        return result.value.decode("ascii")


    def __execReturnJsonText(self, str, size):
        self.dll.CallJdiReturnString.argtypes = [c_char_p, POINTER(c_char), c_int]
        result = ctypes.create_string_buffer(size)
        self.dll.CallJdiReturnJson (str.encode("ascii"), result, size)
        return result.value.decode("ascii")        


    def GetVersion(self):
        return self.__execReturnStr("GetVersion", 32)


    def Load(self, file):
        self.__exec("load " + file)


    def Unload(self):
        self.__exec("unload")


    def Run(self):
        self.__exec("run")


    def QueryDebugMessages(self):
        result = self.__execReturnJsonText("qd", 10000)
        obj = json.loads (result)

        msgs = []

        for entry in obj["result"]:
            if type(entry) is str:
                if entry.endswith('\n'):
                    entry = entry[:-1]
                msgs.append(entry)

        return msgs


    def Execute(self, cmd):
        self.__exec(cmd)
