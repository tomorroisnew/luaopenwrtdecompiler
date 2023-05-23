from Modules.Buffer import Buffer
from Modules.List import List

class ConstantsList(List):
    def __init__(self, buffer: Buffer) -> None:
        self.buffer = buffer

        self.List: Buffer = []

        self.parseConstantList()

    def parseConstantList(self):
        size = self.buffer.readInt()

        for i in range(1, size + 1):
            self.List.append(Constant(self.buffer))

    def __getitem__(self, index):
        return self.List[index]

class Constant:
    def __init__(self, buffer: Buffer) -> None:
        self.buffer = buffer

        self.parseConstant()

    def parseConstant(self):
        self.typeofConstant = self.buffer.readByte()

        if(self.typeofConstant == 0):
            data = None
        elif(self.typeofConstant == 1):
            data = self.buffer.readByte() != 0
        elif(self.typeofConstant == 3):
            data = self.buffer.readBytes(self.sizes['lua_Number'])
        elif(self.typeofConstant == 4):
            data = self.buffer.readString()
        else:
            data = self.buffer.readInt()

        self.value = data