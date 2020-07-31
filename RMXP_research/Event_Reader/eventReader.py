import sys, token, operator 
from tokenize import generate_tokens
from io import StringIO
import pathlib
from pprint import pprint
from funcparserlib.parser import (some, a, many, skip, finished, maybe, with_forward_decls)
from funcparserlib.lexer import make_tokenizer, Token, LexerError

def tokenize(str):
    '''str -> Sequence(Token)'''
    specs = [
        ('Comment', (r'#.*',)),
        ('NL', (r'(\r\n)|\n',)),
        ('Space', (r'[ \t\,]+',)),
        ('Marker', (r'(\[event\])|(\[page\])|(\[end\])',)),
        ('Indent', (r'\[INDENT\]',)),
        ('Dedent', (r'\[DEDENT\]',)),
        ('Script', (r's\:[a-z][a-z\_0-9\.]*',)),
        ('Symbol', (r'\:[a-z][a-z\_0-9]*',)),
        ('Word', (r'[a-z][a-z\_0-9]*',)),
        ('Log_Op', (r'(==)|(>=)|(<=)|(>)|(<)|(!=)',)),
        ('Assign_Op', (r'[\+\-\*/]?=',)),
        ('Add_Op', (r'[\+\-]',)),
        ('Mul_Op', (r'[\*/]',)),
        ('Number', (r'-?[0-9]+(\.[0-9]*)?',)),
        ('Bracket', (r'[\[\]]',)),
        ('Parenthesis', (r'[\(\)]',)),
        ('String', (r'"[^"]*"',)), # '\"' escapes are ignored
    ]
    useless = ['Comment', 'Space']#['Comment', 'NL', 'Space']
    t = make_tokenizer(specs)
    res = [x for x in t(str) if x.type not in useless]
    '''return [ x for idx,x in enumerate(res)
        if (x.type not in ['NL']) or (idx==0) or (x != res[idx-1]) ]'''
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
    def make_number(s):
        try:
            return int(s)
        except ValueError:
            return float(s)
    def eval_expr(z, list):
        'float, [((float, float -> float), float)] -> float'
        return reduce(lambda s, f_x: f_x[0](s, f_x[1]), list, z)
    
    # const(x) [function] takes no arg and returns x
    const  = lambda x: lambda _: x
    # unarg(f) [function] takes arguments and returns f(*x)
    unarg  = lambda f: lambda x: f(*x)
    tokval = lambda tok: tok.value
    # makeop(s,f) [function] returns an operator : symbol s, behaves like actual operator f
    makeop = lambda s, f: op(s) >> const(f)
    # eval [function] takes argument(s) and returns 'eval_expr(*args)'
    eval = unarg(eval_expr)

    number = (
        some(lambda tok: tok.type == 'Number')
        >> tokval
        >> make_number )

    a_tok = lambda t_type, t_val: a(Token(t_type, t_val))

    # Parsing markers
    a_marker = lambda t_val: a_tok('Marker', t_val)
    event_marker = a_marker('[event]')
    page_marker  = a_marker('[page]')
    end_marker   = a_marker('[end]')

    page = page_marker# + config

    #config = maybe( config_var + op('=') + parameter )
    end = skip(finished)
    event = event_marker + maybe(config)# + maybe(expr) + end
    
    return event.parse(tokens)



if __name__ == "__main__":
    cwd = pathlib.Path()
    events = list(cwd.glob('Map000_*'))
    pprint(events)

    for event in events:
        content = None
        with event.open( 'r' ) as f:
            content = f.read().lower()
        
        assert not ( '\t' in content )
        content_noindent = indentation_converter(content)
        tok = tokenize( content_noindent )
        
        with open('test', 'w') as f:
            for token in tok:
                #f.write(str(type(token.type)))
                f.write(str(token) + '\n')
        
        out = parse( tok )
        print(type(out))
        with open('test2', 'w') as f:
            f.write(str(out))