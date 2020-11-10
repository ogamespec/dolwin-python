'''
    Helper module for working with the AnalyzeInfo structure.
    This structure is the key piece of information for UVNA used by Dolwin.
    https://github.com/ogamespec/dolwin-docs/blob/master/EMU/UVNA_en.md
'''

from enum import IntEnum, auto

'''
    The definition must match the definition in the Dolwin source (GekkoAnalyzer.h)
'''
class GekkoInstruction(IntEnum):
    Unknown = -1

    # Integer Arithmetic Instructions
    addi = 0
    addis = auto()
    add = auto()
    add_d = auto()
    addo = auto()
    addo_d = auto()
    subf = auto()
    subf_d = auto()
    subfo = auto()
    subfo_d = auto()
    addic = auto()
    addic_d = auto()
    subfic = auto()
    addc = auto()
    addc_d = auto()
    addco = auto()
    addco_d = auto()
    subfc = auto()
    subfc_d = auto()
    subfco = auto()
    subfco_d = auto()
    adde = auto()
    adde_d = auto()
    addeo = auto()
    addeo_d = auto()
    subfe = auto()
    subfe_d = auto()
    subfeo = auto()
    subfeo_d = auto()
    addme = auto()
    addme_d = auto()
    addmeo = auto()
    addmeo_d = auto()
    subfme = auto()
    subfme_d = auto()
    subfmeo = auto()
    subfmeo_d = auto()
    addze = auto()
    addze_d = auto()
    addzeo = auto()
    addzeo_d = auto()
    subfze = auto()
    subfze_d = auto()
    subfzeo = auto()
    subfzeo_d = auto()
    neg = auto()
    neg_d = auto()
    nego = auto()
    nego_d = auto()
    mulli = auto()
    mullw = auto()
    mullw_d = auto()
    mullwo = auto()
    mullwo_d = auto()
    mulhw = auto()
    mulhw_d = auto()
    mulhwu = auto()
    mulhwu_d = auto()
    divw = auto()
    divw_d = auto()
    divwo = auto()
    divwo_d = auto()
    divwu = auto()
    divwu_d = auto()
    divwuo = auto()
    divwuo_d = auto()

    # Integer Compare Instructions
    cmpi = auto()
    cmp = auto()
    cmpli = auto()
    cmpl = auto()

    # Integer Logical Instructions 
    andi_d = auto()
    andis_d = auto()
    ori = auto()
    oris = auto()
    xori = auto()
    xoris = auto()
    _and = auto()
    and_d = auto()
    _or = auto()
    or_d = auto()
    _xor = auto()
    xor_d = auto()
    nand = auto()
    nand_d = auto()
    nor = auto()
    nor_d = auto()
    eqv = auto()
    eqv_d = auto()
    andc = auto()
    andc_d = auto()
    orc = auto()
    orc_d = auto()
    extsb = auto()
    extsb_d = auto()
    extsh = auto()
    extsh_d = auto()
    cntlzw = auto()
    cntlzw_d = auto()

    # Integer Rotate Instructions
    rlwinm = auto()
    rlwinm_d = auto()
    rlwnm = auto()
    rlwnm_d = auto()
    rlwimi = auto()
    rlwimi_d = auto()

    # Integer Shift Instructions 
    slw = auto()
    slw_d = auto()
    srw = auto()
    srw_d = auto()
    srawi = auto()
    srawi_d = auto()
    sraw = auto()
    sraw_d = auto()

    # Floating-Point Instructions 
    fadd = auto()
    fadd_d = auto()
    fadds = auto()
    fadds_d = auto()
    fsub = auto()
    fsub_d = auto()
    fsubs = auto()
    fsubs_d = auto()
    fmul = auto()
    fmul_d = auto()
    fmuls = auto()
    fmuls_d = auto()
    fdiv = auto()
    fdiv_d = auto()
    fdivs = auto()
    fdivs_d = auto()
    fres = auto()
    fres_d = auto()
    frsqrte = auto()
    frsqrte_d = auto()
    fsel = auto()
    fsel_d = auto()

    fmadd = auto()
    fmadd_d = auto()
    fmadds = auto()
    fmadds_d = auto()
    fmsub = auto()
    fmsub_d = auto()
    fmsubs = auto()
    fmsubs_d = auto()
    fnmadd = auto()
    fnmadd_d = auto()
    fnmadds = auto()
    fnmadds_d = auto()
    fnmsub = auto()
    fnmsub_d = auto()
    fnmsubs = auto()
    fnmsubs_d = auto()

    frsp = auto()
    frsp_d = auto()
    fctiw = auto()
    fctiw_d = auto()
    fctiwz = auto()
    fctiwz_d = auto()

    fcmpu = auto()
    fcmpo = auto()

    mffs = auto()
    mffs_d = auto()
    mcrfs = auto()
    mtfsfi = auto()
    mtfsfi_d = auto()
    mtfsf = auto()
    mtfsf_d = auto()
    mtfsb0 = auto()
    mtfsb0_d = auto()
    mtfsb1 = auto()
    mtfsb1_d = auto()

    fmr = auto()
    fmr_d = auto()
    fneg = auto()
    fneg_d = auto()
    fabs = auto()
    fabs_d = auto()
    fnabs = auto()
    fnabs_d = auto()

    # Paired Single Instructions 
    ps_add = auto()
    ps_add_d = auto()
    ps_sub = auto()
    ps_sub_d = auto()
    ps_mul = auto()
    ps_mul_d = auto()
    ps_div = auto()
    ps_div_d = auto()
    ps_res = auto()
    ps_res_d = auto()
    ps_rsqrte = auto()
    ps_rsqrte_d = auto()
    ps_sel = auto()
    ps_sel_d = auto()
    ps_muls0 = auto()
    ps_muls0_d = auto()
    ps_muls1 = auto()
    ps_muls1_d = auto()
    ps_sum0 = auto()
    ps_sum0_d = auto()
    ps_sum1 = auto()
    ps_sum1_d = auto()

    ps_madd = auto()
    ps_madd_d = auto()
    ps_msub = auto()
    ps_msub_d = auto()
    ps_nmadd = auto()
    ps_nmadd_d = auto()
    ps_nmsub = auto()
    ps_nmsub_d = auto()
    ps_madds0 = auto()
    ps_madds0_d = auto()
    ps_madds1 = auto()
    ps_madds1_d = auto()

    ps_cmpu0 = auto()
    ps_cmpu1 = auto()
    ps_cmpo0 = auto()
    ps_cmpo1 = auto()

    ps_mr = auto()
    ps_mr_d = auto()
    ps_neg = auto()
    ps_neg_d = auto()
    ps_abs = auto()
    ps_abs_d = auto()
    ps_nabs = auto()
    ps_nabs_d = auto()
    ps_merge00 = auto()
    ps_merge00_d = auto()
    ps_merge01 = auto()
    ps_merge01_d = auto()
    ps_merge10 = auto()
    ps_merge10_d = auto()
    ps_merge11 = auto()
    ps_merge11_d = auto()

    # Integer Load Instructions 
    lbz = auto()
    lbzx = auto()
    lbzu = auto()
    lbzux = auto()
    lhz = auto()
    lhzx = auto()
    lhzu = auto()
    lhzux = auto()
    lha = auto()
    lhax = auto()
    lhau = auto()
    lhaux = auto()
    lwz = auto()
    lwzx = auto()
    lwzu = auto()
    lwzux = auto()

    stb = auto()
    stbx = auto()
    stbu = auto()
    stbux = auto()
    sth = auto()
    sthx = auto()
    sthu = auto()
    sthux = auto()
    stw = auto()
    stwx = auto()
    stwu = auto()
    stwux = auto()

    lhbrx = auto()
    lwbrx = auto()
    sthbrx = auto()
    stwbrx = auto()

    lmw = auto()
    stmw = auto()

    lswi = auto()
    lswx = auto()
    stswi = auto()
    stswx = auto()

    # Floating-Point Load Instructions 
    lfs = auto()
    lfsx = auto()
    lfsu = auto()
    lfsux = auto()
    lfd = auto()
    lfdx = auto()
    lfdu = auto()
    lfdux = auto()

    stfs = auto()
    stfsx = auto()
    stfsu = auto()
    stfsux = auto()
    stfd = auto()
    stfdx = auto()
    stfdu = auto()
    stfdux = auto()
    stfiwx = auto()

    # Paired Single Load and Store Instructions
    psq_l = auto()
    psq_lx = auto()
    psq_lu = auto()
    psq_lux = auto()
    psq_st = auto()
    psq_stx = auto()
    psq_stu = auto()
    psq_stux = auto()

    # Branch Instructions
    b = auto()
    ba = auto()
    bl = auto()
    bla = auto()
    bc = auto()
    bca = auto()
    bcl = auto()
    bcla = auto()
    bclr = auto()
    bclrl = auto()
    bcctr = auto()
    bcctrl = auto()

    # Condition Register Instructions
    crand = auto()
    cror = auto()
    crxor = auto()
    crnand = auto()
    crnor = auto()
    creqv = auto()
    crandc = auto()
    crorc = auto()
    mcrf = auto()
    mtcrf = auto()
    mcrxr = auto()
    mfcr = auto()

    # System-related
    twi = auto()
    tw = auto()
    sc = auto()
    mtspr = auto()
    mfspr = auto()
    lwarx = auto()
    stwcx_d = auto()
    sync = auto()
    mftb = auto()
    eieio = auto()
    isync = auto()
    dcbt = auto()
    dcbtst = auto()
    dcbz = auto()
    dcbz_l = auto()
    dcbst = auto()
    dcbf = auto()
    icbi = auto()
    dcbi = auto()
    eciwx = auto()
    ecowx = auto()
    rfi = auto()
    mtmsr = auto()
    mfmsr = auto()
    mtsr = auto()
    mtsrin = auto()
    mfsr = auto()
    mfsrin = auto()
    tlbie = auto()
    tlbsync = auto()


'''
    The definition must match the definition in the Dolwin source (GekkoAnalyzer.h)
'''
class GekkoParam(IntEnum):
    Unknown = -1
    Reg = 0
    FReg = auto()
    Simm = auto()       # The `Imm` property is used instead of the value from `paramBits`
    Uimm = auto()       # The `Imm` property is used instead of the value from `paramBits`
    Crf = auto()
    RegOffset = auto()
    Num = auto()
    Spr = auto()
    Sr = auto()
    Tbr = auto()
    Crb = auto()
    CRM = auto()
    FM = auto()
    Address = auto()    # The `Imm` property is used instead of the value from `paramBits`


'''
    struct AnalyzeInfo from GekkoAnalyzer.h

    A convenient class that includes support for parsing the parameters of the result of the GekkoAnalyze command, 
    as well as a predicate for comparing two objects and the `ToString` method for output.
'''
class Info(object):
    instr = GekkoInstruction.Unknown
    numParam = 0
    param = [ GekkoParam.Unknown, GekkoParam.Unknown, GekkoParam.Unknown, GekkoParam.Unknown, GekkoParam.Unknown ]
    paramBits = [ 0, 0, 0, 0, 0 ]

    Imm = 0         # The value for Immediate parameters is stored here instead of paramBits. I don't know why I did this, it would probably be good to store it in paramBits, but I don't want to redo it anymore.

    pc = 0
    flow = False

    # Array: [Int instr, Int numParams, Int param0, Int paramBits0, Int param1, Int paramBits1, Int param2, Int paramBits2, Int param3, Int paramBits3, Int param4, Int paramBits4, UInt32 immedValue, UInt32 newPc, Bool flow]
    def __init__(self, res:[]):
        if res is None:
            return
        self.instr = res["result"][0]
        self.numParam = res["result"][1]
        for i in range(5):
            self.param[i] = res["result"][2 + 2 * i]
            self.paramBits[i] = res["result"][2 + 2 * i + 1]
            if self.param[i] == GekkoParam.Simm:
                self.Imm = res["result"][12] & 0xffff
            if self.param[i] == GekkoParam.Uimm:
                self.Imm = res["result"][12] & 0xffff
            if self.param[i] == GekkoParam.Address:
                self.Imm = res["result"][12] & 0xffffffff
        self.pc = res["result"][13]
        self.flow = res["result"][14]

    def __eq__(self, other):
        if self.instr != other.instr:
            return False
        if self.numParam != other.numParam:
            return False
        for i in range(self.numParam):
            if self.param[i] != other.param[i]:
                return False
            # It doesn't make sense to compare parameter values for Immediate
            if not (self.param[i] == GekkoParam.Simm or self.param[i] == GekkoParam.Uimm or self.param[i] == GekkoParam.Address):
                if self.paramBits[i] != other.paramBits[i]:
                    return False
            else:
                if self.param[i] == GekkoParam.Simm:
                    if self.Imm != other.Imm:
                        return False
                if self.param[i] == GekkoParam.Uimm:
                    if self.Imm != other.Imm:
                        return False
                if self.param[i] == GekkoParam.Address:
                    if self.Imm != other.Imm:
                        return False
        if self.flow != other.flow:
            return False
        # Checking the `pc` value makes sense only for instructions that change the code flow (flow = True)
        if self.flow:
            if self.pc != other.pc:
                return False
        return True

    def ToString(self, dolwin):
        res = dolwin.ExecuteWithResult ( "GekkoInstrToString " + str(int(self.instr)))
        out = "0x%08X: %s\t\t" % (self.pc, res["result"][0])
        # GekkoInstrParamToString <param> <paramBits> <immedValue>
        for i in range(self.numParam):
            res = dolwin.ExecuteWithResult ( "GekkoInstrParamToString " + str(int(self.param[i])) + " " + str(self.paramBits[i]) + " " + str(self.Imm))
            out += "%s (%s)" % (res["result"][1], res["result"][0])
            if i != (self.numParam - 1):
                out += ", "
        if self.flow:
            out += " <flow control>"
        return out

    def GetInstrName(self, dolwin):
        res = dolwin.ExecuteWithResult ( "GekkoInstrToString " + str(int(self.instr)))
        return res["result"][0]
