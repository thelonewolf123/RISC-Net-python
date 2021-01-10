import json

from cpu import RISC_Net

memory = []

with open('memory/memory.data', 'r') as fileobj:
    memory = json.loads(fileobj.readlines()[0])

print(memory)

add_numbers = [3072, 3264, 3072, 3328, 4304, 0, 49152, 0]

cpu1 = RISC_Net(add_numbers,4)
cpu1.run()
