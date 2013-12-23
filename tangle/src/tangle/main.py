'''
Created on Dec 3, 2012

@author: y2k
'''

if __name__ != '__main__':
    exit()

print('"a dollar today is worth now, in the future." -nic leipzig')
import itertools as it
import time

from multiprocessing import Pool, Value
from ctypes import c_ulong, c_int
timer = time.time()
N = (0, 1)
S = (0, -1)
E = (1, 0)
W = (-1, 0)

dnaLength = 20
bearingStart = N
xyStart = (0, 0)

countTotal = 0
countWinding = 0
countReturnToOrigin = 0
countUncrossed = 0


class Tangle:
    def __init__(self, xy, bearing, dna):
        self.xy = [xy[0], xy[1]]
        self.bearing = bearing
        self.dna = dna
        self.path = []

        #next move nswe
        self.move = False

        self.SetMove(self.dna[0])
        self.path.append(((self.xy[0], self.xy[1]), self.bearing, self.move))
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
    if dna[0] == False:
        return
    countTotal = 0
    countWinding = 0
    countReturnToOrigin = 0
    countUncrossed = 0

    countTotal += 1
    #verify that winding no = 1
    winding = 0
    for i in dna:
        if i:
            winding = winding + 1
        else:
            winding = winding - 1
    if winding != 4:
        return countTotal, countWinding, countReturnToOrigin, countUncrossed
    else:
        countWinding += 1

    aTangle = Tangle(xyStart, bearingStart, dna)

    # do they return to the origin to complete a circut
    if aTangle.path[-1][0] == xyStart:
        countReturnToOrigin += 1
    else:
        return countTotal, countWinding, countReturnToOrigin, countUncrossed

    # have they crossed?
    been = set()
    first = True
    for step in aTangle.path:
        if step[0] in been:
            return countTotal, countWinding, countReturnToOrigin, countUncrossed
        else:
            if first != True:
                been.add(step[0])
            first = False

    countUncrossed += 1


#generate output
#    output = [['o' for x in range(dnaLength * 2)] for x in range(dnaLength * 2)]
#    for step in aTangle.path:
#        if (step[2] == N and step[1] == E) | (step[2] == E and step[1] == N) | (step[2] == S and step[1] == W) | (step[2] == W and step[1] == S) :
#            symbol = '╱'
#        else:
#            symbol = '╲'
#
#        x = step[0][0] + dnaLength  # this is how to determine the square to draw in from using bearing move and xy om the path history
#        y = step[0][1] + dnaLength  # and center the thing
#        if step[1][0] == -1:
#            x = x - 1
#        if step[2][0] == -1:
#            x = x - 1
#
#        if step[1][1] == -1:
#            y = y - 1
#        if step[2][1] == -1:
#            y = y - 1
#
#        output[y][-x] = symbol
#        output[dnaLength][dnaLength] = 'x'
#    return countTotal, countWinding, countReturnToOrigin, countUncrossed, output



    return countTotal, countWinding, countReturnToOrigin, countUncrossed



pool = Pool(4)
print(dnaLength)
for tangle in pool.imap_unordered(checkATangle, it.product([True, False], repeat=dnaLength), chunksize=50000):
    try:
        countTotal += tangle[0]
        countWinding += tangle[1]
        countReturnToOrigin += tangle[2]
        countUncrossed += tangle[3]
    except TypeError:
        pass

##print output    
#    try:
#        for y in tangle[4]:
#            if y == ['o' for x in range(dnaLength * 2)]:
#                continue
#            for x in y:
#                print(x, sep='', end='')
#            print('!')
#        print('_____')
#    except IndexError:
#        pass

pool.close()
pool.join()


print("countTotal", countTotal)
print("countWinding", countWinding)
print("countReturnToOrigin", countReturnToOrigin)
print("countUncrossed", countUncrossed)
print("Timer", time.time() - timer, 'seconds')
