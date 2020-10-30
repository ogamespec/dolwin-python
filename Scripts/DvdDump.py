import sys
import time

'''
    Dump DVD (whole or partially) as image.
    Example:
        MountIso c:/isos/ac.gcm         (mount existing GCM)
        % DvdDump ac.gcm 0x320000   (dump first 50 MBytes, maxSize is optional parameter)

    Note: this is damn slow..
'''
def do_command(dolwin, args):
    if (len(args) < 1):
        print ("Use: % " + __name__.split(".")[-1] + " <file> [maxSize]")
        return

    dvdSize = 0x57058000
    if len(args) >= 2:
        dvdSize = int(args[1], 0)       # Automatically converts dec/hex to int
    sectorSize = 2048

    if dvdSize == 0:
        print ("Zero size specified!")
        return

    print ("Dumping %d bytes" % dvdSize)

    offset = 0

    file = open (args[0], 'wb')

    startTime = time.time()

    while offset < dvdSize:
        try:
            dolwin.Execute ("DvdSeek " + str(offset))
            result = dolwin.ExecuteWithResult ("DvdRead " + str(sectorSize) + " 1")     # Silent mode
            file.write ( bytearray(result["result"]) )
        except Exception as e:
            print(e)
            break

        sys.stdout.write ("\r                ")
        sys.stdout.write ("\r%d / %d" % (offset / sectorSize, dvdSize / sectorSize))        # In sectors
        offset += sectorSize

    file.close()

    endTime = time.time()

    print ("\nDumped to " + args[0] + ". Time elapsed " + "{:.2f}".format(endTime - startTime) + " seconds")
