'''
    Parse the FST of the current disk and list the files
    Example:
        MountIso c:/isos/ac.gcm         (mount existing GCM)
        % DvdListFiles

'''
def do_command(dolwin, args):

    # Check if any DVD is mounted (real GCM image or DolphinSDK virtual disk)

    mounted = False

    res = dolwin.ExecuteWithResult ("DvdInfo 1")        # Silent mode
    #print (res)    

    for i in res["result"]:
        if type(i) == str:
            mounted = i != ""

    if not mounted:
        print ("DVD is not mounted")
        return

    # Get FST offset on disk and its size

    DVD_BB2_OFFSET = 0x0420
    DVD_APPLDR_OFFSET = 0x2440
    BB2_FSTPosition = 4
    BB2_FSTLength = 8
    fstEntrySize = 12;    

    fstOffset = __DvdReadUInt32 (dolwin, DVD_BB2_OFFSET + BB2_FSTPosition)
    fstLength = __DvdReadUInt32 (dolwin, DVD_BB2_OFFSET + BB2_FSTLength)        # Including name table

    print ( "FST offset: 0x%0.8X, length: 0x%0.8X"  % (fstOffset, fstLength))

    if fstOffset <= DVD_APPLDR_OFFSET:
        print ("Suspicious FST offset")
        return

    if fstLength > 16*1024*1024 or fstLength < fstEntrySize:
        print ("Invalid FST size")
        return

    # Get the number of entries in FST

    if __DvdReadUInt8(dolwin, fstOffset) != 1:
        print ("Invalid FST format. The first entry must be of type isDir = 1")
        return

    numEntries = __DvdReadUInt32(dolwin, fstOffset + 8)

    if numEntries * fstEntrySize > fstLength:
        print ("The number of records exceeds the specified FST size (including nametable)")
        return

    nameTableLength = fstLength - numEntries * fstEntrySize
    if nameTableLength <= 0:
        print ("Suspicious nametable size")
        return

    print ("FST entries count: " + str(numEntries))
    print ("Nametable size: " + str(nameTableLength) + " bytes")

    # Load nametable

    dolwin.Execute ("DvdSeek " + str(fstOffset + numEntries * fstEntrySize))
    res = dolwin.ExecuteWithResult ( "DvdRead " + str(nameTableLength) + " 1")
    nametable = res["result"]
    print ("nametable: " + str(nametable))

    # Consecutively display the contents of FST entries (each entry is either a directory or a file)

    entryOffset = fstOffset             # Offset of the current entry
    entries = []                    # Save all entries to this collection

    while numEntries != 0:
        dolwin.Execute ("DvdSeek " + str(entryOffset))
        res = dolwin.ExecuteWithResult ( "DvdRead " + str(fstEntrySize) + " 1")

        entry = FSTEntry()

        entry.id = len(entries)
        entry.isDir = __DvdReadUInt8(dolwin, entryOffset) != 0
        entry.nameOffset = (__DvdReadUInt8(dolwin, entryOffset + 1) << 16) | __DvdReadUInt16(dolwin, entryOffset + 2)

        if entry.isDir:
            entry.parentOffset = __DvdReadUInt32(dolwin, entryOffset + 4)
            entry.nextOffset = __DvdReadUInt32(dolwin, entryOffset + 8)
        else:
            entry.fileOffset = __DvdReadUInt32(dolwin, entryOffset + 4)
            entry.fileLength = __DvdReadUInt32(dolwin, entryOffset + 8)

        __DumpFstEntry (entry, nametable)

        entries.append(entry)
        numEntries -= 1
        entryOffset += fstEntrySize


'''
    Display FST entry contents
'''
def __DumpFstEntry (entry, nametable):
    if entry.isDir:
        print ("directory: nameOffset: 0x%0.8X, parentOffset: 0x%0.8X, nextOffset: 0x%0.8X" % (entry.nameOffset, entry.parentOffset, entry.nextOffset))
    else:
        print ("file: nameOffset: 0x%0.8X, fileOffset: 0x%0.8X, fileLength: 0x%0.8X" % (entry.nameOffset, entry.fileOffset, entry.fileLength))


'''
    Read uint8_t from disk
'''
def __DvdReadUInt8(dolwin, offset):
    dolwin.Execute ("DvdSeek " + str(offset))
    res = dolwin.ExecuteWithResult ( "DvdRead 1 1")
    return res["result"][0]


'''
    Read uint16_t from disk (already swapped to little-endian)
'''
def __DvdReadUInt16(dolwin, offset):
    dolwin.Execute ("DvdSeek " + str(offset))
    res = dolwin.ExecuteWithResult ( "DvdRead 2 1")
    return (res["result"][0] << 8) | (res["result"][1])


'''
    Read uint32_t from disk (already swapped to little-endian)
'''
def __DvdReadUInt32(dolwin, offset):
    dolwin.Execute ("DvdSeek " + str(offset))
    res = dolwin.ExecuteWithResult ( "DvdRead 4 1")
    return (res["result"][0] << 24) | (res["result"][1] << 16) | (res["result"][2] << 8) | (res["result"][3])


'''
    Get zero-terminated ANSI byte string from nametable
'''
def __DvdGetName(nametable, offset):
    return


'''
struct DVDFileEntry
{
    uint8_t      isDir;                  // 1, if directory
    uint8_t      nameOffsetHi;      // Relative to Name Table start
    uint16_t     nameOffsetLo;
    union
    {
        struct                      // file
        {
            uint32_t     fileOffset;        // Relative to disk start (0)
            uint32_t     fileLength;        // In bytes
        };
        struct                      // directory
        {
            uint32_t     parentOffset;   // parent directory FST index
            uint32_t     nextOffset;     // next directory FST index
        };
    };
};
'''
class FSTEntry (object):
    pass
