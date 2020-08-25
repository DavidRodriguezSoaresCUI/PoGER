from pprint import pprint

def cleanup_array( a ):
    if isinstance( a, list ):
        l = len(a)
        if l==0:
            return None
        elif l==1:
            return cleanup_array( a[0] )
        return [ x for x in [ cleanup_array(item) for item in a if item != None] if x!= None]
    return a

pprint( cleanup_array( None ) )
pprint( cleanup_array( [] ) )
pprint( cleanup_array( [[], 1] ) )
pprint( cleanup_array( [[3], 1] ) )
pprint( cleanup_array( [[[5]],1] ) )
pprint( cleanup_array( [[[5,7]],1] ) )