import os
import json
import time

class RISC_Net(object):
    """
    Simple 16 bit risc processor simulator
    """

    def __init__(self, memory, clk, pc_offset=0):
        self.clk = clk

        self.r0 = pc_offset # program counter
        self.r1 = 0         # primary accumulator
        self.r2 = 0         # secondary accumulator
        self.r3 = 0         # general purpose
        self.r4 = 0         # general purpose
        self.r5 = 0         # general purpose
        self.r6 = 0         # general purpose
        self.r7 = 0         # i/o port a
        self.r8 = 0         # i/o port b

        self.rflag = []     # flag register
        self.instruction_reg = [] # store current instruction
        self.is_hlt = False

        self.memory_dump = memory
        self.data_line = 0
        self.address_line = 0

        self.rw = 0

    def run(self):

        while True:
            for offset in range(0,2):

                self.address_line = self.r0+offset
                self.rw = 1
                self.memory()

                instruction = self.data_line

                self.instruction_reg = self.decimal_to_binary(instruction)

                time.sleep(1.0/self.clk)

                if offset == 1:
                    self.instruction_reg += self.decimal_to_binary(instruction)

            opcode,mode,op1,op2 = self.decoder()
            self.control_unit(opcode,mode,op1,op2)

            if self.is_hlt:
                with open('memory/memory.data', 'wb') as fileobj:
                    fileobj.write(bytes(json.dumps(self.memory_dump).encode('utf-8')))
                break

    def binary_to_decimal(self, bits):
        decimal_sum = 0
        for i, j in zip(bits[::-1], range(0, len(bits))):
            decimal_sum += i*(2**j)
        return decimal_sum

    def decimal_to_binary(self, decimal):
        bits = []
        data = [x for x in bin(decimal)][2:]
        bits = [int(x) for x in data]
        bits = bits + [0, ]*(16-len(bits))

        return bits

    def get_register_value(self, reg):

        if reg == 0:
            return self.r0
        elif reg == 1:
            return self.r1
        elif reg == 2:
            return self.r2
        elif reg == 3:
            return self.r3
        elif reg == 4:
            return self.r4
        elif reg == 5:
            return self.r5
        elif reg == 6:
            return self.r6
        elif reg == 7:
            return self.r7
        elif reg == 8:
            return self.r8

    def set_register_value(self, reg, value):

        if reg == 0:
            self.r0 = value
        elif reg == 1:
            self.r1 = value
        elif reg == 2:
            self.r2 = value
        elif reg == 3:
            self.r3 = value
        elif reg == 4:
            self.r4 = value
        elif reg == 5:
            self.r5 = value
        elif reg == 6:
            self.r6 = value
        elif reg == 7:
            self.r7 = value
        elif reg == 8:
            self.r8 = value

    def decoder(self):
        opcode = self.binary_to_decimal(self.instruction_reg[0:4])
        mode   = None
        op1    = None
        op2    = None

        if opcode == 0:
            mode = self.binary_to_decimal(self.instruction_reg[4:6])

            if mode == 0:
                reg1 = self.binary_to_decimal(self.instruction_reg[6:10])

                op1 = self.get_register_value(reg1)
                op2 = self.binary_to_decimal(self.instruction_reg[10:14])

            elif mode == 1:
                reg1 = self.binary_to_decimal(self.instruction_reg[6:10])

                # read value from register
                op1 = self.get_register_value(reg1)
                op2 = self.binary_to_decimal(self.instruction_reg[10:26])

            elif mode == 2:
                mem1 = self.binary_to_decimal(self.instruction_reg[6:22])

                # read value from RAM
                self.rw = 1
                self.address_line = mem1
                self.memory()
                op1 = self.data_line
                op2 = self.binary_to_decimal(self.instruction_reg[10:14])

            elif mode == 3:

                op1 = self.binary_to_decimal(self.instruction_reg[6:22])
                op2 = self.binary_to_decimal(self.instruction_reg[22:26])

        if opcode > 0 and opcode < 9:
            mode = self.binary_to_decimal(self.instruction_reg[4:6])

            if mode == 0:
                reg1 = self.binary_to_decimal(self.instruction_reg[6:10])
                reg2 = self.binary_to_decimal(self.instruction_reg[10:14])
                op1 = self.get_register_value(reg1)
                op2 = self.get_register_value(reg2)

            elif mode == 1:
                reg1 = self.binary_to_decimal(self.instruction_reg[6:10])
                mem1 = self.binary_to_decimal(self.instruction_reg[10:26])

                # read value from register
                op1 = self.get_register_value(reg1)

                # read value from RAM
                self.rw = 1
                self.address_line = mem1
                self.memory()
                op2 = self.data_line

            elif mode == 2:
                mem1 = self.binary_to_decimal(self.instruction_reg[6:22])
                reg1 = self.binary_to_decimal(self.instruction_reg[22:26])

                # read value from RAM
                self.rw = 1
                self.address_line = mem1
                self.memory()
                op1 = self.data_line

                # read value from register
                op2 = self.get_register_value(reg1)

            elif mode == 3:
                reg1 = self.binary_to_decimal(self.instruction_reg[22:26])

                op1 = self.binary_to_decimal(self.instruction_reg[6:22])
                op2 = self.get_register_value(reg1)

        return opcode, mode, op1, op2

    def memory(self):
        if self.rw == 0:
            self.memory_dump[self.address_line] = self.data_line
        elif self.rw == 1:
            self.data_line = self.memory_dump[self.address_line]

    def control_unit(self, opcode, mode, op1, op2):

        if opcode == 0:
            """
            Mov src dest offset
            """
            if mode == 0:
                self.set_register_value(op1, op2)

            elif mode == 1:
                self.rw = 0
                self.data_line = op1
                self.address_line = op2
                self.memory()

            elif mode == 2:
                self.set_register_value(op1, op2)
            elif mode == 3:
                self.set_register_value(op1, op2)
            self.r0 += 2

        elif opcode == 1:
            """
            Add mode op1 op2
            """
            self.arithmetic_logic_unit(opcode, op1, op2)
            self.r0 += 2

        elif opcode == 2:
            """
            Sub mode op1 op2
            """
            self.arithmetic_logic_unit(opcode, op1, op2)
            self.r0 += 2

        elif opcode == 3:
            """
            Mul mode op1 op2
            """
            self.arithmetic_logic_unit(opcode, op1, op2)
            self.r0 += 2

        elif opcode == 4:
            """
            Div mode op1 op2
            """
            self.arithmetic_logic_unit(opcode, op1, op2)
            self.r0 += 2

        elif opcode == 5:
            """
            And mode op1 op2
            """
            self.arithmetic_logic_unit(opcode, op1, op2)
            self.r0 += 2

        elif opcode == 6:
            """
            Or mode op1 op2
            """
            self.arithmetic_logic_unit(opcode, op1, op2)
            self.r0 += 2

        elif opcode == 7:
            """
            Not mode op1 op2
            """
            self.arithmetic_logic_unit(opcode, op1, op2)
            self.r0 += 2

        elif opcode == 8:
            """
            Comp dest op1 op2
            """
            self.arithmetic_logic_unit(opcode, op1, op2)
            self.r0 += 2
            
        elif opcode == 9:
            """
            Jump mem_addr
            """
            self.r0 = op1

        elif opcode == 10:
            """
            JumpEq mem_addr
            """
            if self.rflag[0] == 1:
                self.r0 = op1
        elif opcode == 11:
            """
            JumpLT mem_addr
            """
            if self.rflag[1] == 1:
                self.r0 = op1

        elif opcode == 12:
            """
            Hlt
            """
            self.is_hlt = True

    def arithmetic_logic_unit(self, opcode, op1, op2):
        if opcode == 1:
            """
            Add mode op1 op2
            """
            self.r1 = op1 + op2

        elif opcode == 2:
            """
            Sub mode op1 op2
            """
            self.r1 = op1 - op2

        elif opcode == 3:
            """
            Mul mode op1 op2
            """
            result = op1 * op2

            self.r1 = result & 0x00ff
            self.r2 = result >> 8

        elif opcode == 4:
            """
            Div mode op1 op2
            """
            self.r1 = op1 // op2
            self.r2 = op1 % op2
        elif opcode == 5:
            """
            And mode op1 op2
            """
            self.r1 = op1 & op2

        elif opcode == 6:
            """
            Or mode op1 op2
            """
            self.r1 = op1 | op2

        elif opcode == 7:
            """
            Not mode op1 nul
            """
            self.r1 = ~ op1

        elif opcode == 8:
            """
            Comp dest op1 op2
            """
            if op1 == op2:
                self.rflag[0:2] = [1, 0]
            elif op1 < op2:
                self.rflag[0:2] = [0, 1]
