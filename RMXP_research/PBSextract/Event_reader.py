import RGSS_classes
from RGSS_classes import Event, EventCommand, MoveRoute, MoveCommand, AudioFile, Tone, JSONdecode, JSONencode
import json, pathlib
from pprint import pprint
#from RGSS_Command_conversion import command_to_str

map='Map031'
with open(f'{map}_events.txt','r', encoding='utf-8-sig') as f:
    source=f.read()
    sourceOK = source.replace('\\', '\\\\')
    sourceOK = sourceOK.replace('\\\\"', '\\"')
    #sourceOK = sourceOK.replace('"', '\\"')
    #sourceOK = sourceOK.replace("'", '"')
    #pprint( source )
    eventObjects = json.loads( sourceOK, object_hook=JSONdecode )

print( type(eventObjects) )

this_dir=pathlib.Path()
out_dir=this_dir.joinpath(f'{map}_events')
if not out_dir.is_dir():
    out_dir.mkdir()

for eventObj in eventObjects:
    print( type(eventObj) )
    #pprint( eventObj )

    out_file=out_dir.joinpath(f'{map}_event{eventObj.name}')
    idx=1
    while out_file.is_file():
        out_file=out_dir.joinpath(f'{map}_event{eventObj.name}_{idx}')
        idx+=1

    out_file_obj=pathlib.Path(str(out_file)+'.json')
    with out_file_obj.open( 'w', encoding='utf-8') as f:
        print(f'Event_reader:writing to {out_file_obj}')
        json.dump( eventObj, fp=f, indent=4, default=JSONencode )
    #with open('testfile','r') as f:
    #    pprint( json.load(fp=f, object_hook=JSONdecode))

    eventObj.conversion()
    with out_file.open( 'w', encoding='utf-8') as f:
        print(f'Event_reader:writing to {out_file}')
        for item in RGSS_classes.commands_str:
            f.write( item+'\n' )