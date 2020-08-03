import sys, token, operator 
from tokenize import generate_tokens
from io import StringIO
import pathlib, logging
from pprint import pprint
from funcparserlib.parser import (some, a, many, skip, finished, maybe, with_forward_decls, oneplus)
from funcparserlib.lexer import make_tokenizer, Token, LexerError
from event import Event

import funcparserlib.parser
funcparserlib.parser.debug=True

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
        ('Script', (r's\:[a-z][a-z\_0-9\.\(\)\:]*',)),
        ('Symbol', (r'\:[a-z][a-z\_0-9]*',)),
        ('Bool', (r'(True)|(False)',)), # basically, a string without quotemarks, delimited by spaces
        ('Word', (r'[a-z][a-z\_0-9]*',)), # basically, a string without quotemarks, delimited by spaces
        ('Log_Op', (r'(==)|(>=)|(<=)|(>)|(<)|(!=)',)),
        ('Assign_Op', (r'[\+\-\*/]?=',)),
        ('Op', (r'[\+\-\*/]',)),
        ('Number', (r'-?[0-9]+(\.[0-9]*)?',)),
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
    last_sc = 0
    lines_OK = list()
    for line in lines:
        line_clean = line.lstrip(' ')
        sc = len(line) - len(line_clean)
        if last_sc != sc:
            if last_sc < sc:
                line_clean = '[INDENT]'+line_clean
            else:
                line_clean = '[DEDENT]'+line_clean
            last_sc = sc
        lines_OK.append( line_clean )
    

    return '\n'.join(lines_OK)
        
def parse( tokens ):
    'Sequence(Tokens) -> int/float/None'

    e=Event()
    e.add_behavior()

    def make_number(s):
        try:
            return int(s)
        except ValueError:
            return float(s)

    def new_page( x ):
        e.add_behavior()
        return x
    
    # const(x) [function] takes no arg and returns x
    const  = lambda x: lambda _: x
    # unarg(f) [function] takes arguments and returns f(*x)
    unarg  = lambda f: lambda x: f(*x)
    tokval = lambda tok: tok.value
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

    comma = (
        some(lambda tok: tok.type=='Comma')
        >> tokval )

    '''anything = (
        some(lambda tok: tok.type!='LF' and tok.type=='Marker')
        >> tokval
    )'''

    symbol = (
        some(lambda tok: tok.type=='Symbol')
        >> tokval
    )

    script = (
        some(lambda tok: tok.type=='Script')
        >> tokval
    )

    a_tok = lambda t_type, t_val: a(Token(t_type, t_val))
    
    words = oneplus(word)

    # parsing indentation
    indent = a_tok('Indent', '[INDENT]')
    dedent = a_tok('Indent', '[DEDENT]')

    # parsing keywords
    a_if = a_tok('Word', 'if')
    a_else = a_tok('Word', 'else')

    # parsing ops
    log_op = lambda o: a_tok('Log_Op', o)
    equ = log_op('==')
    geq = log_op('>=')
    leq = log_op('<=')
    gtr = log_op('>')
    lss = log_op('<')
    neq = log_op('!=')
    log_operator = equ | geq | leq | gtr | lss | neq

    assign_op = lambda o: a_tok('Assign_Op', o)
    assi = assign_op('=')
    apls = assign_op('+=')
    amin = assign_op('-=')
    amul = assign_op('*=')
    adiv = assign_op('/=')
    assign_operator = assi | apls | amin | amul | adiv
    
    math_op = lambda o: a_tok('Op', o)
    madd = math_op('+')
    mmin = math_op('-')
    mmul = math_op('*')
    mdiv = math_op('/')
    

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
    page_marker  = a_marker_('[page]') >> new_page
    end_marker   = a_marker_('[end]')

    # Parsing line feeds
    LF = a_tok('LF', '\n')
    LF_ = skip(LF)
    LFs = many(LF)
    LFs_ = skip(maybe(LFs))

    value = number | string | word

    def make_array(n):
        print(f'make_array: n:{type(n)},{n}')
        return [] if (n is None) else [n[0]] + n[1]

    def print_and_return( x ):
        print(f'print_and_return: x,{type(x)}, {x}')
        return x

    a_list = opening_bracket + value + many(skip(maybe(comma)) + value) + closing_bracket >> make_array
    parameter_value = value | a_list
    config_var = word

    deal_with_config = lambda l : e.add_parameter(l)
    config = maybe( config_var + skip(assi) + parameter_value ) >> deal_with_config

    cmd_id = words
    parameter_name = word
    parameter = maybe(parameter_name + assi) + value #>> make_array
    parameters = parameter + many( skip(maybe(comma)) + parameter ) #>> make_array

    def deal_with_cmd(s): 
        print(f'deal_with_cmd: s,{type(s)},{s}')
        e.behavior_add_instruction( cmd_id=''.join(s[0]), parameters=s[1] )
    
    cmd = cmd_id + many(parameters) >> deal_with_cmd

    comparable = number | symbol | script
    log_expr = comparable + log_operator + comparable

    @with_forward_decls
    def code_block(): # hack to use 'statements' above its declaration
        return indent + statements + dedent
    if_cond = skip(a_if) + log_expr + LFs_ + code_block + maybe( skip(a_else) + LFs_ + code_block )

    statement = cmd# | if_cond
    statements = many(statement + LFs_)

    config_or_cond = (maybe( config_var + assign_op_('=') + parameter_value ) >> deal_with_config) \
        | (log_expr >> print_and_return)

    page = (
        page_marker + LFs_ + many(config_or_cond + LF_) + LFs_ + statements + end_marker + LFs_
        >> print_and_return )

    end = skip(finished)
    event = event_marker + LFs_ + oneplus(config + LF_) + LFs_ + many(page) + end
    
    res = event.parse(tokens)
    print('res:{}'.format(res))

    return e

def boolean_converter( s ):
    return s.replace(':ON','True').replace(':OFF','False').replace('true','True').replace('false','False')

if __name__ == "__main__":
    cwd = pathlib.Path()
    events = list(cwd.glob('Map001_*'))
    pprint(events)

    for event in events:
        content = None
        with event.open( 'r' ) as f:
            content = f.read().lower()
        
        assert not ( '\t' in content )
        content_ok = boolean_converter( indentation_converter(content) )
        tok = tokenize( content_ok )
        
        with open('test', 'w') as f:
            for token in tok:
                #f.write(str(type(token.type)))
                f.write(str(token) + '\n')
        
        out = parse( tok )
        print(type(out))
        pprint(str(out))
        '''with open('test2', 'w') as f:
            f.write(str(out))'''