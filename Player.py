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
        print("Moving to " + str(dst))
