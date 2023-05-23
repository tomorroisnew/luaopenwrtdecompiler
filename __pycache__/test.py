from bitstring import BitArray
from bitarray import bitarray
import struct

d = '0001001'

print(int(d[:3], 2))

print(bytearray(b'\x01\x02\x03\x04')[::-1])