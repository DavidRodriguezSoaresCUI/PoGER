# from RGSS_classes import Tileset, Map, MapInfo, Event, Page, Condition, Graphic, EventCommand, MoveRoute, MoveCommand, AudioFile, Tone

from RGSS_Command_conversion import command_to_str
from utils import direction_toString, intersect_dict, substract_dict, flatten_dict, unquote
from pprint import pprint
commands_str=[]

event_ignore_list = ['Boulder_position_checks']

def assert_same_class(obj, c):
    try:
        c2=switcher[obj['_class']]
    except TypeError:
        c2=obj.__class__
    except KeyError:
        print(f'assert_same_class: no "_class", c={c}')
    if c2!=c: 
        if not (c2==EventCommand.__class__ and c==MoveCommand.__class__):
            print(f'Init: class mismatch : {c2} not {c}')

def cfg_cleanup( d ):
    d.pop('tmp_cfg', None)
    d.pop('own_cfg', None)
    d.pop('config', None)
    for k,v in d.items():
        if isinstance(v, str) and (' ' in v) and (not ('"' in v)):
            d[k] = f'"{v}"'

    switcher={
        'Down':'S',
        'Up':'N',
        'Left':'W',
        'Right':'E',
    }
    if 'direction' in d.keys():
        tmp = switcher.get(d['direction'], None)
        assert tmp!=None
        d['direction'] = tmp
    return d

def cfg2str( d ):
    assert isinstance(d, dict)
    return '\r\n'.join( [ f'{k}={v}' for k,v in cfg_cleanup( d ).items() ] )

def add_command_str( *args ):
    (s,concat) = command_to_str(*args)
    if concat:
        import re
        from RGSS_Command_conversion import indent_symbol
        previous = commands_str.pop()
        if previous[-1]=='"':
            previous = previous[:-1]
        after = unquote(s)
        
        s = indent_symbol*args[2] + re.sub('(?<!^) +', ' ', f'{previous} {after}"' ).strip()
    if s:
        commands_str.append( s )


'''class Tileset:

    def __init__(self):
        self.id = 0
        self.name = ''
        self.autotile_names = []
        self.panorama_name = None
        self.panorama_hue = None
        self.fog_name = ""
        self.fog_hue = 0
        self.fog_opacity = 64
        self.fog_blend_type = 0
        self.fog_zoom = 200
        self.fog_sx = 0
        self.fog_sy = 0
        self.battleback_name = ""
        self.passages=None
        self.priorities=None
        self.terrain_tags=None

    @classmethod
    def fromJSON( cls, obj ):
        pass

class CommonEvent:

    def __init__(self):
        self.id = 0
        self.name = ""
        self.trigger = 0
        self.switch_id = 1
        self.list = []

class Map:

    def __init__(self, width, height):
        self.tileset_id = 1
        self.width = width
        self.height = height
        self.autoplay_bgm = False
        self.bgm = None
        self.autoplay_bgs = False
        self.bgs = None
        self.encounter_list = []
        self.encounter_step = 30
        self.data = None
        self.events = None

    @classmethod
    def fromJSON( cls, obj ):
        pass

class MapInfo:

    def __init__(self):
        self.name = ""
        self.parent_id = 0
        self.order = 0
        self.expanded = False
        self.scroll_x = 0
        self.scroll_y = 0 '''

class Event:
    class Page:
        class Condition:

            def __init__(self, obj):
                #print(f"Condition: obj is a {type(obj)}")
                if obj==None:
                    tmp = dict()
                    tmp['_class'] = 'Page::Condition'
                    obj=tmp

                assert_same_class( obj, self.__class__ )

                self._class = obj['_class']
                self.switch1 = obj.get('S1', None)
                self.switch2 = obj.get('S2', None)
                self.self_switch = obj.get('SS', None)
                var = obj.get('Var', False)
                self.variable = var['id'] if var else None
                self.variable_value = var['val'] if var else None

            def __str__(self):
                import PE_variables_switches
                res=''
                
                for s in [self.switch1, self.switch2]:
                    if s!=None:
                        #print(f'Condition::str s={s}')
                        switch = PE_variables_switches.switches.get(int(s), None)
                        if switch:
                            res += f'{switch} == :ON'
                
                if self.self_switch:
                    res += f':{self.self_switch} == :ON'

                if self.variable:
                    variable = PE_variables_switches.variables.get(self.variable, None)
                    if variable:
                        res += f'{variable} >= {self.variable_value}'
                # print(f'Condition::str res={res}')
                return res # cfg2str(substract_dict( self.__dict__, self.__class__(None).__dict__))

        class Graphic:

            def __init__(self, obj):
                if obj==None:
                    tmp = dict()
                    tmp['_class'] = 'Page::Graphic'
                    obj=tmp

                assert_same_class( obj, self.__class__ )

                self._class = obj['_class']
                tile_id = obj.get('tile_id', 0)
                self.graphic = tile_id if (tile_id!=0) else obj.get('character_name', '')

                #self.character_hue = obj.get('character_hue', 0)
                self.direction = obj.get('direction', 'Down')
                self.pattern = obj.get('pattern', 0)
                self.opacity = obj.get('opacity', 255)
                #self.blend_type = obj.get('blend_type', 'Normal')

                #assert isinstance( self.tile_id , int )
                assert isinstance( self.graphic , str ) or isinstance( self.graphic , int ), f'self.graphic invalid type : {self.graphic}, {type(self.graphic)}'
                #assert isinstance( self.character_hue , int )
                assert isinstance( self.direction , str )
                assert isinstance( self.pattern , int )
                assert isinstance( self.opacity , int )
                #assert isinstance( self.blend_type , str )

                if self.graphic=='invisible':
                    self.graphic=''

            def __str__(self):
                return cfg2str( self.get_reduced_dict() )

            def get_reduced_dict(self):
                return substract_dict( self.__dict__, self.__class__(None).__dict__ )


        def __init__(self, obj, silent=True):
            if obj==None:
                tmp = dict()
                tmp['_class'] = 'Page'
                obj=tmp
            assert_same_class( obj, self.__class__ )
            if not silent:
                print("Page constructor")
        
            self._class = obj['_class']
            cond = obj.get('condition', None )
            self.condition = cond if isinstance(cond, self.__class__.Condition) else self.__class__.Condition( cond )
            gra = obj.get('graphic', None )
            self.graphic = gra if isinstance(gra, self.__class__.Graphic) else self.__class__.Graphic( gra )
            self.move = obj.get('move', 'Fixed' )
            self.move_speed = obj.get('move_speed', 3)
            self.move_frequency = obj.get('move_frequency', 3)
            self.walk_anime = obj.get('walk_anime', True)
            self.step_anime = obj.get('step_anime', False)
            self.direction_fix = obj.get('direction_fix', False)
            self.through = obj.get('through', False)
            self.always_on_top = obj.get('always_on_top', False)
            self.trigger = obj.get('trigger', 'onPlayerAction')
            tmp = obj.get('list', None)
            self.list = [ item if (isinstance(item, MoveCommand) or isinstance(item, EventCommand)) else MoveCommand(item) for item in tmp ] if tmp else None

            self.own_cfg = None
            self.tmp_cfg = None

            assert isinstance( self.move_speed, int)
            assert isinstance( self.move_frequency, int)
            assert isinstance( self.walk_anime, bool)
            assert isinstance( self.step_anime, bool)
            assert isinstance( self.direction_fix, bool)
            assert isinstance( self.through, bool)
            assert isinstance( self.always_on_top, bool)
            assert isinstance( self.trigger, str)

        def get_reduced_dict(self):
            return substract_dict( self.__dict__, self.__class__(None).__dict__ )


        def to_s(self):
            #from RGSS_Command_conversion import indent_nb
            #import json
            #d=self.__class__(self.__dict__, silent=True)
            #d=d.__dict__
            #d.pop('list')
            #return '\r\n[PAGE]\r\n' + json.dumps( d, indent=indent_nb, default=JSONencode ) + '\r\n'
            
            return '\r\n[PAGE]\r\n' + f"{cfg2str(self.own_cfg)}\r\n{str(self.condition)}" + '\r\n'

        def get_config(self):
            d = self.get_reduced_dict()
            self.tmp_cfg = flatten_dict( { k:v for k,v in d.items() if k!='list' and k!='condition' and k!='graphic' } )
            self.tmp_cfg.update( self.graphic.get_reduced_dict() )
            return self.tmp_cfg

        def build_own_config(self, base_cfg ):
            #print("build_own_config:crafting page's config")
            #print( f'tmp_cfg:{self.tmp_cfg}' )
            self.own_cfg = substract_dict( self.tmp_cfg, base_cfg )
            #print( f'own_cfg:{self.own_cfg}' )

        def conversion(self):
            commands_str.append( self.to_s() )
            if self.list:
                for command in self.list:
                    command.conversion()
            
    
    def __init__(self, obj):
        assert_same_class( obj, self.__class__ )

        self._class = obj['_class']
        self.id = obj.get('id', -1)
        self.name = obj.get('name', '').replace(' ','_')
        self.xy = [ obj.get('x', 0), obj.get('y', 0) ]
        self.config = None
        self.preset = None

        pages = obj.get('pages', dict())
        if isinstance(pages, dict):
            nbpages = max( [int(k) for k in pages.keys()] ) + 1
            self.pages = [ pages[str(page)] if isinstance(pages[str(page)], self.__class__.Page) else self.__class__.Page( pages[str(page)] ) for page in range(nbpages) ]
        elif isinstance(pages, list):
            self.pages = [ page if isinstance(page, self.__class__.Page) else self.__class__.Page( page ) for page in pages ]
        else:
            raise ValueError(f'Event constructor:pages is of an unexpected type: {type(pages)}')

        assert isinstance( self.name, str )
        assert isinstance( self.xy, list ) and len(self.xy)==2 and isinstance( self.xy[0], int ) and isinstance( self.xy[1], int )

    def to_s(self):
        #from RGSS_Command_conversion import indent_nb
        #import json
        #d=self.__class__(self.__dict__)
        #d=d.__dict__
        #d.pop('pages')
        #return '[EVENT]\r\n' + json.dumps( d, indent=indent_nb, default=JSONencode )
        return '[EVENT]\r\n' + f"xy={self.xy}\r\n{cfg2str(self.config)}"

    def build_config(self):
        from pprint import pprint
        cfg = None
        for page in self.pages:
            #print('build_config:fetching page config')
            page_cfg = page.get_config()
            #print(page_cfg)
            cfg = page_cfg if (cfg==None) else intersect_dict( cfg, page_cfg )

        #print('build_config')
        #pprint(cfg)

        for page in self.pages:
            page.build_own_config( cfg )

        self.config = cfg

    def is_door(self):
        if ('door' in self.name) and ('door' in self.config.get('graphic', '')):
            #print(f'DOOR!: {self.config}')
            self.preset='door'
            self.config['preset'] = 'door'
            self.pages = [ self.pages[0] ]

    def is_exit(self):
        if ('exit' in self.name.lower()) and ('' == self.config.get('graphic', '')):
            #print('exit detected')
            self.preset='exit'
            self.config['preset'] = 'exit'
            assert len(self.pages)==1

    def conversion(self):
        self.build_config()
        self.is_door()
        self.is_exit()
        commands_str.clear()

        if self.name in event_ignore_list:
            return

        commands_str.append( self.to_s() )
        
        for page in self.pages:
            #commands_str.append( f'\r\n[PAGE]' )
            page.conversion()
            commands_str.append('[end]\r\n')

class EventCommand:
    
    def __init__(self, obj):
        assert_same_class( obj, self.__class__ )

        self._class = obj['_class']
        self.code = obj.get( 'code', 0 )
        self.indent = obj.get( 'indent', 0 )
        tmp = obj.get( 'parameters', None )
        if isinstance(tmp, list):
            self.parameters=[ JSONdecode(item) if isinstance(item, dict) else item for item in tmp ]
        else:
            self.parameters=tmp

        assert isinstance( self.code, int )
        assert isinstance( self.indent, int )

    def conversion(self):
        add_command_str(self.code, self.parameters, self.indent)
        if self.code==209: # Set MoveRoute
            self.parameters[1].conversion(self.indent+1)
                    
        
 
class MoveRoute:
    
    def __init__(self, obj):
        assert_same_class( obj, self.__class__ )

        self._class = obj['_class']
        self.repeat = obj.get( 'repeat', True )
        self.skippable = obj.get( 'skippable', False )
        tmp = obj.get( 'list', False )
        self.list = [ item if isinstance(item, MoveCommand) else MoveCommand(item) for item in tmp] if tmp else None

        assert isinstance( self.repeat, bool )
        assert isinstance( self.skippable, bool )

    def conversion(self, indent=0):
        #self.printself()
        for command in self.list:
            command.conversion(indent)

    def printself(self):
        d = flatten_dict( self.__dict__ )
        print( f'MoveRoute:{d}' )

        

class MoveCommand:
    
    def __init__(self, obj):
        assert_same_class( obj, self.__class__ )

        self._class = obj['_class']
        self.code = obj.get( 'code', 0 )
        self.parameters = obj.get( 'parameters', False )

        assert isinstance( self.code, int )

    def conversion(self, indent=0):
        add_command_str(self.code, self.parameters, indent)

class AudioFile:
    def __init__(self, obj):
        assert_same_class( obj, self.__class__ )

        self._class = obj['_class']
        self.name = obj.get( 'name', "" )
        self.volume = obj.get( 'volume', 100 )
        self.pitch = obj.get( 'pitch', 100 )

        assert isinstance( self.name, str )
        assert isinstance( self.volume, int )
        assert isinstance( self.pitch, int )


    def __str__(self):
        #print('AudioFile::str called !')
        return f'"{self.name}", volume={self.volume}, pitch={self.pitch}'

class Tone:
    def __init__(self, obj):
        assert_same_class( obj, self.__class__)

        tmp = obj.get( 'RGBG', None )
        #pprint(obj)
        assert tmp!=None
        self._class = obj['_class']
        self.red = tmp[0]
        self.green = tmp[1]
        self.blue = tmp[2]
        self.gray = tmp[3]

    def to_s(self):
        return f'[{self.red}, {self.green}, {self.blue}, {self.gray}]'

    def isFadeOut(self):
        if self.red==255 and self.green==255 and self.blue==255 and self.gray==0:
            return "White"
        elif self.red==-255 and self.green==-255 and self.blue==-255 and self.gray==0:
            return "Black"
        return False

    def isFadeIn(self):
        if self.red==0 and self.green==0 and self.blue==0 and self.gray==0:
            return True
        return False


switcher = {
    'Page::Condition': Event.Page.Condition,
    'Page::Graphic': Event.Page.Graphic,
    'Page': Event.Page,
    'Event': Event,
    'EventCommand': EventCommand,
    'MoveRoute': MoveRoute,
    'MoveCommand': MoveCommand,
    'AudioFile': AudioFile,
    'Tone': Tone
}

def JSONdecode( obj ):
    c = obj.get('_class', False)
    if not isinstance( c, str ):
        return obj

    # Get the function from switcher dictionary
    corresponding_class = switcher.get(c, None)
    assert corresponding_class != None, f'JSONdecode: object with unexpected class identifier : {c}'
    #print(f"JSONdecode: obj is a {type(obj)}, mapping to {c}")
    return corresponding_class( obj )

def JSONencode( obj ):
    return obj.__dict__


if __name__=="__main__":
    print("RGSS_classes : this file shouldn't be executed")