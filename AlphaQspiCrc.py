import time
import sys
import os
import binascii

BINFILE_PAGE_SIZE = 256
BINFILE_ADR_IDENT = 512
BINFILE_ADR_VERSION = 0
BINFILE_SIZE_VERSION = 16
BINFILE_ADR_CRC = BINFILE_SIZE_VERSION
BINFILE_SIZE_CRC = 2
BINFILE_ADR_SIZE = BINFILE_ADR_CRC + BINFILE_SIZE_VERSION
BINFILE_SIZE_SIZE = 4


def crc16_byte(input_crc, data: bytes, poly=0x8408):
    '''
    CRC-16-CCITT Algorithm
    '''
    cur_byte = 0xFF & data
    return_crc = input_crc
    for _ in range(0, 8):
        if (return_crc & 0x0001) ^ (cur_byte & 0x0001):
            return_crc = (return_crc >> 1) ^ poly
        else:
            return_crc >>= 1
        cur_byte >>= 1
    return_crc = (~return_crc & 0xFFFF)
    return_crc = (return_crc << 8) | ((return_crc >> 8) & 0xFF)

    return return_crc & 0xFFFF


def crc16_bytes(input_crc, data: bytes, poly=0x8408):
    '''
    CRC-16-CCITT Algorithm
    '''
    data = bytearray(data)
    return_crc = input_crc
    for b in data:
        return_crc = crc16_byte(return_crc, b)

    return return_crc


def crc16(data: bytes, poly=0x8408):
    '''
    CRC-16-CCITT Algorithm
    '''
    data = bytearray(data)
    crc = 0xFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)

    return crc & 0xFFFF


if __name__ == '__main__':
    __doc__ = """
    ....
    """
    # print(buffer)
    # print(len(buffer))
    # sys.exit(0)

    str_file_input = 'aqspi.bin'
    file_size = os.stat(str_file_input)
    # print("Size of file :", file_size.st_size, "bytes")
    number_bytes = file_size.st_size
    hex_number_bytes = hex(number_bytes)
    if number_bytes < (BINFILE_PAGE_SIZE * 10):
        print("File - small size!")
        sys.exit(1)

    file_input = open(str_file_input, 'rb')
    crc_file = 0xFFFF
    page_ident = 0
    string_version = ''
    while True:
        if number_bytes > BINFILE_PAGE_SIZE:
            if page_ident == BINFILE_ADR_IDENT:
                file_read = file_input.read(BINFILE_SIZE_VERSION)
                string_version = file_read.decode()
                file_read = file_input.read(BINFILE_PAGE_SIZE - BINFILE_SIZE_VERSION)
            else:
                file_read = file_input.read(BINFILE_PAGE_SIZE)
                crc_file = crc16_bytes(crc_file, file_read)
                # print(file_read)

            page_ident = page_ident + BINFILE_PAGE_SIZE
            number_bytes = number_bytes - BINFILE_PAGE_SIZE
            continue
        else:
            break

    file_read = file_input.read(number_bytes)
    crc_file = crc16_bytes(crc_file, file_read)
    file_input.close()

    hex_crc_file = hex(crc_file)
    print(hex_crc_file)
    print(hex_number_bytes)

    file_size = os.stat(str_file_input)
    # print("Size of file :", file_size.st_size, "bytes")
    number_bytes = file_size.st_size
    file_input = open(str_file_input, 'rb')
    str_file_output = string_version + '_flash' + '.bin'
    file_output = open(str_file_output, 'wb')

    page_ident = 0
    while True:
        if number_bytes > BINFILE_PAGE_SIZE:
            file_read = file_input.read(BINFILE_PAGE_SIZE)

            if page_ident == BINFILE_ADR_IDENT:
                file_output.write(string_version.encode())
                # file_output.write('    '.encode())
                ident_number_bytes = BINFILE_PAGE_SIZE - BINFILE_SIZE_VERSION
                file_output.write((crc_file & 0xFFFF).to_bytes(BINFILE_SIZE_CRC, byteorder="little"))
                ident_number_bytes = ident_number_bytes - BINFILE_SIZE_CRC
                file_output.write((file_size.st_size & 0xFFFFFFFF).to_bytes(BINFILE_SIZE_SIZE, byteorder="little"))
                ident_number_bytes = ident_number_bytes - BINFILE_SIZE_SIZE
                for k in range(ident_number_bytes):
                    file_output.write(bytes([255]))
            else:
                file_output.write(file_read)

            # print(file_read)
            number_bytes = number_bytes - BINFILE_PAGE_SIZE
            page_ident = page_ident + BINFILE_PAGE_SIZE
        else:
            break

    file_read = file_input.read(number_bytes)
    file_output.write(file_read)

    file_input.close()
    file_output.close()

    os.remove(str_file_input)
    os.rename(str_file_output, str_file_input)
