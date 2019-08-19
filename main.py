import os
import time
import sys
from enum import Enum
from TileMap import TileMap
from Tile import Tile
from array import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



characterName = "Bork"

game = "Angband"
gameFont = "Ubuntu Mono"
fontSize = "18"
subWindowRightCols = "50"
subWindowRightSplit = "15"
subWindowTopRows = "0"
subWindowBottomRows = "0"

mapViewWidth = 77
mapViewHeight = 22
mapViewLeftOffset = 13
mapViewTopOffset = 1

actionDelay = 1

class ProfileState(Enum):
    NEW_CHARACTER = 1
    NEW_CHARACTER_AFTER_DEATH = 2
    CHARACTER_ALIVE = 3

############################ Function Defs ############################

def configDriver():
    driver.implicitly_wait(10)
    driver.maximize_window()

def login():
    username = driver.find_element_by_name("username")
    username.send_keys(os.environ["USERNAME"])
    password = driver.find_element_by_name("password")
    password.send_keys(os.environ["PASSWORD"])
    enter = driver.find_element_by_name("name")
    enter.click()
    time.sleep(1)

def selectSettings(game):
    el = driver.find_element_by_id("gameselect")
    for option in el.find_elements_by_tag_name("option"):
        if option.get_attribute("value") == game:
            option.click()
            break
    time.sleep(1)

    el = driver.find_element_by_id("extra-fonts")
    for option in el.find_elements_by_tag_name("option"):
        if option.get_attribute("value") == gameFont:
            option.click()
            break
    time.sleep(1)

    el = driver.find_element_by_id("games-font-size")
    el.clear()
    el.send_keys(fontSize)
    time.sleep(1)

    el = driver.find_element_by_id("subwindow-right")
    el.clear()
    el.send_keys(subWindowRightCols)
    time.sleep(1)

    el = driver.find_element_by_id("subwindow-right-split")
    el.clear()
    el.send_keys(subWindowRightSplit)
    time.sleep(1)

    el = driver.find_element_by_id("subwindow-top")
    el.clear()
    el.send_keys(subWindowTopRows)
    time.sleep(1)

    el = driver.find_element_by_id("subwindow-bottom")
    el.clear()
    el.send_keys(subWindowBottomRows)
    time.sleep(1)

def playGame():
    driver.find_element_by_id('playbutton').click()
    time.sleep(1)

def setIronmanBirthOptions():
    # Birth options
    terminal.send_keys('=')
    time.sleep(1)
    terminal.send_keys('c')
    time.sleep(1)
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)
    terminal.send_keys('d')
    time.sleep(1)
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)
    terminal.send_keys(Keys.ESCAPE)
    time.sleep(1)

def createCharacter(characterName):
    # Race select
    terminal.send_keys('h')
    time.sleep(1)
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)

    # Class select
    terminal.send_keys('a')
    time.sleep(1)

    # Stat generation select
    terminal.send_keys('a')
    time.sleep(1)
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)

    # Character name
    terminal.send_keys(Keys.DELETE)
    time.sleep(1)
    terminal.send_keys(characterName)
    time.sleep(1)
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)
    terminal.send_keys('y')
    time.sleep(1)
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)

def setupSubwindows():
    terminal.send_keys('=')
    time.sleep(1)
    terminal.send_keys('w')
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_RIGHT)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_RIGHT)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    terminal.send_keys(Keys.ARROW_UP)
    time.sleep(1)
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)
    terminal.send_keys(Keys.ESCAPE)
    time.sleep(1)
    terminal.send_keys(Keys.ESCAPE)
    time.sleep(1)


def getMapView():

    mapView = []

    allTerminalLines = getAllTerminalLines()

    linePointer = 0

    #while linePointer < mapViewHeight+mapViewTopOffset


    return mapView


"""
    blankLine = "                                                                                                                                                                             "
    firstLine = wholePageText[:173]

    if firstLine == blankLine:
        wholePageText = wholePageText[:173] + '\n' + wholePageText[173:]

    wholePageTextSplitLines = wholePageText.splitlines()

    linePointer = mapViewTopOffset
    while linePointer < mapViewHeight+mapViewTopOffset :

        line = list(wholePageTextSplitLines[linePointer])

        # Convert ASCII code 183 (A with grave accent) to 46 (Period)
        for i, char in enumerate(line):
            if ord(char)==183:
                line[i]='.'

        line = "".join(line)
        mapView.append(line[mapViewLeftOffset:(mapViewWidth+mapViewLeftOffset)])
        linePointer+=1

    return mapView
"""

def movePlayer(direction):
    if userInput == '9' or userInput == '8' or userInput == '7' or userInput == '6' or userInput == '5' or userInput == '4' or userInput == '3' or userInput == '2' or userInput == '1':
        terminal.send_keys(userInput)
        time.sleep(actionDelay)
    else:
        print("* Invalid direction *")

def printAndFlush(string):
    print(string)
    sys.stdout.flush()

def getAllTerminalLines():
    wholePageText = driver.find_element_by_xpath("//div[@id='terminal-container']//div[@class='terminal']").text
    wholePageTextSplitLines = wholePageText.splitlines()
    return wholePageTextSplitLines

def getProfileState():
    state = ProfileState.CHARACTER_ALIVE
    newCharAfterDeathStr = "New character based on previous one"

    allTerminalLines = getAllTerminalLines()
    firstTerminalLine = allTerminalLines[0]

    if(firstTerminalLine[0:len(newCharAfterDeathStr)]==newCharAfterDeathStr):
        state = ProfileState.NEW_CHARACTER_AFTER_DEATH

    return state



################################# Main #################################


driver = webdriver.Chrome()

configDriver()
printAndFlush('~ Selenium driver configured.\n')

driver.get("http://www.angband.live")
printAndFlush("~ Navigated to http://www.angband.live\n")

login()
printAndFlush("~ Logged in\n")

printAndFlush("~ Selecting game settings...\n")
selectSettings(game)
printAndFlush("+ Done\n")

printAndFlush("~ Starting game\n")
playGame()

terminal = driver.find_element_by_xpath("//div[@id='terminal-container']//div[@class='terminal']")

# "Press any key"
terminal.send_keys(Keys.ENTER)
time.sleep(actionDelay)

profileState = getProfileState()
printAndFlush("~ Profile state: " + profileState.name + '\n')

if profileState == ProfileState.NEW_CHARACTER_AFTER_DEATH:
    terminal.send_keys('N')
    time.sleep(1)
    printAndFlush("~ Creating character...\n")
    createCharacter(characterName)
    printAndFlush("+ Done\n")
elif profileState == ProfileState.NEW_CHARACTER:
    printAndFlush("~ Setting ironman birth settings...\n")
    setIronmanBirthOptions()
    printAndFlush("+ Done\n")
    printAndFlush("~ Creating character...\n")
    createCharacter(characterName)
    printAndFlush("+ Done\n")
elif profileState == ProfileState.CHARACTER_ALIVE:
    printAndFlush("~ Resuming game\n")
else:
    printAndFlush("~ Profile state NOT handled!\n")

printAndFlush("~ Setting up Subwindows...\n")
setupSubwindows()
printAndFlush("+ Done\n")

#mapView = getMapView()
#print(*mapView, sep="\n")


#driver.quit()



"""
map = TileMap(mapViewWidth, mapViewHeight, mapView)
map.print()

userInput = input("Direction: ")

while userInput!='q':

    movePlayer(userInput)

    mapView = getMapView()

    map.checkAndHandleMapViewPositionChange(mapView)
    map.writeTiles(mapView)
    map.updatePlayerPosition()

    map.print()

    userInput = input("Direction: ")

"""
