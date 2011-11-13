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
    data = f.read(4)
    if not data:
        break
    block_type = struct.unpack("<4s", data)[0]
    print block_type,
    if block_type in ["GRUP"]:
        length = struct.unpack("<L", f.read(4))[0]
        print length
        f.read(16)
    elif block_type in ["TES4", "GMST", "KYWD", "LCRT", "AACT", "TXST",
            "GLOB", "CLAS", "FACT", "HDPT", "EYES", "RACE", "SOUN", "ASPC",
            "MGEF", "LTEX", "ENCH", "SPEL", "SCRL", "ACTI", "TACT", "ARMO",
            "BOOK", "CONT", "DOOR", "INGR", "LIGH", "MISC", "APPA", "STAT",
            "MSTT", "GRAS", "TREE", "FLOR", "FURN", "WEAP", "AMMO", "NPC_",
            "LVLN", "KEYM", "ALCH", "IDLM", "COBJ", "PROJ", "HAZD", "SLGM",
            "LVLI", "WTHR", "CLMT", "SPGD", "RFCT", "REGN", "NAVI", "CELL",
            "REFR", "ACHR", "PGRE", "NAVM", "PHZD", "WRLD", "LAND", "DIAL",
            "INFO", "QUST", "IDLE", "PACK", "CSTY", "LSCR", "LVSP", "ANIO",
            "WATR", "EFSH", "EXPL", "DEBR", "IMGS", "IMAD", "FLST", "PERK",
            "BPTD", "ADDN", "AVIF", "CAMS", "CPTH", "VTYP", "MATT", "IPCT",
            "IPDS", "ARMA", "ECZN", "LCTN", "MESG", "DOBJ", "LGTM", "MUSC",
            "FSTP", "FSTS", "SMBN", "SMQN", "SMEN", "DLBR", "MUST", "DLVW",
            "WOOP", "SHOU", "EQUP", "RELA", "SCEN", "ASTP", "OTFT", "ARTO",
            "MATO", "MOVT", "SNDR", "DUAL", "SNCT", "SOPM", "COLL", "CLFM",
            "REVB", "NAVI"]:
        length = struct.unpack("<L", f.read(4))[0]
        print length
        f.read(length + 16)
    else:
        print "unknown"
        sys.exit(1)
