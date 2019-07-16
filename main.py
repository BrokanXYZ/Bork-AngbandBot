import os
import time
from TileMap import TileMap
from Tile import Tile
from array import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



game = 'angband'
game_font = 'monospace'
game_font_size = '16px'
subwindows = '4'
characterName = 'Bork'
startNewGame = False

mapViewWidth = 77
mapViewHeight = 20
mapViewLeftOffset = 14
mapViewTopOffset = 1

############################ Function Defs ############################

def configDriver():
    driver.implicitly_wait(10)
    driver.maximize_window()


def login():
    username = driver.find_element_by_name('username')
    username.send_keys(os.environ['USERNAME'])
    password = driver.find_element_by_name('password')
    password.send_keys(os.environ['PASSWORD'])
    enter = driver.find_element_by_name('name')
    enter.click()
    time.sleep(1)


def deleteProfile():
    deleteButton = driver.find_element_by_id('deletebutton')
    deleteButton.click()
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(3)


def checkProfileCleanliness():
    deleteButton = driver.find_element_by_id('deletebutton')
    if deleteButton.is_displayed():
        return False
    else:
        return True
    time.sleep(1)


def selectGameAndStyleSettings(game, game_font, game_font_size, subwindows):

    el = driver.find_element_by_id('gameselect')
    for option in el.find_elements_by_tag_name('option'):
        if option.get_attribute('value') == game:
            option.click() # select() in earlier versions of webdriver
            break

    el = driver.find_element_by_id('extra-fonts')
    for option in el.find_elements_by_tag_name('option'):
        if option.get_attribute('value') == game_font:
            option.click() # select() in earlier versions of webdriver
            break

    el = driver.find_element_by_id('games-font-size')
    for option in el.find_elements_by_tag_name('option'):
        if option.get_attribute('value') == game_font_size:
            option.click() # select() in earlier versions of webdriver
            break

    el = driver.find_element_by_id('subwindows')
    for option in el.find_elements_by_tag_name('option'):
        if option.get_attribute('value') == subwindows:
            option.click() # select() in earlier versions of webdriver
            break

    driver.find_element_by_id('playbutton').click()
    time.sleep(1)


def createCharacter(characterName):
    # Press any key
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)

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


def getMapView():

    mapView = []

    wholePageText = driver.find_element_by_xpath("//div[@id='terminal-container']//div[@class='terminal']").text
    wholePageTextSplitLines = wholePageText.splitlines()

    linePointer = mapViewTopOffset

    while linePointer < mapViewHeight+mapViewTopOffset :

        line = list(wholePageTextSplitLines[linePointer])

        # Convert ASCII code 183 (A with grave accent) to 46 (Period)
        for i, char in enumerate(line):
            if ord(char)==183:
                line[i]='.'

        line = "".join(line)
        mapView.append(line[mapViewLeftOffset:(mapViewWidth+mapViewLeftOffset-1)])
        linePointer+=1

    return mapView



#######################################################################


driver = webdriver.Chrome()

configDriver()

driver.get("http://www.angband.live")

login()

profileIsClean = checkProfileCleanliness()

if profileIsClean or (not profileIsClean and startNewGame):
    # Create new character
    if not profileIsClean:
        deleteProfile()
    selectGameAndStyleSettings(game, game_font, game_font_size, subwindows)
    terminal = driver.find_element_by_xpath("//div[@id='terminal-container']//div[@class='terminal']")
    createCharacter(characterName)
else:
    # Character could be *dead* or alive
    # ALIVE
    selectGameAndStyleSettings(game, game_font, game_font_size, subwindows)
    terminal = driver.find_element_by_xpath("//div[@id='terminal-container']//div[@class='terminal']")
    # "Press any key"
    terminal.send_keys(Keys.ENTER)
    time.sleep(1)


mapView = getMapView()
#print(*mapView, sep="\n")

map = TileMap(mapViewWidth, mapViewHeight)
map.writeTiles(mapView)
map.print()

# Poll screen

# BEGIN BOT RULE LOOP

# MODES
# A. Descend
# B. Descend
# C. Descend
# D. Descend

# 1. Is there a downstair case visible? YES take it ELSE
# 2. Is there a monster? YES kill it ELSE
# 3. Do you know where to explore? YES explore else
# 4. Find an area to explore then explore
