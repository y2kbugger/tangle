'''
Created on Dec 12, 2012

@author: y2k
'''

if __name__ == '__main__':
    pass

print('"a pic today is now 1000 words, in the dollar." -nc hawkzieg')


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

    aTangle = Tangle(xyStart, bearingStart, dna)

    output = [['o' for x in range(dnaLength * 2)] for x in range(dnaLength * 2)]

    for step in aTangle.path:
        if (step[2] == (0, 1) and step[1] == (1, 0)) | (step[2] == (1, 0) and step[1] == (0, 1)) | (step[2] == (0, -1) and step[1] == (-1, 0)) | (step[2] == (-1, 0) and step[1] == (0, -1)) :
            symbol = '╱'
        else:
            symbol = '╲'

        x = step[0][0] + dnaLength  # this is how to determine the square to draw in from using bearing move and xy om the path history
        y = step[0][1] + dnaLength  # and center the thing
        if step[1][0] == -1:
            x = x - 1
        if step[2][0] == -1:
            x = x - 1

        if step[1][1] == -1:
            y = y - 1
        if step[2][1] == -1:
            y = y - 1

        output[y][-x] = symbol
        output[dnaLength][dnaLength] = 'x'

    for y in output:
        if y == ['o' for x in range(dnaLength * 2)]:
           pass
	# continue
        for x in y:
            print(x, sep='', end='')
        print('!')
    output = [['o' for x in range(dnaLength * 2)] for x in range(dnaLength * 2)]

while True:
    #"enter a string of dna(eg: 100101):  "
    s = input()
    if s == 'q': break
    dnaLength = len(s)
    dna = [bool(int(s[i:i + 1], 2)) for i in range(0, len(s), 1)]
    print("dna:", s)
    print("dnaLength: ", dnaLength)

    checkATangle(dna)
    print("=============================")

