#file = open('ip.lua', 'wb')
import pprint

pp = pprint.PrettyPrinter(indent=4)
class LuaByteCodeDecompiler:
    def __init__(self, fileName) -> None:
        self.buffer = bytearray(open(fileName, 'rb').read())
        self.currentOffset = 0
        self.isTopLevelFunctionRead = False
        self.process()

    def readBytes(self, num=1):
        data = self.buffer[self.currentOffset: self.currentOffset + num]
        self.currentOffset += num
        return data
    
    def readByte(self):
        return self.readBytes(1)[0]
    
    def readHeader(self):
        data = {}

        data['Header Signature'] = self.readBytes(4)[1:].decode() # Header Signature: 4 bytes 
        data['Version Number'] = self.parseVersionNumber(self.readBytes(1)) # Version Number: 1 byte
        data['Format Version'] = self.readByte() # Format version: 1 byte
        data['Endianness'] = 'little' if self.readByte() == 1 else 'big' # Endianness: 1 byte
        data['Sizes'] = {
            'int': self.readByte(), # Size of int: 1 byte
            'size_t': self.readByte(), #Size of size_t: 1 byte
            'instruction': self.readByte(), #Size of instruction: 1 byte
            'lua_Number': self.readByte() # Size of lua_Number: 1 byte
        }
        data['Integral flag'] = self.readByte()

        self.headers = data
        self.sizes = self.headers['Sizes']
    
    def parseVersionNumber(self, byte):
        byte_str = hex(byte[0])[2:]
        high = byte_str[0]
        low = byte_str[1]
        return float(f"{high}.{low}")
    
    def readFunctionBlock(self):
        vararg_mapping = {
            0: 'Normal Function (0)', # A normal function has a 0 vararg flag 
            1: 'VARARG_HASARG (1)', # if LUA_COMPAT_VARARG is set
            2: 'VARARG_ISVARARG (2)', # If the funciton has vararg
            4: 'VARARG_NEEDSARG (4)' # If ... is not used as arg
        }
        
        data = {}

        data['Source Name'] = self.readString() # Source Name: String
        data['Line Defined'] = self.readInt() # Line Defined: Integer
        data['Last Line Defined'] = self.readInt() # Last Line Defined: Integer
        data['Num of upvalues'] = self.readByte() # Number of Upvalues: 1 byte
        data['Num of parameters'] = self.readByte() # Number of parameters: 1 byte
        data['is_vararg'] = vararg_mapping.get(self.readByte()) # is_vararg flag: 1 byte
        data['Max Stack Size'] = self.readByte()

        data['Instruction List'] = self.readInstructionsList()
        data['Constants List'] = self.readConstantsList()
        data['Function Prototype List'] = self.readFunctionPrototypesList()
        data['Source Line Positions List'] = self.readSourceLinePositionsList()
        data['Local Variable List'] = self.readLocalList()
        data['Upvalue List'] = self.readUpvalueList()
        

    def readString(self):
        #print(self.sizes['size_t'])
        size_t = int.from_bytes(self.readBytes(self.sizes['size_t']), byteorder=self.headers['Endianness'], signed=False)
        print(size_t)
        #print(size_t)
        string = self.readBytes(size_t)
        try:
            data = string.decode()
        except:
            data = string

        print(data)

        return data
    
    def readInt(self):
        return int.from_bytes(self.readBytes(self.sizes['int']), byteorder=self.headers['Endianness'], signed=False)
    
    def process(self):
        self.readHeader()
        self.readFunctionBlock()

    def readInstructionsList(self): # Read Instruction list, instructions are 4 bytes.
        instructions = []
        size = self.readInt()
        for i in range(1, size + 1):
            instructions.append(self.readBytes(4))
        return instructions
    
    def readConstantsList(self): 
        """
        Read Constants, format of constant list
        Integer size of constant list
        [
            1 byte type of constant 0 = LUA_TNIL, 1 = LUA_TBOOLEAN, 3 = LUA_TNUMBER, 4 = LUA_TSTRING
        ]
        """
        constants = []
        size = self.readInt()
        for i in range(1, size + 1):
            constants.append(self.readConstant())

        return constants

    def readConstant(self):
        typeofConstant = self.readByte()
        
        # Types
        if(typeofConstant == 0):
            data = None
        elif(typeofConstant == 1):
            data = self.readByte() != 0
        elif(typeofConstant == 3):
            data = self.readBytes(self.sizes['lua_Number'])
        elif(typeofConstant == 4):
            data = self.readString()
        else:
            data = self.readInt()

        return (typeofConstant, data)
    
    def readFunctionPrototypesList(self):
        size = self.readInt()
        
        functions = []

        for i in range(1, size + 1):
            print(i)
            functions.append(self.readFunctionPrototype())

        pp.pprint(functions)

    def readFunctionPrototype(self):
        vararg_mapping = {          
            0: 'Normal Function (0)', # A normal function has a 0 vararg flag 
            1: 'VARARG_HASARG (1)', # if LUA_COMPAT_VARARG is set
            2: 'VARARG_ISVARARG (2)', # If the funciton has vararg
            4: 'VARARG_NEEDSARG (4)' # If ... is not used as arg
        }
        
        data = {}
        
        
        data['Source Name'] = self.readString()
        data['Line Defined'] = self.readInt() # Line Defined: Integer
        data['Last Line Defined'] = self.readInt() # Last Line Defined: Integer
        data['Num of upvalues'] = self.readByte() # Number of Upvalues: 1 byte
        data['Num of parameters'] = self.readByte() # Number of parameters: 1 byte
        data['is_vararg'] = vararg_mapping.get(self.readByte()) # is_vararg flag: 1 byte
        data['Max Stack Size'] = self.readByte()

        """
        YUNG MGA FUNCTION PROTOTYPE, MAY GANITO RIN. RECURSIVE YUNG READFUNCTIONPROTOTYPELIST
        """
        data['Instruction List'] = self.readInstructionsList()
        data['Constants List'] = self.readConstantsList()
        data['Function Prototype List'] = self.readFunctionPrototypesList()
        data['Source Line Positions List'] = self.readSourceLinePositionsList()
        data['Local Variable List'] = self.readLocalList()
        data['Upvalue List'] = self.readUpvalueList()

        return data
    
    def readSourceLinePositionsList(self):
        data = []

        size = self.readInt()
        print("tite maliit:" + str(size))

        for i in range(1, size + 1):
            data.append(self.readInt())
        for i in data:
            print("TITE: " + str(data))
        return data
    
    def readLocalList(self):
        data = []

        size = self.readInt()

        for i in range(1, size + 1):
            data.append(self.readLocalVariable())

        return data

    def readLocalVariable(self):
        data = {}

        data['varname'] = self.readString()
        data['startpc'] = self.readInt()
        data['endpc'] = self.readInt()

        return data
    
    def readUpvalueList(self):
        data = []

        size = self.readInt()

        for i in range(1, size + 1):
            data.append(self.readString())


decompiler = LuaByteCodeDecompiler('ip.lua')
#print(decompiler.)