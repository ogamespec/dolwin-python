from .GekkoAnalyzer import *

'''
    GekkoCore assembler tests.
'''
def do_command(dolwin, args):
    try:
        __BranchOpcodes(dolwin)
        __CompareOpcodes(dolwin)
        __ConditionOpcodes(dolwin)
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
    __BranchShortTest (dolwin)
    __BranchBOBI (dolwin)


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


'''
    Test instructions: bc, bca, bcl, bcla
'''
def __BranchShortTest(dolwin):
    defaultPc = 0x80003100

    # Trivial cases

    # bc 12, 0, 0x80004000
    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x80004000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x41800F00:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # bca 12, 0, 0x00004000
    instr = __asm (
        dolwin,
        GekkoInstruction.bca, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x00004000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x41804002:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # bcl 12, 0, 0x80004000
    instr = __asm (
        dolwin,
        GekkoInstruction.bcl, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x80004000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x41800F01:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # bcla 12, 0, 0x00004000
    instr = __asm (
        dolwin,
        GekkoInstruction.bcla, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x00004000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x41804003:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # Corner case values for absolute branch: [xxxx xxxx xxxx xxxx iiii iiii iiii iixx]
    # i = [0100 0000 0000 00xx]: address = 0x4000
    # i = [0111 1111 1111 11xx]: address = 0x7FFC
    # i = [1000 0000 0000 00xx]: address = 0xFFFF8000
    # i = [1111 1111 1111 11xx]: address = 0xFFFFFFFC

    instr = __asm (
        dolwin,
        GekkoInstruction.bca, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x4000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x41804002:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bca, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x7FFC, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x41807FFE:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bca, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0xFFFF8000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x41808002:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bca, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0xFFFFFFFC, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4180FFFE:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # Bad corner cases for absolute branch
    # address: 0x8000 -- invalid
    # address: 0xFFFF7FFC -- invalid

    instr = __asm (
        dolwin,
        GekkoInstruction.bca, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x8000, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bca, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0xFFFF7FFC, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # Corner case values for non-absolute branch
    # i = [0000 0000 0000 00xx]: offset = 0x0
    # i = [0111 1111 1111 11xx]: offset = 0x7FFC
    # i = [1000 0000 0000 00xx]: offset = 0xFFFF8000
    # i = [1111 1111 1111 11xx]: offset = 0xFFFFFFFC
    # Range from address 0x0: [0, 0x7FFC], [0xFFFF8000, 0xFFFFFFFC]
    # Range from address 0xffff'fffc: [0xfffffffc, 0x7FF8], [0xFFFF7FFC, 0xFFFFFFF8]

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0x41800000:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x7FFC, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0x41807FFC:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0xFFFF8000, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0x41808000:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0xFFFFFFFC, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0x4180FFFC:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0xfffffffc, 
        0xfffffffc)
    text = __disasm(dolwin, 0xfffffffc, instr)
    if instr != 0x41800000:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x7FF8, 
        0xfffffffc)
    text = __disasm(dolwin, 0xfffffffc, instr)
    if instr != 0x41807FFC:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0xFFFF7FFC, 
        0xfffffffc)
    text = __disasm(dolwin, 0xfffffffc, instr)
    if instr != 0x41808000:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0xFFFFFFF8, 
        0xfffffffc)
    text = __disasm(dolwin, 0xfffffffc, instr)
    if instr != 0x4180FFFC:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")        

    # Bad corner cases for non-absolute branch
    # pc: 0, address: 0x8000 ( +0x8000)
    # pc: 0, address: 0xFFFF7FFC ( -0x8004)
    # pc: 0xFFFFFFFC, address: 0x7FFC ( +0x8000)
    # pc: 0xFFFFFFFC, address: 0xFFFF7FF8 ( -0x8004)

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x8000, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0xFFFF7FFC, 
        0)
    text = __disasm(dolwin, 0, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0x7FFC, 
        0xFFFFFFFC)
    text = __disasm(dolwin, 0xFFFFFFFC, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bc, 
        [GekkoParam.Num, GekkoParam.Num, GekkoParam.Address], 
        [12, 0, 0], 
        0xFFFF7FF8, 
        0xFFFFFFFC)
    text = __disasm(dolwin, 0xFFFFFFFC, instr)
    if instr != 0:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")


def __BranchBOBI (dolwin):
    defaultPc = 0x80003100

    instr = __asm (
        dolwin,
        GekkoInstruction.bcctr, 
        [GekkoParam.Num, GekkoParam.Num], 
        [4, 10], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4C8A0420:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bcctrl, 
        [GekkoParam.Num, GekkoParam.Num], 
        [4, 10], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4C8A0421:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bclr, 
        [GekkoParam.Num, GekkoParam.Num], 
        [4, 10], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4C8A0020:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    # bdnzlr-
    instr = __asm (
        dolwin,
        GekkoInstruction.bclr, 
        [GekkoParam.Num, GekkoParam.Num], 
        [16, 0], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4E000020:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.bclrl, 
        [GekkoParam.Num, GekkoParam.Num], 
        [4, 10], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4C8A0021:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")


#################################################################################################

def __CompareOpcodes(dolwin):
    defaultPc = 0x80003100

    instr = __asm (
        dolwin,
        GekkoInstruction.cmp, 
        [GekkoParam.Crf, GekkoParam.Reg, GekkoParam.Reg], 
        [3, 2, 1], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x7D820800:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.cmpl, 
        [GekkoParam.Crf, GekkoParam.Reg, GekkoParam.Reg], 
        [3, 2, 1], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x7D820840:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")        

    instr = __asm (
        dolwin,
        GekkoInstruction.cmpi, 
        [GekkoParam.Crf, GekkoParam.Reg, GekkoParam.Simm], 
        [3, 2, 0], 
        0x7fff, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x2D827FFF:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.cmpi, 
        [GekkoParam.Crf, GekkoParam.Reg, GekkoParam.Simm], 
        [3, 2, 0], 
        0x8000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x2D828000:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.cmpi, 
        [GekkoParam.Crf, GekkoParam.Reg, GekkoParam.Simm], 
        [3, 2, 0], 
        0xffff, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x2D82FFFF:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.cmpli, 
        [GekkoParam.Crf, GekkoParam.Reg, GekkoParam.Uimm], 
        [3, 2, 0], 
        0x7fff, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x29827FFF:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.cmpli, 
        [GekkoParam.Crf, GekkoParam.Reg, GekkoParam.Uimm], 
        [3, 2, 0], 
        0x8000, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x29828000:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.cmpli, 
        [GekkoParam.Crf, GekkoParam.Reg, GekkoParam.Uimm], 
        [3, 2, 0], 
        0xffff, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x2982FFFF:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")


#################################################################################################

# Пиздец какие важные опкоды, без них не может жить ни один программист. (извиняюсь за издевательский тон, но нахуя оверинжинирить архитектуру?)

def __ConditionOpcodes(dolwin):
    defaultPc = 0x80003100

    instr = __asm (
        dolwin,
        GekkoInstruction.crand, 
        [GekkoParam.Crb, GekkoParam.Crb, GekkoParam.Crb], 
        [7, 0, 31], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4CE0FA02:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.crandc, 
        [GekkoParam.Crb, GekkoParam.Crb, GekkoParam.Crb], 
        [7, 0, 31], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4CE0F902:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.creqv, 
        [GekkoParam.Crb, GekkoParam.Crb, GekkoParam.Crb], 
        [7, 0, 31], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4CE0FA42:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.crnand, 
        [GekkoParam.Crb, GekkoParam.Crb, GekkoParam.Crb], 
        [7, 0, 31], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4CE0F9C2:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.crnor, 
        [GekkoParam.Crb, GekkoParam.Crb, GekkoParam.Crb], 
        [7, 0, 31], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4CE0F842:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.cror, 
        [GekkoParam.Crb, GekkoParam.Crb, GekkoParam.Crb], 
        [7, 0, 31], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4CE0FB82:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.crorc, 
        [GekkoParam.Crb, GekkoParam.Crb, GekkoParam.Crb], 
        [7, 0, 31], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4CE0FB42:
        raise Exception(__name__.split(".")[-1] + " `" + text + "` failed!")

    instr = __asm (
        dolwin,
        GekkoInstruction.crxor, 
        [GekkoParam.Crb, GekkoParam.Crb, GekkoParam.Crb], 
        [7, 0, 31], 
        0, 
        defaultPc)
    text = __disasm(dolwin, defaultPc, instr)
    if instr != 0x4CE0F982:
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
