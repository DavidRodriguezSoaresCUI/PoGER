# from RGSS_classes import Tileset, Map, MapInfo, Event, Page, Condition, Graphic, EventCommand, MoveRoute, MoveCommand, AudioFile, Tone

from RGSS_Command_conversion import command_to_str
from pprint import pprint
commands_str=[]


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

def add_command_str( *args ):
    (s,concat) = command_to_str(*args)
    if concat:
        s = commands_str.pop()+', ' + s
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
                    tmp['_class']=='Page::Condition'
                    obj=tmp

                assert_same_class( obj, self.__class__ )

                self._class = obj['_class']
                self.switch1 = obj.get('S1', None)
                self.switch2 = obj.get('S2', None)
                self.self_switch = obj.get('SS', None)
                var = obj.get('Var', False)
                self.variable = var['id'] if var else None
                self.variable_value = var['val'] if var else None

        class Graphic:

            def __init__(self, obj):
                if obj==None:
                    tmp = dict()
                    tmp['_class']=='Page::Graphic'
                    obj=tmp

                assert_same_class( obj, self.__class__ )

                self._class = obj['_class']
                self.tile_id = obj.get('tile_id', 0)
                self.character_name = obj.get('character_name', '')
                self.character_hue = obj.get('character_hue', 0)
                self.direction = obj.get('direction', 'Down')
                self.pattern = obj.get('pattern', 0)
                self.opacity = obj.get('opacity', '')
                self.blend_type = obj.get('blend_type', 'Normal')

                assert isinstance( self.tile_id , int )
                assert isinstance( self.character_name , str )
                assert isinstance( self.character_hue , int )
                assert isinstance( self.direction , str )
                assert isinstance( self.pattern , int )
                assert isinstance( self.opacity , int )
                assert isinstance( self.blend_type , str )


        def __init__(self, obj):
            assert_same_class( obj, self.__class__ )
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

            assert isinstance( self.move_speed, int)
            assert isinstance( self.move_frequency, int)
            assert isinstance( self.walk_anime, bool)
            assert isinstance( self.step_anime, bool)
            assert isinstance( self.direction_fix, bool)
            assert isinstance( self.through, bool)
            assert isinstance( self.always_on_top, bool)
            assert isinstance( self.trigger, str)


        def to_s(self):
            from RGSS_Command_conversion import indent_nb
            import json
            d=self.__class__(self.__dict__)
            d=d.__dict__
            d.pop('list')
            
            return '\r\n[PAGE]\r\n' + json.dumps( d, indent=indent_nb, default=JSONencode ) + '\r\n'

        def conversion(self):
            commands_str.append( self.to_s() )
            if self.list:
                for command in self.list:
                    command.conversion()
            
    
    def __init__(self, obj):
        assert_same_class( obj, self.__class__ )

        self._class = obj['_class']
        self.name = obj.get('name', '')
        self.x = obj.get('x', 0)
        self.y = obj.get('y', 0)
        
        pages = obj.get('pages', dict())
        if isinstance(pages, dict):
            nbpages = max( [int(k) for k in pages.keys()] ) + 1
            self.pages = [ pages[str(page)] if isinstance(pages[str(page)], self.__class__.Page) else self.__class__.Page( pages[str(page)] ) for page in range(nbpages) ]
        elif isinstance(pages, list):
            self.pages = [ page if isinstance(page, self.__class__.Page) else self.__class__.Page( page ) for page in pages ]
        else:
            raise ValueError(f'Event constructor:pages is of an unexpected type: {type(pages)}')

        assert isinstance( self.name, str )
        assert isinstance( self.x, int )
        assert isinstance( self.x, int )

    def to_s(self):
        from RGSS_Command_conversion import indent_nb
        import json
        d=self.__class__(self.__dict__)
        d=d.__dict__
        d.pop('pages')
        
        return '[EVENT]\r\n' + json.dumps( d, indent=indent_nb, default=JSONencode )

    def conversion(self):
        commands_str.clear()
        commands_str.append( self.to_s() )
        for page in self.pages:
            #commands_str.append( f'\r\n[PAGE]' )
            page.conversion()

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
        for command in self.list:
            command.conversion(indent)

        

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
