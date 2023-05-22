from Modules.Buffer import Buffer

class Header:
    def __init__(self, buffer: Buffer) -> None:
        self.buffer = buffer

        # FIELDS
        #self.HeaderSignature, self.VersionNumber, self.FormatVersion, self.Endianness, self.Sizes, self.IntegralFlag = None

        self.parseHeader()

    def parseHeader(self):
        self.HeaderSignature = self.buffer.readBytes(4)[1:].decode() # Header Signature: 4 bytes 
        self.VersionNumber = self.parseVersionNumber(self.buffer.readBytes(1)) # Version Number: 1 byte
        self.FormatVersion = self.buffer.readByte() # Format version: 1 byte
        self.Endianness = 'little' if self.buffer.readByte() == 1 else 'big' # Endianness: 1 byte
        self.Sizes = Sizes(self.buffer)
        self.IntegralFlag = self.buffer.readByte()

        self.buffer.sizes = self.Sizes
        self.buffer.Header = self

    def parseVersionNumber(self, byte):
        byte_str = hex(byte[0])[2:]
        high = byte_str[0]
        low = byte_str[1]
        return float(f"{high}.{low}")

class Sizes:
    def __init__(self, buffer: Buffer) -> None:
        self.buffer = buffer
        self.int = self.buffer.readByte()
        self.size_t = self.buffer.readByte()
        self.instruction = self.buffer.readByte()
        self.lua_Number = self.buffer.readByte()