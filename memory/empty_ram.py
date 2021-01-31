import json

# width = 16 bits

data = [[0,]*16]*16384

with open('memory.json', 'w') as fileobj:
    fileobj.write(json.dumps(data))
