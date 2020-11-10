from .GekkoAnalyzer import *

'''
    Testing the GekkoCore Instruction Analyzer.

    The internal GekkoCore commands are used for testing: GekkoAnalyze, GekkoInstrToString and GekkoInstrParamToString.

    Testing is divided into instruction categories. Each instruction is tested separately.

'''
def do_command(dolwin, args):
    try:
        __EmptyOpcode(dolwin)
        __BranchOpcodes(dolwin)
        __CompareOpcodes(dolwin)
        __ConditionOpcodes(dolwin)
        __FPUOpcodes(dolwin)
        __FPULoadStoreOpcodes(dolwin)
        __IntegerOpcodes(dolwin)
        __LoadStoreOpcodes(dolwin)
        __LogicalOpcodes(dolwin)
        __PairedSingleOpcodes(dolwin)
        __PSLoadStoreOpcodes(dolwin)
        __RotateOpcodes(dolwin)
        __ShiftOpcodes(dolwin)
        __SystemOpcodes(dolwin)
    except Exception as e:
        print(e)


'''
    The base method that calls the parser gets the results and compares them with what should be obtained.
'''
def __test(dolwin, opcode, should):
    defaultPc = 0x80000000
    info = Info(dolwin.ExecuteWithResult ("GekkoAnalyze 0x%08X 0x%08X" % (defaultPc, opcode)))
    print (info.ToString(dolwin))
    if info != should:
        raise Exception(__name__.split(".")[-1] + ": " + info.GetInstrName(dolwin) + " test failed")


def __EmptyOpcode(dolwin):
    
    # Actually nop (ori r0, r0, 0), for testing infrastructure  (DEBUG)
    s = Info(None)
    s.instr = GekkoInstruction.ori
    s.numParam = 3
    s.param = [ GekkoParam.Reg, GekkoParam.Reg, GekkoParam.Uimm ]
    s.paramBits = [ 0, 0, 0 ]
    s.Imm = 0

    __test (dolwin, 0x60000000, s)
    return


#################################################################################################

def __BranchOpcodes(dolwin):
    return

#################################################################################################

def __CompareOpcodes(dolwin):
    return

#################################################################################################

def __ConditionOpcodes(dolwin):
    return

#################################################################################################

def __FPUOpcodes(dolwin):
    return

#################################################################################################

def __FPULoadStoreOpcodes(dolwin):
    return

#################################################################################################

def __IntegerOpcodes(dolwin):
    return

#################################################################################################

def __LoadStoreOpcodes(dolwin):
    return

#################################################################################################

def __LogicalOpcodes(dolwin):
    return

#################################################################################################

def __PairedSingleOpcodes(dolwin):
    return

#################################################################################################

def __PSLoadStoreOpcodes(dolwin):
    return

#################################################################################################

def __RotateOpcodes(dolwin):
    return

#################################################################################################

def __ShiftOpcodes(dolwin):
    return

#################################################################################################

def __SystemOpcodes(dolwin):
    return
