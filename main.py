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

    def load(self, mem):
        self.mem = mem

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

def s(a, b, c):
    return a * 16**2 + b * 16 + c

if __name__ == '__main__':

    vm = VM(16, speed=0.1)
    if len(sys.argv) > 1:
        random.seed(int(sys.argv[1]))
        vm.load([random.randrange(0, vm.size**3) for _ in range(vm.size)])
    else:
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
        prog[13] = random.randrange(-10, 10)
        prog[14] = random.randrange(-10, 10)

        vm.load(prog)


    vm.dump_init()
    while True:
        vm.dump()
        try:
            vm.tick()
        except AssertionError as e:
            print(e)
            break
