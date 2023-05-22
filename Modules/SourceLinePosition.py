from Modules.Buffer import Buffer
from Modules.List import List

class SourceLinePositionsList(List):
    def __init__(self, buffer: Buffer) -> None:
        self.buffer = buffer
        
        self.List = []

        self.parseSourceLinePositionsList()

    def parseSourceLinePositionsList(self):
        size = self.buffer.readInt()

        for i in range(1, size + 1):
            self.buffer.readInt()