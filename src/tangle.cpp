/*
 * tangle.cpp
 *
 *  Created on: Dec 20, 2012
 *      Author: y2k
 */

/*
 ============================================================================
 Name        : tangle
 Author      : y2k
 Version     :
 Copyright   : Your copyright notice
 Description : 
 ============================================================================
 */

#include <climits>
#include <iostream>
#include <unordered_set>
#include "tangle.h"


bool getDnaPiece(const unsigned long dna, int n){
//will return the turn at a particular part of the DNA
//the number one needed to be typecast so that shifting bits
//to make the mask would not knock it off the end
//should now work with dna > 30
	return(dna & ((long)1<<(n-1)));
}

//will take a long and output the binary in decimal
void entireDnaOut(const unsigned long dna){
  for (int n = sizeof(dna) * CHAR_BIT; n > 0; --n){
    std::cout << getDnaPiece(dna, n);
  }
}

//output only the relevant segment of dna
void dnaOut(const unsigned long dna){
  for (int n = DNA_LENGTH; n > 0; --n){
    std::cout << getDnaPiece(dna, n);
  }
}

int winding(const unsigned long dna){
  //determine the amount of times that the path makes and complete loop around
  int winding = 0;
  for (unsigned int n = DNA_LENGTH; n > 0; --n){
    if(getDnaPiece(dna, n) == 1){
      winding++;
    } else{
      winding--;
    }
  }
  //std::cout << winding << "\n";
  return(winding);
}

void move(bool vertical, bool positive, int &x, int &y){
  if(vertical){
    if(positive){
      y++;
    }else{
      y--;
		}
  }else{
    if(positive){
      x++;
    }else{
      x--;
    }
  }


//printf("moving to (%d,%d)\n", x, y);
  return;
}

void turn(bool &vertical, bool &positive, bool turn){
  //defines a basis for what direction you will be facing after making a turn
  //based upon your previous direction
  //vertical true is north and south and positive true is north and east
  // turn positive is left or counterclockwise
  positive = (vertical xor (positive xor turn));
  vertical = not vertical;
}

bool returnToOrigin(const unsigned long dna){
  //
  bool vertical = true;
  bool postive = true;
  int x = 0;
  int y = 0;
  for (unsigned int n = DNA_LENGTH; n > 0; --n){
    move(vertical, postive, x, y);
    turn(vertical, postive, getDnaPiece(dna, n));
    move(vertical, postive, x, y);
  }
  if(y==0 and x==0){
    return(true);
  }else{
    return(false);
  }

}

bool un_crossed(const unsigned long dna){
  //do the paths ever cross?
  // let's  walk and mark the path in a 2-d array and check to see if we step on ourselves
  bool vertical = true;
  bool postive = true;
  int x = 0;
  int y = 0;
  bool path[DNA_LENGTH * 2][DNA_LENGTH * 2] = {{false}};
  for (unsigned int n = DNA_LENGTH; n > 0; --n){
    move(vertical, postive, x, y);
    turn(vertical, postive, getDnaPiece(dna, n));
    move(vertical, postive, x, y);

    if(path[x+DNA_LENGTH][y+DNA_LENGTH] == true){
        return(false);
    }else{
        path[x+DNA_LENGTH][y+DNA_LENGTH] = true;
    }
  }
  return(true);
}

unsigned long rotate_dna_left(const unsigned long dna, int n){
//rotate the bits in a barrel fashion              VVV and trim off any that sticks out into a more significant bit
  return ((dna << n) | (dna >> (DNA_LENGTH - n) )) & ~((~(long)0) << DNA_LENGTH);
}


unsigned long maximize_dna(const unsigned long dna){
  unsigned long highest_dna = 0;
  for(unsigned int n = DNA_LENGTH; n>0; n--){
    if(rotate_dna_left(dna,n) > highest_dna) highest_dna = rotate_dna_left(dna,n);
  }
  return highest_dna;
}

bool unique_in_plane(const unsigned long dna, std::unordered_set<unsigned long> &seen ){
  if( seen.count(dna) == 1){
      return false;
  }else{
      seen.insert(dna);
      return true;
  }

}

bool unique_free(const unsigned long dna, std::unordered_set<unsigned long> &seen ){
  if( (seen.count(dna) == 1) or (seen.count(maximize_dna(reverse64(dna))) == 1)){
      return false;
  }else{

      seen.insert(dna);
      return true;
  }

}

unsigned long reverse64(unsigned long b) {
   b = (b & 0xFFFFFFFF00000000) >> 32 | (b & 0x00000000FFFFFFFF) << 32;
   b = (b & 0xFFFF0000FFFF0000) >> 16 | (b & 0x0000FFFF0000FFFF) << 16;
   b = (b & 0xFF00FF00FF00FF00) >>  8 | (b & 0x00FF00FF00FF00FF) <<  8;
   b = (b & 0xF0F0F0F0F0F0F0F0) >>  4 | (b & 0x0F0F0F0F0F0F0F0F) <<  4;
   b = (b & 0xCCCCCCCCCCCCCCCC) >>  2 | (b & 0x3333333333333333) <<  2;
   b = (b & 0xAAAAAAAAAAAAAAAA) >>  1 | (b & 0x5555555555555555) <<  1;

   //slide back down for DNA_length less than 64
   b = b >> (sizeof(b)*CHAR_BIT-DNA_LENGTH);
   return b;
}
