#!/usr/bin/env python

# @@@ NOTE: THIS IS A WORK IN PROGRESS, AS I TRY TO WORK OUT HOW THE FILE
# @@@ FORMAT WORKS.


import struct
import sys

if len(sys.argv) == 2:
    TES_FILE = sys.argv[1]
else:
    print "usage: %s <tes-file>" % sys.argv[0]
    sys.exit(1)

f = open(TES_FILE)

while True:
    block_type = struct.unpack("<4s", f.read(4))[0]
    print block_type,
    if block_type in ["TES4", "GRUP", "GMST", "KYWD", "LCRT", "AACT", "TXST",
            "GLOB", "CLAS", "MGEF"]:
        # these blocks seem to be a fixed size rather than using the first
        # two bytes to indicate length
        print "-"
        print "\t%08X%08X%08X%08X%08X" % struct.unpack("<LLLLL", f.read(20))
    elif block_type in ["HEDR", "CNAM", "INTV", "EDID", "DATA", "OBND",
            "TX00", "TX01", "DNAM", "DODT", "TX03", "TX05", "TX07", "TX02",
            "TX04", "FNAM", "FLTV", "FULL", "DESC", "FACT", "VENV", "PLVD",
            "MAST", "MDOB", "KSIZ", "KWDA"]:
        # these blocks seem to indicate their length in the first two bytes
        length = struct.unpack("<H", f.read(2))[0]
        print length
        f.read(length)
    else:
        print "unknown"
        sys.exit(1)
