import sys

import json

# width = 16 bits


class Assembler(object):

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.opcode_map = {"mov": 0, "add": 1, "sub": 2, "mul": 3, "div": 4, "and": 5,
                           "or": 6, "not": 7, "cmp": 9, "jmp": 9, "je": 10, "jle": 11, "hlt": 12}

        self.binary_opcodes = ["mov","add","sub","mul","div","and","or","cmp"]
        self.unary_opcodes = ["not","jmp","je","jle"]


        self.run()

    def run(self):
        program_lines = self.read_file()

        for line in program_lines:
            hex_result = self.encoder(line)
            print(hex_result)

    def read_file(self):
        data = []

        with open(self.input_file, 'r') as fileobj:
            data = fileobj.readlines()

        return data

    def binary_to_decimal(self, bits):
        decimal_sum = 0
        for i, j in zip(bits[::-1], range(0, len(bits))):
            decimal_sum += i*(2**j)
        return decimal_sum

    def decimal_to_binary(self, decimal,pad):
        bits = []
        data = [x for x in bin(decimal)][2:]
        bits = [int(x) for x in data]
        bits = bits + [0, ]*(pad-len(bits))

        return bits

    def get_register_bit(self,reg):

        if reg == "r0":
            return self.decimal_to_binary(0,4)
        elif reg == "r1":
            return self.decimal_to_binary(1,4)
        elif reg == "r2":
            return self.decimal_to_binary(2,4)
        elif reg == "r3":
            return self.decimal_to_binary(3,4)
        elif reg == "r4":
            return self.decimal_to_binary(4,4)
        elif reg == "r5":
            return self.decimal_to_binary(5,4)
        elif reg == "r6":
            return self.decimal_to_binary(6,4)
        elif reg == "r7":
            return self.decimal_to_binary(7,4)
        elif reg == "r8":
            return self.decimal_to_binary(8,4)


    def hex_encoder(self,opcode,op1,op2):
        mode = None
        hex_code = []
        hex_code += self.decimal_to_binary(self.opcode_map[opcode],4)

        if opcode in self.binary_opcodes:
            if op1[0] == "r" and op2[0] == "r":
                hex_code += [0,0]
                hex_code += self.get_register_bit(op1)
                hex_code += self.get_register_bit(op2)
            elif op1[0] == "r" and op2[0] == "$":
                hex_code += [0,1]
                hex_code += self.get_register_bit(op1)
                hex_code += self.decimal_to_binary(op2[1:],16)
            elif op1[0] == "$" and op2[0] == "r":
                hex_code += [1,0]
                hex_code += self.decimal_to_binary(op1[1:],16)
                hex_code += self.get_register_bit(op2)
            elif op1[0] == "#" and op2[0] == "r":
                hex_code += [1,1]
                hex_code += self.decimal_to_binary(op1[1:],16)
                hex_code += self.get_register_bit(op2)

        elif opcode in self.unary_opcodes:
            if opcode == "not":
                if op1[0] == "r":
                    hex_code += [0,0]
                    hex_code += self.get_register_bit(op1)
                elif op1[0] == "$":
                    hex_code += [1,0]
                    hex_code += self.decimal_to_binary(op1[1:],16)
                elif op1[0] == "#":
                    hex_code += [1,1]
                    hex_code += self.decimal_to_binary(op1[1:],16)
            else:
                hex_code += self.decimal_to_binary(op1[1:],16)

        hex_code = hex_code + [0, ]*(32-len(hex_code))

        return hex_code

    def encoder(self, line):
        instruction = line.replace(",","").split(" ")
        op1 = None
        op2 = None
        opcode = instruction[0]
        print(f'opcode = {opcode}')
        if opcode in self.binary_opcodes:
            op1 = instruction[1]
            # print(f'op1 = {op1}')
            op2 = instruction[2]
            # print(f'op2 = {op2}')
        elif opcode in self.unary_opcodes:
            op1 = instruction[1]
            # print(f'op1 = {op1}')

        result = self.hex_encoder(opcode,op1,op2)
        return result

if __name__ == "__main__":
    asm = Assembler("src/add.asm","output.mem")
