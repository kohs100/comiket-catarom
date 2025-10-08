import zipfile

from pathlib import Path

from util import resolve_case_insensitive
from isolib import openLocalISOFile
from cmktlib import open_buf

import fsspec  # type: ignore


def get_iso_path(prefix: str, cmkt: int) -> Path:
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


def get_rom_zip(cmkt: int):
    with openLocalISOFile(get_iso_path("mounted/", cmkt)) as iso:
        buf = iso.get_file(f"/C0{cmkt}CUTH.CCZ")
        with zipfile.ZipFile(buf) as zf:
            print(zf.namelist())


def search_circle(qry: str, cmkt: int):
    with openLocalISOFile(get_iso_path("mounted/", cmkt)) as iso:
        for entry in iso.list_files("/CDATA/"):
            fname = str(entry)
            if fname.startswith(f"C{cmkt}ROM"):
                rom_num_str = fname[6]
                if rom_num_str.isdigit():
                    rom_num = int(rom_num_str)
                    if 0 < rom_num:
                        data = open_buf(cmkt, entry.get_buffer())
                        for cname, cyomi, aname, sname in data:
                            assert cname is not None
                            if qry in cname:
                                print(
                                    f"Found {cname} in C{cmkt} Day{rom_num} - {cyomi} / {aname} / {sname}"
                                )


def main():
    fs = fsspec.filesystem(  # type: ignore
        "blockcache",
        target_protocol="local",
        cache_storage="./local-iso-cache",
        same_names=True,
    )

    cmkts: list[int] = list(range(56, 71)) + [73, 75, 79, 80]

    for cmkt in cmkts:
        print(f" --- C{cmkt} --- ")
        search_circle("たそもれら", cmkt)


if __name__ == "__main__":
    main()
