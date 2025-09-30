#!/bin/bash

set -euo pipefail

# NUMS="56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 73 75 79 80 82"
NUMS="59 60 61 62 63 64 65 66 67 68 69 70 73 75 79 80 82"

for NUM in $NUMS
do

7z x "Catalogs/CCC$NUM.ISO" -o"extracted/C$NUM"

done