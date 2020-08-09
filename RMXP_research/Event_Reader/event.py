from pprint import pprint
import sys

debug = True

class Event:

    DEFAULT_CONFIG = {
        'name':'UNNAMED',
        'xy':None,
        'graphic':None,
        'pattern':0,
        'opacity':255,
        'transparent':False,
        'direction':'s',
        'trigger':'onplayeraction',
        'move_animation':True,
        'stop_animation':False,
        'direction_fix':False,
        'through':False,
        'always_on_top':False,
        'movement':'fixed',
        'movement_speed':'slow',
        'preset':None,
    }

    PRESET_LIST = ['door', 'exit', 'berry_plant']

    VALID_DIRECTIONS = ['s', 'w', 'n', 'e']

    VALID_TRIGGERS = ['onplayeraction', 'onplayertouch', 'ontouch', 'onautorun', 'ready', 'onseen']

    VALID_MOVEMENTS = ['fixed', 'random', 'approach']

    VALID_MOVEMENT_SPEEDS = ['slow', 'fast']

    def __init__(self, event_file):
        self.file = event_file
        self.config=dict( self.DEFAULT_CONFIG )
        self.behaviors=list()
        self.current_behavior=None
        self.triggered = False
        self.final = False
        self.process_init()

    def process_init( self ):
        from eventReader import build_event
        from utils import ast_display, ast_cleanup
        
        ast = ast_cleanup( build_event( self.file ) )

        self.apply_config( ast[0] )
        self.enforce_config_compliance()

        for b in ast[1]:
            self.add_behavior( b )
        print(self)

    def apply_config( self, ast ):
        from utils import unquote
        for item in ast:
            cfg = item[0]
            value = item[1:] if len(item)>2 else item[1]
            if isinstance(value, str):
                value = unquote( value )
            assert cfg in self.config, f'E:apply_config error : {cfg} not in configuration'
            self.config[cfg] = value
            #print(f'apply_config : {cfg} <- {value}')

    def enforce_config_compliance( self ):
        must_be_str = ['name']
        c = lambda cfg, t: isinstance( self.config[cfg], t )
        assert c( 'name', str )
        
        must_be_int = ['pattern', 'opacity']
        for item in must_be_int:
            assert c( item, int )
    
        must_be_bool = ['transparent', 'move_animation', 'stop_animation', 'direction_fix', 'through', 'always_on_top']
        for item in must_be_bool:
            assert c( item, bool )

        cfg = lambda x: self.config[x]
        xy = cfg('xy')
        assert isinstance( xy, list ) and len(xy)==2 and isinstance( xy[0], int ) and isinstance( xy[1], int )
        
        assert cfg('direction') in Event.VALID_DIRECTIONS
        
        assert (cfg('trigger') in Event.VALID_TRIGGERS) or cfg('trigger').startswith('onseen')
        
        assert c( 'graphic', str ) or c( 'graphic', int ) or cfg('graphic')==None

        assert cfg('movement') in Event.VALID_MOVEMENTS

        assert cfg('movement_speed') in Event.VALID_MOVEMENT_SPEEDS

    def add_behavior( self, ast ):
        assert not self.final, 'E.add_behavior: Cannot add behavior to finalized Event.'
        if debug:
            print(f'E:add_behavior : adding a behavior')

        self.behaviors.append(Behavior(ast))

    def choose_behavior(self):
        valid_b = [ idx for idx,b in enumerate(self.behaviors) if b.satisfies_conditions() ]
        assert 0 < len(valid_b), 'E.choose_behavior: no behavior satisfies its conditions'
        self.current_behavior = max(valid_b)

    def finalize_behaviors(self):
        if not self.final:
            for b in self.behaviors:
                b.finalize()
            self.final = True

    def trigger( self, t ):
        assert self.triggered==False, 'E.trigger : Already triggered.'
        tri = self.config.get( 'trigger', None )
        if tri and (tri==t):
            self.triggered = True
            self.finalize_behaviors()
            self.choose_behavior()

    def walk(self):
        pass

    def step(self):
        ''' Perform a step : either walking animation or behavior '''
        if self.triggered:
            self.triggered = self.behaviors[self.current_behavior].step()
        if not self.triggered:
            self.walk()

    def __str__(self):
        return 'Event: '+str(self.__dict__) # + '\n'.join([ str(b) for b in self.behaviors ])


class Behavior:

    def __init__(self,  ast):
        self.config=dict()
        self.conditions=list()
        self.instructions=list()
        self.final = False
        self.tick = 0

        self.process_ast( ast )

    def process_ast( self, ast ):

        from utils import ast_display
        #print(f'B:process_ast')
        #ast_display( ast )
        l = len(ast)
        assert l==1 or l==2
        self.apply_config_cond( ast[0] )
        if l==2:
            self.build_instructions( ast[1] )

    def apply_config_cond( self, ast ):
        from utils import ast_display
        #print(f'B:apply_config_cond')
        #ast_display( ast )
        for item in ast:
            if isinstance( item, str ):
                self.conditions.append( item )
            else:
                cfg = item[0]
                value = item[1:] if len(item)>2 else item[1]
                assert cfg in Event.DEFAULT_CONFIG
                self.config[cfg] = value

    def build_instructions( self, ast ):
        from utils import ast_display
        #print(f'B:build_instructions')
        ast_display( ast )
        for item in ast:
            self.instructions.append( item )

    def prepare_instruction(self,i):
        # prepare isntructions, so they can be passed to exec()
        pass

    def finalize( self ):
        self.final = True
    pass

    def satisfies_conditions(self):
        return all([ exec(cond) for cond in self.conditions ])

    def step(self):
        # implement 
        assert self.final, 'B.step : behavior unfinalized'
        try:
            instr = self.instructions[self.tick]
            # TODO : exec()
        except IndexError:
            self.tick = 0
            return False

        self.tick += 1
        return True

    def __str__(self):
        return str(self.__dict__)
