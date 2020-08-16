
def try_make_number(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

def try_make_int_list(s):
    if not isinstance( s, str ):
        return s
    items = s.split(',')
    if len(items)<2:
        return s
    
    try:
        return [ int(item) for item in items ]
    except ValueError:
        return s

def dict_make_int( d, l ):
    for item in l:
        d[item] = int(d[item])
    return d