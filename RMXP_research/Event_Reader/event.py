debug = True

class Event:

    def __init__(self):
        self.xy=None
        self.config=dict()
        self.behaviors=list()
        self.current_behavior=None
        self.triggered = False
        self.final = False

    def add_parameter( self, p ):
        assert not self.final, 'E.add_parameter: Cannot add parameter to finalized Event.'

        if p==None:
            return
        assert isinstance(p, tuple)
        p_name, p_value = p
        print('add_parameter: p_name {},{}'.format(type(p_name),p_name))
        print('add_parameter: p_value {},{}'.format(type(p_value),p_value))
        assert isinstance( p_name, str )
        assert type(p_value) in [int, float, str, list], 'add_parameter: type error : {},{}'.format(type(p_value), p_value)

        if debug:
            print(f'E:add_parameter : adding parameter {p_name}')

        if p_name=='xy':
            # thorough initial position test
            assert isinstance(p_value, list) and len(p_value)==2 and all([isinstance(p_value[i], int) \
                and 0<=p_value[i] for i in range(2)]), 'add_parameter: invalid p_value {}'.format(p_value)
            self.xy=p_value
        else:
            self.config[p_name]=p_value

    def add_behavior( self ):
        assert not self.final, 'E.add_behavior: Cannot add behavior to finalized Event.'
        if debug:
            print(f'E:add_behavior : adding a behavior')
            
        self.behaviors.append(Behavior(self.config))

    def behavior_add_parameter( self, p ):
        self.behaviors[-1].add_parameter(p)

    def behavior_add_instruction( self, **kwargs ):
        return self.behaviors[-1].add_instruction(**kwargs)

    def choose_behavior(self):
        valid_b = [ idx for idx,b in enumerate(self.behaviors) if b.satisfies_conditions() ]
        assert 0 < len(valid_b), 'E.choose_behavior: no behavior satisfies its conditions'
        self.current_behavior = max(valid_b)

    def finalize_behaviors(self):
        if not self.final:
            for b in self.behaviors:
                b.finalize()
            self.final = True

    def trigger( self, t ):
        assert self.triggered==False, 'E.trigger : Already triggered.'
        tri = self.config.get( 'trigger', None )
        if tri and (tri==t):
            self.triggered = True
            self.finalize_behaviors()
            self.choose_behavior()

    def walk(self):
        pass

    def step(self):
        ''' Perform a step : either walking animation or behavior '''
        if self.triggered:
            self.triggered = self.behaviors[self.current_behavior].step()
        if not self.triggered:
            self.walk()

    def __str__(self):
        return 'Event: '+str(self.__dict__) + '\n'.join([ str(b) for b in self.behaviors ])


class Behavior:

    def __init__(self, cfg):
        self.config=dict(cfg)
        self.conditions=list()
        self.instructions=list()
        self.final = False
        self.tick = 0

    def add_parameter(self, p):
        assert not self.final, 'B.add_parameter: Cannot add parameter to finalized Behavior.'
        # TODO : separate config and conditions

        if p==None:
            return
        assert isinstance(p, tuple)
        p_name, p_value = p
        print('B.add_parameter: p_name {},{}'.format(type(p_name),p_name))
        print('B.add_parameter: p_value {},{}'.format(type(p_value),p_value))
        assert isinstance( p_name, str )
        assert type(p_value) in [int, float, str, list], 'B.add_parameter: type error : {},{}'.format(type(p_value), p_value)

        if debug:
            print(f'B:add_parameter : adding parameter {p_name}')

        if p_name=='xy':
            raise ValueError('unexpected redefinition of parameter "xy"')
        else:
            self.config[p_name]=p_value

    def add_instruction(self, **kwargs):
        assert not self.final, 'B.add_instruction: Cannot add instruction to finalized Behavior.'

        if debug:
            print(f'B:add_instruction : adding instruction')
            for k,v in kwargs.items():
                print(f'B:add_instruction : k={k},v={v}')

        clean = {k:v for k,v in kwargs.items() if v!=None}
        self.instructions.append( clean )
        #self.instructions.append( self.prepare_instruction( i ) )
        return clean

    def prepare_instruction(self,i):
        # prepare isntructions, so they can be passed to exec()
        pass

    def finalize( self ):
        self.final = True
    pass

    def satisfies_conditions(self):
        return all([ exec(cond) for cond in self.conditions ])

    def step(self):
        # implement 
        assert self.final, 'B.step : behavior unfinalized'
        try:
            instr = self.instructions[self.tick]
            # TODO : exec()
        except IndexError:
            self.tick = 0
            return False

        self.tick += 1
        return True

    def __str__(self):
        return str(self.__dict__)
