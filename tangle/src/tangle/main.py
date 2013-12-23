'''
Created on Dec 3, 2012

@author: y2k
'''



if __name__ != '__main__':
    exit()

print('"a dollar today is worth now, in the future." -nic leipzig')
import numpy as np
import itertools as it

#double occupancy True, False, False, True, False, False, True, False, False, True, True, False, False, False, True, False, False, False, True
dna = [True, False, False, True, False, False, True, False, False, True, True, False, False, False, True, True, False, False, False, True]
#dna = [True, False, False, True, False, False, True, False, False, True, True, False, False, True, False, False, True, False, False, True]

#dna = [False, False, True, False, True, False]

dnaLength = 8


N = np.array([0, 1])
S = np.array([0, -1])
E = np.array([1, 0])
W = np.array([-1, 0])

bearingStart = N
xyStart = np.array([0, 0])


class Tangle:
    def __init__(self, xy, bearing, dna):
        self.xy = np.array(xy)
        self.bearing = bearing
        self.dna = dna
        self.path = {}

        for turn in dna:
            self.move(turn)

    def move(self, counterClockwise):
        self.path[(self.xy[0], self.xy[1])] = (self.bearing, counterClockwise)


        self.xy += self.bearing


        if counterClockwise:
            if np.array_equiv(self.bearing, N):
                self.bearing = W
            elif np.array_equiv(self.bearing, E):
                self.bearing = N
            elif np.array_equiv(self.bearing, S):
                self.bearing = E
            elif np.array_equiv(self.bearing, W):
                self.bearing = S
        else:
            if np.array_equiv(self.bearing, N):
                self.bearing = E
            elif np.array_equiv(self.bearing, E):
                self.bearing = S
            elif np.array_equiv(self.bearing, S):
                self.bearing = W
            elif np.array_equiv(self.bearing, W):
                self.bearing = N

        self.xy += self.bearing  # now step in the new direction

count = 0

for dna in it.product([True, False], repeat=dnaLength):
    winding = 0
    for i in dna:
        if i:
            winding = winding + 1
        else:
            winding = winding - 1
    print('winding', winding)
    if abs(w) != 4:
        #pass
        continue
    count = count + 1
    aTangle = Tangle(xyStart, bearingStart, dna)

    if np.array_equiv(aTangle.bearing, N):
        bearing = ' N'
    elif np.array_equiv(aTangle.bearing, E):
        bearing = ' E'
    elif np.array_equiv(aTangle.bearing, S):
        bearing = ' S'
    elif np.array_equiv(aTangle.bearing, W):
        bearing = ' W'
        #print(aTangle.xy, bearing)

    if False:
        for y in range(len(dna), -len(dna), -1):
            for x in range(-len(dna), len(dna)):
                if (x, y) in aTangle.path:
                    if aTangle.path[(x, y)][1]:
                        if np.array_equiv(aTangle.path[(x, y)][0], N):
                            print('╮ ', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], E):
                            print('╯ ', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], S):
                            print(' ╰', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], W):
                            print(' ╭', sep='', end='')
                    else:
                        if np.array_equiv(aTangle.path[(x, y)][0], N):
                            print('╭-', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], E):
                            print('-╮', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], S):
                            print('-╯', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], W):
                            print('╰-', sep='', end='')
                else:
                    print('oo', sep='', end='')

            print('!')
    else:
        for y in range(len(dna), -len(dna), -1):
            for x in range(-len(dna), len(dna)):
                if (x, y) in aTangle.path:
                    if aTangle.path[(x, y)][1]:
                        if np.array_equiv(aTangle.path[(x, y)][0], N):
                            print('╲', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], E):
                            print('╱', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], S):
                            print('╲', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], W):
                            print('╱', sep='', end='')
                    else:
                        if np.array_equiv(aTangle.path[(x, y)][0], N):
                            print('╱', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], E):
                            print('╲', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], S):
                            print('╱', sep='', end='')
                        elif np.array_equiv(aTangle.path[(x, y)][0], W):
                            print('╲', sep='', end='')
                else:
                    print('o', sep='', end='')

            print('!')
print("total", 2 ** dnaLength)
print("winding no = +-1", count)
print("winding no != +-1", 2 ** dnaLength - count)
print("% retained by winding", (count) / (2 ** dnaLength))

