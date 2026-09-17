#!/bin/sh
# Builds the release zip (GameData/SEP-KAS1-Patch + LICENSE + README) into dist/.
set -e
cd "$(dirname "$0")"
v=$(python3 -c "import json;d=json.load(open('GameData/SEP-KAS1-Patch/SEP-KAS1-Patch.version'))['VERSION'];print(f\"{d['MAJOR']}.{d['MINOR']}.{d['PATCH']}\")")
mkdir -p dist && rm -f "dist/SEP-KAS1-Patch-$v.zip"
zip -qr "dist/SEP-KAS1-Patch-$v.zip" GameData LICENSE README.md
echo "dist/SEP-KAS1-Patch-$v.zip"
