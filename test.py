import json

from cpu import RISC_Net

memory = []

with open('memory/memory.data', 'r') as fileobj:
    memory = json.load(fileobj.readlines()[0])

print(memory)

add_numbers = [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,] + [0,]*6 + [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,] + [0,]*6 +[0,0,0,1,0,0,0,0,1,1,0,1,0,0,] + [0,]*14 +[1,1,0,0,]+[0,]*28

cpu1 = RISC_Net(add_numbers,5)
cpu1.run()
