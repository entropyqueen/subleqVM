#!/usr/bin/env python3

import sys
import pickle

import random

def s(*v):
    w = 0
    for i,x in enumerate(v):
        w += 16**(len(v) - i - 1) * x
    return w

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: %s <file.s>')

    prog = [
        s(11, 13, 1),
        s(12, 11, 2),
        s(0, 0, 3),
        s(0, 14, 4),

        s(15, 0, 5),
        s(12, 10, 7),
        s(9, 9, 4),
        s(0, 0, 0),

        0, 0, 0, 0,
        0, 0, 0, 0,
    ]
    prog[10] = 1
    prog[13] = random.randrange(0, 10)
    prog[14] = random.randrange(0, 10)

    with open(sys.argv[1], 'wb') as f:
        pickle.dump(prog, f)
