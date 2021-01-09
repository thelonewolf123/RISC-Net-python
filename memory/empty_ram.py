import os

with open('memory.data','wb') as fileobj:
    for _ in range(0,25000):
        fileobj.write(b'0000')