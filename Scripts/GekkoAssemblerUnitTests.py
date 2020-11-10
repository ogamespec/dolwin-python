from .GekkoAnalyzer import *

'''
    GekkoCore assembler tests.
'''
def do_command(dolwin, args):
    defaultPc = 0x80003100

    # 0x383FAABB addi r1, r31, -21829
    instr = __asm (
        dolwin,
        GekkoInstruction.addi, 
        [GekkoParam.Reg, GekkoParam.Reg, GekkoParam.Simm], 
        [1, 31, 0], 
        0xaabb, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x383FAABB:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")
    else:
        print (text + "\t\t\tsuccess!")


'''
    Assemble the Gekko instruction
'''
def __asm(dolwin, instrType, param: [], paramBits: [], imm, pc):
    numParams = len(param)
    # Int instr, Int numParams, Int param0, Int paramBits0, Int param1, Int paramBits1, Int param2, Int paramBits2, Int param3, Int paramBits3, Int param4, Int paramBits4, UInt32 immedValue, UInt32 Pc    
    cmd = "GekkoAssemble " + str(int(instrType)) + " " + str(numParams) + " "
    for i in range(5):
        if i >= numParams:
            cmd += "0 0 "
        else:
            cmd += str(int(param[i])) + " " + str(paramBits[i]) + " "
    cmd += str(imm) + " 0x%08X" % pc
    res = dolwin.ExecuteWithResult(cmd)
    return res["result"]


'''
    Disassemble the Gekko instruction
'''
def __disasm(dolwin, pc, opcode):
    res = dolwin.ExecuteWithResult("GekkoDisasmNoMemAccess " + ("0x%08X" % pc) + (" 0x%08X" % opcode) + " 1 1")     # show address and bytes
    return res["result"][0]
