class Buffer:
    def __init__(self, data) -> None:
        self.buffer = bytearray(data)
        self.currentOffset = 0
    
    def readBytes(self, num=1):
        data = self.buffer[self.currentOffset: self.currentOffset + num]
        self.currentOffset += num
        return data
    
    def readByte(self):
        return self.readBytes(1)[0]
    
    def readString(self):
        #print(self.sizes['size_t'])
        size_t = int.from_bytes(self.readBytes(self.sizes.size_t), byteorder=self.Header.Endianness, signed=False)
        #print(size_t)
        string = self.readBytes(size_t)
        try:
            data = string.decode()
        except:
            data = string

        return data
    
    def readInt(self):
        return int.from_bytes(self.readBytes(self.sizes.int), byteorder=self.Header.Endianness, signed=False)