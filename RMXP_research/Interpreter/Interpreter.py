import sys
import pbInterpreter
from utils import ast_display, unpack_list

DEBUG_LVL = 0

class Interpreter:

    def __init__( self ):
        self.glob = dict( {':debug':False} )
        self.last_choice = None
        self.scriptInterpreter = pbInterpreter.pbInterpreter( self )

    def debug( self ):
        return self.glob[':debug']

    def set(self, gl, val ):
        self.glob[ gl.lower() ] = val
        if DEBUG_LVL > 0:
            print( f'Interpreter::set: {str(self.glob)}')

    def execute( self, loc, instr ):
        import sys
        debug = self.debug()
        if DEBUG_LVL > 0:
            print( f'Interpreter::execute: instr={instr if debug else None}' )
        from utils import ast_display
        if debug:
            ast_display( instr )

        first_item = instr[0]
        if isinstance( first_item, list ):
            ( remaining_instr, do_continue ) = self.execute( loc, first_item )
            
            if remaining_instr:
                remaining_instr.extend( instr[1:] )
            else:
                remaining_instr = instr[1:]
        elif isinstance( first_item, str ):
            if ('glob' in first_item) or ('local' in first_item):
                ( remaining_instr, do_continue ) = self.execute_raw( loc, first_item )
                if len(instr)>1:
                    remaining_instr = instr[1:]
            else:
                try:
                    func_name = 'exec_' + first_item
                    func = getattr( self, func_name ) # ( instr[1:] )
                    if DEBUG_LVL > 0:
                        print( f'I.execute: func_name={func_name}, func={func}' )
                    ( remaining_instr, do_continue ) = func( loc, instr[1:] )
                except:
                    try:
                        ( remaining_instr, do_continue ) = self.scriptInterpreter.execute( first_item )
                        if len(instr)>1:
                                remaining_instr = remaining_instr.extend(instr[1:]) if remaining_instr else instr[1:]
                    except:
                        raise NotImplementedError(f'I::execute : nothing implemented for {instr}')

        else:
            raise NotImplementedError(f'I::execute : not str or list {instr}')
        
        if debug:
            print( f'I::remaining_instr={remaining_instr}' )
        #sys.exit()
        return ( remaining_instr, do_continue )

    def check_condition( self, loc, cond ):
        res = eval( cond, { 'local':loc, 'glob':self.glob } )
        if DEBUG_LVL > 0:
            print( f'Interpreter::check_condition: cond={cond}, loc={loc}, res={res}' )
        return res

    def exec_if( self, loc, instr ):
        assert len(instr) >= 2
        cond_value = self.check_condition( loc, instr[0] )
        if DEBUG_LVL > 0:
            print( f'I:exec_if: f{instr}, cond_value={cond_value}' )

        if cond_value:
            return ( instr[1], True )
        else:
            # else case
            assert len(instr) == 3
            return ( instr[2], True )

    def exec_show_text( self, loc, instr ):
        from utils import get_list_element_count, retrieve_single_element
        n = get_list_element_count( instr )
        assert n==1, f'I:exec_show_text: list has {n} elements, expected 1.'
        text = retrieve_single_element( instr )
        if DEBUG_LVL > 0:
            print( f'I:exec_show_text: f{text}' )
        #from utils import ast_display
        #ast_display( instr )
        self.display_text( text )

        return (None, False)

    def execute_raw( self, loc, instr ):
        if DEBUG_LVL > 0:
            print( f'I:execute_raw : instr={instr}, loc={loc}, self={str(self)}' )
        exec( instr, { 'local':loc, 'glob':self.glob } )
        if DEBUG_LVL > 0:
            print( f'I:execute_raw : AFTER loc={loc}, self={str(self)}' )
        return ( None, True )

    def exec_choose( self, loc, instr ):
        if DEBUG_LVL > 0:
            print( 'I:exec_choose' )
        instr_ok = unpack_list(instr)

        assert instr_ok[0]=='choices'
        choices=instr_ok[1]

        default = None
        if len(instr_ok)==3:
            defaults = unpack_list(instr_ok[2])
            assert len(defaults)==2
            default = defaults[1]
            assert defaults[0]=='default' and isinstance(default, int) and 1 <= default and default <= len(choices)
            
        user_choice = self.display_choices( choices, default )
        if DEBUG_LVL > 0:
            print( f"I:exec_choose: {user_choice} was chosen !")
        self.last_choice = user_choice
        return ( None, True )

    def exec_when( self, loc, instr ):
        if DEBUG_LVL > 0:
            print( 'I:exec_when' )
        instr_ok = unpack_list(instr)
        assert len(instr_ok)==2
        if self.debug():
            ast_display(instr_ok)

        choice = instr_ok[0]
        if self.last_choice != choice or self.last_choice == None:
            if DEBUG_LVL > 0:
                print(f'I:exec_when: Ignored when block')
            return ( None, True )
        else:
            if DEBUG_LVL > 0:
                print(f'I:exec_when: when block to be executed')
            when_block = instr_ok[1]
            return ( when_block, True )
        
    def display_text( self, text ):
        print( f' $ {text}' )

    def display_choices( self, choices, default=None ):
        ''' choices user input
        remember : choice and default are 1-indexed and python lists are 0-index
        '''
        suffix = F'[LEAVE BLANK FOR DEFAULT ({choices[default-1]})]' if default else '[MUST CHOOSE AN OPTION]'
        while True:
            self.display_text('Please select one of the following options : ' + suffix)
            for idx,choice in enumerate(choices):
                self.display_text(f' {idx+1} : {choice} ')
            
            user_choice = input(" >> Choice : ")
            if user_choice=='' and default:
                return choices[default-1]
            try:
                tmp = int(user_choice)
                if 1 <= tmp and tmp <= len(choices):
                    return choices[tmp-1]
            except ValueError:
                self.display_text('INVALID VALUE ENTERED !')


    def __str__(self):
        return str(self.__dict__)
