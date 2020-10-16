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


    '''
        Outputting debug messages requires special handling.
        Debug messages come as an array of Channel:Text pairs. 
        The channel name is obtained with the `GetChannelName` command. 
        The channel name is not displayed if it is empty.
    '''
    def QueryDebugMessages(self):
        result = self.__execReturnJsonText("qd", 10000)
        obj = json.loads (result)

        msgs = []
        lastChannelName = ""

        for entry in obj["result"]:
            if type(entry) is int:
                lastChannelName = self.__execReturnStr("GetChannelName " + str(entry), 32)
                if lastChannelName == "Header":
                    lastChannelName = ""
            if type(entry) is str:
                if entry.endswith('\n'):
                    entry = entry[:-1]
                if lastChannelName != "":
                    if entry != "":
                        msgs.append(lastChannelName + ": " + entry)
                    else:
                        msgs.append("")
                else:
                    msgs.append(entry)

        return msgs


    '''
        General purpose method for executing any command if no result is required.
    '''
    def Execute(self, cmd):
        self.__exec(cmd)


    '''
        General purpose method, to execute any command, if result is required.
        The result is returned as a deserialized Json representation.
    '''
    def ExecuteWithResult(self, cmd):
        result = self.__execReturnJsonText(cmd, 10000)
        return json.loads (result)        
