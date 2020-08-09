import sys, token, operator 
from tokenize import generate_tokens
from io import StringIO
import pathlib, logging
from pprint import pprint
from funcparserlib.parser import (some, a, many, skip, finished, maybe, with_forward_decls, oneplus)
from funcparserlib.lexer import make_tokenizer, Token, LexerError
from event import Event
from collections.abc import Iterable
from utils import unquote

DEBUG=False

def tokenize(str):
    '''str -> Sequence(Token)'''
    specs = [
        ('Comment', (r'#.*',)),
        ('LF', (r'(\r\n)|\n',)),
        ('Space', (r'[ \t]+',)),
        ('Comma', (r'\,',)),
        ('Keyword', (r'(if)|(else)|(when)|(loop)|(break)',)),
        #('Command', (r'',)),
        ('Marker', (r'(\[event\])|(\[page\])|(\[end\])',)),
        ('Indent', (r'(\[INDENT\])|(\[DEDENT\])',)),
        ('Script', (r's\:.*',)),
        ('Symbol', (r'\:[a-z][a-z\_0-9]*',)),
        ('CMD_ID',(r'(step)|(turn)|(move event)|(wait)|(set)|(play)|(show text)|(choose)|(change text options)|(end execution)|(label)|(goto)|(transfer player)|(set move route)|(screen shake)|(transition)|(show picture)|(move picture)|(erase picture)|(set weather)|(fade out bgm)|(memorize bgx)|(restore bgx)|(restore all)|(return to title screen)|(save)',)),
        ('TurnValue', (r'"?((90 Right)|(90 Left)|(180)|(90 random)|(random)|(towards player)|(away from player))"?',)),
        ('Bool', (r'(True)|(False)',)), # basically, a string without quotemarks, delimited by spaces
        ('Word', (r'[a-z][a-z\_0-9]*',)), # basically, a string without quotemarks, delimited by spaces
        ('Log_Op', (r'(==)|(>=)|(<=)|(>)|(<)|(!=)',)),
        ('Assign_Op', (r'[\+\-\*/]?=',)),
        ('Op', (r'[\+\-\*/]',)),
        ('Number', (r'-?[0-9]+(\.[0-9]+)?',)),
        ('Bracket', (r'[\[\]]',)),
        #('Parenthesis', (r'[\(\)]',)),
        ('String', (r'"[^"]*"',)), # '\"' escapes are ignored
    ]
    useless = ['Comment', 'Space']#['Comment', 'NL', 'Space']
    t = make_tokenizer(specs)
    res = [x for x in t(str) if x.type not in useless]
    '''return [ x for idx,x in enumerate(res)
        if (x.type not in ['LF']) or (idx==0) or (x != res[idx-1]) ]'''
    return res

def indentation_converter( s ):
    ''' interprets indentation '''
    
    lines = s.split('\n')
    last_ind = 0
    ind_len = 0
    lines_OK = list()
    for line in lines:
        line_clean = line.lstrip(' ')
        ind = len(line) - len(line_clean)
        diff = last_ind - ind
        if diff!=0:
            if ind_len==0:
                ind_len = ind
                if DEBUG:
                    print(f'indentation_converter : ind_len={ind_len}')
            if diff < 0:
                n = (-diff) // ind_len
                line_clean = '[INDENT]'*n + line_clean
            else:
                n = diff // ind_len
                line_clean = '[DEDENT]'*n + line_clean
            last_ind = ind
        lines_OK.append( line_clean )
    

    return '\n'.join(lines_OK)
        
def parse( tokens ):
    'Sequence(Tokens) -> int/float/None'

    def make_number(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def flatten_list( l ):
        import functools
        return functools.reduce(operator.iconcat, l, [])

    def new_page( x ):
        e.add_behavior()
        return x

    def print_and_return( x ):
        print(f'print_and_return: x,{type(x)}, {x}')
        return x
    
    # const(x) [function] takes no arg and returns x
    const  = lambda x: lambda _: x
    # unarg(f) [function] takes arguments and returns f(*x)
    unarg  = lambda f: lambda x: f(*x)
    tokval = lambda tok: tok.value
    symval = lambda tok: f'glob["{tok.value}"]'
    scriptval = lambda tok: tok.value[2:] if ( '(' in tok.value ) else tok.value[2:]+'()'
    # makeop(s,f) [function] returns an operator : symbol s, behaves like actual operator f
    makeop = lambda s, f: op(s) >> const(f)
    assign_op = lambda s: a(Token('Assign_Op', s)) >> tokval
    assign_op_ = lambda s: skip(assign_op(s))

    number = (
        some(lambda tok: tok.type == 'Number')
        >> tokval
        >> make_number )

    string = (
        some(lambda tok: tok.type == 'String')
        >> tokval )

    word = (
        some(lambda tok: tok.type=='Word')
        >> tokval )

    cmd_id = (
        some(lambda tok: tok.type=='CMD_ID')
        >> tokval )

    comma = (
        some(lambda tok: tok.type=='Comma')
        >> tokval )

    '''anything = (
        some(lambda tok: tok.type!='LF' and tok.type=='Marker')
        >> tokval
    )'''

    symbol = (
        some(lambda tok: tok.type=='Symbol')
        >> symval
    )

    script = (
        some(lambda tok: tok.type=='Script')
        >> scriptval
    )

    turn_value = (
        some(lambda tok: tok.type=='TurnValue')
        >> tokval
        >> unquote
    )

    a_tok = lambda t_type, t_val: a(Token(t_type, t_val))
    
    words = oneplus(word)

    # parsing indentation
    indent = skip(a_tok('Indent', '[INDENT]'))
    dedent = skip(a_tok('Indent', '[DEDENT]'))

    def bool2str( b ):
        switcher = {
            ':on':True,
            ':off':False,
            'True':True,
            'False':False
        }
        return switcher[b]


    # parsing booleans
    b_true = a_tok('Bool', 'True')
    b_false = a_tok('Bool', 'False')
    b_true2 = a_tok('Symbol', ':on')
    b_false2 = a_tok('Symbol', ':off')
    bool_value = ( 
        (b_true | b_false | b_true2 | b_false2)
        >> tokval
        >> bool2str )


    # parsing keywords ('Keyword', (r'(if)|(else)|(when)|(loop)|(break)',)),
    kw = lambda o: a_tok('Keyword', o)
    a_if    = kw('if') >> tokval
    a_else  = kw('else') >> tokval
    a_when  = kw('when') >> tokval
    a_loop  = kw('loop') >> tokval
    a_break = kw('break') >> tokval

    # parsing ops
    log_op = lambda o: a_tok('Log_Op', o)
    equ = log_op('==')
    equ2 = a_tok('Word', 'is')
    geq = log_op('>=')
    leq = log_op('<=')
    gtr = log_op('>')
    lss = log_op('<')
    neq = log_op('!=')
    log_operator = (equ | equ2 | geq | leq | gtr | lss | neq)  >> tokval

    assign_op = lambda o: a_tok('Assign_Op', o)
    assi = assign_op('=')
    apls = assign_op('+=')
    amin = assign_op('-=')
    amul = assign_op('*=')
    adiv = assign_op('/=')
    assign_operator = (assi | apls | amin | amul | adiv) >> tokval
    
    math_op = lambda o: a_tok('Op', o)
    madd = math_op('+')
    mmin = math_op('-')
    mmul = math_op('*')
    mdiv = math_op('/')
    math_operator = ( madd | mmin | mmul | mdiv ) >> tokval
    

    # Parsing brackets
    a_bracket = lambda s: a_tok('Bracket', s)
    a_bracket_ = lambda s: skip(a_bracket(s))
    opening_bracket = a_bracket_('[')
    closing_bracket = a_bracket_(']')

    # Parsing parenthesis
    a_parenthesis = lambda s: a_tok('Parenthesis', s)
    a_parenthesis_ = lambda s: skip(a_parenthesis(s))
    opening_bracket = a_bracket_('[')
    closing_bracket = a_bracket_(']')

    # Parsing markers
    a_marker = lambda t_val: a_tok('Marker', t_val)
    a_marker_ = lambda t_val: skip(a_marker(t_val))
    event_marker = a_marker_('[event]')
    page_marker  = a_marker_('[page]') # >> new_page
    end_marker   = a_marker_('[end]')

    # Parsing line feeds
    LF = a_tok('LF', '\n')
    LF_ = skip(LF)
    LFs = many(LF)
    LFs_ = skip(maybe(LFs))

    value = number | string | word | turn_value

    def cleanup_array( a ):
        if isinstance( a, list ):
            l = len(a)
            if l==0:
                return None
            elif l==1:
                return cleanup_array( a[0] )
        return a

    def make_array(n):
        if DEBUG:
            print(f'make_array: n:{type(n)},{n}')
        if isinstance(n, str):
            return n
        if n==None:
            return None #[]
        if n[1]==[] or n[1]==None:
            return [n[0]] if isinstance(n[0], list) else n[0] 
        if not isinstance(n[1], list):
            return [n[0], n[1]]
        return [n[0]] + n[1]

    def make_str( a ):
        if DEBUG:
            print( f'make_str : a {type(a)}, {a}' )
        if isinstance(a, Iterable) and (not isinstance(a, str)):
            return ' '.join( [ item if isinstance(item, str) else str(item) for item in a ] )
        return a

    a_list = (
        (opening_bracket + value + many(skip(maybe(comma)) + value) + closing_bracket)
        >> make_array )

    parameter_value = value | a_list | bool_value
    config_var = word

    deal_with_config = lambda l : e.add_parameter(l)
    config = (
        maybe( config_var + skip(assi) + parameter_value )
        >> make_array ) # >> deal_with_config

    parameter_name = word
    parameter = maybe(parameter_name + skip(assi)) + parameter_value
    parameters = parameter + many( skip(maybe(comma)) + parameter )
    
    cmd = ( cmd_id + many(parameters) )

    comparable = number | symbol | script | bool_value | word
    log_expr = (
        ( comparable + log_operator + comparable )
        >> make_str )

    @with_forward_decls
    def code_block(): # hack to use 'statements' above its declaration
        return indent + LFs_ + statements + dedent
        
    if_block = (a_if + (log_expr | script) + LFs_ + code_block + maybe( skip(a_else) + LFs_ + code_block ) ) 

    expression = (
        ( oneplus( math_operator | number | symbol ) | log_expr | script | parameter_value )
        >> make_str ) # | number | symbol | #  | num_expr
    
    var_manipulation = (
        (symbol + assign_operator + expression)
        >> make_str)

    when_block = a_when + value + LFs_ + code_block

    # TODO : loop
    statement = ( cmd | if_block | var_manipulation | when_block | script | a_break )

    statements = many(statement + LFs_)

    config_or_cond = maybe( ( config_var + assign_op_('=') + parameter_value )  | log_expr )

    page = ( page_marker + LFs_ + many(config_or_cond + LF_) + LFs_ + statements + skip(end_marker) + LFs_ ) # >> print_and_return #

    end = skip(finished)
    event = LFs_ + event_marker + LFs_ + oneplus(config + LF_) + LFs_ + many(page) + end
    
    res = event.parse(tokens)
    #print('res:{}'.format(res))

    return res

def boolean_converter( s ):
    return s.replace('true','True').replace('false','False')

def build_event( event_file, test=True ):
    assert isinstance( event_file, pathlib.Path ) and event_file.is_file()

    content = None
    with event_file.open( 'r' ) as f:
        content = f.read().lower()
    
    assert not ( '\t' in content )
    content_ok = boolean_converter( indentation_converter(content) )
    tok = tokenize( content_ok )
    
    if test:
        with open('test', 'w') as f:
            for token in tok:
                #f.write(str(type(token.type)))
                f.write(str(token) + '\n')
    
    out = parse( tok )
    #print(type(out))
    #pprint(out)
    '''with open('test2', 'w') as f:
        f.write(str(out))'''
    return out

if __name__ == "__main__":
    cwd = pathlib.Path()
    events = list(cwd.glob('011_*'))
    pprint(events)

    for event_file in events:
        e = Event( event_file )
        for b in e.behaviors:
            print('behavior')
            pprint(str(b))
