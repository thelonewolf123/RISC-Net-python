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
            self.encoder(line)

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

    def decimal_to_binary(self, decimal):
        bits = []
        data = [x for x in bin(decimal)][2:]
        bits = [int(x) for x in data]
        bits = bits + [0, ]*(16-len(bits))

        return bits

    def encoder(self, line):
        instruction = line.replace(",","").split(" ")
        op1 = None
        op2 = None
        opcode = instruction[0]
        print(f'opcode = {opcode}')
        if opcode in self.binary_opcodes:
            op1 = instruction[1]
            print(f'op1 = {op1}')
            op2 = instruction[2]
            print(f'op2 = {op2}')
        elif opcode in self.unary_opcodes:
            op1 = instruction[1]
            print(f'op1 = {op1}')
        
if __name__ == "__main__":
    asm = Assembler("src/add.asm","output.mem")
