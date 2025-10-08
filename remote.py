from isolib import openHTTPISOFile
from cmktlib import open_buf


def get_iso_path(cmkt: int) -> str:
    with open("archive.index", "rt") as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            i, path = line.split(":", 1)

            if int(i) == cmkt:
                return path
        raise KeyError(f"cmkt {cmkt} not found in index file")


def search_circle(qry: str, cmkt: int):
    with openHTTPISOFile(get_iso_path(cmkt)) as iso:
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
    cmkts: list[int] = [57, 66, 67, 75]

    for cmkt in cmkts:
        print(f" --- C{cmkt} --- ")
        search_circle("たそもれら", cmkt)


if __name__ == "__main__":
    main()
