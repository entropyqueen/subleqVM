#!/usr/bin/env python3

import sys
import pickle

R0 = 0x10
R1 = 0x11
R2 = 0x12
R3 = 0x13
R4 = 0x14
R5 = 0x15
R6 = 0x16
R7 = 0x17
R8 = 0x18
R9 = 0x19
RA = 0x1a
RB = 0x1b
RC = 0x1c
RD = 0x1d
RE = 0x1e
RF = 0x1f

SYS_WR = 0x20
SYS_RD = 0x21
SYS_RND = 0x22
SYS_RTC = 0x23

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage: %s <source.s> <output.bin>' % sys.argv[0])
        exit()

    print('Debug: loading [%s]' % sys.argv[1])

    prog = {}

    BASE_OFFSET = 0x30      # entrypoint cf bin_file_notes.txt
    SIZE_TEXT = 13 * 3      # Nb of instructions in .text
    SIZE_GAP = 0x10         # this could also be 0

    data = BASE_OFFSET + SIZE_TEXT + SIZE_GAP
    data_addr = data
    data_len = data + 2
    data_one = data + 1
    data_start = data_addr + 3
    print('.data addr = %s' % hex(data))

    PADDING = 0x00
    prog['.text'] = [
        # init
        R0, R0, 0x33,           # R0 = 0
        R1, R1, 0x36,           # R1 = 0
        R0, data_addr, 0x39,    # R0 -= &Hello World\n"

        0x40, 0x40, 0x3c,       # MEM[PC+5] = 0
        0x40, R0, 0x3f,         # MEM[PC+5] = &"Hello World\n"
        R1, PADDING, 0x42,      # R1 -= str[i]
        SYS_WR, R1, 0x45,       # SYS_WR = str[i]
        SYS_WR, SYS_WR, 0x48,   # SYS_WR = 0
        R1, R1, 0x4b,
        R0, data_one, 0x4e,     # R0 -= 1
        data_len, data_one, 0x0,  # LEN -= 1
        0x0, 0x0, 0x39,

        0x0, 0x0, 0x0
    ]

    prog['.data'] = bytearray(b'%c\x01\x0dHello World!\n' % data_start)
    prog['mem'] = 0

    with open(sys.argv[2], 'wb') as f:
        pickle.dump(prog, f)
