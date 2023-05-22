from Modules.Buffer import Buffer
from Modules.Header import Header
from Modules.Chunks import Chunks

import pprint

class LuaByteCodeDecompiler:
    def __init__(self, fileName) -> None:
        self.buffer = Buffer(open(fileName, 'rb').read())
    
    """
    Entry Point for Parsing
    """
    def parse(self):
        self.Header = Header(self.buffer)
        #print(self.Header.VersionNumber)

        # Parse Chunks
        self.Chunks = Chunks(self.buffer)

def recursive_vars(obj):
    result = {}
    for attr in vars(obj):
        val = getattr(obj, attr)
        if isinstance(val, list):
            result[attr] = [recursive_vars(item) if hasattr(item, '__dict__') else item for item in val]
        elif hasattr(val, '__dict__'):
            result[attr] = recursive_vars(val)
        else:
            result[attr] = val
    return result

x = LuaByteCodeDecompiler('domain_redirect.lua')
x.parse()
pprint.pprint(vars(x.Chunks.ConstantsList[0]))