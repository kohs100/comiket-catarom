from util import resolve_case_insensitive, iglob_ci
from typing import Dict
from io import BytesIO

COLUMNS = ["CIRCLE_NAME", "CIRCLE_YOMI", "AUTHOR_NAME", "SHINKAN_NAME"]

FORMATS: Dict[int, Dict[str, int | None]] = {
    56: {
        "CIRCLE_NAME": 7,
        "CIRCLE_YOMI": None,
        "AUTHOR_NAME": 8,
        "SHINKAN_NAME": 9
    },
    58: {
        "CIRCLE_NAME": 9,
        "CIRCLE_YOMI": None,
        "AUTHOR_NAME": 10,
        "SHINKAN_NAME": 11
    },
    60: {
        "CIRCLE_NAME": 9,
        "CIRCLE_YOMI": 10,
        "AUTHOR_NAME": 11,
        "SHINKAN_NAME": 12
    },
}

def find_format(cmkt: int) -> Dict[str, int | None]:
    keys = FORMATS.keys()
    keys = filter(lambda key: key <= cmkt, keys)
    key = max(list(keys))
    # print(f"Using format-C{key} for C{cmkt}")
    return FORMATS[key]

def open_rom(cmkt: int, path: str) -> list[list[str | None]]:
    data: list[list[str | None]] = []
    fmt = find_format(cmkt)

    with open(path, "rt", encoding="cp932", errors='ignore') as f:
        for line in f:
            assert line.endswith("\n")
            line = line[:-1]
            if len(line) == 0:
                continue
            tokens = line.split("\t")

            row: list[str | None] = []
            for col in COLUMNS:
                idx = fmt[col]
                if idx is None:
                    row.append(None)
                else:
                    row.append(tokens[idx])
            data.append(row)
    return data

def open_buf(cmkt: int, buf: BytesIO) -> list[list[str | None]]:
    data: list[list[str | None]] = []
    fmt = find_format(cmkt)

    for line in buf.readlines():
        line = line.decode(encoding="cp932", errors='ignore')
        assert line.endswith("\n")
        line = line[:-1]
        if len(line) == 0:
            continue
        tokens = line.split("\t")

        row: list[str | None] = []
        for col in COLUMNS:
            idx = fmt[col]
            if idx is None:
                row.append(None)
            else:
                row.append(tokens[idx])
        data.append(row)
    return data

def main():
    find_circle = "たそもれら"
    cmkts: list[int] = list(range(56, 71)) + [73, 75, 79, 80]
    for cmkt in cmkts:
        path = resolve_case_insensitive(f"extracted/c{cmkt}/cdata/")
        pat = path / f"c{cmkt}rom*.txt"
        roms = iglob_ci(str(pat))
        for rom in roms:
            rom_name = rom.split("/")[-1]
            cmkt_num = int(rom_name[1:3])
            rom_num_str = rom_name[6:7]
            if rom_num_str == ".":
                rom_num_str = "ALL"
            elif rom_num_str == "0":
                rom_num_str = "OUT"
            else:
                rom_num_str = str(int(rom_num_str))

            # print(f"Opening {cmkt_num}-{rom_num_str}")
            data = open_rom(cmkt_num, rom)

            for cname, cyomi, aname, sname in data:
                assert cname is not None
                if cname == find_circle:
                    print(f"Found {find_circle} in C{cmkt_num} Day{rom_num_str} - {cyomi} / {aname} / {sname}")

if __name__ == "__main__":
    main()
