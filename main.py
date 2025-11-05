from pathlib import Path

# import zipfile

from util import resolve_case_insensitive
from isolib import openLocalISOFile, openHTTPISOFile, ISOFile
from cmktlib import open_buf

def get_iso_path_ia(cmkt: int) -> str:
    with open("archive.index", "rt") as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            i, path = line.split(":", 1)

            if int(i) == cmkt:
                return path
        raise KeyError(f"cmkt {cmkt} not found in index file")

def get_iso_path_local(prefix: str, cmkt: int) -> Path:
    def resolve_file(fname: str) -> str:
        if fname == "-":
            return f"CCC{cmkt}.iso"
        elif fname == "-A":
            return f"CCC{cmkt}A.iso"
        else:
            return fname

    def resolve_dir(dname: str) -> str:
        if dname == "-":
            return f"comiket-{cmkt}-cd"
        else:
            return dname

    with open("mounted.index", "rt") as f:
        found = prefix
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            i, path = line.split(":")

            if int(i) == cmkt:
                spath = path.split("/")
                if len(spath) == 1:
                    found += resolve_file(spath[0])
                elif len(spath) == 2:
                    found += resolve_dir(spath[0])
                    found += "/"
                    found += resolve_file(spath[1])
                else:
                    raise ValueError(f"Invalid index row: {line}")
        if found:
            return resolve_case_insensitive(found)
        else:
            raise KeyError(f"cmkt {cmkt} not found in index file")


# def get_rom_zip(cmkt: int):
#     with openLocalISOFile(get_iso_path("mounted/", cmkt)) as iso:
#         buf = iso.get_file(f"/C0{cmkt}CUTH.CCZ")
#         with zipfile.ZipFile(buf) as zf:
#             print(zf.namelist())

def search(iso: ISOFile, qry: str, cmkt: int):
    CDATA_PATH="/CDATA/" if cmkt < 81 else f"/DATA{cmkt}/CDATA/"
    for entry in iso.list_files(CDATA_PATH):
        fname = str(entry)
        if fname.startswith(f"C{cmkt}ROM"):
            rom_num_str = fname[6]
            if rom_num_str.isdigit():
                rom_num = int(rom_num_str)
                if 0 < rom_num:
                    data = open_buf(cmkt, entry.get_buffer())
                    for cname, cyomi, aname, sname in data:
                        assert cname is not None
                        if qry in cname or (aname is not None and qry in aname):
                            print(
                                f"Found {cname} in C{cmkt} Day{rom_num} - {cyomi} / {aname} / {sname}"
                            )

def search_circle_local(qry: str, cmkt: int):
    iso_path = get_iso_path_local("mounted/", cmkt)
    # print("Opening ISO: ", iso_path)
    with openLocalISOFile(iso_path) as iso:
        search(iso, qry, cmkt)

def search_circle_ia(qry: str, cmkt: int):
    with openHTTPISOFile(get_iso_path_ia(cmkt)) as iso:
        search(iso, qry, cmkt)


def main():
    # cmkts: list[int] = list(range(56, 74)) + [75, 80]
    cmkts = list(range(56, 74)) + [75, 76, 77] + list(range(79, 83))

    for cmkt in cmkts:
        print(f" --- C{cmkt} --- ")
        search_circle_ia("たそもれら", cmkt)
        # search_circle_local("和泉つばす", cmkt)


if __name__ == "__main__":
    main()
