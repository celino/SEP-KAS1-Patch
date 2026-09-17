#!/bin/sh
# Builds the release zip (GameData/SEP-KAS1-Patch + LICENSE + README) into dist/.
set -e
cd "$(dirname "$0")"
v=$(python3 -c "import json;d=json.load(open('GameData/SEP-KAS1-Patch/SEP-KAS1-Patch.version'))['VERSION'];print(f\"{d['MAJOR']}.{d['MINOR']}.{d['PATCH']}\")")
mkdir -p dist && rm -f "dist/SEP-KAS1-Patch-$v.zip"
python3 -c "import shutil,zipfile,os
z=zipfile.ZipFile('dist/SEP-KAS1-Patch-$v.zip','w',zipfile.ZIP_DEFLATED)
for root,_,fs in os.walk('GameData'):
    [z.write(os.path.join(root,f)) for f in fs]
z.write('LICENSE'); z.write('README.md'); z.close()"
echo "dist/SEP-KAS1-Patch-$v.zip"
