#!/usr/bin/env python3

from time import sleep
import random
import argparse

import pickle

class VM:

    def __init__(self, size, speed=None):
        self.size = size
        self.pc = 0
        self.mem = [0] * size
        self.speed = speed
        self.debug = False

    ##
    ## Debugging utilities
    ##

    def fmt(self, r):
        i, r = r
        a, b, c = self.decode()

        if i == self.pc:
            s = "[[%s]]" % r
        elif i == a:
            s = "A %d A" % r
        elif i == b:
            s = "B %d B" % r
        elif i == c:
            s = "C %d C" % r
        else:
            s = str(r)
        return s.ljust(10)

    def dump(self):
        print("".join(map(self.fmt, enumerate(self.mem))))

    def dump_init(self):
        print("".join("%-*d" % (10, i) for i in range(16)))

    ##
    ## Program loader utilities
    ##

    def prog_parse_from_file(self, f_name):
        with open(f_name, 'rb') as f:
            x = pickle.load(f)
        return x

    def random_load(self):
        self.mem = [random.randrange(0, vm.size**3) for _ in range(vm.size)]

    def load(self, mem):
        self.mem = mem

    ##
    ## Implementation
    ##

    def decode(self):
        b, c = divmod(self.mem[self.pc], self.size)
        a, b = divmod(b, self.size)
        return a, b, c

    def subleq(self):
        a, b, c = self.decode()
        assert -self.size < a < self.size, "Segmentation fault."

        aa = self.mem[a]
        bb = self.mem[b]

        self.mem[a] = aa - bb
        self.pc = (c if self.mem[a] <= 0 else self.pc + 1) % self.size

        if self.debug:
            print(dict(aa=aa, bb=bb, sub=aa-bb, nxt=pc))

    def tick(self):
        self.subleq()
        if self.speed:
            sleep(self.speed)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='OISC VM implementation using subleq instructions.')
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument('file', metavar='FILE', nargs='?', default=None,
            help='bytecode to load (compiled with asm.py)')
    grp.add_argument('--seed', '-s', metavar='S', default=None,
            help='seed for loading random program')
    args = parser.parse_args()

    vm = VM(16, speed=0.1)

    # Load a program (either from file or random)
    if args.file != None:
        prog = vm.prog_parse_from_file(args.file)
        print("%r" % prog)
        vm.load(prog)
    else:
        random.seed(args.seed)
        vm.random_load()

    # Init display and run.
    vm.dump_init()
    while True:
        vm.dump()
        try:
            vm.tick()
        except AssertionError as e:
            print(e)
            break
