import random
import tkinter as tk
from tkinter import Canvas
import numpy as np
from PIL import Image, ImageDraw

mapSize = 0

tilesArray = [0, 1, 2, 3, 4]
tileDic = {
    0: [0, 1],
    1: [0, 1, 2, 4],
    2: [1, 2, 3, 4],
    3: [2, 3, 5],
    4: [1, 2, 4],
    5: [3, 5]
}

colorDic = {
    0: "#12660C",
    1: "#86DE33",
    2: "#E0EB2A",
    3: "#099CD6",
    4: "#808080",
    5: "#00008B"
}


def CleanStone(map, line, col, mapSize):
    sandCount = 0
    grassCount = 0

    if line - 1 >= 0:
        if map[line - 1][col][0] == 1:
            grassCount += 1
        elif map[line - 1][col][0] == 2:
            sandCount += 1

    if line + 1 <= mapSize - 1:
        if map[line + 1][col][0] == 1:
            grassCount += 1
        elif map[line + 1][col][0] == 2:
            sandCount += 1

    if col - 1 >= 0:
        if map[line][col - 1][0] == 1:
            grassCount += 1
        elif map[line][col - 1][0] == 2:
            sandCount += 1

    if col + 1 <= mapSize - 1:
        if map[line][col + 1][0] == 1:
            grassCount += 1
        elif map[line][col + 1][0] == 2:
            sandCount += 1

    if grassCount > 2:
        map[line][col][0] = 1
    elif sandCount > 2:
        map[line][col][0] = 2

def CleanOcean(map, line, col, mapSize):
    invalidCount = 0

    if line - 2 >= 0:
        if map[line - 2][col][0] not in [3, 5]:
            invalidCount += 1

    if line + 2 <= mapSize - 1:
        if map[line + 2][col][0] not in [3, 5]:
            invalidCount += 1

    if col - 2 >= 0:
        if map[line][col - 2][0] not in [3, 5]:
            invalidCount += 1

    if col + 2 <= mapSize - 1:
        if map[line][col + 2][0] not in [3, 5]:
            invalidCount += 1

    if line - 1 >= 0 and col - 1 >= 0:
        if map[line - 1][col - 1][0] not in [3, 5]:
            invalidCount += 1

    if line - 1 >= 0 and col + 1 <= mapSize - 1:
        if map[line - 1][col + 1][0] not in [3, 5]:
            invalidCount += 1

    if line + 1 <= mapSize - 1 and col - 1 >= 0:
        if map[line + 1][col - 1][0] not in [3, 5]:
            invalidCount += 1

    if line + 1 <= mapSize - 1 and col + 1 <= mapSize - 1:
        if map[line + 1][col + 1][0] not in [3, 5]:
            invalidCount += 1

    if invalidCount > 0:
        map[line][col][0] = 3

def CleanShallowWater(map, line, col, mapSize):
    deepWaterCount = 0

    if line - 1 >= 0:
        if map[line - 1][col][0] == 5:
            deepWaterCount += 1

    if line + 1 <= mapSize - 1:
        if map[line + 1][col][0] == 5:
            deepWaterCount += 1

    if col - 1 >= 0:
        if map[line][col - 1][0] == 5:
            deepWaterCount += 1

    if col + 1 <= mapSize - 1:
        if map[line][col + 1][0] == 5:
            deepWaterCount += 1
    if deepWaterCount > 3:
        map[line][col][0] = 3

def CleanGrass(map, line, col, mapSize):
    forestCount = 0

    if line - 1 >= 0:
        if map[line - 1][col][0] == 0:
            forestCount += 1

    if line + 1 <= mapSize - 1:
        if map[line + 1][col][0] == 0:
            forestCount += 1

    if col - 1 >= 0:
        if map[line][col - 1][0] == 0:
            forestCount += 1

    if col + 1 <= mapSize - 1:
        if map[line][col + 1][0] == 0:
            forestCount += 1
    if forestCount > 2:
        map[line][col][0] = 0

def CleanSand(map, line, col, mapSize):
    waterCount = 0

    if line - 1 >= 0:
        if map[line - 1][col][0] == 3:
            waterCount += 1

    if line + 1 <= mapSize - 1:
        if map[line + 1][col][0] == 3:
            waterCount += 1

    if col - 1 >= 0:
        if map[line][col - 1][0] == 3:
            waterCount += 1

    if col + 1 <= mapSize - 1:
        if map[line][col + 1][0] == 3:
            waterCount += 1
    if waterCount > 2:
        map[line][col][0] = 3

def GetLine(input, mapSize):
    return int(np.ceil(input / mapSize) - 1)

def GetColumn(input, mapSize):
    returnVal = (input % mapSize) - 1
    if returnVal == -1:
        returnVal = mapSize - 1
    return returnVal

def RemoveTile(tiles):
    allTiles = tilesArray
    tilesToBeRemoved = []
    tilesToSubtract = []

    for i in tiles:
        tilesToSubtract += tileDic.get(i)

    for i in allTiles:
        if i not in tilesToSubtract:
            tilesToBeRemoved.append(i)

    return tilesToBeRemoved


def CollapseLocation(map, line, col, tiles, direction, mapSize):
    if len(tiles) == len(tilesArray):
        return

    tilesToBeRemoved = RemoveTile(tiles)

    if line - 1 >= 0 and direction in [0, 1]:
        if len(map[line - 1][col]) > 1:
            for i in tilesToBeRemoved:
                if i in map[line - 1][col]:
                    map[line - 1][col].remove(i)
            if len(map[line - 1][col]) != len(tilesArray):
                CollapseLocation(map, line - 1, col, map[line - 1][col], 1, mapSize)

    if line + 1 <= mapSize - 1 and direction in [0, 2]:
        if len(map[line + 1][col]) > 1:
            for i in tilesToBeRemoved:
                if i in map[line + 1][col]:
                    map[line + 1][col].remove(i)
            if len(map[line + 1][col]) != len(tilesArray):
                CollapseLocation(map, line + 1, col, map[line + 1][col], 2, mapSize)

    if col - 1 >= 0 and direction in [0, 1, 2, 3]:
        if len(map[line][col - 1]) > 1:
            for i in tilesToBeRemoved:
                if i in map[line][col - 1]:
                    map[line][col - 1].remove(i)
            if len(map[line][col - 1]) != len(tilesArray):
                CollapseLocation(map, line, col - 1, map[line][col - 1], 3, mapSize)

    if col + 1 <= mapSize - 1 and direction in [0, 1, 2, 4]:
        if len(map[line][col + 1]) > 1:
            for i in tilesToBeRemoved:
                if i in map[line][col + 1]:
                    map[line][col + 1].remove(i)
            if len(map[line][col + 1]) != len(tilesArray):
                CollapseLocation(map, line, col + 1, map[line][col + 1], 4, mapSize)

    return map

def RandomizeMap(map, mapSize):
    progressTracker = 0
    progressBar = 0
    randomLocation = random.randint(1, mapSize * mapSize)
    randomTile = random.randint(0, len(tilesArray) - 1)
    randomTile = 1

    for i in range(len(tilesArray)):
        if i != randomTile:
            map[GetLine(randomLocation, mapSize)][GetColumn(randomLocation, mapSize)].remove(i)

    progressTracker += 1
    print("Progress: 0 / 100")

    map = CollapseLocation(map, GetLine(randomLocation, mapSize), GetColumn(randomLocation, mapSize), [randomTile], 0, mapSize)

    whileCon = True

    while whileCon:
        whileCon = False
        minLen = len(tilesArray) + 1
        minLensArray = []

        for idLine, line in enumerate(map):
            for idCol, col in enumerate(line):
                if len(col) < minLen and len(col) != 1:
                    minLensArray.clear()
                    minLen = len(col)
                    minLensArray.append([idLine, idCol])
                elif len(col) == minLen:
                    minLensArray.append([idLine, idCol])

        randomLocationArray = random.choice(minLensArray)

        randomTile = random.choice(map[randomLocationArray[0]][randomLocationArray[1]])

        for i in tilesArray:
            if i in map[randomLocationArray[0]][randomLocationArray[1]] and i != randomTile:
                map[randomLocationArray[0]][randomLocationArray[1]].remove(i)

        progressTracker += 1
        if progressTracker % (mapSize * mapSize / 100) == 0:
            progressBar += 1
            print(f"Progress: {progressBar} / 100")

        map = CollapseLocation(map, randomLocationArray[0], randomLocationArray[1], [randomTile], 0, mapSize)

        for line in map:
            for col in line:
                if len(col) != 1:
                    whileCon = True
                    break
            if whileCon:
                break

def GenerateMap(mapSizeInput, filename):
    mapSize = mapSizeInput

    map = []
    mapchild = []

    for i in range(mapSize):
        for j in range(mapSize):
            mapchild.append(tilesArray.copy())
        map.append(mapchild)
        mapchild = []

    RandomizeMap(map, mapSize)
    window = tk.Tk()
    window.title("Random Map")

    squareSize = 800 / mapSize
    canvas = Canvas(window, height=mapSize * squareSize, width=mapSize * squareSize, cursor="circle")
    canvas.pack()

    color = "red"

    imageToSave = Image.new(mode="RGB", size=(int(mapSize * squareSize), int(mapSize * squareSize)))
    draw = ImageDraw.Draw(imageToSave)

    for i in range(mapSize):
        for j in range(mapSize):

            if map[i][j][0] == 1:
                CleanGrass(map, i, j, mapSize)
            if map[i][j][0] == 2:
                CleanSand(map, i, j, mapSize)
            elif map[i][j][0] == 3:
                CleanShallowWater(map, i, j, mapSize)
            elif map[i][j][0] == 4:
                CleanStone(map, i, j, mapSize)
            elif map[i][j][0] == 5:
                CleanOcean(map, i, j, mapSize)

            color = colorDic.get(map[i][j][0])
            x1 = i * squareSize
            y1 = j * squareSize
            x2 = x1 + squareSize
            y2 = y1 + squareSize
            canvas.create_rectangle((x1, y1, x2, y2), fill=color)
            draw.rectangle((x1, y1, x2, y2), fill=color)

    imageToSave.save(f"Map-Output/{filename}.png")
    window.mainloop()