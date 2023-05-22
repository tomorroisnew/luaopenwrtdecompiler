from Modules.Chunks import Chunks

OPCODES = {
    0: 'MOVE',
    1: 'LOADK', 
    2: 
}

class Disassembler:
    def __init__(self, chunk: Chunks) -> None:
        self.chunk = chunk

    def analyze(self):
        for i in self.chunk.InstructionList:
            print(i)