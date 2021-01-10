# RISC-Net

## Blocks
- Rigisters
- ALU
- Control Unit
- Memory
 
## Instructions
- Mov  mode src dest

- Add  mode op1 op2
- Sub  mode op1 op2
- Mul  mode op1 op2
- Div  mode op1 op2

- And  mode op1 op2
- Or   mode op1 op2
- Not  mode op1 

- Comp mode op1  op2

- Jump   mem_addr  
- JumpEq mem_addr  
- JumpLT mem_addr  

- Hlt   

## Modes
- 0000 => op1->reg, op2->reg
- 0001 => op1->reg, op2->mem_addr
- 0010 => op1->mem_addr, op2->reg
- 0011 => op1->value, op2->reg

## Instructions width

### Mode 00
- Mov mode reg reg nul\*4 -> 4 2 4 4 0\*18
- Add mode reg reg nul\*4 -> 4 2 4 4 0\*18

### Mode 01
- Mov mode reg mem_addr nul\*4 -> 4 2 4 16 0\*6
- Add mode reg mem_addr nul\*4 -> 4 2 4 16 0\*6 

### Mode 10
- Mov mode mem_addr reg nul\*4 -> 4 2 16 4 0\*6
- Add mode mem_addr reg nul\*4 -> 4 2 16 4 0\*6 

### Mode 11
- Mov mode value reg nul\*4 -> 4 2 16 4 0\*6
- Add mode value reg nul\*4 -> 4 2 16 4 0\*6 

## Registers

- R0 => program counter
- R1 => Primary accumulator
- R2 => Secondary accumulator
- R3 => General purpose
- R4 => General purpose
- R5 => General purpose
- R6 => General purpose
- R7 => I/O Port A
- R8 => I/O Port B 

- RFlag => flag register (3 bits)

## Flag register Map

- Width => 16
- 0 => Zero Flag
- 1 => Less Than Flag
- 2 => Carry Flag

## Assembly guide

#### Mov 
    1. Used to copy data from ram to register, register to register, register to ram and copy values directly to register

##### Addressing Modes
    - direct addressing mode
        mov r3, $100

        r3   - gp register
        $100 - address on RAM
    
    - register addressing mode
    
        mov r5, r4
      
        r5,r4 - gp registers
    
    - imediate addressing mode
        
        mov #17,r4

        17 - decimal value
        r4 - gp register

### Control flow instructions

#### Jmp
    1. Unconditional jump, used to change the program conter value to whatever value we want.

    ##### Addressing Modes
        - direct addressing mode
            jmp $100

            $100 - address on RAM