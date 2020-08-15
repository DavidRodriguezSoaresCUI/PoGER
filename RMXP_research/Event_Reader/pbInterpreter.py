import re, sys
from pprint import pprint

class pbInterpreter:

    ''' Implements 'pb' scripts from Pokemon Essentials '''

    FOSSILS = [ 'Fossil1', 'Fossil3', 'Fossil3' ]

    def __init__(self, base_interpreter):
        self.base_interpreter = base_interpreter

    def execute( self, script ):

        #print(f'pbI:execute {script}')
        match = re.match( r'([a-z_0-9]+)\(?([^\(,]+),?([^\(,]+)*\)(.*)', script )
        if match:
            from utils import try_make_number
            pprint( match.groups() )
            func_name = match.group(1)
            
            p1 = match.group(2)
            parameters = [ try_make_number(p1) ] if p1 else []
            
            more_p = match.group(3)
            if more_p:
                for item in more_p:
                    if item and item!='':
                        parameters.append( try_make_number(item) )

            extra = match.group(4)
            if extra and extra!='':
                raise ValueError(f'pbI::exec: Found unexpected extra characters after command (extra={extra} in {script})')
            
            func = getattr( self, func_name )
            #print( f'I.execute: func_name={func_name}, parameters={parameters}' )
            ( remaining_instr, do_continue ) = func( parameters )

        else:
            #raise ValueError(f'pbI::exec: no match')
            self.base_interpreter.display_text(f'Unknown script {script}. Please check and correct. Skipping ..')
            return ( None, True )
        
        return ( remaining_instr, do_continue )

    def pbchoosefossil( self, parameters ):
        #print('pbI::pbchoosefossil')
        self.base_interpreter.display_text('Choose a fossil.')
        choice = self.base_interpreter.display_choices( pbInterpreter.FOSSILS )
        self.base_interpreter.set( ':fossilbeingrevived', choice )

        return ( None, True )
        

        