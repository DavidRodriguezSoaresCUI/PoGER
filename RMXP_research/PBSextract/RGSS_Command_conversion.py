#from RGSS_classes import EventCommand, MoveCommand, Tone, MoveRoute
import RGSS_classes

''' Used codes : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 
16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 33, 34, 37, 38, 39, 40, 
41, 42, 44, 101, 102, 104, 106, 108, 111, 112, 113, 115, 118, 119, 
121, 122, 123, 125, 201, 202, 208, 209, 210, 221, 222, 223, 225, 231, 
232, 235, 236, 241, 242, 247, 248, 249, 250, 314, 354, 355, 401, 402, 
404, 408, 411, 412, 413, 655
'''

indent_nb=2
indent_symbol=' '*indent_nb
last_code=None

def subject_to_string( s ):
    if s==-1:
        return ':self'
    elif s==0:
        return ':player'
    else:
        return f'subject_to_string:Undocumented subject {s}'

def quote( s ):
    return '"'+s.replace('\\', '\\\\').replace('"', '\\"')+'"'

def direction_toString( dir ):
    switcher={
        0:'Keep',
        2:'Down',
        4:'Left',
        6:'Right',
        8:'Up',
    }
    res=switcher.get(dir, None)
    assert res, f"direction_toString:Undocumented: {dir}"
    return res

def SS_val_str( val ):
    SS_switcher = {
        0:'ON',
        1:'OFF'
    }
    return SS_switcher[val]

def command_0( parameters ):
    assert parameters==None
    return "END"

def command_1( parameters ):
    assert parameters==None
    return "Move Down"

def command_2( parameters ):
    assert parameters==None
    return "Move Left"

def command_3( parameters ):
    assert parameters==None
    return "Move Right"

def command_4( parameters ):
    assert parameters==None
    return "Move Up"

def command_5( parameters ):
    assert parameters==None
    return "Move SW"

def command_6( parameters ):
    assert parameters==None
    return "Move SE"

def command_7( parameters ):
    assert parameters==None
    return "Move NW"

def command_8( parameters ):
    assert parameters==None
    return "Move NE"

def command_9( parameters ):
    assert parameters==None
    return "Move at random"

def command_10( parameters ):
    assert parameters==None
    return "Move Towards Player"

def command_11( parameters ):
    assert parameters==None
    return "Move away from player"

def command_12( parameters ):
    assert parameters==None
    return "1 step forward"

def command_13( parameters ):
    assert parameters==None
    return "1 step backwards"

def command_14( parameters ):
    print(f'command_14: parameters={parameters}, {type(parameters)}')
    return "Jump X+,Y+"

def command_15( parameters ):
    #print(f'command_15: parameters={parameters}, {type(parameters)}')
    seconds=parameters
    assert isinstance(seconds, int)
    return f"Wait seconds, {seconds}"

def command_16( parameters ):
    assert parameters==None
    return "Turn down"

def command_17( parameters ):
    assert parameters==None
    return "Turn left"

def command_18( parameters ):
    assert parameters==None
    return "Turn right"

def command_19( parameters ):
    assert parameters==None
    return "Turn Up"

def command_20( parameters ):
    assert parameters==None
    return "Turn 90 Right"

def command_21( parameters ):
    assert parameters==None
    return "Turn 90 Left"

def command_22( parameters ):
    assert parameters==None
    return "Turn 180"

def command_23( parameters ):
    assert parameters==None
    return "Turn 90 random"

def command_24( parameters ):
    assert parameters==None
    return "Turn random"

def command_25( parameters ):
    assert parameters==None
    return "Turn towards player"

def command_26( parameters ):
    assert parameters==None
    return "Turn away from player"

def command_33( parameters ): # Freeze every animation
    assert parameters==None
    return "Stop Animation ON"

def command_34( parameters ):
    assert parameters==None
    return "Stop Animation OFF"

def command_37( parameters ): # Walk through Walls
    assert parameters==None
    #print(f'command_37: parameters={parameters}, {type(parameters)}')
    return "WTW ON"

def command_38( parameters ):
    assert parameters==None
    #print(f'command_37: parameters={parameters}, {type(parameters)}')
    return "WTW OFF"

def command_39( parameters ): # Always on top
    assert parameters==None
    return "AOT ON"

def command_40( parameters ):
    assert parameters==None
    return "AOT OFF"

def command_41( parameters ):
    print(f'command_41: parameters={parameters}, {type(parameters)}')
    return "Change graphic"

def command_42( parameters ):
    #print(f'command_42: parameters={parameters}, {type(parameters)}')
    opa=parameters
    assert isinstance(opa, int)
    return f"Change opacity, {opa}"

def command_44( parameters ):
    print(f'command_44: parameters={parameters}, {type(parameters)}')
    return "Play SE"

def command_101( parameters ):
    #print(f'command_101: parameters={parameters}, {type(parameters)}')
    assert isinstance(parameters, str)
    return "Show Text, "+quote(parameters)

def command_401( parameters ): # see 101
    #print(f'command_401: parameters={parameters}, {type(parameters)}')
    global last_code
    
    if not (last_code==101 or last_code==401):
        raise ValueError( f'command_401: last_code={last_code}, not 101 or 401' )
    
    assert isinstance(parameters, str)
    return (quote(parameters), True)
    #return "Show More Text"

def command_102( parameters ):
    #print(f'command_102: parameters={parameters}, {type(parameters)}')
    assert len(parameters)==2
    choices=str(parameters[0])
    return f"Show Choices, {choices}, default={parameters[1]}"

def command_104( parameters ):
    print(f'command_104: parameters={parameters}, {type(parameters)}')
    return "Change Text Options"

def command_106( parameters ):
    #print(f'command_106: parameters={parameters}, {type(parameters)}')
    assert isinstance( parameters, int )
    return f"Wait, {parameters}"

def command_108( parameters ): # differenciate for particle effect
    #print(f'command_108: parameters={parameters}, {type(parameters)}')
    assert isinstance( parameters, str )
    return f"# {quote(parameters)}"

def command_408( parameters ): # see 108
    #print(f'command_408: parameters={parameters}, {type(parameters)}')
    global last_code
    
    if not (last_code==108 or last_code==408):
        raise ValueError( f'command_408: last_code={last_code}, not 108 or 408' )
    
    assert isinstance(parameters, str)
    return (f"# {quote(parameters)}", True)

def command_111( parameters ):
    code=parameters[0]
    assert isinstance(code, int)
    s=''
    if code==1:
        # Variable check
        from PE_variables_switches import variables
        op_switcher={
            0:'==',
            1:'>=',
            2:'<=',
            3:'>',
            4:'<',
            5:'!=',
        }
        var=variables.get( parameters[1], None )
        val=parameters[3]
        op=op_switcher.get( parameters[4], None)
        assert isinstance(var, str) and isinstance(op, str)
        s=f':{var} {op} {val}'
    elif code==2:
        # Self-switch check
        ss=parameters[1]
        assert isinstance(ss,str) and len(ss)==1
        val=SS_val_str( parameters[2] )
        s=f':{ss} is {val}'
    elif code==12:
        # Script condition
        s=parameters[1]
        assert len(parameters)==2
        assert isinstance(s, str)
    else:
        print(f'command_111: parameters={parameters}, {type(parameters)}')
        s=f'Unimplemented interpretation for code {code}'

    return f"Conditional Branch, {s}"

def command_112( parameters ):
    print(f'command_112: parameters={parameters}, {type(parameters)}')
    return "Loop"

def command_113( parameters ):
    print(f'command_113: parameters={parameters}, {type(parameters)}')
    return "Break Loop"

def command_115( parameters ):
    #print(f'command_115: parameters={parameters}, {type(parameters)}')
    return "Exit Event Processing"

def command_118( parameters ):
    #print(f'command_118: parameters={parameters}, {type(parameters)}')
    label=parameters
    assert isinstance(label, str)
    return f"Label, {label}"

def command_119( parameters ):
    #print(f'command_119: parameters={parameters}, {type(parameters)}')
    label=parameters
    assert isinstance(label, str)
    return f"Jump to Label, {label}"

def command_121( parameters ):
    print(f'command_121: parameters={parameters}, {type(parameters)}')
    return "Control Switches"

def command_122( parameters ):
    import PE_variables_switches
    var = PE_variables_switches.variables.get( parameters[0], None )
    op_switcher = {
        0:'=',
        1:'+=',
        2:'-=',
        3:'*=',
        4:'/=',
        5:'%='
    }
    operation = op_switcher.get( parameters[2], None )
    assert operation
    operand = parameters[3]
    s=''
    if operand==0:
        assert len(parameters)==5
        s=f'{parameters[4]}'
    elif operand==1:
        from PE_variables_switches import variables
        assert len(parameters)==5
        s=variables.get( parameters[4], None )
        assert s
    else:
        print(f'command_122: parameters={parameters}, {type(parameters)}')
        s='Unimplemented operand'

    return f"Control Variables, {var} {operation} {s}"

def command_123( parameters ):
    #print(f'command_123: parameters={parameters}, {type(parameters)}')
    ss=parameters[0]
    val=SS_val_str( parameters[1] )
    return f"Control Self Switch, :{ss}, {val}"

def command_125( parameters ):
    print(f'command_125: parameters={parameters}, {type(parameters)}')
    return "Change Gold"

def command_201( parameters ):
    #print(f'command_201: parameters={parameters}, {type(parameters)}')
    assert len(parameters)==6
    dest_map, dest_x, dest_y = parameters[1], parameters[2], parameters[3]
    direction=direction_toString(parameters[4])
    fading = 'Fading' if (parameters[5]==0) else 'NoFading' 
    return f"Transfer Player, destination=({dest_map},{dest_x},{dest_y}), direction={quote(direction)}, fading={quote(fading)}"

def command_202( parameters ):
    print(f'command_202: parameters={parameters}, {type(parameters)}')
    return "Set Event Location"

def command_208( parameters ):
    print(f'command_208: parameters={parameters}, {type(parameters)}')
    return "Change Transparent Flag [in VX: 211]"

def command_209( parameters ):
    #print(f'command_209: parameters={parameters}, {type(parameters)}')
    subject=subject_to_string(parameters[0])
    #moveroute=parameters[1]
    return f"Set Move Route, {subject}"

def command_210( parameters ):
    #print(f'command_210: parameters={parameters}, {type(parameters)}')
    return "Wait for Move's Completion"

# https://www.youtube.com/watch?v=4ykNtsDQKVM
def command_221( parameters ):
    #print(f'command_221: parameters={parameters}, {type(parameters)}')
    assert parameters==None
    return "Prepare for Transition (freeze screen)"

def command_222( parameters ):
    #print(f'command_222: parameters={parameters}, {type(parameters)}')
    assert isinstance(parameters, str)
    return f"Execute Transition, {parameters}"

def command_223( parameters ):
    from RGSS_classes import Tone
    #print(f'command_223: parameters={parameters}, {type(parameters)}')
    tone, nbFrames = parameters[0], parameters[1]
    assert isinstance(tone, Tone) and isinstance( nbFrames, int) and len(parameters)==2
    fadeout, fadein = tone.isFadeOut(), tone.isFadeIn()
    #print( f'tone:{tone.to_s()}, fadein={fadein}, fadeout={fadeout}')
    if fadeout:
        return f'Fadeout, {fadeout}'
    elif fadein:
        return f'Fadein'
    else:
        return f"Change Screen Color Tone, {tone.to_s()}"

def command_225( parameters ):
    print(f'command_225: parameters={parameters}, {type(parameters)}')
    return "Screen Shake"

def command_231( parameters ):
    print(f'command_231: parameters={parameters}, {type(parameters)}')
    return "Show Picture"

def command_232( parameters ):
    print(f'command_232: parameters={parameters}, {type(parameters)}')
    return "Move Picture"

def command_235( parameters ):
    print(f'command_235: parameters={parameters}, {type(parameters)}')
    return "Erase Picture"

def command_236( parameters ):
    print(f'command_236: parameters={parameters}, {type(parameters)}')
    return "Set Weather Effects"

def command_241( parameters ):
    print(f'command_241: parameters={parameters}, {type(parameters)}')
    return "Play BGM"

def command_242( parameters ):
    print(f'command_242: parameters={parameters}, {type(parameters)}')
    return "Fade Out BGM"

def command_247( parameters ):
    assert parameters==None
    return "Memorize BGM/BGS"

def command_248( parameters ):
    assert parameters==None
    return "Restore BGM/BGS"

def command_249( parameters ):
    #print(f'command_249: parameters={parameters}, {type(parameters)}')
    from RGSS_classes import AudioFile
    import json
    audio=parameters
    assert isinstance(audio, AudioFile)
    s = json.dumps( audio.__dict__ )
    return f"Play ME, {s}"

def command_250( parameters ):
    from RGSS_classes import AudioFile
    import json
    #print(f'command_250: parameters={parameters}, {type(parameters)}')
    audio=parameters
    assert isinstance(audio, AudioFile)
    s = json.dumps( audio.__dict__ )
    return f"Play SE, {s}"

def command_314( parameters ):
    # ignore parameter
    return "Recover All"

def command_354( parameters ):
    assert parameters==None
    return "Return to Title Screen"

def command_355( parameters ):
    #print(f'command_355: parameters={parameters}, {type(parameters)}')
    assert isinstance( parameters, str )
    return "Script, "+quote(parameters)

def command_655( parameters ):
    #print(f'command_655: parameters={parameters}, {type(parameters)}')
    global last_code
    
    if not (last_code==355 or last_code==655):
        raise ValueError( f'command_655: last_code={last_code}, not 355 or 655' )
    
    assert isinstance(parameters, str)
    return (quote(parameters), True)
    #print(f'command_355: parameters={parameters}, {type(parameters)}')
    #return "Script continued"

def command_402( parameters ):
    #print(f'command_402: parameters={parameters}, {type(parameters)}')
    assert isinstance( parameters, list )
    choice_id=parameters[0]
    choice_str=parameters[1]
    assert isinstance( choice_id, int )
    assert isinstance( choice_str, str )
    return f"When '{choice_str}'"

def command_404( parameters ):
    assert parameters==None
    return None#"NOP/end of 'When'"

def command_411( parameters ):
    assert parameters==None
    return "Else"

def command_412( parameters ):
    assert parameters==None
    return "Branch END"

def command_413( parameters ): # Goes with Loop:112
    print(f'command_413: parameters={parameters}, {type(parameters)}')
    return "Repeat Above"

'''
when 37 # Walk through walls
    return "WTW ON"
when 38 # Walk through walls
    return "WTW OFF"
when 39 # Always on top
    return "AOT ON"
when 40 # Always on top
    return "AOT OFF"
when 101 # Show Text
    return "Show Text"
when 102 # Show Choices
    return "Show Choices"
when 103 # Input Number
    return "Input Number"
when 104 # Change Text Options [not in VX]
    return "Change Text Options [not in VX]"
when 105 # Button Input Processing [not in VX]
    return "Button Input Processing [not in VX]"
when 106 # Wait [in VX: 230]
    return "Wait [in VX: 230]"
when 111 # Conditional Branch
    return "Conditional Branch"
when 112 # Loop
    return "Loop"
when 113 # Break Loop
    return "Break Loop"
when 115 # Exit Event Processing
    return "Exit Event Processing"
when 116 # Erase Event [in VX: 214]
    return "Erase Event [in VX: 214]"
when 117 # Call Common Event
    return "Call Common Event"
when 118 # Label
    return "Label"
when 119 # Jump to Label
    return "Jump to Label"
when 121 # Control Switches
    return "Control Switches"
when 122 # Control Variables
    return "Control Variables"
when 123 # Control Self Switch
    return "Control Self Switch"
when 124 # Control Timer
    return "Control Timer"
when 125 # Change Gold
    return "Change Gold"
when 126 # Change Items
    return "Change Items"
when 127 # Change Weapons
    return "Change Weapons"
when 128 # Change Armor
    return "Change Armor"
when 129 # Change Party Member
    return "Change Party Member"
when 131 # Change Windowskin [not in VX]
    return "Change Windowskin [not in VX]"
when 132 # Change Battle BGM
    return "Change Battle BGM"
when 133 # Change Battle End ME
    return "Change Battle End ME"
when 134 # Change Save Access
    return "Change Save Access"
when 135 # Change Menu Access
    return "Change Menu Access"
when 136 # Change Encounter
    return "Change Encounter"
when 201 # Transfer Player
    return "Transfer Player"
when 202 # Set Event Location
    return "Set Event Location"
when 203 # Scroll Map
    return "Scroll Map"
when 204 # Change Map Settings
    return "Change Map Settings"
when 205 # Change Fog Color Tone [in VX: Set Move Route]
    return "Change Fog Color Tone [in VX: Set Move Route]"
when 206 # Change Fog Opacity [in VX: Get on/off Vehicle]
    return "Change Fog Opacity [in VX: Get on/off Vehicle]"
when 207 # Show Animation [in VX: 212]
    return "Show Animation [in VX: 212]"
when 208 # Change Transparent Flag [in VX: 211]
    return "Change Transparent Flag [in VX: 211]"
when 209 # Set Move Route [in VX: 205]
    return "Set Move Route [in VX: 205]"
when 210 # Wait for Move's Completion
    return "Wait for Move's Completion"
when 221 # Prepare for Transition [Not in VX, now called Fadeout Screen]
    return "Prepare for Transition [Not in VX, now called Fadeout Screen]"
when 222 # Execute Transition [Not in VX, now called Fadein Screen]
    return "Execute Transition [Not in VX, now called Fadein Screen]"
when 223 # Change Screen Color Tone
    return "Change Screen Color Tone"
when 224 # Screen Flash
    return "Screen Flash"
when 225 # Screen Shake
    return "Screen Shake"
when 231 # Show Picture
    return "Show Picture"
when 232 # Move Picture
    return "Move Picture"
when 233 # Rotate Picture
    return "Rotate Picture"
when 234 # Change Picture Color Tone
    return "Change Picture Color Tone"
when 235 # Erase Picture
    return "Erase Picture"
when 236 # Set Weather Effects
    return "Set Weather Effects"
when 241 # Play BGM
    return "Play BGM"
when 242 # Fade Out BGM
    return "Fade Out BGM"
when 245 # Play BGS
    return "Play BGS"
when 246 # Fade Out BGS
    return "Fade Out BGS"
when 247 # Memorize BGM/BGS [not in VX]
    return "Memorize BGM/BGS [not in VX]"
when 248 # Restore BGM/BGS [not in VX]
    return "Restore BGM/BGS [not in VX]"
when 249 # Play ME
    return "Play ME"
when 250 # Play SE
    return "Play SE"
when 251 # Stop SE
    return "Stop SE"
when 301 # Battle Processing
    return "Battle Processing"
when 302 # Shop Processing
    return "Shop Processing"
when 303 # Name Input Processing
    return "Name Input Processing"
when 311 # Change HP
    return "Change HP"
when 312 # Change SP
    return "Change SP"
when 313 # Change State
    return "Change State"
when 314 # Recover All
    return "Recover All"
when 315 # Change EXP
    return "Change EXP"
when 316 # Change Level
    return "Change Level"
when 317 # Change Parameters
    return "Change Parameters"
when 318 # Change Skills
    return "Change Skills"
when 319 # Change Equipment
    return "Change Equipment"
when 320 # Change Actor Name
    return "Change Actor Name"
when 321 # Change Actor Class
    return "Change Actor Class"
when 322 # Change Actor Graphic
    return "Change Actor Graphic"
when 331 # Change Enemy HP
    return "Change Enemy HP"
when 332 # Change Enemy SP
    return "Change Enemy SP"
when 333 # Change Enemy State
    return "Change Enemy State"
when 334 # Enemy Recover All
    return "Enemy Recover All"
when 335 # Enemy Appearance
    return "Enemy Appearance"
when 336 # Enemy Transform
    return "Enemy Transform"
when 337 # Show Battle Animation
    return "Show Battle Animation"
when 338 # Deal Damage
    return "Deal Damage"
when 339 # Force Action
    return "Force Action"
when 340 # Abort Battle
    return "Abort Battle"
when 351 # Call Menu Screen
    return "Call Menu Screen"
when 352 # Call Save Screen
    return "Call Save Screen"
when 353 # Game Over
    return "Game Over"
when 354 # Return to Title Screen
    return "Return to Title Screen"
when 355 # Script
    return "Script"
when 401 # 101 extension for longer text
    return "Show More Text"
when 402 # When [**]
    return "When [**]"
when 403 # When Cancel
    return "When Cancel"
when 411 # Else
    return "Else"
when 413 # Repeat Above
    return "Repeat Above"
when 601 # If Win
    return "If Win"
when 602 # If Escape
    return "If Escape"
when 603 # If Lose
    return "If Lose"
'''

'''
def command_103( parameters ):
    return "Input Number"

def command_105( parameters ):
    return "Button Input Processing [not in VX]"

def command_116( parameters ):
    return "Erase Event [in VX: 214]"

def command_117( parameters ):
    return "Call Common Event"

def command_124( parameters ):
    return "Control Timer"

def command_126( parameters ):
    return "Change Items"

def command_127( parameters ):
    return "Change Weapons"

def command_128( parameters ):
    return "Change Armor"

def command_129( parameters ):
    return "Change Party Member"

def command_131( parameters ):
    return "Change Windowskin [not in VX]"

def command_132( parameters ):
    return "Change Battle BGM"

def command_133( parameters ):
    return "Change Battle End ME"

def command_134( parameters ):
    return "Change Save Access"

def command_135( parameters ):
    return "Change Menu Access"

def command_136( parameters ):
    return "Change Encounter"

def command_203( parameters ):
    return "Scroll Map"

def command_204( parameters ):
    return "Change Map Settings"

def command_205( parameters ):
    return "Change Fog Color Tone [in VX: Set Move Route]"

def command_206( parameters ):
    return "Change Fog Opacity [in VX: Get on/off Vehicle]"

def command_207( parameters ):
    return "Show Animation [in VX: 212]"

def command_224( parameters ):
    return "Screen Flash"

def command_233( parameters ):
    return "Rotate Picture"

def command_234( parameters ):
    return "Change Picture Color Tone"

def command_245( parameters ):
    return "Play BGS"

def command_246( parameters ):
    return "Fade Out BGS"

def command_251( parameters ):
    return "Stop SE"

def command_301( parameters ):
    return "Battle Processing"

def command_302( parameters ):
    return "Shop Processing"

def command_303( parameters ):
    return "Name Input Processing"

def command_311( parameters ):
    return "Change HP"

def command_312( parameters ):
    return "Change SP"

def command_313( parameters ):
    return "Change State"

def command_315( parameters ):
    return "Change EXP"

def command_316( parameters ):
    return "Change Level"

def command_317( parameters ):
    return "Change Parameters"

def command_318( parameters ):
    return "Change Skills"

def command_319( parameters ):
    return "Change Equipment"

def command_320( parameters ):
    return "Change Actor Name"

def command_321( parameters ):
    return "Change Actor Class"

def command_322( parameters ):
    return "Change Actor Graphic"

def command_331( parameters ):
    return "Change Enemy HP"

def command_332( parameters ):
    return "Change Enemy SP"

def command_333( parameters ):
    return "Change Enemy State"

def command_334( parameters ):
    return "Enemy Recover All"

def command_335( parameters ):
    return "Enemy Appearance"

def command_336( parameters ):
    return "Enemy Transform"

def command_337( parameters ):
    return "Show Battle Animation"

def command_338( parameters ):
    return "Deal Damage"

def command_339( parameters ):
    return "Force Action"

def command_340( parameters ):
    return "Abort Battle"

def command_351( parameters ):
    return "Call Menu Screen"

def command_352( parameters ):
    return "Call Save Screen"

def command_353( parameters ):
    return "Game Over"

def command_403( parameters ):
    return "When Cancel"

def command_509( parameters ):
    return "RPG::MoveCommand Object"

def command_601( parameters ):
    return "If Win"

def command_602( parameters ):
    return "If Escape"

def command_603( parameters ):
    return "If Lose"
'''

def command_to_str( code, parameters, indent=0 ):
    assert isinstance(code, int)
    assert isinstance(indent, int)
    global last_code

    if code==404:
        return (None, False)

    func = globals().get( f'command_{code}', None )
    ret=None
    if callable(func):
        res = func( parameters )
        if isinstance( res, str ):
            ret = (indent_symbol*indent + res.strip(), False)
        elif (isinstance( res, tuple ) and isinstance(res[0],str) and isinstance(res[1],bool)):
            ret = (indent_symbol*indent + res[0].strip(), res[1])
        else:
            raise ValueError( f'command_to_str: Code {code} has no output') 
    else:
        raise ValueError( f'command_to_str: Undocumented code {code}')
    

    last_code=code
    if ret:
        return ret



