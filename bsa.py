#!/usr/bin/env python

import struct
import sys

if len(sys.argv) == 2:
    BSA_FILE = sys.argv[1]
    EXTRACT_FILE = None
elif len(sys.argv) == 4:
    BSA_FILE = sys.argv[1]
    EXTRACT_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]
else:
    print "usage: %s <bsa-file> [<file-to-extract> <output-filename>]" % sys.argv[0]
    sys.exit(1)

HEADER_LENGTH = 0x24

f = open(BSA_FILE)
header = f.read(HEADER_LENGTH)

bsa, version, offset, flags1, folder_count, file_count, folder_names_length, \
    file_names_length, flags2 = struct.unpack("<4sLLLLLLLL", header)

assert bsa == "BSA\x00"
assert version == 104
assert offset == HEADER_LENGTH

folders = [struct.unpack("<QLL", f.read(16)) for i in range(folder_count)]

files = []

for folder_hash, folder_file_count, folder_offset in folders:
    folder_path_length = ord(f.read(1))
    folder_path = f.read(folder_path_length)[:-1]
    
    for i in range(folder_file_count):
        file_hash, file_size, file_offset = struct.unpack("<QLL", f.read(16))
        files.append((file_hash, file_size, file_offset, folder_path))

assert folder_count == len(folders)
assert file_count == len(files)

file_num = 0 
current_filename = ""
found = False
while file_num < file_count:
    ch = f.read(1)
    if ch == "\x00":
        file_hash, file_size, file_offset, folder_path = files[file_num]
        if EXTRACT_FILE:
            if folder_path + "\\" + current_filename == EXTRACT_FILE:
                f.seek(file_offset)
                file_path_length = ord(f.read(1))
                file_path = f.read(file_path_length)
                assert file_path == EXTRACT_FILE
                file_length = struct.unpack("<L", f.read(4))[0]
                unknown = f.read(2)
                block_tag = 0
                out = open(OUTPUT_FILE, "w")
                while block_tag == 0:
                    block_tag, block_length, block_notlength = struct.unpack("<BHH", f.read(5))
                    assert block_length + block_notlength == 0xFFFF
                    data = f.read(block_length)
                    out.write(data)
                out.close()
                found = True
                break
        else:
            print "%s\\%s hash=%08X offset=%d length=%d" % \
                (folder_path, current_filename, file_hash, file_offset, file_size)
        current_filename = ""
        file_num += 1
    else:
        current_filename += ch

if EXTRACT_FILE and not found:
    print "File not found."
