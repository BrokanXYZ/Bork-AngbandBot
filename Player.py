from enum import Enum


class PlayerPriority(Enum):
    DESCEND = 1

class PlayerState(Enum):
    IDLE = 1
    ATTACKING = 2
    SEARCHING_FOR_EXIT = 3

class Player:
    def __init__(self, tileMap, terminal):
        self.tileMap = tileMap
        self.terminal = terminal

        self.priority = PlayerPriority.DESCEND
        self.state = PlayerState.IDLE

    def move(self, key):
        if key in ['1','2','3','4','5','6','7','8','9']:
            self.terminal.sendInput(key)

            newMapView = self.terminal.getMapView()
            self.tileMap.checkAndHandleMapViewPositionChange(newMapView)
            self.tileMap.writeTiles(newMapView)
            self.tileMap.updatePlayerPosition()

    def moveTo(self, dst):
        print("Moving from " + str(self.tileMap.getPlayerPosition()) + " to " + str(dst))
        path = self.tileMap.getPathTo(dst)
        print(str(path))

        while len(path) > 0:
            coords = path.pop()
            playerPosition = self.tileMap.getPlayerPosition()
            diff = ((coords[0] - playerPosition[0]), (coords[1] - playerPosition[1]))

            if diff == (1,0):
                self.move('6')
            elif diff == (-1,0):
                self.move('4')
            elif diff == (0,1):
                self.move('2')
            elif diff == (0,-1):
                self.move('8')
            elif diff == (1,1):
                self.move('3')
            elif diff == (-1,-1):
                self.move('7')
            elif diff == (1,-1):
                self.move('9')
            elif diff == (-1,1):
                self.move('1')
            else:
                print("unhandled direction!!")
