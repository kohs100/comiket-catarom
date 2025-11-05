# Comiket-catarom

Parse comiket cd-rom catalog and perform global search

## Comic Market CD-ROM Catalog Directory Structure

https://www.comiket.co.jp/cd-rom/DataFormatBackNumber.html

### CJM Format
* C56 ~ C61
* CDATA - Circle data in Shift-JIS (cp942)
* JDATA - Page data in JPEG
* MDATA - Map data

### CJMU Format
* C62 ~ C63
* CDATA - Circle data in Shift-JIS (cp942)
* JDATA - Page data in JPEG
* MDATA - Map data
* UDATA - Circle data in Unicode(UTF-16 BE)

### CJMPU Format
* C64
* CDATA - Circle data in Shift-JIS (cp942)
* JDATA - Page data in JPEG
* MDATA - Map data
* PDATA - Page data in PNG
* UDATA - Circle data in Unicode(UTF-16 BE)

### CMPU Format
* C65 ~ C77 ~ ?
* CDATA - Circle data in Shift-JIS (cp942)
* MDATA - Map data
* PDATA - Page data in PNG
* UDATA - Circle data in Unicode(UTF-16 BE)

### CMU Format
* ? ~ C79 ~ C80
* CDATA - Circle data in Shift-JIS (cp942)
* MDATA - Map data
* UDATA - Circle data in Unicode(UTF-16 BE)
* Hires circle cut data in C0XXCUTH.CCZ (zip format)
* Lores circel cut data in C0XXCUTL.CCZ (zip format)

### DVD Format
* C81 ~ C82
* Follows CMPU Format in DATA82 directory
* Also there is CCZ format circle cut data in DATA82N/C0XXCUTX.CCZ