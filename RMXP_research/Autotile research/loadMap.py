#!/usr/bin/env python3
import codecs, json
from pprint import pprint
import numpy as np
from drslib import insure_python_version, check_os_compatibility, say_hello, skipNlines
from pathlib import Path

cwd = Path('.').resolve()
say_hello( 'LoadMap', cwd )
insure_python_version( '3.6.0' )
check_os_compatibility( ['windows', 'wsl'] )
skipNlines(2)

mapname='Map032'
with open(f'{mapname}.txt', encoding='utf-8-sig') as f:
        data = json.load(f)
map=np.array(data['Table']['data'])
map_uniq_tmp = np.unique(map)
map_uniq = map_uniq_tmp[map_uniq_tmp<384]
map_autotiles = np.sort(map_uniq%48)

print(f"Autotiles values found in {mapname} :")
pprint( np.unique(map_autotiles) )