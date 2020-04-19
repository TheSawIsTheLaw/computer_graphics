def reflectPointsXY(pointsArray, xCenter, yCenter):
    prevLen = len(pointsArray)
    for i in range(prevLen):
        pointsArray.append((pointsArray[i][1] - yCenter + xCenter, pointsArray[i][0] - xCenter + yCenter,
                            pointsArray[i][2]))


def reflectPointsY(pointsArray, xCenter):
    prevLen = len(pointsArray)
    for i in range(prevLen):
        pointsArray.append((-(pointsArray[i][0] - xCenter) + xCenter, pointsArray[i][1], pointsArray[i][2]))


def reflectPointsX(pointsArray, yCenter):
    prevLen = len(pointsArray)
    for i in range(prevLen):
        pointsArray.append((pointsArray[i][0], -(pointsArray[i][1] - yCenter) + yCenter, pointsArray[i][2]))
