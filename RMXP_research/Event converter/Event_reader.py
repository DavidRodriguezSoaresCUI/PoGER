import RGSS_classes
from RGSS_classes import Event, JSONdecode, JSONencode # EventCommand, MoveRoute, MoveCommand, AudioFile, Tone, 
import json, pathlib, re, pickle
from pprint import pprint
from utils import unquote

known_scripts=[]

def known_metaevents( source, verbose=False ):

    go_up_through_door_before = re.escape('''{ "_class":"EventCommand", "code": 209, "indent": 0, "parameters": [ 0, { "_class":"MoveRoute", "repeat": false, "skippable": true, "list": [ { "_class":"MoveCommand", "code": 44, "parameters": { "_class":"AudioFile", "name":"Door enter", "volume":100, "pitch":100 } },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 17, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 18, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 19, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 } ] } ] },
 { "_class":"EventCommand", "code": 210, "indent": 0, "parameters": null },
 { "_class":"EventCommand", "code": 209, "indent": 0, "parameters": [ -1, { "_class":"MoveRoute", "repeat": false, "skippable": true, "list": [ { "_class":"MoveCommand", "code": 37, "parameters": null },
 { "_class":"MoveCommand", "code": 4, "parameters": null },
 { "_class":"MoveCommand", "code": 38, "parameters": null } ] } ] },
 { "_class":"EventCommand", "code": 210, "indent": 0, "parameters": null },
 { "_class":"EventCommand", "code": 208, "indent": 0, "parameters": 0 },
 { "_class":"EventCommand", "code": 209, "indent": 0, "parameters": [ 0, { "_class":"MoveRoute", "repeat": false, "skippable": true, "list": [ { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 18, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 17, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 16, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 } ] } ] },
 { "_class":"EventCommand", "code": 210, "indent": 0, "parameters": null },
 { "_class":"EventCommand", "code": 223, "indent": 0, "parameters": [ { "_class":"Tone", "RGBG":[-255, -255, -255, 0] }, 6 ] },
 { "_class":"EventCommand", "code": 106, "indent": 0, "parameters": 8 },
 { "_class":"EventCommand", "code": 208, "indent": 0, "parameters": 1 },
 { "_class":"EventCommand", "code": 201, "indent": 0, "parameters": [ ''')
    go_up_through_door_after = re.escape(''', 1 ] },
 { "_class":"EventCommand", "code": 223, "indent": 0, "parameters": [ { "_class":"Tone", "RGBG":[0, 0, 0, 0] }, 6 ] }''')

    go_up_through_door = go_up_through_door_before + r'([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)' + go_up_through_door_after

    go_down_out_door = '''{ "_class":"EventCommand", "code": 111, "indent": 0, "parameters": [ 12, "get_character(0).onEvent?" ] },
 { "_class":"EventCommand", "code": 208, "indent": 1, "parameters": 0 },
 { "_class":"EventCommand", "code": 209, "indent": 1, "parameters": [ 0, { "_class":"MoveRoute", "repeat": false, "skippable": true, "list": [ { "_class":"MoveCommand", "code": 44, "parameters": { "_class":"AudioFile", "name":"Door enter", "volume":100, "pitch":100 } },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 17, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 18, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 19, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 } ] } ] },
 { "_class":"EventCommand", "code": 210, "indent": 1, "parameters": null },
 { "_class":"EventCommand", "code": 208, "indent": 1, "parameters": 1 },
 { "_class":"EventCommand", "code": 209, "indent": 1, "parameters": [ -1, { "_class":"MoveRoute", "repeat": false, "skippable": true, "list": [ { "_class":"MoveCommand", "code": 1, "parameters": null } ] } ] },
 { "_class":"EventCommand", "code": 210, "indent": 1, "parameters": null },
 { "_class":"EventCommand", "code": 209, "indent": 1, "parameters": [ 0, { "_class":"MoveRoute", "repeat": false, "skippable": true, "list": [ { "_class":"MoveCommand", "code": 18, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 17, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 },
 { "_class":"MoveCommand", "code": 16, "parameters": null },
 { "_class":"MoveCommand", "code": 15, "parameters": 2 } ] } ] },
 { "_class":"EventCommand", "code": 210, "indent": 1, "parameters": null },
 { "_class":"EventCommand", "code": 412, "indent": 0, "parameters": null },
 { "_class":"EventCommand", "code": 355, "indent": 0, "parameters": "setTempSwitchOn(\\"A\\")" }'''

    fading_transfer=re.escape('''{ "_class":"EventCommand", "code": 250, "indent": 0, "parameters": { "_class":"AudioFile", "name":"Door exit", "volume":80, "pitch":100 } },
 { "_class":"EventCommand", "code": 223, "indent": 0, "parameters": [ { "_class":"Tone", "RGBG":[-255, -255, -255, 0] }, 6 ] },
 { "_class":"EventCommand", "code": 106, "indent": 0, "parameters": 8 },
 { "_class":"EventCommand", "code": 201, "indent": 0, "parameters": [ ''') + r'([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)' + re.escape(''', 1 ] },
 { "_class":"EventCommand", "code": 223, "indent": 0, "parameters": [ { "_class":"Tone", "RGBG":[0, 0, 0, 0] }, 6 ] }''')


    match = re.search( go_up_through_door, source )
    if match:
        if verbose:
            print('known_metaevents: go_up_through_door event detected')
        replacement = r'{ "_class":"EventCommand", "code": 201, "indent": 0, "parameters": [ \1, \2, \3, \4, \5, 0 ] }'
        source = re.sub( go_up_through_door, replacement, source)
        if go_down_out_door in source:
            if verbose:
                print('known_metaevents: go_down_out_door event detected')
            source = source.replace( go_down_out_door, '', 1 )

    match = re.search( fading_transfer, source )
    if match:
        if verbose:
            print('known_metaevents: fading_transfer event detected')
        replacement = r'{ "_class":"EventCommand", "code": 201, "indent": 0, "parameters": [ \1, \2, \3, \4, \5, 0 ] }'
        source = re.sub( fading_transfer, replacement, source)
        if go_down_out_door in source:
            if verbose:
                print('known_metaevents: go_down_out_door event detected')
            source = source.replace( go_down_out_door, '', 1 )


    return source

def process_events( events, output_object_JSON=True ):
    from pathlib import Path
    assert isinstance( events, Path )
    global known_scripts

    map        = events.stem
    events_dir = events.parents[0]
    output_dir = events_dir.joinpath(f'{map}_events')
    
    print(f'processing {map}')

    def get_map_events():
        with events.open('r', encoding='utf-8-sig') as f:
            source=f.read()
            sourceOK = known_metaevents( source )
            sourceOK = sourceOK.replace('\\', '\\\\')
            sourceOK = sourceOK.replace('\\\\"', '\\"')
            
            return sourceOK

    def make_safe_filenames( id, name, overwrite=False ):
        out_file = output_dir.joinpath(f'{map}_{id}_{name}')
        if not overwrite:
            idx=1
            while out_file.is_file():
                out_file = output_dir.joinpath(f'{map}_{id}_{name}_{idx}')
                idx+=1
        return out_file, pathlib.Path(str(out_file)+'.json')

    
    sourceOK = get_map_events()
    if not sourceOK:
        return

    if not output_dir.is_dir():
        output_dir.mkdir()

    eventObjects = json.loads( sourceOK, object_hook=JSONdecode )
    #print( type(eventObjects) )


    for eventObj in eventObjects:
        
        out_file, out_file_obj = make_safe_filenames( eventObj.id, eventObj.name, overwrite=True )
        #print(f'out_file, out_file_obj:{out_file}, {out_file_obj}')

        if output_object_JSON:
            with out_file_obj.open( 'w', encoding='utf-8') as f:
                #print(f'Event_reader:writing to {out_file_obj}')
                json.dump( eventObj, fp=f, indent=4, default=JSONencode )

        eventObj.conversion()

        if output_object_JSON:
            if RGSS_classes.commands_str == []:
                out_file_obj.unlink()
                return
        
        with out_file.open( 'w', encoding='utf-8') as f:
            #print(f'Event_reader:writing to {out_file}')
            for item in RGSS_classes.commands_str:
                f.write( item+'\n' )

        with out_file.open( 'r', encoding='utf-8') as f:
            #print(f'Event_reader:writing to {out_file}')
            data=f.read()
            match = re.search( r's:([^\(\)\n]+).*?\n', data )
            if match:
                for item in match.groups():
                    if not (item in known_scripts):
                        #print( f'new script : {item} from {map}' )
                        known_scripts.append( item )
                        

def find_events():
    import pathlib
    mapfolder = pathlib.Path().joinpath('Maps')
    assert mapfolder.is_dir(), f'{mapfolder} directory not found !'

    from FileCollector import FileCollector
    fc = FileCollector( mapfolder )
    res = fc.collect( pattern = '**/*.events' )
    return [ f for f in res if f.is_file() and (f.stem).isdigit() ]
    

if __name__ == "__main__":
    events = find_events()
    print( f'Found {len(events)} maps with events !')
    events_dict = { int(e.stem):e for e in events }
    available_maps = sorted(list(events_dict.keys()))
    from time import time

    while True:
        print( f'\nMaps : {available_maps}')
        selection = input('Selection ([Q]uit/[A]ll/number) : ')
        
        start = time()
        if selection.isdigit():
            selection = int(selection)
            if selection in available_maps:
                process_events( events_dict[ selection ] )
                print(f'Processing took {time()-start:0.1f} seconds !')
            else:
                print( f"Map {selection} is not available. Please try again.\n")
        elif selection.lower() == 'q':
            break
        elif selection.lower() == 'a':
            import multiprocessing as mp
            pool = mp.Pool(mp.cpu_count()) # set up multiprocessing
            pool.map_async( process_events, events ) # process all events in parallel
            pool.close() # closes the pool
            pool.join() # waits for every process_map to be finished
            print(f'Processing took {time()-start:0.1f} seconds !')
        else:
            print( f'Selection "{selection}" unrecognized. Please try again.\n')

    if known_scripts:
        with open('scripts.log', 'w', encoding='utf-8') as f:
            for item in known_scripts:
                f.write( item + '\n' )

    print( "\nEnd of program. Have a nice day !" )
