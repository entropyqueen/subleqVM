#
# this is an example file
# those are comments and should be ignored by the asm
#
# The program gets its input from registers r0 and r1
# multiplies them
# store the result in rf
#
# This example file will help us create the basis for the asm
# 

# We'll need at least a .text section for the code
section .text
	
	# if we ommit the third operand, the opcode value
	# shall be directly updated to pc+1
	sbl r2, r0
	sbl r3, r2
	sbl r4, r1
	@loop
		sbl rf, r4
		
		# Substract r3 with the value contained in .data
		# and jmp to 0 (i.e: halt) if r3 == 0 after the sub
		sbl r3, d:one, 0
		# 0 - 0 ==> 0 <=> jmp t:loop
		sbl 0, 0, t:loop

# .data section allows us to have some data loaded in memory
# those shall be directly referencable in other sections
# using the prefix d:
#
# for example, accessing the variable "one":
# 	d:one
section .data
	one = 1

# This program does not require memory
# referencing memory address is done by
# prefixing a value with 'm:'
# 
# for example, accessing first slot of memory:
# 	m:1
section mem
	mem = 0
