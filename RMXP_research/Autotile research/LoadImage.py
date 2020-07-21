
import codecs, json
import re, os
import pathlib, timeit
from pprint import pprint
from collections import defaultdict

def insureModuleInstalled( module ):
    import sys, importlib
    if isinstance( module, list):
        for m in module:
            insureModuleInstalled( m )
    else:
        try:
            from pip import main as pipmain
        except:
            try:
                from pip._internal import main as pipmain
            except:
                from pip._internal.cli import main as pipmain
        if not (module in sys.modules):
            pipmain(['install', module])
            globals()[module] = importlib.import_module(module)

insureModuleInstalled( ['pandas', 'PIL', 'numpy'] )
import pandas as pd
import numpy as np
from PIL import Image

def clear_screen():
    os.system('cls') if os.name == 'nt' else os.system('clear')

TILESIZE=32
TILESET_ZERO=384
SUBTILESIZE=int(TILESIZE/2)
SUBTILE_BOX={'NW':(0, 0, SUBTILESIZE, SUBTILESIZE),
            'NE':(SUBTILESIZE, 0, TILESIZE, SUBTILESIZE),
            'SE':(SUBTILESIZE, SUBTILESIZE, TILESIZE, TILESIZE),
            'SW':(0, SUBTILESIZE, SUBTILESIZE, TILESIZE)}
SUBTILE_DIRECTIONS=['NW', 'NE', 'SE', 'SW']
SUBTILE_DECODER='AutotileDecode.csv'
GLOBAL_TILE_ACCESSOR_FILE=pathlib.Path('GTA')
GLOBAL_TILE_ACCESSOR=dict()
        

'''class safelist(list):
    def get( self, idx, default ):
        try:
            return self[idx]
        except IndexError:
            return default'''


'''
https://www.pythoninformer.com/python-libraries/pillow/creating-animated-gif/
'''



class SpriteSheetReader:
    
    def __init__(self, imageName):
        self.spritesheet = Image.open(imageName)
        self.nbCellPerCol = int(self.spritesheet.height / TILESIZE)
        self.nbCellPerRow = int(self.spritesheet.width / TILESIZE)
        self.size = self.nbCellPerCol * self.nbCellPerRow
        GLOBAL_TILE_ACCESSOR[imageName] = self
        self.stats=defaultdict(int)
        
    def getTilefromCoordinates(self, tileX, tileY):
        posX = (TILESIZE * tileX)
        posY = (TILESIZE * tileY)
        box = (posX, posY, posX + TILESIZE, posY + TILESIZE)
        return self.spritesheet.crop(box)
        
    def getTilefromID(self, tileID, frame=None):
        (row, col) = divmod(tileID, self.nbCellPerRow)
        self.stats[tileID]+=1
        #print(f'row={row}, col={col}')
        return self.getTilefromCoordinates(col,row)

    def __str__(self):
        return f'SpriteSheet: {self.nbCellPerCol}x{self.nbCellPerRow} cells.'

    def getStats(self):
        return self.stats


    


class AutotileSetReader:
    
    def __init__(self, imageName):
        assert pathlib.Path(imageName).is_file(), f'File {imageName} not found.'
        print(f'Loading Autotile "{imageName}"')
        self.autotileset = Image.open(imageName)
        (width, height) = self.autotileset.size
        # determining autotile format (cell and frame number)
        self.nbCellPerCol = int(height / TILESIZE)
        self.nbFrames = int(width / TILESIZE) if self.nbCellPerCol==1 else int(width / (3*TILESIZE))
        self.nbCellPerRow = int(width / (self.nbFrames*TILESIZE))
        self.nbCellPerFrame = self.nbCellPerCol * self.nbCellPerRow
        self.size = self.nbCellPerCol * self.nbCellPerRow
        self.decoder = self.loadDecoder()
        self.subtiles = self.loadSubtiles() # Indexed (by frameID) list of dictionnaries, each containing subtiles indexed by direction and decoder index
        self.tiles = dict() # dictionary, contains tiles indexed by frameID and tileID
        self.imageName = imageName
        GLOBAL_TILE_ACCESSOR[imageName] = self
        
    
    def __str__(self):
        return f'Autotile: {self.nbCellPerCol}x{self.nbCellPerRow} cells @{self.nbFrames} frames, ' + \
            f'format={self.autotileset.format}, size={self.autotileset.size}' #+', mode={self.spritesheet.mode}'


    def loadDecoder( self ):
        data = pd.read_csv( SUBTILE_DECODER, header=0, index_col=0 )
        assert isinstance(data, pd.DataFrame)
        decoder=[None for _ in range(48)]#deque([], maxlen=48)
        for row in data.itertuples():
            cardinalDir = dict()
            cardinalDir['NW'] = row.NW_subtile_Ax
            cardinalDir['NE'] = row.NE_subtile_Bx
            cardinalDir['SE'] = row.SE_subtile_Cx
            cardinalDir['SW'] = row.SW_subtile_Dx
            decoder[row.Index] = cardinalDir
            
        return decoder


    def loadSubtiles_h( self, frame ):

        subtileDBframe = dict()
        for dir in SUBTILE_DIRECTIONS:
            subtileDBframe[dir] = [None for _ in range(11)]
        for x in range(1,11):
            (tileY, tileX) = divmod(x+1, self.nbCellPerRow)
            tileX += self.nbCellPerRow * frame
            tile = self.getTilefromCoordinates( tileX, tileY )
            for dir in SUBTILE_DIRECTIONS:
                subtile = tile.crop( SUBTILE_BOX[dir] )
                subtileDBframe[dir][x] = subtile
        return subtileDBframe

    def is3x4(self):
        return (self.nbCellPerCol==4 and self.nbCellPerRow==3)

    def is1x1(self):
        return (self.nbCellPerCol==1 and self.nbCellPerRow==1)

    def loadSubtiles(self):
        if self.is3x4():
            subtileDB = [None for _ in range(self.nbFrames)]
            for frame in range(self.nbFrames):
                subtileDB[frame] = self.loadSubtiles_h( frame )
            return subtileDB
        elif self.is1x1():
            return None
        else:
            raise ValueError(f'loadSubtiles@{self.imageName}:Unknown Autotile format (not 4x3 or 1x1)')
        

    def saveSubtiles(self):
        ''' Helper function to insure subtile data is OK by saving each to be observed. '''
        for frame, subtileforframe in enumerate(self.subtiles):
            #iterate as needed to explore every subtile of each frame
            for dir in SUBTILE_DIRECTIONS:
                for idx, subtile in enumerate(subtileforframe[dir]):
                    if subtile:
                        filename=f'SaveSubtiles\\saveSubtiles_frame{frame}_{dir}{idx}.png'
                        subtile.save(filename)
                    else:
                        pass
                        #print(f'saveSubtiles: No subtile for frame={frame}, dir={dir}, idx={idx}')

        
    def getTilefromCoordinates(self, tileX, tileY):
        posX = (TILESIZE * tileX)
        posY = (TILESIZE * tileY)
        box = (posX, posY, posX + TILESIZE, posY + TILESIZE)
        return self.autotileset.crop(box)
        
    def buildTile( self, frame, cardinalDir ):
        ''' Helper function for self.buildTiles
        Builds a tile from 4 subtiles, given a frame ID and cardinal directions IDs
        Returns a tile.
        '''
        #print(f'buildTile: cardinalDir:{type(cardinalDir)}')
        #print(f'buildTile: len(self.subtiles)={len(self.subtiles)}')
        #print(f'buildTile: frame={frame}')
        #print(f'buildTile@{self.imageName}: type(self.subtiles)={type(self.subtiles)}')
        
        newTile = Image.new( "RGBA", (TILESIZE, TILESIZE) )
        for direction in SUBTILE_DIRECTIONS:
            subtile = self.subtiles[frame][direction][cardinalDir[direction]]
            newTile.paste(subtile, SUBTILE_BOX[direction])
        return newTile
        
    def buildTiles( self, frame=0 ):
        ''' Builds a tile database.
        Each tile corresponds to an entry in the decoder, which maps a tile ID to 
        cardinal direction IDs (values) to select the right subtile to use.
        Returns an indexed tile list.
        '''
        print(f'buildTile@{self.imageName}, frame {frame}')
        if self.is1x1():
            return self.getTilefromCoordinates( frame, 0)
        elif self.is3x4():
            tiles = [None for _ in range(len(self.decoder))]
            for idx, cardinalDir in enumerate(self.decoder):
                if not cardinalDir:
                    continue
                tiles[idx] = self.buildTile( frame, cardinalDir )
            return tiles
        raise ValueError(f'buildTiles: Illegal state.')
    
    def getTilefromID(self, tileID, _frame=0):
        ''' Returns the correct tile, given the tileID and frame '''
        frame = _frame % self.nbFrames
        if not self.tiles.get( frame, False ):
            # init self.tiles[frame]
            self.tiles[frame] = self.buildTiles(frame=frame)
        
        if self.is3x4():
            return self.tiles[frame][tileID] 
        elif self.is1x1():
            return self.tiles[frame]
        raise ValueError(f'getTilefromID: Illegal state.')


class ReadMap:
    def __init__(self, mapname):
        with open(f'{mapname}.txt', encoding='utf-8-sig') as f:
            try:
                data = json.load(f)
            except:
                print(f"Invalid JSON file '{mapname}'")
                sys.exit()
            self.map=np.array(data['Table']['data'])
            self.tilesetname=data["Tileset"]
            self.tileset=GLOBAL_TILE_ACCESSOR[self.tilesetname+'.png'] if GLOBAL_TILE_ACCESSOR.get(self.tilesetname+'.png', False) else SpriteSheetReader(self.tilesetname+'.png')
            self.autotilesetnames = [s+'.png' for s in re.split("([A-Z][^A-Z]*)", data["AutoTileset"]) if s]
            self.autotilesets = [GLOBAL_TILE_ACCESSOR[s] if GLOBAL_TILE_ACCESSOR.get(s, False) else AutotileSetReader(s) for s in self.autotilesetnames]

        (self.nbLayers, self.height, self.width) = self.map.shape
        self.nbTiles = self.height * self.width
        self.mapName = mapname
        self.frame = 0
    
    def __str__(self):
        return f'ReadMap: {self.map.shape}, tileset="{self.tileset}" ({self.tileset.size}), ' + \
            f'autotilesets={self.autotilesetnames} ({len(self.autotilesets)})'

    def printMap(self):
        for y in range(self.height):
            print(self.map[y])

    def getTilefromID_h( self, tileID ):
        ''' Helper function for self.getTilefromID
        From absolute tileID, returns a tuple of the tileset and relative tileID
        '''
        if not tileID in range(48, TILESET_ZERO+self.tileset.size):
            #print(f"getTilefromID: tileID out of range : {tileID} !in [48, {TILESET_ZERO+self.tileset.size}).")
            return (None, None)
        if tileID < TILESET_ZERO:
            (div,actualTileID) = divmod( tileID, 48 )
            autotileset_idx = (div)-1
            #print(f'tileID={tileID}, Autotile={autotileset_idx}, idx={mod}')
            return (self.autotilesets[autotileset_idx], actualTileID)
        else:
            #print(f'tileID={tileID}, Tileset, idx={tileID-TILESET_ZERO}')
            return (self.tileset, tileID-TILESET_ZERO)

    def getTilefromID(self, tileID):
        (tileset_reader, actualTileID) = self.getTilefromID_h( tileID )
        return tileset_reader.getTilefromID(actualTileID, self.frame) if tileset_reader else None

    def makePNG_h(self, outImg, n=0, layer=0):
        while n < self.nbTiles:
            (y,x) = divmod(n, self.width)
            tile_id = self.map[layer][y][x]
            tile = self.getTilefromID( tile_id )
            if tile:
                destBox = (x * TILESIZE, y * TILESIZE, (x+1) * TILESIZE, (y+1) * TILESIZE)
                outImg.paste( tile, destBox )
            #print(f'makePNG_h: n={n}, x={x}, y={y}, tile_id={tile_id}')
            n+=1

    def makePNG(self, outFile=None):
        if not outFile:
            outFile = f'{self.mapName}_out.png'
        outImg = Image.new( "RGBA", (self.width*TILESIZE, self.height*TILESIZE), color=(0,0,0,1) )
        self.makePNG_h( outImg )
        outImg.save(outFile)

    def makeLayeredPNG_h( self ):
        layers = [Image.new( "RGBA", (self.width*TILESIZE, self.height*TILESIZE), color=(0,0,0,1) ) for _ in range(3)]
        for i in range(self.nbLayers):
            self.makePNG_h( layers[i], layer=i )
        return layers

    def makeLayeredPNG( self, outFile=None, just_return=False ):
        if not outFile:
            outFile = f'{self.mapName}_out.png'
        layers = self.makeLayeredPNG_h()
        for i,layer in enumerate(layers):
            layer.save( f'layer_{i}.png' )
        for i in range(1,self.nbLayers):
            layers[0].paste( layers[i], (0,0), layers[i] )
        if just_return:
            return layers[0]
        else:
            layers[0].save(outFile)


    def makeGIF( self, outFile=None, FPS=5 ):
        if not outFile:
            outFile = f'{self.mapName}_out.gif'
        images = [None for _ in range(8)]
        for frame in range(8):
            self.frame = frame
            images[frame] = self.makeLayeredPNG( just_return=True )
            #images[frame].save( f'{self.mapName}_frame_{frame}.png' )
        images[0].save(outFile,
               save_all=True,
               append_images=images[1:],
               duration=1000./FPS,
               loop=0)

    def makeSmallerTileset(self):
        tilesetStats = self.tileset.getStats()
        usedTileIDs = [id for id in tilesetStats]
        print(usedTileIDs)
        # Creating a new map
        h = ((len(usedTileIDs)-1) // 8)+1
        print(f'{self.tilesetname}: {len(usedTileIDs)} tiles used, so h={h}')
        outImg = Image.new( "RGBA", (8*TILESIZE, h*TILESIZE), color=(0,0,0,1) )
        newMap = self.map.copy()
        print(type(newMap))
        newID_base=0
        for id in usedTileIDs:
            absoluteID = id+TILESET_ZERO
            newMap[self.map==absoluteID] = newID_base+TILESET_ZERO
            tile = self.tileset.getTilefromID( id )
            if tile:
                (y,x) = divmod(newID_base,8)
                destBox = (x * TILESIZE, y * TILESIZE, (x+1) * TILESIZE, (y+1) * TILESIZE)
                print(f'ID map: {absoluteID}->{newID_base+TILESET_ZERO}, loc={destBox}')
                outImg.paste( tile, destBox )
            newID_base+=1
        newTilesetName=f'{self.mapName}_{self.tilesetname}'
        outImg.save( newTilesetName+'.png' )
        with open(f'{self.mapName}.txt', encoding='utf-8-sig') as f:
            data = json.load(f)
        data['Table']['data']=newMap.tolist()
        data["Tileset"]=newTilesetName
        with open(f'{self.mapName}_compacted.txt', 'w', encoding='utf-8-sig') as f:
            json.dump(data, f)








starttime = timeit.default_timer()
clear_screen()
print('=========================================')
print('=========================================')
mapnames=['Map034']#['Map034_compacted']#['Map031','Map032','Map034']
for mapname in mapnames:
    reader = ReadMap(mapname)
    print(reader)
    #reader.printMap()
    reader.makeGIF()
    #reader.makeSmallerTileset()
print('Done')
'''
reader = AutotileSetReader('Flowers1.png')
print(reader)
for i in range(8):
    tile=reader.getTilefromID(tileID=0, _frame=i)
    tile.save(f'Flowers1_{i}.png')'''

print(f"Execution time : {timeit.default_timer() - starttime} s.")

# Timeit data : Map034           : 18.1s
#               Map034_compacted :  7.1s