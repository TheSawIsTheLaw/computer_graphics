from lab_04.reflection import *
from lab_04.shittyFuncs import *


def middlePointEllipseAlg(xCenter, yCenter, radiusX, radiusY, colour = "#000000"):
    pointsArray = []

    sqrRadX = radiusX * radiusX
    sqrRadY = radiusY * radiusY

    limit = niceRound(radiusX / sqrt(1 + sqrRadY / sqrRadX))

    curX = 0
    curY = radiusY
    pointsArray.append((curX + xCenter, curY + yCenter, colour))

    func = sqrRadY - niceRound(sqrRadX * (radiusY - 1 / 4))
    while curX < limit:
        if func > 0:
            curY -= 1
            func -= sqrRadX * curY * 2

        curX += 1
        func += sqrRadY * (curX + curX + 1)
        pointsArray.append((curX + xCenter, curY + yCenter, colour))

    limit = niceRound(radiusY / sqrt(1 + sqrRadX / sqrRadY))

    curX = radiusX
    curY = 0
    pointsArray.append((curX + xCenter, curY + yCenter, colour))

    func = sqrRadX - niceRound(sqrRadY * (curX - 1 / 4))
    while curY < limit:
        if func > 0:
            curX -= 1
            func -= 2 * sqrRadY * curX

        curY += 1
        func += sqrRadX * (curY + curY + 1)
        pointsArray.append((curX + xCenter, curY + yCenter, colour))

    reflectPointsX(pointsArray, yCenter)
    reflectPointsY(pointsArray, xCenter)

    return pointsArray


def bresenhamEllipseAlg(xCenter, yCenter, radiusX, radiusY, colour = "#000000"):
    pointsArray = []

    curX = 0
    curY = radiusY

    sqrRadX = radiusX * radiusX
    sqrRadY = radiusY * radiusY

    pointsArray.append((curX + xCenter, curY + yCenter, colour))

    delta = sqrRadY - sqrRadX * (radiusY + radiusY + 1)
    while curY > 0:
        if delta <= 0:
            negDek = delta + delta + sqrRadX * (curY + curY - 1)
            curX += 1
            delta += sqrRadY * (curX + curX + 1)
            if negDek >= 0:
                curY -= 1
                delta += sqrRadX * (-curY - curY + 1)
        else:
            posDek = delta + delta + sqrRadY * (-curX - curX - 1)
            curY -= 1
            delta += sqrRadX * (-curY - curY + 1)
            if posDek < 0:
                curX += 1
                delta += sqrRadY * (curX + curX + 1)
        pointsArray.append((curX + xCenter, curY + yCenter, colour))

    reflectPointsY(pointsArray, xCenter)
    reflectPointsX(pointsArray, yCenter)

    return pointsArray


def parameterEllipseAlg(xCenter, yCenter, radiusX, radiusY, colour = "#000000"):
    pointsArray = []

    if radiusX > radiusY:
        step = 1 / radiusX
    else:
        step = 1 / radiusY

    i = 0
    while i <= pi / 2 + step:
        curX = xCenter + radiusX * cos(i)
        curY = yCenter + radiusY * sin(i)
        pointsArray.append((curX, curY, colour))

        i += step

    reflectPointsY(pointsArray, xCenter)
    reflectPointsX(pointsArray, yCenter)
    return pointsArray


def canonicalEllipseAlg(xCenter, yCenter, radiusX, radiusY, colour = "#000000"):
    pointsArray = []

    sqrRadX = radiusX * radiusX
    sqrRadY = radiusY * radiusY
    sqrMix = sqrRadX * sqrRadY

    limitX = niceRound(xCenter + radiusX / sqrt(1 + sqrRadY / sqrRadX))
    limitY = niceRound(yCenter + radiusY / sqrt(1 + sqrRadX / sqrRadY))

    for curX in range(xCenter, limitX):
        curY = yCenter + sqrt(sqrMix - (curX - xCenter) * (curX - xCenter) * sqrRadY) / radiusX
        pointsArray.append((curX, curY, colour))

    for curY in range(limitY, yCenter - 1, -1):
        curX = xCenter + sqrt(sqrMix - (curY - yCenter) * (curY - yCenter) * sqrRadX) / radiusY
        pointsArray.append((curX, curY, colour))

    reflectPointsX(pointsArray, xCenter)
    reflectPointsY(pointsArray, yCenter)
    return pointsArray
