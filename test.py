import sys
import json

from cpu import RISC_Net

def main():
    memory = []

    with open(sys.argv[1], 'r') as fileobj:
        memory = json.loads(fileobj.readlines()[0])

    # print(memory)

    cpu1= RISC_Net(memory, 4)
    cpu1.run()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print(f"Usage: {sys.argv[0]} <path to program file>")