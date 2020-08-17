from pprint import pprint

class Dex:
    ''' Basic class for indexing instances '''
    def __init__(self, items, id_field, name_field):
        if isinstance(items, list):
            if isinstance(items[0], PokedexEntry):
                self.items = { e.data[id_field]:e for e in items }
                self.name2id = { e.data[name_field]:_id for _id,e in self.items.items() }
            else:
                self.items = { e[id_field]:e for e in items }
                self.name2id = { e[name_field]:_id for _id,e in self.items.items() }
        else:
            raise NotImplementedError

    def get(self, _id):
        if isinstance( _id, str ):
            # get item by name
            return self.items[ self.name2id[_id] ]
        elif isinstance( _id, int ):
            # get item by id
            return self.items[ _id ]
        raise NotImplementedError(f'Dex:get: cannot get item from id {id} {type(id)}')

    def name_to_id(self):
        return dict( self.name2id )

    def id_to_name(self):
        return { v:k for k,v in self.name2id.items() }



class PokedexEntry:

    PKMN_DATA = [
        'Name',
        'InternalName',
        'Kind',
        'Type1',
        'Pokedex',
        'Moves',
        'Color',
        'BaseStats',
        'Rareness',
        'GenderRate',
        'Happiness',
        'Shape',
        'GrowthRate',
        'StepsToHatch',
        'BaseEXP',
        'EffortPoints',
        'Compatibility',
        'Height',
        'Weight'
    ]

    PKMN_DATA_OPT = [
        'Abilities',
        'HiddenAbility',
        'EggMoves',
        'BattlerPlayerY',
        'BattlerEnemyY',
        'BattlerAltitude',
        'FormName',
        'RegionalNumbers',
        'Type2',
        'Evolutions',
        'Habitat',
        'WildItemCommon',
        'WildItemUncommon',
        'WildItemRare',
        'Incense'
    ]

    # GenderRate -> species female rate (percent)
    PKMN_GENDERRATE_CONV = {
        'AlwaysMale':0,
        'FemaleOneEighth':1/8,
        'Female25Percent':1/4,
        'Female50Percent':1/2,
        'Female75Percent':3/4,
        'FemaleSevenEighths':7/8,
        'AlwaysFemale':1,
        'Genderless':-1
    }

    def __init__(self, parsed_item):
        self.data = dict()

        
        if isinstance(parsed_item, dict):
            self.init_cleanup( parsed_item )
        else:
            raise NotImplementedError('Pokemon not initialized via known method.')

    def init_cleanup( self, parsed_item ):
        #print('P.init_from_pbs')
        import ini, sys, re
        from utils import try_make_int_list, try_make_number

        config = parsed_item
        
        for e in [ 'BaseStats', 'EffortPoints', 'RegionalNumbers' ]:
            try:
                config[e] = try_make_int_list( config[e] )
            except KeyError:
                if e in PokedexEntry.PKMN_DATA:
                    raise KeyError(f"{config['Name']} has no element {e} !")

        # move conversion
        move_items = config['Moves'].split(',')
        config['Moves'] = { move_items[2*i+1]:int(move_items[2*i]) for i in range( int(len(move_items)/2) ) }

        # eggGroup conversion
        _tmp = config.get( 'Compatibility', None )
        if _tmp and (',' in _tmp):
            config['Compatibility'] = [ s for s in _tmp.split(',') ]


        # evolutions conversion
        if config.get( 'Evolutions', None ):
            move_items = config['Evolutions'].split(',')
            config['Evolutions'] = { try_make_number(move_items[3*i+2]):move_items[3*i] for i in range( int(len(move_items)/3) ) }

        # genderrate conversion
        config['GenderRate'] = PokedexEntry.PKMN_GENDERRATE_CONV[ config['GenderRate'] ]

        # eggmoves conversion
        if config.get( 'EggMoves', None ):
            config['EggMoves'] = config['EggMoves'].split(',')

        # integrity check
        for e in PokedexEntry.PKMN_DATA:
            assert e in config, f"Pokemon {config['id']} lacks mandatory element {e}."

        self.data = config

    def add_shadow_moves( self, moves ):
        for sm in moves:
            (self.data['Moves'])[sm] = 'Shadow'

    def __str__(self):
        return str(self.__dict__)

