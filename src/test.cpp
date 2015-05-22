/*
 * test.cpp
 *
 *  Created on: Dec 23, 2012
 *      Author: y2k
 */

#include <time.h>
#include <iostream>
#include <unordered_set>
#include <climits>
#include "tangle.h"

int mains() {
  std::cout << "\"a test totest is now futest, in the dollar.\" -noc lipzieg\n\n";

  unsigned long test;
  unsigned long testReversed;
  test = 0b1100100011001000;
  std::cout << test << "\n";
  dnaOut(test); std::cout << "\n";
  testReversed = reverse64(test);
  dnaOut(testReversed); std::cout << "\n";
  return(0);
}
