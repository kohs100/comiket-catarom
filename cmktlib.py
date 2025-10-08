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
