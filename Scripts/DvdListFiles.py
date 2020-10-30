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

    nametable = __DvdReadLargeChunk(dolwin, fstOffset + numEntries * fstEntrySize, nameTableLength)
    #print ("nametable: " + str(nametable))

    # Collect all FST entries into a common collection for easy display

    entryOffset = fstOffset             # Offset of the current entry
    entries = []                    # Save all entries to this collection

    while numEntries != 0:
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

        entries.append(entry)
        numEntries -= 1
        entryOffset += fstEntrySize

    # Consecutively display the contents of FST entries (each entry is either a directory or a file)

    print ("category [entry_id]: path (nameOffset), ... directory/file specific info")

    for e in entries:
        __DumpFstEntry (e, entries, nametable)


'''
    Display FST entry contents
'''
def __DumpFstEntry (entry, entries, nametable):
    if entry.isDir:
        if entry.id == 0:
            print ("dir [0]: (root)")
        else:
            print ("dir [%d]: %s (%d), parent: %d, next: %d" % (entry.id, __DvdGetName(nametable, entry.nameOffset), entry.nameOffset, entry.parentOffset, entry.nextOffset))
    else:
        fullPath = __DvdGetName(nametable, entry.nameOffset)

        # To understand how the FST hierarchical structure works, see the bottom of this file.

        # Get parent directory by iterating over FST entries backward until isDir = 1 is encountered.
        # The `next` value for the directory must be greater file ID

        parentDirId = 0
        currentId = entry.id
        
        while currentId != 0:
            if entries[currentId].isDir and entries[currentId].nextOffset > entry.id:
                parentDirId = currentId
                break
            currentId -= 1

        # Recursively climb up directories until a directory with parent = 0 is encountered

        while parentDirId != 0:
            fullPath = __DvdGetName(nametable, entries[parentDirId].nameOffset) + "/" + fullPath
            parentDirId = entries[parentDirId].parentOffset
        fullPath = "/" + fullPath

        print ("file [%d]: %s (%d), offset: 0x%0.8X, len: 0x%0.8X" % (entry.id, fullPath, entry.nameOffset, entry.fileOffset, entry.fileLength))


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
    Load large block of data. Loading is performed in chunks no larger than a sector.
'''
def __DvdReadLargeChunk(dolwin, offset, size):
    result = []
    DVD_SECTOR_SIZE = 2048

    while size != 0:
        actualSize = min (size, DVD_SECTOR_SIZE)
        dolwin.Execute ("DvdSeek " + str(offset))
        res = dolwin.ExecuteWithResult ( "DvdRead " + str(actualSize) + " 1")
        result += res["result"]
        offset += actualSize
        size -= actualSize

    return result


'''
    Get zero-terminated ANSI byte string from nametable
'''
def __DvdGetName(nametable, offset):
    len = 0
    while nametable[offset + len] != 0:
        len += 1
    return bytearray(nametable[offset:offset+len]).decode()


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



'''

An example of a directory structure in FST:

/
    AudioRes
        Banks 
            LuiSe2_0.aw
            LuiSec0_0.aw
            LuiSec1_0.aw
            LuiSec2_0.aw
        JaiInit.aaf             -- file
        Seqs
            JaiArcS.arc
        Stream
            TMansion.afc
            TMOpen.afc
    CVS
        ...


dir [84]: AudioRes (981), parent: 0, next: 96
dir [85]: Banks (990), parent: 84, next: 90
file [86]: /AudioRes/Banks/LuiSe2_0.aw (996), offset: 0x4D5785F0, len: 0x0003EA60
file [87]: /AudioRes/Banks/LuiSec0_0.aw (1008), offset: 0x4D5B7050, len: 0x002325C0
file [88]: /AudioRes/Banks/LuiSec1_0.aw (1021), offset: 0x4D7E9610, len: 0x00637200
file [89]: /AudioRes/Banks/LuiSec2_0.aw (1034), offset: 0x4DE20810, len: 0x005E1CE0
file [90]: /AudioRes/JaiInit.aaf (1047), offset: 0x56D96820, len: 0x0003B900
dir [91]: Seqs (1059), parent: 84, next: 93
file [92]: /AudioRes/Seqs/JaiArcS.arc (1064), offset: 0x4E4024F0, len: 0x0008DEA0
dir [93]: Stream (1076), parent: 84, next: 96
file [94]: /AudioRes/Stream/TMansion.afc (1083), offset: 0x4E490390, len: 0x000DE040
file [95]: /AudioRes/Stream/TMOpen.afc (1096), offset: 0x4E56E3D0, len: 0x0024FC00
dir [96]: CVS (1107), parent: 0, next: 100

As you can see, the `next` field in the `Banks` directory points to the `JaiInit.aaf` file, where the current level of the `Banks` folder hierarchy ends.

'''
