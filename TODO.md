# TODO

## Features
1. Add some syscalls -> write / read
	* add a register which will be populated with stdin ?
	* we can also have control registers for thoses? ==> allowing for blocking reads and controled output

2. syscall rand()
	* provide a random input each tick

3. ASM
	* create a grammar for asm files so that it becomes less of a pain to write
	* using pyparsing would be great

4. Docs

## Debug


## Enhancement

1. improve bytecode format

2. Implement aslr in the loader

3. refactor the loader to another class

4. Change dmp_fmt to take register names instead of memmory @s
	* this also implies to refactor the VM to use those registers instead of the memory
	* Shall we have register separated from the memory ? --> safer but harder to implem

