from enum import Enum


class TileType(Enum):
    MONSTER = 1
    OBJECT = 2
    DESTRUCTABLE_OBSTACLE = 3
    INDESTRUCTABLE_OBSTACLE = 4
    PASSABLE_TERRAIN = 5


tilePath = '../TileDefinitions/tileDefinitions.txt'
terrainPath = '../TileDefinitions/OfficialSource/Terrain.txt'
objectPath = '../TileDefinitions/OfficialSource/Object.txt'
monsterBasePath = '../TileDefinitions/OfficialSource/Monster_Base.txt'

tileFile = open(tilePath, 'w')



#### TERRAIN ####

terrainFile = open(terrainPath, 'r')
terrainTxtList = terrainFile.readlines()

tileFile.write('\n')
tileFile.write('#####  Terrain Definitions  #####\n')
tileFile.write('\n')

name = ''
char = ''
asciiCode = 0
type = ''

for line in terrainTxtList:
    if line[:4] == 'name':
        name = line[5:-1]
    elif line[:8] == 'graphics':
        char = line[9]
        asciiCode = ord(char)
        tileFile.write(name + ',' + char + ',' + str(asciiCode) + ',\n')

terrainFile.close()



#### OBJECT ####

objectFile = open(objectPath, 'r')
objectTxtList = objectFile.readlines()

tileFile.write('\n')
tileFile.write('#####  Object Definitions  #####\n')
tileFile.write('\n')

name = ''
char = ''
asciiCode = 0
type = TileType.OBJECT.name

for line in objectTxtList:
    if line[:4] == 'name':
        name = line[5:-1]
    elif line[:8] == 'graphics':
        char = line[9]
        asciiCode = ord(char)
        tileFile.write(name + ',' + char + ',' + str(asciiCode) + ',' + type + '\n')

objectFile.close()



#### MONSTER_BASE ####

monsterBaseFile = open(monsterBasePath, 'r')
monsterBaseTxtList = monsterBaseFile.readlines()

tileFile.write('\n')
tileFile.write('#####  Monster_Base Definitions  #####\n')
tileFile.write('\n')

name = ''
char = ''
asciiCode = 0
type = TileType.MONSTER.name

for line in monsterBaseTxtList:
    if line[:4] == 'name':
        name = line[5:-1]
    elif line[:5] == 'glyph':
        char = line[6]
        asciiCode = ord(char)
        tileFile.write(name + ',' + char + ',' + str(asciiCode) + ',' + type + '\n')

objectFile.close()




tileFile.close()
