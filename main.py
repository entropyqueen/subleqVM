#!/usr/bin/env python3

from time import sleep
import colorama
import random

class VM:

    def __init__(self, size):
        self.size = size
        self.pc = 0
        self.mem = [0] * size

    def fmt(self, r):
        i, r = r
        a, b = divmod(self.mem[self.pc])

        if i == self.pc:
            s = "[[%s]]" % r
        elif i == a:
            s = "A %d A" % a
        elif i == B:
            s = "B %d B" % b
        else:
            s = str(r)
        return s.ljust(8)

    def dump(self):
        print("".join(map(self.fmt, enumerate(self.mem))))

    def load(self, mem):
        self.mem = mem

    def subleq(self, inst):
        a, b = divmod(inst, self.size)
        assert a < self.size and b < self.size
        aa = self.mem[a]
        bb = self.mem[b]
        self.mem[a] = aa - bb
        if aa <= bb:
            return aa - bb
        return self.pc + 1

    def tick(self):
        self.pc = self.subleq(self.mem[self.pc]) % self.size
        sleep(1)

if __name__ == '__main__':

    vm = VM(16)
    vm.load([random.randrange(0, vm.size**2) for _ in range(vm.size)])
    while True:
        vm.tick()
        vm.dump()
