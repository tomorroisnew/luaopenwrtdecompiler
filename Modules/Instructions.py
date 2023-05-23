from Modules.Buffer import Buffer
from Modules.List import List

class InstructionsLIst(List):
    def __init__(self, buffer: Buffer) -> None:
        self.buffer = buffer

        self.List = []

        self.readInstructionsList()

    def readInstructionsList(self):
        size = self.buffer.readInt()

        for i in range(1, size + 1):
            self.List.append(self.buffer.readBytes(4))