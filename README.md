# subleqVM
OISC (One Instruction Set Computer) VM using subleq (SUbstract and Branch if Less or EQual) instruction

## Implementation

### VM

This is the virtual machine, it takes a program as parameter or a seed with `-s` to execute random program.

```
usage: vm.py [-h] [--seed SEED] [--memsz SIZE] [--speed SPEED] [--verbose]
             [--dump-fmt DUMP_FMT]
             [FILE]

OISC VM implementation using subleq instructions.

positional arguments:
  FILE                  Bytecode to load (compiled with asm.py)

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

#### syscall
1. Write
  * The VM will print the last memory word if it is > 0.
2. read
  * still not implemented

### ASM

The ASM is here to help the creation of a program file, still work in progress.


## TODO

see the file [TODO.md](TODO.md)


## Contributions

For any contribution, please create a new branch then pull request

