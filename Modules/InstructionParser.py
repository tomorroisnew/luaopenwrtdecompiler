from enum import IntEnum
from colored import fg, bg, attr
from Modules.Chunks import Chunks

class PATCHEDOPCODES(IntEnum):
    GETTABLE = 0      # Copy a value between registers
    GETGLOBAL = 1     # Load a constant into a register
    SETGLOBAL = 2  # Load a boolean into a register
    SETUPVAL = 3   # Load nil values into a range of registers
    SETTABLE = 4  # Read an upvalue into a register
    NEWTABLE = 5 # Read a global variable into a register
    SELF = 6  # Read a table element into a register
    LOADNIL = 7 # Write a register value into a global variable
    LOADK = 8  # Write a register value into an upvalue
    LOADBOOL = 9  # Write a register value into a table element
    GETUPVAL = 10 # Create a new table
    LT = 11     # Prepare an object method for calling
    LE = 12      # Addition operator
    EQ = 13      # Subtraction operator
    DIV = 14      # Multiplication operator
    MUL = 15      # Division operator
    SUB = 16      # Modulus (remainder) operator
    ADD = 17      # Exponentiation operator
    MOD = 18      # Unary minus operator
    POW = 19      # Logical NOT operator
    UNM = 20      # Length operator
    NOT = 21   # Concatenate a range of registers
    LEN = 22      # Unconditional jump
    CONCAT = 23       # Equality test
    JMP = 24       # Less than test
    TEST = 25       # Less than or equal to test
    TESTSET = 26     # Boolean test, with conditional jump
    MOVE = 27  # Boolean test, with conditional jump and assignment
    FORLOOP = 28     # Call a closure
    FORPREP = 29 # Perform a tail call
    TFORLOOP = 30   # Return from function call
    SETLIST = 31  # Iterate a numeric for loop
    CLOSE = 32  # Initialization for a numeric for loop
    CLOSURE = 33 # Iterate a generic for loop
    CALL = 34  # Set a range of array elements for a table
    RETURN = 35    # Close a range of locals being used as upvalues
    TAILCALL = 36  # Create a closure of a function prototype
    VARARG = 37   # Assign vararg function arguments to registers

PatchedMapping = {
    'iABC': [PATCHEDOPCODES.MOVE, PATCHEDOPCODES.LOADNIL, PATCHEDOPCODES.LOADBOOL, PATCHEDOPCODES.GETUPVAL, PATCHEDOPCODES.SETUPVAL, PATCHEDOPCODES.GETTABLE, PATCHEDOPCODES.SETTABLE, PATCHEDOPCODES.ADD, PATCHEDOPCODES.SUB, PATCHEDOPCODES.MUL, PATCHEDOPCODES.DIV, PATCHEDOPCODES.MOD, PATCHEDOPCODES.POW, PATCHEDOPCODES.UNM, PATCHEDOPCODES.NOT, PATCHEDOPCODES.LEN, PATCHEDOPCODES.CONCAT, PATCHEDOPCODES.CALL, PATCHEDOPCODES.RETURN, PATCHEDOPCODES.TAILCALL, PATCHEDOPCODES.VARARG, PATCHEDOPCODES.SELF, PATCHEDOPCODES.EQ, PATCHEDOPCODES.LT, PATCHEDOPCODES.LE, PATCHEDOPCODES.TEST, PATCHEDOPCODES.TESTSET, PATCHEDOPCODES.TFORLOOP, PATCHEDOPCODES.NEWTABLE, PATCHEDOPCODES.SETLIST, PATCHEDOPCODES.CLOSE, ],
    'iABx': [PATCHEDOPCODES.LOADK, PATCHEDOPCODES.GETGLOBAL, PATCHEDOPCODES.SETGLOBAL, PATCHEDOPCODES.CLOSURE],
    'iAsBx': [PATCHEDOPCODES.JMP, PATCHEDOPCODES.FORPREP, PATCHEDOPCODES.FORLOOP]
}

GREEN = fg('green')
RESET = attr('reset')
BLUE = fg('blue')

def MOVE(A, C, B, Bx, sBx, Chunk: Chunks):
    print(f'{GREEN}MOVE            {BLUE}R(A), R(B){RESET}')

def LOADNIL(A, C, B, Bx, sBx, Chunk: Chunks):
    print(f'{GREEN}LOADNIL         {BLUE}R(A), R(B){RESET}')

def LOADK(A, C, B, Bx, sBx, Chunk: Chunks):
    print(f'{GREEN}LOADK           {BLUE}R(A), "{str(Chunk.ConstantsList[Bx].value)}"' + RESET)
    
def LOADBOOL(A, C, B, Bx, sBx, Chunk: Chunks):
    print(f'{GREEN}LOADBOOL        {BLUE}R(A), R(B), R(C){RESET}')

def GETGLOBAL(A, C, B, Bx, sBx, Chunk: Chunks):
    print(f'{GREEN}GETGLOBAL       {BLUE}R(A), "{str(Chunk.ConstantsList[Bx].value)}"{RESET}')

def SETGLOBAL(A, C, B, Bx, sBx, Chunk: Chunks):
    print(f'{GREEN}SETGLOBAL       {BLUE}R(A), "{str(Chunk.ConstantsList[Bx].value)}"{RESET}')

def GETUPVAL(A, C, B, Bx, sBx, Chunk: Chunks):
    print(f'{GREEN}GETUPVAL        {BLUE}R(A), UpValue[{str(B)}]{RESET}')

def SETUPVAL(A, C, B, Bx, sBx, Chunk: Chunks):
    print(f'{GREEN}SETUPVAL        {BLUE}R(A), UpValue[{str(B)}]{RESET}')

functionMapping = {
    PATCHEDOPCODES.MOVE: MOVE,
    PATCHEDOPCODES.LOADNIL: LOADNIL,
    PATCHEDOPCODES.LOADK: LOADK,
    PATCHEDOPCODES.LOADBOOL: LOADBOOL,
    PATCHEDOPCODES.GETGLOBAL: GETGLOBAL,
    PATCHEDOPCODES.SETGLOBAL: SETGLOBAL,
    PATCHEDOPCODES.GETUPVAL: GETUPVAL,
    PATCHEDOPCODES.SETUPVAL: SETUPVAL
}