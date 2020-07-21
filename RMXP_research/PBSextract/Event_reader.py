import RGSS_classes
from RGSS_classes import Event, EventCommand, MoveRoute, MoveCommand, AudioFile, Tone, JSONdecode, JSONencode
import json 
from pprint import pprint
#from RGSS_Command_conversion import command_to_str

map='Map006'
with open(f'{map}_events.txt','r', encoding='utf-8-sig') as f:
    source=f.read()
    sourceOK = source.replace('\\', '\\\\')
    sourceOK = sourceOK.replace('\\\\"', '\\"')
    #sourceOK = sourceOK.replace('"', '\\"')
    #sourceOK = sourceOK.replace("'", '"')
    #pprint( source )
    eventObjects = json.loads( sourceOK, object_hook=JSONdecode )

print( type(eventObjects) )

for eventObj in eventObjects:
    print( type(eventObj) )
    #pprint( eventObj )
    with open(f'{map}_event{eventObj.name}.obj','w', encoding='utf-8') as f:
        json.dump( eventObj, fp=f, indent=4, default=JSONencode )
    #with open('testfile','r') as f:
    #    pprint( json.load(fp=f, object_hook=JSONdecode))

    eventObj.conversion()
    with open(f'{map}_event{eventObj.name}', 'w', encoding='utf-8') as f:
        for item in RGSS_classes.commands_str:
            f.write( item+'\n' )