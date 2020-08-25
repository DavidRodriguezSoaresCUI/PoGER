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

def get_list_element_count( l ):
    assert isinstance( l, list )
    count = 0
    for elem in l:
        count += get_list_element_count(elem) if isinstance(elem, list) else 1
    return count

def retrieve_single_element_h( l ):
    if isinstance( l, list ):
        for e in l:
            tmp = retrieve_single_element_h( e )
            if tmp:
                return tmp
    else:
        return l

def retrieve_single_element( l ):
    assert isinstance( l, list )
    res = retrieve_single_element_h( l )
    #print( f'retrieve_single_element: {l}->{res}' )
    return res

def unpack_list( l ):
    assert isinstance( l, list )
    if len(l)==0:
        raise ValueError('Failed to unpack list, perhaps is it empty ?')
    elif len(l)==1:
        return unpack_list(l[0])
    else:
        return l

def try_make_number(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s