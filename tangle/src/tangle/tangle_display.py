'''
Created on Dec 12, 2012

@author: y2k

Read STDIN or a file and pick out the lines that contain a DNA string
eg:"100101". Process these DNA strings into diagrams that describe
the shape of the tangle:

16 : 1110001001001000
ooooooooooooooooo╱╲ooooooooooooo!
oooooooooooooooo╱oo╲oooooooooooo!
ooooooooooooooo╱o╱╲o╲ooooooooooo!
ooooooooooooooo╲xo╱o╱ooooooooooo!
ooooooooooooooooo╱o╱oooooooooooo!
ooooooooooooooooo╲╱ooooooooooooo!
================================

piping echo will allow you to view custom DNAs:
$ echo 01110001 | python3 /home/PATH/TO/SCRIPT/tangle_display.py

'''

if __name__ == '__main__':
    pass

print('"a pic today is now 1000 words, in the dollar." -nc hawkzieg')

import fileinput

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

        #next move NSWE
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


def printATangle(dna):
    dnaLength = len(dna)
    dnaString = dna
    dna = [bool(int(s[i:i + 1], 2)) for i in range(0, len(s), 1)]
    aTangle = Tangle(xyStart, bearingStart, dna)
    dna = [bool(int(s[i:i + 1], 2)) for i in range(0, len(s), 1)]
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

    
    #do the actual drawing:
    print("")
    print(dnaLength, ":", dnaString)
    
    for row in output:
        strRow = ''.join(row)
        if strRow != 'o' * dnaLength * 2:
            #only print the row if it contains something interesting
            print(strRow)
     
    print("=" * dnaLength * 2)


for line in fileinput.input():
    #read in from STDIN or a file, strings of DNA eg:"100101"
    s = line.strip()
    
    if len(s) == 0: continue #ignore lines of only whitespace
    if len(s.strip("10")) != 0:
        print(s) #print out lines that contain data that isn't DNA
        continue #only let in strings that have only zeros and ones
    
    printATangle(s)
    
    

