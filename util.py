from typing import Union, Iterable
from pathlib import Path

import glob
import os
import unicodedata

def resolve_case_insensitive(path: Union[str, Path]) -> Path:
    """주어진 경로 문자열을 대소문자 무시에 맞춰 실제 디스크에 존재하는
    '정확한 대소문자' 경로로 보정해서 반환. 없으면 None."""
    p = Path(path)

    # 이미 정확히 존재하면 바로 반환
    if p.exists():
        return p.resolve()

    # 시작점 설정
    parts = p.parts
    if p.is_absolute():
        cur = Path(parts[0])
        parts = parts[1:]
    else:
        cur = Path.cwd()

    # 각 단계마다 디렉터리 엔트리를 열어 case-insensitive 매칭
    for part in parts:
        want = unicodedata.normalize("NFC", part).casefold()
        with os.scandir(cur) as it:
            matched_name = None
            for entry in it:
                name_ci = unicodedata.normalize("NFC", entry.name).casefold()
                if name_ci == want:
                    matched_name = entry.name
                    break
        if matched_name is None:
            raise FileNotFoundError
        cur = cur / matched_name
    return cur.resolve()

def ci_pattern(pat: str) -> str:
    out: list[str] = []
    in_class = 0
    for ch in pat:
        if ch == '[':
            in_class += 1
        elif ch == ']' and in_class:
            in_class -= 1
        if in_class or not ch.isalpha():
            out.append(ch)
        else:
            out.append(f'[{ch.lower()}{ch.upper()}]')
    return ''.join(out)

def iglob_ci(pattern: str, recursive: bool = True) -> Iterable[str]:
    return glob.iglob(ci_pattern(pattern), recursive=recursive)
