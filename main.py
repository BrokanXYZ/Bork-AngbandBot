import os
import time
import sys
from enum import Enum
from TileMap import TileMap
from Terminal import Terminal
from Player import Player
from array import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# User defined vars
characterName = "Bork"
game = "Angband"
gameFont = "Ubuntu Mono"
fontSize = "18"
subWindowRightCols = 50
subWindowRightSplit = 15
subWindowTopRows = 0
subWindowBottomRows = 0
actionDelay = 1

# fixed vars
mapViewLeftOffset = 12
mapViewRightOffset = subWindowRightCols + 1
mapViewBottomOffset = 2
mapViewTopOffset = 1
terminalHeight = 49
terminalWidth = 169
mapViewWidth = terminalWidth - (mapViewLeftOffset + mapViewRightOffset)
mapViewHeight = terminalHeight - (mapViewTopOffset + mapViewBottomOffset)

tileMap = None
player = None
driver = None
terminal = None

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
    el.send_keys(str(subWindowRightCols))
    time.sleep(1)

    el = driver.find_element_by_id("subwindow-right-split")
    el.clear()
    el.send_keys(str(subWindowRightSplit))
    time.sleep(1)

    el = driver.find_element_by_id("subwindow-top")
    el.clear()
    el.send_keys(str(subWindowTopRows))
    time.sleep(1)

    el = driver.find_element_by_id("subwindow-bottom")
    el.clear()
    el.send_keys(str(subWindowBottomRows))
    time.sleep(1)

def playGame():
    driver.find_element_by_id('playbutton').click()
    time.sleep(1)

def setIronmanBirthOptions():
    # Birth options
    terminal.sendInput('=')
    terminal.sendInput('c')
    terminal.sendInput(Keys.ENTER)
    terminal.sendInput('d')
    terminal.sendInput(Keys.ENTER)
    terminal.sendInput(Keys.ESCAPE)

def createCharacter(characterName):
    # Race select
    terminal.sendInput('h')
    terminal.sendInput(Keys.ENTER)

    # Class select
    terminal.sendInput('a')

    # Stat generation select
    terminal.sendInput('a')
    terminal.sendInput(Keys.ENTER)

    # Character name
    terminal.sendInput(Keys.DELETE)
    terminal.sendInput(characterName)
    terminal.sendInput(Keys.ENTER)
    terminal.sendInput('y')
    terminal.sendInput(Keys.ENTER)

def setupSubwindows():
    terminal.sendInput('=')
    terminal.sendInput('w')
    terminal.sendInput(Keys.ARROW_RIGHT)
    terminal.sendInput(Keys.ARROW_DOWN)
    terminal.sendInput(Keys.ARROW_DOWN)
    terminal.sendInput(Keys.ARROW_DOWN)
    terminal.sendInput(Keys.ARROW_DOWN)
    terminal.sendInput(Keys.ARROW_DOWN)
    terminal.sendInput(Keys.ARROW_DOWN)
    terminal.sendInput(Keys.ENTER)
    terminal.sendInput(Keys.ARROW_DOWN)
    terminal.sendInput(Keys.ARROW_DOWN)
    terminal.sendInput(Keys.ARROW_DOWN)
    terminal.sendInput(Keys.ARROW_DOWN)
    terminal.sendInput(Keys.ENTER)
    terminal.sendInput(Keys.ARROW_RIGHT)
    terminal.sendInput(Keys.ARROW_UP)
    terminal.sendInput(Keys.ARROW_UP)
    terminal.sendInput(Keys.ARROW_UP)
    terminal.sendInput(Keys.ARROW_UP)
    terminal.sendInput(Keys.ENTER)
    terminal.sendInput(Keys.ARROW_UP)
    terminal.sendInput(Keys.ARROW_UP)
    terminal.sendInput(Keys.ARROW_UP)
    terminal.sendInput(Keys.ARROW_UP)
    terminal.sendInput(Keys.ARROW_UP)
    terminal.sendInput(Keys.ARROW_UP)
    terminal.sendInput(Keys.ENTER)
    terminal.sendInput(Keys.ESCAPE)
    terminal.sendInput(Keys.ESCAPE)

def printAndFlush(string):
    print(string)
    sys.stdout.flush()

def setupGame():
    global terminal
    global driver

    printAndFlush("\n---------------------- Begin Setup ----------------------\n")

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

    terminalElem = driver.find_element_by_xpath("//div[@id='terminal-container']//div[@class='terminal']")
    terminal = Terminal(terminalElem, driver, terminalWidth, terminalHeight, mapViewTopOffset, mapViewBottomOffset, mapViewLeftOffset, mapViewRightOffset, actionDelay)

    # "Press any key"
    terminal.sendInput(Keys.ENTER)

    profileState = terminal.getProfileState()
    printAndFlush("~ Profile state: " + profileState.name + '\n')

    if profileState.value == ProfileState.NEW_CHARACTER_AFTER_DEATH.value:
        terminal.sendInput('N')
        printAndFlush("~ Creating character...\n")
        createCharacter(characterName)
        printAndFlush("+ Done\n")
    elif profileState.value == ProfileState.NEW_CHARACTER.value:
        printAndFlush("~ Setting ironman birth settings...\n")
        setIronmanBirthOptions()
        printAndFlush("+ Done\n")
        printAndFlush("~ Creating character...\n")
        createCharacter(characterName)
        printAndFlush("+ Done\n")
    elif profileState.value == ProfileState.CHARACTER_ALIVE.value:
        printAndFlush("~ Resuming game\n")
    else:
        printAndFlush("~ Profile state NOT handled!\n")

    #printAndFlush("~ Setting up Subwindows...\n")
    #setupSubwindows()
    #printAndFlush("+ Done\n")

    printAndFlush("\n-------------------- Setup Complete! --------------------\n")

################################# Main #################################

setupGame()

tileMap = TileMap(mapViewWidth, mapViewHeight, terminal.getMapView())
#tileMap.print()

player = Player(tileMap, terminal)

while True:
    tileMap.clearAndUpdateExplorableTiles()
    player.moveTo(tileMap.getClosestExplorableTile())


#userInput = input("Input: ")

#while userInput!='Q':
    #player.move(userInput)
    #tileMap.print()
    #userInput = input("Input: ")

driver.quit()
