'''
Created on Dec 12, 2012

@author: y2k
'''

if __name__ == '__main__':
    pass

print('"a worth today is now future, in the dollar." -noc lipzieg')
import itertools as it
import time

timer = time.time()

dnaLength = 16

countWinding = 0
countReturnToOrigin = 0
countUncrossed = 0

N = (0, 1)
S = (0, -1)
E = (1, 0)
W = (-1, 0)
bearingStart = N
xyStart = (0, 0)
class Tangle:
    def __init__(self, xy, bearing, dna):
        self.xy = [xy[0], xy[1]]
        self.bearing = bearing
        self.dna = dna
        self.path = []

        #next move nswe
        self.move = False

        self.SetMove(self.dna[0])
        for turn in self.dna:
            self.Move(turn)
            self.bearing = self.move
            self.SetMove(turn)
            self.path.append(((self.xy[0], self.xy[1]), self.bearing, self.move))

    def SetMove(self, counterClockwise):

        if counterClockwise:
            if self.bearing == N:
                self.move = W
            elif self.bearing == E:
                self.move = N
            elif self.bearing == S:
                self.move = E
            elif self.bearing == W:
                self.move = S
        else:
            if self.bearing == N:
                self.move = E
            elif self.bearing == E:
                self.move = S
            elif self.bearing == S:
                self.move = W
            elif self.bearing == W:
                self.move = N

    def Move(self, counterClockwise):

        self.xy[0] = self.xy[0] + self.bearing[0]  # step in existing direction
        self.xy[1] = self.xy[1] + self.bearing[1]  # step in existing direction
        self.xy[0] = self.xy[0] + self.move[0]  # now step in the new direction
        self.xy[1] = self.xy[1] + self.move[1]  # now step in the new direction

def checkATangle(dna):
    #does it start off right handed
    if dna[0] == False:
        pass
        #return
    #is the winding number equal to exactly positive 1
    global countReturnToOrigin
    global countWinding
    global countUncrossed
    if 2 * dna.count(True) != dnaLength + 4:
        return
    else:
        countWinding += 1

    #does it return home
    bearing = 'N'
    N = 0
    S = 0
    E = 0
    W = 0

    for step in dna:
        if step:
            if bearing == 'N':
                N += 1
                bearing = 'W'
            elif bearing == 'E':
                E += 1
                bearing = 'N'
            elif bearing == 'S':
                S += 1
                bearing = 'E'
            elif bearing == 'W':
                W += 1
                bearing = 'S'
        else:
            if bearing == 'N':
                N += 1
                bearing = 'E'
            elif bearing == 'E':
                E += 1
                bearing = 'S'
            elif bearing == 'S':
                S += 1
                bearing = 'W'
            elif bearing == 'W':
                W += 1
                bearing = 'N'

    if not (E == W and N == S):
        return
    else:
        countReturnToOrigin += 1

    # have they crossed?
    been = set()
    first = True

    aTangle = Tangle(xyStart, bearingStart, dna)
    for step in aTangle.path:
        if step[0] in been:
            return
        else:
            if first != True:
                been.add(step[0])
            first = False

    countUncrossed += 1

    strDNA = ""
    for x in dna:
        if x == True:
            strDNA += "1"
        else:
            strDNA += "0"
    print(strDNA)

    

countTotal = 0
print(dnaLength)
for dna in it.product([True, False], repeat=dnaLength):
    countTotal += 1
    checkATangle(dna)

print('count', countTotal)
print('countWinding', countWinding)
print('countReturnToOrigin', countReturnToOrigin)
print('countUncrossed', countUncrossed)
print('time', time.time() - timer)

