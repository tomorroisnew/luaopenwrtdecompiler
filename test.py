def byte_to_float(byte):
    byte_str = hex(byte[0])[2:]
    high = byte_str[0]
    low = byte_str[1]
    return float(f"{high}.{low}")

print(byte_to_float(bytearray([0x51])))
