#!/usr/bin/env python3

from time import sleep
import random
import sys

class VM:

    def __init__(self, size, speed=None):
        self.size = size
        self.pc = 0
        self.mem = [0] * size
        self.speed = speed
        self.debug = False

    def fmt(self, r):
        i, r = r
        a, b = divmod(self.mem[self.pc], self.size)

        if i == self.pc:
            s = "[[%s]]" % r
        elif i == a:
            s = "A %d A" % r
        elif i == b:
            s = "B %d B" % r
        else:
            s = str(r)
        return s.ljust(8)

    def dump(self):
        print("".join(map(self.fmt, enumerate(self.mem))))

    def load(self, mem):
        self.mem = mem

    def subleq(self, inst):
        a, b = divmod(inst, self.size)
        assert -self.size < a < self.size, "Segmentation fault."
        aa = self.mem[a]
        bb = self.mem[b]
        if self.debug:
            print(dict(mem=self.mem[a], aa=aa, bb=bb, sub=aa-bb, nxt=(aa-bb)%16 if aa - bb <= 0 else self.pc + 1))
        self.mem[a] = aa - bb
        if self.mem[a] <= 0:
            return self.mem[a]
        return self.pc + 1

    def tick(self):
        self.pc = self.subleq(self.mem[self.pc]) % self.size
        if self.speed:
            sleep(self.speed)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        random.seed(int(sys.argv[1]))
    vm = VM(16, speed=0.1)
    vm.load([random.randrange(0, vm.size**2) for _ in range(vm.size)])
    while True:
        vm.dump()
        try:
            vm.tick()
        except AssertionError as e:
            print(e)
            break
