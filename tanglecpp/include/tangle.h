/*
 * tangle.h
 *
 *  Created on: Dec 23, 2012
 *      Author: y2k
 */

#include <unordered_set>

#ifndef TANGLE_H_
#define TANGLE_H_

//forward declarations

//configure the length that you want the dna to be here
const unsigned int DNA_ORDER = 6;

const unsigned long DNA_LENGTH = 4*DNA_ORDER;

bool getDnaPiece(unsigned long dna, int n);
void entireDnaOut(const unsigned long dna);
void dnaOut(const unsigned long dna);
int winding(const unsigned long dna);
void move(bool vertical, bool positive, int &x, int &y);
void turn(bool &vertical, bool &positive, bool turn);
bool returnToOrigin(const unsigned long dna);
bool un_crossed(const unsigned long dna);

unsigned long rotate_dna_left(const unsigned long dna, int n);
unsigned long maximize_dna(const unsigned long dna);
bool unique_in_plane(const unsigned long dna, std::unordered_set<unsigned long> &seen );
bool unique_free(const unsigned long dna, std::unordered_set<unsigned long> &seen );

unsigned long reverse64(unsigned long b);


#endif /* TANGLE_H_ */
