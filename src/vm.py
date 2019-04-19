#!/usr/bin/env python3

import sys
import random
import argparse
import pickle

from termcolor import colored
from time import sleep, time


class VM:

    SYS_SZ = 0x30
    REGS_START = 0x10
    REGS_END = 0x1f

    MEM_GAP = 0x10

    DISPLAY_SPACING = 10

    REGS = {
        'R0': 0x10,
        'R1': 0x11,
        'R2': 0x12,
        'R3': 0x13,
        'R4': 0x14,
        'R5': 0x15,
        'R6': 0x16,
        'R7': 0x17,
        'R8': 0x18,
        'R9': 0x19,
        'RA': 0x1a,
        'RB': 0x1b,
        'RC': 0x1c,
        'RD': 0x1d,
        'RE': 0x1e,
        'RF': 0x1f,

        'SYS_WR': 0x20,

        'SYS_RDA': 0x21,
        'SYS_RDL': 0x22,
        'SYS_RDC': 0x23,

        'SYS_RND': 0x24,

        'SYS_RTC': 0x25,
    }

    def __init__(self, size, speed=None, verbose=False, dmp_fmt=None):
        self.size = size
        self.pc = 0
        self.mem = [0] * self.size
        self.speed = speed
        self.is_halted = False

        # display
        self.debug = False
        self.verbose = verbose
        self.dump_pc = False
        self.dmp_fmt = self.parse_dump_fmt(dmp_fmt)

    #
    # Debugging utilities
    #
    def parse_dump_fmt(self, s):
        if s is None:
            return range(len(self.mem))
        r = []
        for x in s.split(','):
            if x == 'PC':
                self.dump_pc = True
                continue
            try:
                r.append(int(x, 0))
            except ValueError:
                try:
                    r.append(VM.REGS[x])
                except KeyError as e:
                    print('%r' % e)
        return list(sorted(r))

    def dump(self):
        a, b, c = self.decode()
        text = ''
        if self.verbose:
            for i in self.dmp_fmt:
                label_color_for_i = {
                    a: ('A', 'red'),
                    b: ('B', 'yellow'),
                    c: ('C', 'cyan'),
                }

                try:
                    label, color = label_color_for_i[i]
                except KeyError:
                    tmp = "%d" % self.mem[i]
                    tmp = tmp.ljust(self.DISPLAY_SPACING)
                else:
                    tmp = "%d [%s]" % (self.mem[i], label)
                    tmp = tmp.ljust(self.DISPLAY_SPACING)
                    tmp = colored(tmp, color)
                text += tmp

            if self.dump_pc:
                pc_text = colored('[PC]: %s:[%s]' % (
                    hex(self.pc), ','.join(map(hex, (a, b, c)))), 'green'
                )
            else:
                pc_text = ''

            print('%s %s' % (text, pc_text))

    def dump_init(self):
        if self.verbose:
            print("".join("%-*s" % (
                self.DISPLAY_SPACING, hex(i)
            ) for i in range(self.size) if (
                    self.dmp_fmt is not None and (
                        self.dmp_fmt == 'all' or i in self.dmp_fmt
                    )
                )
            ))

    #
    # Program loader utilities
    #

    def prog_parse_from_file(self, f_name):
        with open(f_name, 'rb') as f:
            x = pickle.load(f)
        return x

    def random_load(self):
        self.mem = [random.randrange(0, vm.size**3) for _ in range(self.size)]

    def load(self, prog, params):
        assert type(prog) == dict, "Program format invalid."
        assert '.text' in prog.keys(), (
                "Program does not contain .text section."
        )

        prog_size = self.SYS_SZ + len(prog['.text'])
        if '.data' in prog.keys():
            prog_size += len(prog['.data']) + self.MEM_GAP
        if 'stack' in prog.keys():
            prog_size += prog['stack'] + self.MEM_GAP

        assert prog_size <= self.size, (
                "Not enough memory to load this program "
                "(at least %s words required)." % prog_size
        )

        # LOAD .text to memory.
        # start @ 0x30 (sys is before that)
        base_text = self.SYS_SZ
        for i, d in enumerate(prog['.text']):
            self.mem[base_text + i] = d

        # LOAD .data after .text
        # (also add GAP because why not.
        base_data = base_text + len(prog['.text']) + self.MEM_GAP
        if '.data' in prog.keys():
            for i, d in enumerate(prog['.data']):
                self.mem[base_data + i] = d

        # mem starts @ base_data + len(prog['.data']) + MEM_GAP

        # LOAD program's arguments
        for i, d in enumerate(params[:0xf]):
            self.mem[self.REGS_START + i] = int(d)

        # if everything loaded properly, we can set PC to the entrypoint:
        self.pc = base_text

    #
    # Implementation
    #

    def decode(self):
        a = self.mem[(self.pc) % self.size]
        b = self.mem[(self.pc + 1) % self.size]
        c = self.mem[(self.pc + 2) % self.size]

        return a, b, c

    def subleq(self):

        a, b, c = self.decode()
        assert -self.size < a < self.size and -self.size < b < self.size, (
            "Segmentation fault."
        )

        aa = self.mem[a]
        bb = self.mem[b]

        self.mem[a] = aa - bb
        self.pc = (c if self.mem[a] <= 0 else self.pc + 3) % self.size

        if self.debug:
            print(dict(aa=aa, bb=bb, sub=aa-bb, nxt=self.pc))

    def sys_write(self):
        # Syscall write
        # Display what is stored at SYS_WR if > 0
        if self.mem[self.REGS['SYS_WR']] > 0:
            print('%s' % chr(self.mem[self.REGS['SYS_WR']] % 127), end='')
            sys.stdout.flush()

    def sys_read(self):
        # Syscall read
        # if SYS_RDC > 0 ; copy SYS_RDL bytes from STDIN to addr in SYS_RDA
        if self.mem[self.REGS['SYS_RDC']] > 0:
            data_in = input()[:self.mem[self.REGS['SYS_RDL']]]
            base = self.mem[self.REGS['SYS_RDA']]

            assert base + len(data_in) < self.size, (
                "Segmentation fault, u broke da memory"
            )
            for i, b in enumerate(data_in):
                if i >= self.mem[self.REGS['SYS_RDL']]:
                    break
                self.mem[base + i] = b

    def sys_rand(self):
        self.mem[self.REGS['SYS_RND']] = random.random()

    def sys_rtc(self):
        self.mem[self.REGS['SYS_RTC']] = time()

    def do_syscalls(self):
        self.sys_rand()
        self.sys_rtc()
        self.sys_write()
        self.sys_read()

    def tick(self):

        self.subleq()

        self.do_syscalls()

        # HALT if PC == 0
        if self.pc == 0:
            self.is_halted = True

        if self.speed:
            sleep(self.speed)

    def run(self):
        while not self.is_halted:
            self.dump()
            self.tick()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
            description='OISC VM implementation using subleq instructions.')
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument('file', metavar='FILE', nargs='?', default=None,
                     help='Bytecode to load (compiled with asm.py)')
    grp.add_argument('--seed', '-S', metavar='SEED', default=None,
                     help='Seed for loading random program')
    parser.add_argument('--memsz', '-m', metavar='SIZE', default=16, type=int,
                        help='Change the virtual memory size (default is 16)')
    parser.add_argument(
            '--speed', '-s', type=float, default=0,
            help='VM speed (this goes into a sleep, so 0 => fast'
    )
    parser.add_argument(
            '--verbose', '-v', action='store_const', default=False,
            required='-d' in sys.argv or '--dump-fmt' in sys.argv,
            const=True, help='Enable verbose messages')
    parser.add_argument(
            '--dump-fmt', '-d', type=str, default=None,
            help='List of memory or register addrs to dump when -v is present.'
            'For exemple: R0,48,0x11,SYS_RTC '
            'Will output R0, values of memory addr 48 '
            '(==entry point), 0x11 (==r1) and SYS_RTC value'
    )
    parser.add_argument(
            'prog_args', metavar='ARG', nargs='*',
            help='Arguments that will be passed to the program'
    )
    args = parser.parse_args()

    vm = VM(args.memsz, speed=args.speed,
            verbose=args.verbose, dmp_fmt=args.dump_fmt)

    # Load a program (either from file or random)
    if args.file is not None:
        try:
            prog = vm.prog_parse_from_file(args.file)
            vm.load(prog, args.prog_args)
        except (AssertionError, FileNotFoundError) as e:
            print(e)
            exit()
    else:
        random.seed(args.seed)
        vm.random_load()

    # Init display and run.
    vm.dump_init()
    try:
        vm.run()
        print('Halted.')
    except AssertionError as e:
        print(e)
