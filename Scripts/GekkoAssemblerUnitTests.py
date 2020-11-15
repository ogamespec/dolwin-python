from .GekkoAnalyzer import *

'''
    GekkoCore assembler tests.
'''
def do_command(dolwin, args):
    try:
        __BranchOpcodes(dolwin)
    except Exception as e:
        print(e)


def __TestTemplate(dolwin):
    defaultPc = 0x80003100
    # addi r1, r31, -21829
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


#################################################################################################

def __BranchOpcodes(dolwin):
    __BranchLongTest (dolwin)


'''
    Test instructions: b, ba, bl, bla
'''
def __BranchLongTest(dolwin):
    defaultPc = 0x80003100

    # Trivial cases

    # b 0x80004000
    instr = __asm (
        dolwin,
        GekkoInstruction.b, 
        [GekkoParam.Address], 
        [0], 
        0x80004000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x48000F00:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # ba 0x00004000
    instr = __asm (
        dolwin,
        GekkoInstruction.ba, 
        [GekkoParam.Address], 
        [0], 
        0x00004000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x48004002:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # bl 0x80004000
    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0x80004000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x48000F01:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # bla 0x00004000
    instr = __asm (
        dolwin,
        GekkoInstruction.bla, 
        [GekkoParam.Address], 
        [0], 
        0x00004000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x48004003:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # Corner case values for absolute branch: [xxxx xxii iiii iiii iiii iiii iiii iixx]
    # i = 0: address = 0
    # i = 1: address = 4
    # i = [01 0000 0000 0000 0000 0000 00]: address = 0x100'0000
    # i = [01 1111 1111 1111 1111 1111 11]: address = 0x1FF'FFFC
    # i = [10 0000 0000 0000 0000 0000 00]: address = 0xfe00'0000
    # i = [11 1111 1111 1111 1111 1111 11]: address = 0xFFFF'FFFC

    instr = __asm (
        dolwin,
        GekkoInstruction.ba, 
        [GekkoParam.Address], 
        [0], 
        0x0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x48000002:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.ba, 
        [GekkoParam.Address], 
        [0], 
        0x4, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x48000006:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.ba, 
        [GekkoParam.Address], 
        [0], 
        0x1000000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x49000002:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.ba, 
        [GekkoParam.Address], 
        [0], 
        0x1FFFFFC, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x49FFFFFE:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")        

    instr = __asm (
        dolwin,
        GekkoInstruction.ba, 
        [GekkoParam.Address], 
        [0], 
        0xfe000000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4A000002:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.ba, 
        [GekkoParam.Address], 
        [0], 
        0xFFFFFFFC, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4BFFFFFE:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # Bad corner cases for absolute branch
    # address: 0x200'0000 -- invalid
    # address: 0x8000'0000 -- invalid
    # address: 0xFDFF'FFFC -- invalid

    instr = __asm (
        dolwin,
        GekkoInstruction.ba, 
        [GekkoParam.Address], 
        [0], 
        0x2000000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.ba, 
        [GekkoParam.Address], 
        [0], 
        0x80000000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.ba, 
        [GekkoParam.Address], 
        [0], 
        0xFDFFFFFC, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")        

    # Corner case values for non-absolute branch
    # i = [01 0000 0000 0000 0000 0000 00]: offset = 0
    # i = [01 1111 1111 1111 1111 1111 11]: offset = 0x1FF'FFFC
    # i = [10 0000 0000 0000 0000 0000 00]: offset = 0xfe00'0000
    # i = [11 1111 1111 1111 1111 1111 11]: offset = 0xFFFF'FFFC
    # Range from address 0x0: [0, 0x1FF'FFFC], [0xFE000000, 0xFFFFFFFC]
    # Range from address 0xffff'fffc: [0xffff'fffc, 0x1FF'FFF8], [0xFDFF'FFFC, 0xFFFF'FFF8]

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0x48000001:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0x1fffffc, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0x49FFFFFD:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0xFE000000, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0x4A000001:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0xFFFFFFFC, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0x4BFFFFFD:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0xfffffffc, 
        0xfffffffc)
    text = __disasm(dolwin, 0xfffffffc, instr)
    if instr != 0x48000001:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0x1FFFFF8, 
        0xfffffffc)
    text = __disasm(dolwin, 0xfffffffc, instr)
    if instr != 0x49FFFFFD:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0xFDFFFFFC, 
        0xfffffffc)
    text = __disasm(dolwin, 0xfffffffc, instr)
    if instr != 0x4A000001:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0xFFFFFFF8, 
        0xfffffffc)
    text = __disasm(dolwin, 0xfffffffc, instr)
    if instr != 0x4BFFFFFD:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # Bad corner cases for non-absolute branch
    # pc: 0, address: 0x200'0000 ( +0x200'0000)
    # pc: 0, address: 0xFDFF'FFFC ( -0x200'0004)
    # pc: 0xFFFFFFFC, address: 0x1FF'FFFC ( +0x200'0000)
    # pc: 0xFFFFFFFC, address: 0xFDFF'FFF8 ( -0x200'0004)

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0x2000000, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0xFDFFFFFC, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0x1FFFFFC, 
        0xFFFFFFFC)
    text = __disasm(dolwin, 0xFFFFFFFC, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bl, 
        [GekkoParam.Address], 
        [0], 
        0xFDFFFFF8, 
        0xFFFFFFFC)
    text = __disasm(dolwin, 0xFFFFFFFC, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")


#################################################################################################


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
