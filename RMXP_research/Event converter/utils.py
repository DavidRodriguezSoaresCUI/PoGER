# from utils import frame2ms, subject_to_string, quote, unquote, direction_toString, SS_val_str, intersect_dict, substract_dict, flatten_dict

def flatten_dict(d):
    items = dict()
    for k, v in d.items():
        if isinstance(v, dict):
            items.update( flatten_dict(v) )
        elif isinstance(v, list):
            items[k] = [ flatten_dict(x) if isinstance(x,dict) else x.__dict__ for x in v ]
        elif isinstance(v, int) or isinstance(v, float) or isinstance(v, bool) or isinstance(v, str) or v==None:
            items[k] = v
        else:
            items.update( flatten_dict(v.__dict__) )
    if '_class' in items:
        del items['_class']
    return items

def substract_dict( base_d, sub_d, verbose=False ):
    diff = { k:v for k,v in base_d.items() if v!=sub_d.get(k, 0 if (v==None) else None ) }
    if verbose:
        from pprint import pprint
        print('substract_dict BEGIN')
        print('base_d')
        pprint(base_d)
        print('sub_d')
        pprint(sub_d)
        print('difference')
        pprint(diff)
        print('substract_dict END')
    return diff

def intersect_dict( base_d, other_d ):
    return { k:v for k,v in base_d.items() if v==other_d.get(k, 0 if (v==None) else None ) }

def frame2ms( i ):
    assert isinstance(i, int)
    return i*50

def subject_to_string( s ):
    if s==-1:
        return ':player'
    elif s==0:
        return ':self'
    else:
        #print( f'subject_to_string:Undocumented subject {s}' )
        return s

def quote( s ):
    return '"'+s.replace('\\', '\\\\').replace('"', '\\"')+'"'

def unquote( s ):
    return s.replace('"','')

def direction_toString( dir ):
    switcher={
        0:'K',
        2:'S',
        4:'W',
        6:'E',
        8:'N',
    }
    res=switcher.get(dir, None)
    assert res, f"direction_toString:Undocumented: {dir}"
    return res

def SS_val_str( val ):
    SS_switcher = {
        0:':ON',
        1:':OFF'
    }
    return SS_switcher[val]

def common_relations_decoder( relation, value ):
    switcher = None
    if relation == 1:
        switcher = {
            0 : 'Top',
            1 : 'Middle',
            2 : 'Bottom'
        }
    elif relation == 2:
        switcher = {
            0 : 'Show',
            1 : 'Hide'
        }
    elif relation == 3:
        return SS_val_str(value)
    elif relation == 4:
        switcher = {
            0 : '+=',
            1 : '-='
        }
    elif relation == 5:
        return direction_toString( value )
    elif relation == 6:
        switcher = {
            0:'==',
            1:'>=',
            2:'<=',
            3:'>',
            4:'<',
            5:'!=',
        }
    elif relation == 8:
        switcher = {
            0 : '>=',
            1 : '<='
        }
    elif relation == 9:
        switcher = {
            0:'=',
            1:'+=',
            2:'-=',
            3:'*=',
            4:'/=',
            5:'%='
        }
    elif relation == 11:
        switcher = {
            0:'NW',
            1:'Centered'
        }
    elif relation == 12:
        switcher = {
            0:'Normal',
            1:'Additive',
            2:'Substractive'
        }
    elif relation == 13:
        switcher = {
            0:'None',
            1:'Rain',
            2:'Storm',
            3:'Snow'
        }
    else:
        raise ValueError(f'common_relations_decoder: no decoder for relation {relation}.')
        
    return switcher[value]
    