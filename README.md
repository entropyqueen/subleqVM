# subleqVM
OISC (One Instruction Set Computer) VM using subleq (SUbstract and Branch if Less or EQual) instruction

## Implementation

### VM

This is the virtual machine, it takes a program as parameter or a seed with `-s` to execute random program.

```
usage: vm.py [-h] [--seed SEED] [--memsz SIZE] [--verbose] [FILE]

OISC VM implementation using subleq instructions.

positional arguments:
  FILE                  bytecode to load (compiled with asm.py)

optional arguments:
  -h, --help            show this help message and exit
  --seed SEED, -s SEED  seed for loading random program
  --memsz SIZE, -m SIZE
                        change the virtual memory size (default is 16)
  --verbose, -v         be verbose
```

### ASM

The ASM is here to help the creation of a program file, still work in progress.


## TODO

see the file [TODO.md](TODO.md)


## Contributions

For any contribution, please create a new branch then pull request

