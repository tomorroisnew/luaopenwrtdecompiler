from Modules.Buffer import Buffer
from Modules.Instructions import InstructionsLIst
from Modules.Constant import ConstantsList
from Modules.LocalVariables import LocalVariablesList
from Modules.SourceLinePosition import SourceLinePositionsList
from Modules.Upvalues import UpvaluesList
from Modules.List import List

class Chunks(List):
    def __init__(self, buffer: Buffer) -> None:
        self.buffer = buffer

        self.List = []

        self.parseChunks()

    def parseChunks(self):
        vararg_mapping = {
            0: 'Normal Function (0)', # A normal function has a 0 vararg flag 
            1: 'VARARG_HASARG (1)', # if LUA_COMPAT_VARARG is set
            2: 'VARARG_ISVARARG (2)', # If the funciton has vararg
            4: 'VARARG_NEEDSARG (4)' # If ... is not used as arg
        }

        self.SourceName = self.buffer.readString() # Source Name: String
        self.LineDefined = self.buffer.readInt() # Line Defined: Integer
        self.LastLineDefined = self.buffer.readInt() # Last Line Defined: Integer
        self.numUpvalues = self.buffer.readByte() # Number of Upvalues: 1 byte
        self.numParameters = self.buffer.readByte() # Number of parameters: 1 byte
        self.is_vararg = vararg_mapping.get(self.buffer.readByte()) # is_vararg flag: 1 byte
        self.MaxStackSize = self.buffer.readByte()

        self.InstructionList = InstructionsLIst(self.buffer) # List Of Instruction
        self.ConstantsList = ConstantsList(self.buffer) # List of Constants
        self.ChunksList = [] # List of Function Prototypes/Chunks
        self.parseChunksList()

        """
        Debug Info
        """
        #debugInfo = DebugInfo(self.buffer)
        self.SourceLinePositionsList = SourceLinePositionsList(self.buffer) # List of Source Line Positions, for debugging purpose
        self.LocalVariablesList = LocalVariablesList(self.buffer) # List of Local Variables for debugging purpose
        self.UpvaluesList = UpvaluesList(self.buffer) # List of Upvalues for debugging purpose

    def parseChunksList(self):
        size = self.buffer.readInt()

        for i in range(1, size + 1):
            self.ChunksList.append(Chunks(self.buffer))