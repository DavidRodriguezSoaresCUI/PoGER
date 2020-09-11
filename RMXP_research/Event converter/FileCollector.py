import pathlib

class FileCollector:
    ''' File collector '''
    def __init__( self, root, debug=False, verbose=False ):
        self.root = root
        assert isinstance(debug, bool)
        self.debug = debug
        self.v  = verbose

        if self.debug:
            print("root : {}".format( self.root ))

    def collect( self, pattern='**/*.*' ):
        files = []

        if isinstance( pattern, list ):
            patterns = pattern
            assert 0 < len(patterns)
            for p in patterns:
                files.extend( self.collect(p) )
        else:
            if self.debug:
                #print("Collecting files ..")
                print("pattern : '{}'".format(pattern))

            files = [item.resolve() for item in self.root.glob( pattern ) if item.is_file()]

            if self.debug:
                print( "\tFound {} files in {}".format(len(files), self.root) )
                #print("Collecting files OK!")
            elif self.v:
                print( "\t{} : {}".format(pattern, len(files)) )
        return files