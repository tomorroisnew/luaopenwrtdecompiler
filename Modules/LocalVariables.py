from Modules.Buffer import Buffer
from Modules.List import List

class LocalVariablesList(List):
    def __init__(self, buffer: Buffer) -> None:
        self.buffer = buffer
        
        self.List = []

        self.parseLocalVariablesList()

    def parseLocalVariablesList(self):
        size = self.buffer.readInt()

        for i in range(1, size + 1):
            self.List.append(LocalVariable(self.buffer))

class LocalVariable:
    def __init__(self, buffer) -> None:
        self.buffer = buffer

        self.varname = self.buffer.readString()
        self.startpc = self.buffer.readInt()
        self.endpc = self.buffer.readInt()