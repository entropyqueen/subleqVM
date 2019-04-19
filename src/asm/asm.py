#!/usr/bin/env python3

import sys
import pickle

INST_SZ = 128


def pack(*v):
    """Packs value to fit into a word"""
    w = 0
    for i, x in enumerate(v):
        w += INST_SZ**(len(v) - i - 1) * x
    return w


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: %s <source.s> <output.bin>' % sys.argv[0])
        exit()

    print('Debug: loading [%s]' % sys.argv[1])

    prog = {}

    BASE_OFFSET = 0x30      # entrypoint cf bin_file_notes.txt
    SIZE_TEXT = 6 * 3         # Nb of instructions in .text
    SIZE_GAP = 0x10      # this could also be 0

    data = BASE_OFFSET + SIZE_TEXT + SIZE_GAP
    data_one = data

    prog['.text'] = [
        0x12, 0x10, 0x33,        # r2 -= r0
        0x13, 0x12, 0x36,        # r3 -= r2
        0x14, 0x11, 0x39,        # r4 -= r1

        0x1f, 0x14, 0x34,        # rf -= r4 == rf += r1
        0x13, data_one, 0x00,    # r3 -= data['one'] ; jmp 0 if r3<0
        0, 0, 0x39,              # jmp @3
    ]

    prog['.data'] = bytearray(1)
    prog['.data'][0] = 1
    prog['mem'] = 0

    prog['inst_sz'] = INST_SZ

    with open(sys.argv[2], 'wb') as f:
        pickle.dump(prog, f)
