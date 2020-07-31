class Event:

    def __init__(self):
        self.xy=None
        self.config=dict()
        self.behaviors=list()

    def add_parameter( self, p ):
        if p==None:
            return
        assert isinstance(p, tuple)
        p_name, p_value = p
        print('add_parameter: p_name {},{}'.format(type(p_name),p_name))
        print('add_parameter: p_value {},{}'.format(type(p_value),p_value))
        assert isinstance( p_name, str )
        assert type(p_value) in [int, float, str, list], 'add_parameter: type error : {},{}'.format(type(p_value), p_value)
        if p_name=='xy':
            # thorough initial position test
            assert isinstance(p_value, list) and len(p_value)==2 and all([isinstance(p_value[i], int) \
                and 0<=p_value[i] for i in range(2)]), 'add_parameter: invalid p_value {}'.format(p_value)
            self.xy=p_value
        else:
            self.config[p_name]=p_value

    def add_behavior( self ):
        self.behaviors.append(Behavior(self.config))

    def behavior_add_parameter( self, p ):
        self.behaviors[-1].add_parameter(p)

    def behavior_add_instruction( self, i ):
        self.behaviors[-1].add_instruction(i)

    def trigger( self, t ):
        pass

    def step(self):
        pass

    def __str__(self):
        return 'Event: '+str(self.__dict__)


class Behavior:

    def __init__(self, cfg):
        self.config=dict(cfg)
        self.instructions=list()

    def add_parameter(self, p):
        if p==None:
            return
        assert isinstance(p, tuple)
        p_name, p_value = p
        print('B.add_parameter: p_name {},{}'.format(type(p_name),p_name))
        print('B.add_parameter: p_value {},{}'.format(type(p_value),p_value))
        assert isinstance( p_name, str )
        assert type(p_value) in [int, float, str, list], 'B.add_parameter: type error : {},{}'.format(type(p_value), p_value)
        if p_name=='xy':
            raise ValueError('unexpected redefinition of parameter "xy"')
        else:
            self.config[p_name]=p_value

    def add_instruction(self):
        pass
    pass
