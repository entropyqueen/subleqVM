#!/usr/bin/env python3

import sys
import pickle

import random

INST_SZ = 16


def pack(*v):
    """Packs value to fit into a word"""
    w = 0
    for i, x in enumerate(v):
        w += INST_SZ**(len(v) - i - 1) * x
    return w


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: %s <file.s>')

    prog = {}

    prog['.text'] = [
        pack(11, 13, 1),
        pack(12, 11, 2),
        pack(0, 0, 3),
        pack(0, 14, 4),

        pack(15, 0, 5),
        pack(12, 10, 7),
        pack(9, 9, 4),
        pack(0, 0, 0),

        0, 0, 0, 0,
        0, 0, 0, 0,
    ]
    prog['.text'][10] = 1
    prog['.text'][13] = random.randrange(0, 10)
    prog['.text'][14] = random.randrange(0, 10)

    print('len(.text) == %d' % len(prog['.text']))
    prog['.data'] = [b'Hello world\n']
    prog['stack'] = 0

    with open(sys.argv[1], 'wb') as f:
        pickle.dump(prog, f)
