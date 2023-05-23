from Modules.Chunks import Chunks
from Modules.Buffer import Buffer
from bitstring import BitArray
from Modules.Header import Header
from enum import IntEnum
from Modules.InstructionParser import functionMapping, PATCHEDOPCODES, PatchedMapping

from enum import IntEnum

class OPCODES(IntEnum):
    MOVE = 0      # Copy a value between registers
    LOADK = 1     # Load a constant into a register
    LOADBOOL = 2  # Load a boolean into a register
    LOADNIL = 3   # Load nil values into a range of registers
    GETUPVAL = 4  # Read an upvalue into a register
    GETGLOBAL = 5 # Read a global variable into a register
    GETTABLE = 6  # Read a table element into a register
    SETGLOBAL = 7 # Write a register value into a global variable
    SETUPVAL = 8  # Write a register value into an upvalue
    SETTABLE = 9  # Write a register value into a table element
    NEWTABLE = 10 # Create a new table
    SELF = 11     # Prepare an object method for calling
    ADD = 12      # Addition operator
    SUB = 13      # Subtraction operator
    MUL = 14      # Multiplication operator
    DIV = 15      # Division operator
    MOD = 16      # Modulus (remainder) operator
    POW = 17      # Exponentiation operator
    UNM = 18      # Unary minus operator
    NOT = 19      # Logical NOT operator
    LEN = 20      # Length operator
    CONCAT = 21   # Concatenate a range of registers
    JMP = 22      # Unconditional jump
    EQ = 23       # Equality test
    LT = 24       # Less than test
    LE = 25       # Less than or equal to test
    TEST = 26     # Boolean test, with conditional jump
    TESTSET = 27  # Boolean test, with conditional jump and assignment
    CALL = 28     # Call a closure
    TAILCALL = 29 # Perform a tail call
    RETURN = 30   # Return from function call
    FORLOOP = 31  # Iterate a numeric for loop
    FORPREP = 32  # Initialization for a numeric for loop
    TFORLOOP = 33 # Iterate a generic for loop
    SETLIST = 34  # Set a range of array elements for a table
    CLOSE = 35    # Close a range of locals being used as upvalues
    CLOSURE = 36  # Create a closure of a function prototype
    VARARG = 37   # Assign vararg function arguments to registers

Mapping = {
    'iABC': [OPCODES.MOVE, OPCODES.LOADNIL, OPCODES.LOADBOOL, OPCODES.GETUPVAL, OPCODES.SETUPVAL, OPCODES.GETTABLE, OPCODES.SETTABLE, OPCODES.ADD, OPCODES.SUB, OPCODES.MUL, OPCODES.DIV, OPCODES.MOD, OPCODES.POW, OPCODES.UNM, OPCODES.NOT, OPCODES.LEN, OPCODES.CONCAT, OPCODES.CALL, OPCODES.RETURN, OPCODES.TAILCALL, OPCODES.VARARG, OPCODES.SELF, OPCODES.EQ, OPCODES.LT, OPCODES.LE, OPCODES.TEST, OPCODES.TESTSET, OPCODES.TFORLOOP, OPCODES.NEWTABLE, OPCODES.SETLIST, OPCODES.CLOSE, ],
    'iABx': [OPCODES.LOADK, OPCODES.GETGLOBAL, OPCODES.SETGLOBAL, OPCODES.CLOSURE],
    'iAsBx': [OPCODES.JMP, OPCODES.FORPREP, OPCODES.FORLOOP]
}

class Disassembler:
    def __init__(self, chunk: Chunks, header: Header) -> None:
        self.chunk = chunk

        self.header = header

        self.AssemblyList = []

    def analyze(self):
        for i in self.chunk.InstructionList:
            #i: Buffer = Buffer(i)
            self.parseInstruction(i, customOpcodes=PATCHEDOPCODES, customMapping=PatchedMapping, functionMapping=functionMapping)


    def parseInstruction(self, instruction, customOpcodes = None, customMapping = None, functionMapping=None):
        if(not customOpcodes):
            opcodes = OPCODES
            mapping = Mapping
        else:
            opcodes = customOpcodes
            mapping = customMapping

        instruction = self.readInt(instruction)

        Opcode = opcodes(self.get_bits(instruction, 0, 6))
        Type = None

        for types in mapping:
            if Opcode in mapping[types]:
                Type = types

        #print(Type)

        A = self.get_bits(instruction, 6, 8)
        C = self.get_bits(instruction, 8 + 6, 9)
        B = self.get_bits(instruction, 6 + 8 + 9, 9)
        Bx = self.get_bits(instruction, 8 + 6, 18)
        sBx = self.get_bits(instruction, 8 + 6, 18)
        #print(A, B, C)
        try:
            functionMapping[Opcode](A,C,B,Bx,sBx, self.chunk) # Register A, C, B, Bx, sBx, chunk is also passed for the list of constants
        except:
            pass

    def readInt(self, buffer):
        return int.from_bytes(buffer, byteorder=self.header.Endianness, signed=False)
    
    def get_bits(self, num: int, position: int, size: int):
        return (num>>position) & (~((~0)<<size))