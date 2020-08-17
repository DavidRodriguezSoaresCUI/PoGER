from pathlib import Path
from pprint import pprint
import time, re, ini, sys, csv

DEBUG = True

class pbEngine:

    # Current entries in the self.data dict :
    # - Machines : dict (move [str] => pokemon InternalName [list of str])
    # - PokemonForms : dict (pokemon InternalName+'-'+formID [str] => dict( PokedexEntry override [str] => value [*] ))
    # - Moves : Dex of moves [dict], see documentation for field names
    # - Metadata : dict( map id [int] => dict( field name [str] => value [*] ) ), see documentation for field names
    # - Items : Dex of items [dict], see documentation for field names
    # - Abilities : Dex of abilities [dict], see documentation for field names
    # - Berryplants : dict( berry tree InternalName [str] => list of 4 values )
    # - Pokedex : Dex of PokedexEntries
    # - Types : To be redone in a more elegant manner, Dex of types [dict], see documentation for field names

    PBS_FILES = [
        'pokemon.txt',
        'berryplants.txt',
        'abilities.txt',
        'items.txt',
        'metadata.txt',
        'moves.txt',
        'pokemonforms.txt',
        'shadowmoves.txt',
        'tm.txt',
        'types.txt'
    ]

    def __init__(self, pbs_location, demo=False):
        self.pbs_location = pbs_location
        assert self.pbs_location.is_dir(), f'{self.pbs_location} directory not found !'
        self.data = dict()
        self.demo = demo
        
        self.importPBSdata()

    def importPBSdata( self ):
        for f in pbEngine.PBS_FILES:
            pbs_f = self.pbs_location.joinpath( f )
            if pbs_f.is_file():
                self.readPBS( pbs_f )
            else:
                print( f'importPBSdata: {pbs_f} not found !' )

    def readPBS( self, pbs_f ):
        import re
        from pprint import pformat
        with pbs_f.open( 'r', encoding='utf-8-sig' ) as f:
            content = f.read()

        content_noSep = re.sub( r'\#[\-]+\ *(\n)|(\r\n)', '', content )
        
        '''test_out = Path( str(pbs_f).replace('.txt','_test.txt') )
        with test_out.open( 'w' ) as f:
            f.write( '{}'.format(content_items) )'''
        
        func_name = 'readPBS_' + pbs_f.stem
        func = getattr( self, func_name )
        func( content_noSep )


    def readPBS_pokemon( self, items ):
        if DEBUG:
            print(f'readPBS_pokemon called')

        from pbEngine_classes import Dex, PokedexEntry

        start = time.time()

        # fix for ini style
        _items = re.sub( r'\=\ *($|\n)', '=null\n', items )

        parsed = ini.parse(_items)
        pkmns = list()
        for k,v in parsed.items():
            v['id'] = k
            pkmns.append( PokedexEntry(v) )
        self.data['Pokedex'] = Dex( pkmns, id_field='id', name_field='InternalName' )
        print(f"{len(list(self.data['Pokedex'].items.keys()))} pokémon found !")
        print(f'Loaded pokedex in {round((time.time()-start)*1000)} ms.')

        while self.demo:
            name = input('Enter a pokemon (Q to quit) : ')
            if name.lower()=='q':
                break
            
            try:
                p = self.get_pokemon(name)
                print('Displaying data for pokemon {name} :')
                pprint( str(p) )
            except:
                print('Unknown Pokemon')
            
        if False:
            print('Displaying dex number<->name for each pokemon')
            pkdex = self.data['Pokedex']
            pprint( pkdex.name_to_id() )
            pprint( pkdex.id_to_name() )


    def get_pokemon( self, name ):
        return self.data['Pokedex'].get(name)

    def readPBS_berryplants( self, items ):
        if DEBUG:
            print(f'readPBS_berryplants called')

        assert isinstance(items, str)
        from utils import try_make_int_list

        start = time.time()
        d = ini.parse( items )
        print(f'{len(d)} berryplants found !')
        self.data['Berryplants'] = { k:try_make_int_list(v) for k,v in d.items() }
        print(f'Loaded berries in {round((time.time()-start)*1000)} ms.')

    def readPBS_abilities( self, items ):
        if DEBUG:
            print(f'readPBS_abilities called')

        assert isinstance(items, str)
        from utils import try_make_number
        from pbEngine_classes import Dex

        start = time.time()
        reader = csv.DictReader( items.splitlines(), fieldnames=['id','InternalName','Name','Description'] )
        abilities = list()
        for a in reader:
            a['id'] = int(a['id'])
            abilities.append(a)
        self.data['Abilities'] = Dex( abilities, id_field='id', name_field='InternalName' )
        print(f'{len(abilities)} abilities found !')
        print(f'Loaded abilities in {round((time.time()-start)*1000)} ms.')

    def readPBS_items( self, items ):
        if DEBUG:
            print(f'readPBS_items called')

        assert isinstance(items, str)
        from utils import dict_make_int
        from pbEngine_classes import Dex

        start = time.time()
        fieldnames = [
            'id','InternalName','Name','NamePlural','Pocket','Price','Description','Use','BattleUse','Special','Machine']
        reader = csv.DictReader( items.splitlines(), fieldnames=fieldnames )
        _items = list()
        for i in reader:
            i_ok = dict_make_int( i, ['id','Pocket','Use','BattleUse','Special'] )
            _items.append( i_ok )

        self.data['Items'] = Dex( _items, id_field='id', name_field='InternalName' )
        print(f'{len(_items)} items found !')
        print(f'Loaded items in {round((time.time()-start)*1000)} ms.')

    def readPBS_metadata( self, items ):
        if DEBUG:
            print(f'readPBS_metadata called')

        from utils import try_make_int_list

        start = time.time()
        parsed = ini.parse( items )
        meta = dict()
        for k,v in parsed.items():
            meta[int(k)] = { k2:try_make_int_list(v2) for k2,v2 in v.items() }
        
        self.data['Metadata'] = meta
        print(f'{len(meta)} maps found !')
        print(f'Loaded map metadata in {round((time.time()-start)*1000)} ms.')

    def readPBS_moves( self, items ):
        if DEBUG:
            print(f'readPBS_moves called')

        assert isinstance(items, str)
        from utils import dict_make_int
        from pbEngine_classes import Dex

        start = time.time()
        fieldnames = [
            'id','InternalName','Name','code','Power','Type',
            'Category','Accuracy','PP','EffectChance','Target',
            'Priority','Flags','Description']
        reader = csv.DictReader( items.splitlines(), fieldnames=fieldnames )
        moves = list()
        for m in reader:
            del m['code']
            m_ok = dict_make_int( m, ['id','Target','Priority'] )
            moves.append( m_ok )

        self.data['Moves'] = Dex( moves, id_field='id', name_field='InternalName' )
        print(f'{len(moves)} moves found !')
        print(f'Loaded moves in {round((time.time()-start)*1000)} ms.')

    def readPBS_pokemonforms( self, items ):
        if DEBUG:
            print(f'readPBS_pokemonforms called')

        start = time.time()
        parsed = ini.parse( items )
        
        self.data['PokemonForms'] = parsed
        print(f'{len(list(parsed.keys()))} forms found !')
        print(f'Loaded pokemon forms in {round((time.time()-start)*1000)} ms.')

    def readPBS_shadowmoves( self, items ):
        if DEBUG:
            print(f'readPBS_shadowmoves called')

        from pbEngine_classes import Dex
        pokedex = self.data['Pokedex']

        start = time.time()
        parsed = ini.parse( items )
        for pkmn_name,moves in parsed.items():
            #print(f'Adding move(s) {moves} to {pkmn_name}.')
            pkmn = pokedex.get( pkmn_name )
            pkmn.add_shadow_moves( [ s for s in moves.split(',') ] )

        print(f'Loaded shadow moves in {round((time.time()-start)*1000)} ms.')
        #print( self.data['Pokedex'].get('BUTTERFREE') )

    def readPBS_tm( self, items ):
        if DEBUG:
            print(f'readPBS_tm called')

        from pbEngine_classes import Dex

        start = time.time()
        parsed = ini.parse( items )
        machines = dict()
        for move, pkmns in parsed.items():
            assert isinstance(move, str)
            l = list(pkmns.keys())
            assert len(l)==1
            _pkmns = [ s for s in l[0].split(',') ]
            machines[move] = _pkmns

        
        self.data['Machines'] = machines
        print(f'{len(machines)} machines found !')
        print(f'Loaded machines in {round((time.time()-start)*1000)} ms.')
        #print( self.data['Pokedex'].get('BUTTERFREE') )

    def readPBS_types( self, items ):
        if DEBUG:
            print(f'readPBS_types called')

        from pbEngine_classes import Dex

        start = time.time()
        parsed = ini.parse( items )
        types = list()
        for k,v in parsed.items():
            v['id'] = int(k)
            types.append(v)
        
        self.data['Types'] = Dex( types, id_field='id', name_field='InternalName' )
        print(f'{len(types)} types found !')
        print(f'Loaded types in {round((time.time()-start)*1000)} ms.')

        
        