#! /usr/bin/env python3
'''
Created on Dec 12, 2012

@author: y2k

TODO:add docstrings
TODO:seperate the check types because some just waste time for
some algorithms
Todo:when separating out the checks build the counting into outside so as to not slowdown the algorithm.
todo: unit test for results that can be applied separtly from the benchmark runs.
    benchmark --  compared speed
    unittest -- compare accuracy
make the c++ part a library so we can call it from python.

TODO:get rid of class for checking maybe
todo:free object removal (right vs left handed)
todo: make the algorithms use order instead of length /4

'''

if __name__ == '__main__':
    pass

print('"a worth today is now future, in the dollar." -noc lipzieg')
from collections import deque
import itertools as it
import time


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
    ReturnToOrigin = 0
    Winding = 0
    Uncrossed = 0

    #does it start off right handed
    if dna[0] == False:
        pass
        #return ReturnToOrigin, Winding, Uncrossed
    #is the winding number equal to exactly positive 1
    
    
    if 2 * dna.count(True) != len(dna) + 4:
        return None
        return ReturnToOrigin, Winding, Uncrossed

    else:
        Winding += 1

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
        return None
        return ReturnToOrigin, Winding, Uncrossed
    else:
        ReturnToOrigin += 1

    # have they crossed?
    been = set()
    first = True

    aTangle = Tangle(xyStart, bearingStart, dna)
    for step in aTangle.path:
        if step[0] in been:
            return None
            return ReturnToOrigin, Winding, Uncrossed
        else:
            if first != True:
                been.add(step[0])
            first = False

    Uncrossed += 1

    strDNA = ""
    for x in dna:
        if x == True:
            strDNA += "1"
        else:
            strDNA += "0"
    print(strDNA)

    return strDNA 
    return ReturnToOrigin, Winding, Uncrossed


    
def brute(maxdnalength):
    print('Using brute algorithm')
    

    countTotal = 0
    countWinding = 0
    countReturnToOrigin = 0
    countUncrossed = 0

    for i in range(1,maxdnalength+1):
        if i%4 != 0 : continue
        dnas = list()
        for dna in it.product([True, False], repeat=i):
            dna = tuple(maximise(dna))
            if dna not in dnas:
                dnas.append(dna)
                countTotal += 1
                ReturnToOrigin, Winding, Uncrossed = checkATangle(dna)
                countReturnToOrigin += ReturnToOrigin 
                countWinding += Winding
                countUncrossed += Uncrossed


    print('count', countTotal)
    print('countWinding', countWinding)
    print('countReturnToOrigin', countReturnToOrigin)
    print('countUncrossed', countUncrossed)

def dnatoint(x):
    # http://pastebin.com/x1FEP9gY
    y = 0
    for i,j in enumerate(x):
        if j: y += int(j)<<i
    return y

def maximise(dna):
    maxval = 0 
    maxdna = dna
    dnadeque = deque(dna)
    for i in dna: 
        dnadeque.rotate(1)
        val = dnatoint(dnadeque)
        if val>maxval:
            maxval=val
            maxdna = tuple(dnadeque)
    return maxdna
    
def grow(dna, maxdnalength, growndnas=list()):
    for n, item in enumerate(dna):
        growndna = list(dna)
        # replace each piece with 5 pieces that is guareteed to connect
        # this will raise the order of the dna by 1
        # will yield len(dna) new possible dnas to be tested
        growndna[n:n+1] = False, True, True, True, False
        # maximise and deduplicate in situ
        growndna = tuple(maximise(growndna))
        if growndna not in growndnas:
            growndnas.append(growndna)
            yield growndna
            # recurse down up to the maximum chain depth
            if len(growndna)<maxdnalength:
                # print("grown len: {}".format(len(growndnas)))
                yield from grow(growndna, maxdnalength, growndnas)
                # print("grown len after: {}".format(len(growndnas)))


def growing(maxdnalength):
    print('Using growing algorithm')
    countTotal = 1
    countWinding = 0
    countReturnToOrigin = 0
    countUncrossed = 0

    # process the diminuative??? what is the right math word?
    dna = (True, True, True, True)
    checkATangle(dna)
    
    goodDNA = set()
    for newdna in grow(dna, maxdnalength):
        countTotal += 1
        # ReturnToOrigin, Winding, Uncrossed = checkATangle(newdna)
        
        result = checkATangle(newdna) 
        # make sure that the algorythm does not inadvertantly cause dupes
        # # print("resultant dna {}:".format(result))
        # if result is not None:
        #     try:
        #         assert result not in goodDNA
        #     except AssertionError:
        #         print("resultant duplicate dna {}:".format(result))
        #         # raise
        #     goodDNA.add(result)

        
        # countReturnToOrigin += ReturnToOrigin 
        # countWinding += Winding
        # countUncrossed += Uncrossed

    # print('count', countTotal)
    # print('countWinding', countWinding)
    # print('countReturnToOrigin', countReturnToOrigin)
    # print('countUncrossed', countUncrossed)

def main():
    timer = time.time()
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--dnaLength", metavar='N', type=int,
                        help="maximum length to enumerate",
                        default=12)
    parser.add_argument("--alg",  choices=['brute','grow'], default='brute',
                        help="choose which algorythm should be used")
    args = parser.parse_args()

    print("Enumerating tangles up to length {}".format(args.dnaLength))
    if args.alg == 'grow':
        growing(args.dnaLength)
    elif args.alg == 'brute':
        brute(args.dnaLength)
    else:
        print("invalid algorythm choice")

    print('time', time.time() - timer)


if __name__ == '__main__':
    main()
