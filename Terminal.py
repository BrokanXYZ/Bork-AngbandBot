import time
from enum import Enum

class ProfileState(Enum):
    NEW_CHARACTER = 1
    NEW_CHARACTER_AFTER_DEATH = 2
    CHARACTER_ALIVE = 3

class Terminal:
    def __init__(self, terminalElem, webDriver, terminalWidth, terminalHeight, mapViewTopOffset, mapViewBottomOffset, mapViewLeftOffset, mapViewRightOffset, actionDelay):
        self.terminalElem = terminalElem
        self.webDriver = webDriver
        self.terminalWidth = terminalWidth
        self.terminalHeight = terminalHeight
        self.mapViewTopOffset = mapViewTopOffset
        self.mapViewBottomOffset = mapViewBottomOffset
        self.mapViewLeftOffset = mapViewLeftOffset
        self.mapViewRightOffset = mapViewRightOffset
        self.actionDelay = actionDelay

    def sendInput(self, key):
        self.terminalElem.send_keys(key)
        time.sleep(self.actionDelay)

    def getAllLines(self):
        allTerminalText = self.webDriver.execute_script("return spyglass[\"default\"].grabText(0,0,0," + str(self.terminalHeight-1) + ")")
        allTerminalLines = allTerminalText.splitlines()
        return allTerminalLines

    def getProfileState(self):
        state = ProfileState.CHARACTER_ALIVE
        newCharAfterDeathStr = "New character based on previous one"

        allTerminalLines = self.getAllLines()
        firstTerminalLine = allTerminalLines[0]

        if(firstTerminalLine[0:len(newCharAfterDeathStr)]==newCharAfterDeathStr):
            state = ProfileState.NEW_CHARACTER_AFTER_DEATH

        return state

    def getMapView(self):
        mapView = []
        allTerminalLines = self.getAllLines()
        linePointer = self.mapViewTopOffset

        while linePointer <  len(allTerminalLines) - self.mapViewBottomOffset:

            line = list(allTerminalLines[linePointer])

            # Convert ASCII code 183 (A with grave accent) to 46 (Period)
            for i, char in enumerate(line):
                if ord(char)==183:
                    line[i]='.'

            # Not all terminal lines are the width of the terminal
            while len(line) < self.terminalWidth:
                line.append(' ')

            line = "".join(line)
            mapViewLine = line[self.mapViewLeftOffset:len(line)-self.mapViewRightOffset]
            mapView.append(mapViewLine)

            linePointer+=1

        return mapView
