from Tile import Tile
import math

class TileMap:
    def __init__(self, mapViewWidth, mapViewHeight, mapView):
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

        # Initial tile write
        self.writeTiles(mapView)

        # Initialize player's position
        self.updatePlayerPosition()

    def getTileMapCharAt(self, x, y):
        return self.map[y][x].char

    def updatePlayerPosition(self):
        # Get player's position
        startingPoint = (int(self.mapViewCenter[0]-(self.mapViewWidth/2)),int(self.mapViewCenter[1]-(self.mapViewHeight/2)))
        i = startingPoint[0]
        j = startingPoint[1]
        playerFound = False

        while j < len(self.map) and not playerFound:
            while i < len(self.map[j]) and not playerFound:
                if self.map[j][i].char == '@':
                    playerFound = True
                    self.playerPosition = (i,j)
                i = i + 1
            j = j + 1
            i = startingPoint[0]

    def checkAndHandleMapViewPositionChange(self, mapView):
        # Find player's position in new mapView
        i = 0
        j = 0
        playerFound = False
        playerMapViewPosition = (0,0)

        while j < len(mapView) and not playerFound:
            while i < len(mapView[j]) and not playerFound:
                if mapView[j][i] == '@':
                    playerFound = True
                    playerMapViewPosition = (i,j)
                i = i + 1
            j = j + 1
            i = 0

        # Get player's previous mapViewPositions
        previousPlayerPositionMap = self.playerPosition
        topLeftCornerOfMapView = (int(self.mapViewCenter[0]-(self.mapViewWidth/2)),int(self.mapViewCenter[1]-(self.mapViewHeight/2)))
        previousPlayerPositionMapView = ((previousPlayerPositionMap[0]-topLeftCornerOfMapView[0]), (previousPlayerPositionMap[1]-topLeftCornerOfMapView[1]))

        # Compare current and previous mapViewPositions
        diffMapViewPositions = ((playerMapViewPosition[0]-previousPlayerPositionMapView[0]), (previousPlayerPositionMapView[1]-playerMapViewPosition[1]))

        mapViewShiftRight = diffMapViewPositions[0]>2
        mapViewShiftLeft = diffMapViewPositions[0]<-2
        mapViewShiftUp = diffMapViewPositions[1]<-2
        mapViewShiftDown = diffMapViewPositions[1]>2

        mapViewDiagonalShift = (mapViewShiftRight and mapViewShiftUp) or (mapViewShiftRight and mapViewShiftDown) or (mapViewShiftLeft and mapViewShiftUp) or (mapViewShiftLeft and mapViewShiftDown)
        mapViewVerticalShift = mapViewShiftUp or mapViewShiftDown
        mapViewHorizontalShift = mapViewShiftRight or mapViewShiftLeft

        if mapViewDiagonalShift:
            self.mapViewCenter = (self.mapViewCenter[0] + (diffMapViewPositions[0]), self.mapViewCenter[1] + (diffMapViewPositions[1]))
        elif mapViewVerticalShift:
            self.mapViewCenter = (self.mapViewCenter[0], self.mapViewCenter[1] + (diffMapViewPositions[1]))
        elif mapViewHorizontalShift:
            self.mapViewCenter = (self.mapViewCenter[0] + (diffMapViewPositions[0]), self.mapViewCenter[1])

        print("mapViewCenter = " + str(self.mapViewCenter[0]) + ', ' + str(self.mapViewCenter[1]))
        print("diffMapViewPositions = " + str(diffMapViewPositions[0]) + ', ' + str(diffMapViewPositions[1]))


    def writeTiles(self, mapView):
        # Top left hand corner of mapView from the perspective of self.map (starting point!)
        startingPoint = (int(self.mapViewCenter[0]-(self.mapViewWidth/2)),int(self.mapViewCenter[1]-(self.mapViewHeight/2)))
        mapRowPointer = startingPoint[1]
        mapColPointer = startingPoint[0]

        for line in mapView:
            for char in line:
                self.map[mapRowPointer][mapColPointer] = self.tileDefinitions[str(ord(char))]
                mapColPointer = mapColPointer + 1
            mapColPointer = startingPoint[0]
            mapRowPointer = mapRowPointer + 1

    def print(self):
        for row in self.map:
            for tile in row:
                print(tile.char, end='')
            print()
