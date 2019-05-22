
tileDefPath = '../TileDefinitions/tileDefinitions.txt'

tileDefFile = open(tileDefPath, 'r')
tileDefLines = tileDefFile.readlines()


tileCodeCountDict = {}
duplicateIssueExists = False
defCount = 0


for line in tileDefLines:

    if len(line)>1 and line[0]!='#':
        defCount += 1
        asciiCode = (line.split(','))[2]
        # Ascii code is for a comma
        if asciiCode == '':
            asciiCode = 44

        if asciiCode not in tileCodeCountDict:
            tileCodeCountDict[asciiCode] = 1
        else:
            tileCodeCountDict[asciiCode] += 1
            duplicateIssueExists = True

print()
print('There are ' + str(defCount) + ' tile definitions.')
print()

if duplicateIssueExists:
    print('Duplicate ASCII code issue(s) detected...')
    for k, v in tileCodeCountDict.items():
        if v > 1:
            print(str(k) + ' - ' + str(v) + ' duplicates')


tileDefFile.close()
