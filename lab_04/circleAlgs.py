from lab_04.reflection import *
from math import *

def middlePointCircleAlg(xCenter, yCenter, radius, colour = "#000000"):
    pointsArray = []

    curX = radius
    curY = 0
    pointsArray.append((curX + xCenter, curY + yCenter, colour))

    func = 1 - radius

    while curY < curX:
        curY += 1
        if func > 0:
            curX -= 1
            func -= curX - 2 + curX

        func += curY + curY + 3
        pointsArray.append((curX + xCenter, curY + yCenter, colour))
    reflectPointsXY(pointsArray, xCenter, yCenter)
    reflectPointsY(pointsArray, xCenter)
    reflectPointsX(pointsArray, yCenter)
    return pointsArray


def bresenhamCircleAlg(xCenter, yCenter, radius, colour = "#000000"):
    pointsArray = []

    curX = 0
    curY = radius
    pointsArray.append((curX + xCenter, curY + yCenter, colour))

    delta = 2 - radius - radius
    while curX < curY:
        if delta <= 0:
            d = delta + delta + curY + curY - 1
            curX += 1
            if d >= 0 :
                curY -= 1
                delta += 2 * (curX - curY + 1)
            else:
                delta += curX + curX + 1
        else:
            d = delta - curX + delta - curX - 1
            curY -= 1
            if d < 0:
                curX += 1
                delta += curX + curX - curY - curY + 2
            else:
                delta -= curY + curY - 1
        pointsArray.append((curX + xCenter, curY + yCenter, colour))

    reflectPointsXY(pointsArray, xCenter, yCenter)
    reflectPointsY(pointsArray, xCenter)
    reflectPointsX(pointsArray, yCenter)
    return pointsArray


def parameterCircleAlg(xCenter, yCenter, radius, colour = "#000000"):
    pointsArray = []
    degreeStep = 1 / radius
    i = 0
    while i <= pi / 4 + degreeStep:
        curX = xCenter + radius * cos(i)
        curY = yCenter + radius * sin(i)
        pointsArray.append((curX, curY, colour))
        i += degreeStep

    reflectPointsXY(pointsArray, xCenter, yCenter)
    reflectPointsY(pointsArray, xCenter)
    reflectPointsX(pointsArray, yCenter)
    return pointsArray


def canonicalCircleAlg(xCenter, yCenter, radius, colour = "#000000"):
    pointsArray = []
    sqrRad = radius * radius
    for curX in range(xCenter, round(xCenter + radius / sqrt(2)) + 1):
        curY = yCenter + sqrt(sqrRad - (curX - xCenter) * (curX - xCenter))
        pointsArray.append((curX, curY, colour))
    reflectPointsXY(pointsArray, xCenter, yCenter)
    reflectPointsY(pointsArray, xCenter)
    reflectPointsX(pointsArray, yCenter)
    return pointsArray