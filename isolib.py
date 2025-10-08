import pycdlib
from io import BytesIO
from pathlib import Path


class ISOEntry:
    def __init__(self, isofile: "ISOFile", filename: str, fullpath: str):
        self.isofile = isofile

        assert (
            filename.isupper() and fullpath.isupper()
        ), "Please use normalized path to initialize ISOEntry"

        self.filename = filename
        self.fullpath = fullpath

    def __str__(self):
        return self.filename

    def get_buffer(self) -> BytesIO:
        buf = BytesIO()
        self.isofile.iso.get_file_from_iso_fp(outfp=buf, iso_path=self.fullpath)  # type: ignore
        buf.seek(0)

        return buf


class ISOFile:
    def __init__(self, iso_path: Path):
        self.iso_path = iso_path
        self.iso = pycdlib.PyCdlib()  # type: ignore
        self.iso.open(str(iso_path), "rb")

    def get_file(self, fullpath: str) -> BytesIO:
        assert fullpath.isupper(), "Please use upper-case path."
        assert fullpath.startswith("/")

        basedir, filename = fullpath.rsplit("/", -1)

        if len(basedir) == 0:
            basedir = "/"

        for entry in self.list_files(basedir):
            if str(entry) == filename:
                return entry.get_buffer()
        raise KeyError(f"{fullpath} not found!!")

    def list_files(self, dirpath: str) -> list[ISOEntry]:
        assert dirpath == dirpath.upper(), "Please use upper-case path."

        fnames_ver: dict[str, int | None] = {}
        for entry in self.iso.list_children(iso_path=dirpath):  # type: ignore
            bname: bytes = entry.file_identifier()  # type: ignore
            assert isinstance(bname, bytes)

            if bname == b".":
                continue
            elif bname == b"..":
                continue

            # Normalize to upper case.
            name: str = bname.decode().upper()

            if ";" in name:
                realname, verid = name.rsplit(";", 1)
                verid = int(verid)

                if realname not in fnames_ver:
                    fnames_ver[realname] = verid
                else:
                    cur_verid = fnames_ver[realname]
                    assert cur_verid is not None
                    assert cur_verid != verid
                    if cur_verid < verid:
                        fnames_ver[realname] = verid
            else:
                assert name not in fnames_ver
                fnames_ver[name] = None

        ret: list[ISOEntry] = []
        for filename, verid in fnames_ver.items():
            if verid is None:
                fullpath = f"{dirpath}/{filename}"
            else:
                fullpath = f"{dirpath}/{filename};{verid}"
            ret.append(ISOEntry(self, filename, fullpath))

        return ret
