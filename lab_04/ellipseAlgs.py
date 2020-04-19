from lab_04.reflection import *
from lab_04.shittyFuncs import *


def canonicalEllipseAlg(xCenter, yCenter, radiusX, radiusY, colour = "#000000"):
    pointsArray = []

    sqrRadX = radiusX * radiusX
    sqrRadY = radiusY * radiusY
    sqrMix = sqrRadX * sqrRadY

    limitX = niceRound(xCenter + radiusX / sqrt(1 + sqrRadY / sqrRadX))
    limitY = niceRound(yCenter + radiusY / sqrt(1 + sqrRadX / sqrRadY))

    for curX in range(xCenter, limitX):
        curY = yCenter + sqrt(sqrMix - (curX - xCenter)*(curX - xCenter) * sqrRadY) / radiusX
        pointsArray.append((curX, curY, colour))

    for curY in range(limitY, yCenter - 1, -1):
        curX = xCenter + sqrt(sqrMix - (curY - yCenter)*(curY - yCenter) * sqrRadX) / radiusY
        pointsArray.append((curX, curY, colour))

    reflectPointsX(pointsArray, xCenter)
    reflectPointsY(pointsArray, yCenter)
    return pointsArray