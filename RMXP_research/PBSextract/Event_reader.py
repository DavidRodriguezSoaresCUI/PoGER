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

def process_map( map_nb ):
    global known_scripts
    map = f'{map_nb:03}'
    this_dir=pathlib.Path('Maps')
    out_dir=this_dir.joinpath(f'{map}_events')
    assert this_dir.is_dir(), f'{pathlib.Path().resolve()}'
    
    print(f'processing {map}')

    def get_map_events():
        events_file = this_dir.joinpath(f'{map}.events')
        if not events_file.is_file():
            print(f'get_map_events: event file "{str(events_file)}" not found.')
            return None

        with events_file.open('r', encoding='utf-8-sig') as f:
            source=f.read()
            sourceOK = known_metaevents( source )
            sourceOK = sourceOK.replace('\\', '\\\\')
            sourceOK = sourceOK.replace('\\\\"', '\\"')
            #sourceOK = sourceOK.replace('"', '\\"')
            #sourceOK = sourceOK.replace("'", '"')
            #pprint( source )
            return sourceOK

    def make_safe_filenames( id, name, overwrite=False ):
        out_file=out_dir.joinpath(f'{map}_{id:03}_{name}')
        if not overwrite:
            idx=1
            while out_file.is_file():
                out_file=out_dir.joinpath(f'{map}_{id:03}_{name}_{idx}')
                idx+=1
        return out_file, pathlib.Path(str(out_file)+'.json')


    
    sourceOK = get_map_events()
    if not sourceOK:
        return

    if not out_dir.is_dir():
        out_dir.mkdir()

    eventObjects = json.loads( sourceOK, object_hook=JSONdecode )
    #print( type(eventObjects) )


    for eventObj in eventObjects:
        #print( type(eventObj) )
        #pprint( eventObj )

        out_file, out_file_obj = make_safe_filenames( eventObj.id, eventObj.name, overwrite=True )
        #print(f'out_file, out_file_obj:{out_file}, {out_file_obj}')

        with out_file_obj.open( 'w', encoding='utf-8') as f:
            #print(f'Event_reader:writing to {out_file_obj}')
            json.dump( eventObj, fp=f, indent=4, default=JSONencode )

        eventObj.conversion()
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

def pickle_this(data, save_file, print_on_success=None):
    save_file = pathlib.Path( save_file )
    with save_file.open(mode="wb") as fp:   #Pickling
        pickle.dump(data, fp)
        if print_on_success:
            assert isinstance( print_on_success, str )
            print( print_on_success )

def unpickle_this(save_file, print_on_success=None):
    save_file = pathlib.Path( save_file )
    if save_file.is_file():
        with save_file.open(mode="rb") as fp:   # Unpickling
            if print_on_success:
                assert isinstance( print_on_success, str )
                print( print_on_success )
            return pickle.load(fp)
    return None

def main():
    '''global known_scripts
    tmp = unpickle_this('known_scripts')
    if tmp:
        known_scripts = tmp'''
    
    '''for i in range(2,75):
        process_map( i )'''
    process_map( 11 )

    with open('scripts.log', 'w', encoding='utf-8') as f:
        for item in known_scripts:
            f.write( item + '\n' )

    '''print(f'known_scripts: .')
    for item in known_scripts:
        print(item)
    pickle_this( known_scripts, 'known_scripts' )'''

if __name__ == "__main__":
    main()
