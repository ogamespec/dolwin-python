# Show Gekko GPRs

def do_command(dolwin, args):
    if len(args) == 0:
        for i in range(0, 32):
            res = dolwin.ExecuteWithResult("GetGpr " + str(i))
            print (str(i) + ": 0x%0.8X" % res["result"])
    else:
        res = dolwin.ExecuteWithResult("GetGpr " + args[0])
        print (args[0] + ": 0x%0.8X" % res["result"])
