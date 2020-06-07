from math import sin, cos, sqrt


def expFirst(x, z):
    return sin(x) * cos(x)


def expSecond(x, z):
    return sin(x) * cos(z) * cos(x * z)


def expThird(x, z):
    return sqrt(x * x / 3 + z * z)

def expFourth(x, z):
    return abs(x + z)