/*
 * main.cpp
 *
 *  Created on: Dec 23, 2012
 *      Author: y2k
 */

#include <time.h>
#include <iostream>
#include <unordered_set>
#include <climits>
#include "tangle.h"

int main() {
  std::cout << "\"a worth today is now future, in the dollar.\" -noc lipzieg\n\n";
  clock_t begin = clock();

  unsigned long dna;
  unsigned long maxdna;
  unsigned long countTotal = 0;
  unsigned long countWinding = 0;
  unsigned long countReturnToOrigin = 0;
  unsigned long countUncrossed = 0;
  unsigned long countUniqueInPlane = 0;
  unsigned long countUniqueFree = 0;

  std::unordered_set<unsigned long> seen;
  std::unordered_set<unsigned long> seenFree;

  std::cout << "DNA_ORDER: " << DNA_ORDER << "\n";
  std::cout << "DNA_LENGTH: " << DNA_LENGTH << "\n";
  std::cout << "Polyominoe perimeter: " << DNA_ORDER * 2 + 2 << "\n";

  //main loop for iterating over every possible combination of left and right turns
  for (dna = 0; (dna+1) <= (((long)1 << (DNA_LENGTH - 1))); ++dna){
    countTotal++;

    if(winding(dna) != -4) continue;
    countWinding++; //std::cout << "winds!\n";
    if(not returnToOrigin(dna)) continue;
    countReturnToOrigin++; //std::cout << "     returns!!\n";
    if(not un_crossed(dna)) continue;
    countUncrossed++; //std::cout << "            uncrossed!!!\n";

    maxdna = maximize_dna(dna);

    if(not unique_in_plane(maxdna, seen)) continue;
    countUniqueInPlane++; //std::cout << "                     uniqueInPlane!!!!\n";
    if(not unique_free(maxdna, seenFree)) continue;
    countUniqueFree++; //std::cout << "                                  uniqueFree!!!!!\n";

    std::cout << "\n";
    dnaOut(maxdna);
    //std::cout << maxdna; this outputs dna as the decimal
  }
  std::cout << "\n";
  std::cout << "\n";
  std::cout << "DNA_ORDER: " << DNA_ORDER << "\n";
  std::cout << "DNA_LENGTH: " << DNA_LENGTH << "\n";
  std::cout << "Polyominoe perimeter: " << DNA_ORDER * 2 + 2 << "\n";
  std::cout << "\n";
  std::cout << "final countTotal: " << countTotal << "\n";
  std::cout << "final countWinding: " << countWinding << "\n";
  std::cout << "final countReturnToOrigin: " << countReturnToOrigin << "\n";
  std::cout << "final countUncrossed: " << countUncrossed << "\n";
  std::cout << "final countUniqueInPlane: " << countUniqueInPlane << "\n";
  std::cout << "final countUniqueFree: " << countUniqueFree << "\n";
  std::cout << "final duration: " << ((double)(clock() - begin) / CLOCKS_PER_SEC) << "\n";
  return(0);
}
