import json

# width = 16 bits

data = [0,]*1000

with open('memory.data', 'wb') as fileobj:
    fileobj.write(bytes(json.dumps(data).encode('utf-8')))
