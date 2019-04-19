# subleqVM
OISC (One Instruction Set Computer) VM using subleq (SUbstract and Branch if Less or EQual) instruction

## Implementation

### VM

This is the virtual machine, it takes a program as parameter or a seed with `-s` to execute random program.

```
usage: vm.py [-h] [--seed SEED] [--memsz SIZE] [--speed SPEED] [--verbose]
             [--dump-fmt DUMP_FMT]
             [FILE] [ARG [ARG ...]]

OISC VM implementation using subleq instructions.

positional arguments:
  FILE                  Bytecode to load (compiled with asm.py)
  ARG                   Arguments that will be passed to the program

optional arguments:
  -h, --help            show this help message and exit
  --seed SEED, -S SEED  Seed for loading random program
  --memsz SIZE, -m SIZE
                        Change the virtual memory size (default is 16)
  --speed SPEED, -s SPEED
                        VM speed (this goes into a sleep, so 0 => fast
  --verbose, -v         Enable verbose messages
  --dump-fmt DUMP_FMT, -d DUMP_FMT
                        List of registers to dump when -v is present exemple:
                        13,14,15
```

Test run wiht mul.bin:
```
python vm.py -m 128 -v -d R0,R1,RF,PC asm/bin/mul.bin 3 5
0x10      0x11      0x1f
3 [B]     5         0          [PC]: 0x30:[0x12,0x10,0x33]
3         5         0          [PC]: 0x33:[0x13,0x12,0x36]
3         5 [B]     0          [PC]: 0x36:[0x14,0x11,0x39]
3         5         0 [A]      [PC]: 0x39:[0x1f,0x14,0x34]
3         5         5          [PC]: 0x3c:[0x13,0x52,0x0]
3         5         5          [PC]: 0x3f:[0x0,0x0,0x39]
3         5         5 [A]      [PC]: 0x39:[0x1f,0x14,0x34]
3         5         10         [PC]: 0x3c:[0x13,0x52,0x0]
3         5         10         [PC]: 0x3f:[0x0,0x0,0x39]
3         5         10 [A]     [PC]: 0x39:[0x1f,0x14,0x34]
3         5         15         [PC]: 0x3c:[0x13,0x52,0x0]
Halted.
```

The program takes input from r0 (addr 16) and r1 (addr 17) and multiply them, then store the result in rf (addr 31).
It also uses a static data from the `.data` section (addr 70), containing the value `1`.

Test run with Hello World:
```
$ python vm.py -m 128 asm/bin/hello_world.bin 
Hello World!
Halted.
```

#### syscall
1. Write (SYS_WR)
  * The VM will print the content of the memory at addr SYS_WR if > 0
2. Read (SYS_RD)
  * still not implemented
3. Rand (SYS_RND)
  * populates SYS_RND with a random value at each tick
4. Real Time Clock (SYS_RTC)
  * Populates SYS_RTC with a time.time() at each tick

### ASM

The ASM is here to help the creation of a program file, still work in progress.


## TODO

see the file [TODO.md](TODO.md)


## Contributions

Do not hesitate to pull request if you have fun ideas
