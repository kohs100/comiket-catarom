import pycdlib
from io import BytesIO
import zipfile

## Comic Market CD-ROM Catalog Directory Structure
## https://www.comiket.co.jp/cd-rom/DataFormatBackNumber.html
# CJM Format
# ? ~ C56 ~ C61
# CDATA - Circle data in Shift-JIS (cp942)
# JDATA - Page data in JPEG
# MDATA - Map data
FORMAT_CJM = ["CDATA", "JDATA", "MDATA"]

# CJMU Format
# C62 ~ C63
# CDATA - Circle data in Shift-JIS (cp942)
# JDATA - Page data in JPEG
# MDATA - Map data
# UDATA - Circle data in Unicode(UTF-16 BE)
FORMAT_CJMU = ["CDATA", "JDATA", "MDATA", "UDATA"]

# CJMPU Format
# C64
# CDATA - Circle data in Shift-JIS (cp942)
# JDATA - Page data in JPEG
# MDATA - Map data
# PDATA - Page data in PNG
# UDATA - Circle data in Unicode(UTF-16 BE)
FORMAT_CJMPU = ["CDATA", "JDATA", "MDATA", "PDATA", "UDATA"]

# CMPU Format
# C65 ~ C75 ~ ?
# CDATA - Circle data in Shift-JIS (cp942)
# MDATA - Map data
# PDATA - Page data in PNG
# UDATA - Circle data in Unicode(UTF-16 BE)
FORMAT_CMPU = ["CDATA", "MDATA", "PDATA", "UDATA"]

# CMU Format
# ? ~ C79 ~ C80
# CDATA - Circle data in Shift-JIS (cp942)
# MDATA - Map data
# UDATA - Circle data in Unicode(UTF-16 BE)
# Hires circle cut data in C0XXCUTH.CCZ (zip format)
# Lores circel cut data in C0XXCUTL.CCZ (zip format)
FORMAT_CMU = ["CDATA", "MDATA", "UDATA"]

# DVD Format
# ? ~ C82
# Follows CMPU Format in DATA82 directory
# Also there is CCZ format circle cut data in DATA82N/C0XXCUTX.CCZ
FORMAT_DVD = ["DATA82/CDATA", "DATA82/MDATA", "DATA82/PDATA", "DATA82/UDATA"]


def get_rom_zip(cmkt: int):
    iso = pycdlib.PyCdlib()
    iso.open(f"Catalogs/CCC{cmkt}.ISO", "rb")

    buf = BytesIO()

    iso.get_file_from_iso_fp(outfp=buf, iso_path=f"/C0{cmkt}CUTH.CCZ")
    buf.seek(0)

    with zipfile.ZipFile(buf) as zf:
        print(zf.namelist())

def get_rom(cmkt: int):
    iso = pycdlib.PyCdlib()
    iso.open(f"Catalogs/CCC{cmkt}.ISO", "rb")

    for entry in iso.list_children(iso_path="/CDATA"):
        print(entry.file_identifier())

def main():
    cmkts: list[int] = list(range(56, 71)) + [73, 75, 79, 80]

    get_rom(56)


if __name__ == "__main__":
    main()
