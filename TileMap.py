from Tile import Tile
import math

class TileMap:
    def __init__(self, mapViewWidth, mapViewHeight):

        self.mapViewWidth = mapViewWidth
        self.mapViewHeight = mapViewHeight

        # Init tile definitions
        tileDefPath = './TileDefinitions/tileDefinitions.txt'
        tileDefFile = open(tileDefPath, 'r')
        tileDefLines = tileDefFile.readlines()
        self.tileDefinitions = {}

        for line in tileDefLines:
            if len(line)>1 and line[0]!='#':
                explodedLine = line.split(',')
                name = explodedLine[0]
                asciiCode = explodedLine[1]
                tileType = explodedLine[2]
                char = chr(int(asciiCode))
                self.tileDefinitions[asciiCode] = Tile(name, tileType, asciiCode, char)
        tileDefFile.close()

        # Init map tiles
        mapMultiplier = 3
        self.mapWidth = mapViewWidth*mapMultiplier
        self.mapHeight = mapViewHeight*mapMultiplier
        self.map = [[Tile('name','tileType',35,'#') for i in range(self.mapWidth)] for j in range(self.mapHeight)]

        self.origin = (math.floor(self.mapWidth/2),math.floor(self.mapHeight/2))
        self.mapViewCenter = self.origin


    def writeTiles(self, mapView):

        # Top left hand corner of mapView from the perspective of self.map (starting point!)
        startingPoint = (int(self.mapViewCenter[1]-(self.mapViewHeight/2)),int(self.mapViewCenter[0]-(self.mapViewWidth/2)))
        mapRowPointer = startingPoint[0]
        mapColPointer = startingPoint[1]

        for line in mapView:
            for char in line:
                self.map[mapRowPointer][mapColPointer] = self.tileDefinitions[str(ord(char))]
                mapColPointer = mapColPointer + 1
            mapColPointer = startingPoint[1]
            mapRowPointer = mapRowPointer + 1
            

    def print(self):
        for row in self.map:
            for tile in row:
                print(tile.char, end='')
            print()
