last_indent=0

def ast_display( ast, leading='', idx=-1 ):
    if isinstance( ast, list ) or isinstance( ast, tuple ):
        print( f'{leading} {len(ast)}' )
        next_leading = f"{leading.replace('+','|')} + -"
        for idx,item in enumerate(ast):
            ast_display( item, next_leading )

    else:
        print( f'{leading}|{ast}' )

def ast_cleanup( ast ):
    if isinstance( ast, tuple ):
        ast = list(ast) # tuple -> list for ease of use
    if isinstance( ast, list ):
        if len(ast)>1 and ast[-1]==[]:
            # there are a lot of [] at the end of lists/tuples : artifacts to remove
            del ast[-1]
        return [ ast_cleanup(x) for x in ast if (x!=None) ]
    else:
        return ast


def unquote( s ):
    return s.replace('"','')