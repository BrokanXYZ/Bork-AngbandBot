from Tile import Tile
import math
import sys

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
                asciiCode = int(explodedLine[1])
                type = explodedLine[2].strip()
                char = chr(int(asciiCode))
                self.tileDefinitions[asciiCode] = Tile(name, type, asciiCode, char)
        tileDefFile.close()

        # Init map tiles
        mapMultiplier = 3
        self.mapWidth = mapViewWidth*mapMultiplier
        self.mapHeight = mapViewHeight*mapMultiplier
        self.map = [[Tile("unknown grid", "INDESTRUCTABLE_OBSTACLE", 32, ' ') for i in range(self.mapWidth)] for j in range(self.mapHeight)]
        self.origin = (math.floor(self.mapWidth/2),math.floor(self.mapHeight/2))
        self.mapViewCenter = self.origin

        # Initial tile write
        self.writeTiles(mapView)

        # Init explorableTiles
        self.explorableTiles = []

        # Init player's position
        self.playerPosition = self.getPlayerPosition()

    def getTileMapCharAt(self, x, y):
        return self.map[y][x].char

    def getTile(self, x, y):
        return self.map[y][x]

    def getPlayerPosition(self):
        # Get player's position
        startingPoint = (int(self.mapViewCenter[0]-(self.mapViewWidth/2)),int(self.mapViewCenter[1]-(self.mapViewHeight/2)))
        x = startingPoint[0]
        y = startingPoint[1]
        playerPosition = (-1,-1)
        playerFound = False

        while y < (startingPoint[1] + self.mapViewHeight) and not playerFound:
            while x < (startingPoint[0] + self.mapViewWidth) and not playerFound:
                if self.getTileMapCharAt(x, y) == '@':
                    playerFound = True
                    playerPosition = (x,y)
                x = x + 1
            y = y + 1
            x = startingPoint[0]

        return playerPosition

    def getClosestExplorableTile(self):

        if len(self.explorableTiles) == 0:
            raise Exception("There are no more explorable tiles... Bork doesn't know what to do!!")

        playerPosition = self.getPlayerPosition()
        closestExplorableTile = self.explorableTiles[0]
        shortestDistance = self.distance(playerPosition, self.explorableTiles[0])
        i = 1

        while i < len(self.explorableTiles):
            distance = self.distance(playerPosition, self.explorableTiles[i])
            if distance < shortestDistance:
                shortestDistance = distance
                closestExplorableTile = self.explorableTiles[i]
            i = i + 1

        return closestExplorableTile

    # A* Pathfinding Algorithm
    def getPathTo(self, dst):
        # Key: coords
        # Value: (cost, parentCoords)
        openNodes = dict()
        closedNodes = dict()

        path = []
        pathFound = False
        openNodes[self.playerPosition] = (0, None)

        # Determine path
        while not pathFound:
            currentNodeCoords = None
            currentNodeCost = sys.maxsize

            # Get lowest cost open node
            for key, value in openNodes.items():
                coords = key
                cost = value[0]
                if cost < currentNodeCost:
                    currentNodeCost = cost
                    currentNodeCoords = coords

            # Add node to closedNodes and remove from openNodes
            closedNodes[currentNodeCoords] = openNodes[currentNodeCoords]
            del openNodes[currentNodeCoords]

            if currentNodeCoords == dst:
                pathFound = True
            else:
                x = currentNodeCoords[0]
                y = currentNodeCoords[1]

                # Handle neighbors
                neighbors = [(x+1,y),(x+1,y+1),(x+1,y-1),(x-1,y),(x-1,y-1),(x-1,y+1),(x,y+1),(x,y-1)]

                for neighbor in neighbors:
                    neighborTile = self.getTile(neighbor[0], neighbor[1])

                    if neighborTile.type == "INDESTRUCTABLE_OBSTACLE" or neighbor in closedNodes:
                        pass
                    elif neighbor not in openNodes or (neighbor in openNodes and (currentNodeCost+1 < openNodes[neighbor][0])):
                        openNodes[neighbor] = (currentNodeCost+1, currentNodeCoords)

        # Form path
        currentNodeCoords = dst

        while closedNodes[currentNodeCoords][1] != None:
            path.append(currentNodeCoords)
            currentNodeCoords = closedNodes[currentNodeCoords][1]

        return path

    def getNodeCost(self, node, dst):
        return (self.distance(self.playerPosition, node) + self.distance(dst, node))


    def distance(self, src, dst):
        # ** Diagonal moves are the same distance as horizontal or vertical moves **
        xDiff = math.fabs(dst[0]-src[0])
        yDiff = math.fabs(dst[1]-src[1])

        if xDiff > yDiff:
            return xDiff
        else:
            return yDiff

    def updatePlayerPosition(self):
        self.playerPosition = self.getPlayerPosition()

    def clearAndUpdateExplorableTiles(self):
        self.explorableTiles = []

        for i, row in enumerate(self.map):
            for j, tile in enumerate(row):
                if tile.type == "PASSABLE_TERRAIN" or tile.type == "OBJECT" or tile.type == "MONSTER":
                    isAdjToUnexploredTile = False

                    try:
                        if self.map[i+1][j].asciiCode == 32:
                            isAdjToUnexploredTile = True
                        elif self.map[i-1][j].asciiCode == 32:
                            isAdjToUnexploredTile = True
                        elif self.map[i][j+1].asciiCode == 32:
                            isAdjToUnexploredTile = True
                        elif self.map[i][j-1].asciiCode == 32:
                            isAdjToUnexploredTile = True
                        elif self.map[i+1][j+1].asciiCode == 32:
                            isAdjToUnexploredTile = True
                        elif self.map[i+1][j-1].asciiCode == 32:
                            isAdjToUnexploredTile = True
                        elif self.map[i-1][j+1].asciiCode == 32:
                            isAdjToUnexploredTile = True
                        elif self.map[i-1][j-1].asciiCode == 32:
                            isAdjToUnexploredTile = True
                    except IndexError:
                        pass

                    if isAdjToUnexploredTile:
                        x = j
                        y = i
                        self.explorableTiles.append((x,y))

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

        #print("mapViewCenter = " + str(self.mapViewCenter[0]) + ', ' + str(self.mapViewCenter[1]))
        #print("diffMapViewPositions = " + str(diffMapViewPositions[0]) + ', ' + str(diffMapViewPositions[1]))

    def writeTiles(self, mapView):
        # Top left hand corner of mapView from the perspective of self.map (starting point!)
        startingPoint = (int(self.mapViewCenter[0]-(self.mapViewWidth/2)),int(self.mapViewCenter[1]-(self.mapViewHeight/2)))
        mapRowPointer = startingPoint[1]
        mapColPointer = startingPoint[0]

        for line in mapView:
            for char in line:
                self.map[mapRowPointer][mapColPointer] = self.tileDefinitions[ord(char)]
                mapColPointer = mapColPointer + 1
            mapColPointer = startingPoint[0]
            mapRowPointer = mapRowPointer + 1

    def print(self):
        for row in self.map:
            for tile in row:
                print(tile.char, end='')
            print()
