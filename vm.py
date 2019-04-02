#!/usr/bin/env python3

import random
import argparse
import pickle

from termcolor import colored
from time import sleep

class VM:

    DISPLAY_SPACING = 10

    def __init__(self, size, speed=None, verbose=False):
        self.size = size
        self.pc = 0
        self.mem = [0] * size
        self.speed = speed
        self.debug = False
        self.verbose = verbose

    ##
    ## Debugging utilities
    ##

    def fmt(self, r):
        i, r = r
        a, b, c = self.decode()

        if i == self.pc or i == a or i == b or i == c:
            s = str(r).ljust(self.DISPLAY_SPACING - 3)
        else:
            s = str(r).ljust(self.DISPLAY_SPACING)

        if i == self.pc:
            s = colored("PC:%s" % s, 'green')
        elif i == a:
            s = colored("A: %s" % s, 'red')
        elif i == b:
            s = colored("B: %s" % s, 'yellow')
        elif i == c:
            s = colored("C: %s" % s, 'cyan')

        return s

    def dump(self):
        if self.verbose:
            print("".join(map(self.fmt, enumerate(self.mem))))

    def dump_init(self):
        if self.verbose:
            print("".join("%-*d" % (self.DISPLAY_SPACING, i) for i in range(self.size)))

    ##
    ## Program loader utilities
    ##

    def prog_parse_from_file(self, f_name):
        with open(f_name, 'rb') as f:
            x = pickle.load(f)
        return x

    def random_load(self):
        self.mem = [random.randrange(0, vm.size**3) for _ in range(self.size)]

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
    grp.add_argument('--seed', '-s', metavar='SEED', default=None,
            help='seed for loading random program')
    parser.add_argument('--verbose', '-v', action='store_const', default=False, const=True,
            help='be verbose')
    args = parser.parse_args()

    vm = VM(16, speed=0.1, verbose=args.verbose)

    # Load a program (either from file or random)
    if args.file != None:
        prog = vm.prog_parse_from_file(args.file)
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