
from intelhex import IntelHex


FLASH_START_ADDRESS = 0x8000000
FLASH_END_ADDRESS = 0x80C0000
QSPI_START_ADDRESS = 0x90000000
QSPI_END_ADDRESS = 0x92000000


if __name__ == '__main__':
    ih = IntelHex();
    ih.loadhex('Alpha.hex')

    #  print(ih.addresses())

    # i = ih.segments()
    # print(ih.segments())
    fileFlash = open('aflash.bin', 'wb')
    fileQspi = open('aqspi.bin', 'wb')
    flash_end_address = 0
    qspi_end_address = 0

    for x in ih.segments():
        # print(hex(x[0]))
        # print(hex(x[1]))
        if x[0] >= FLASH_START_ADDRESS and x[1] < FLASH_END_ADDRESS:
            if flash_end_address < x[1]:
                flash_end_address = x[1]
        if x[0] >= QSPI_START_ADDRESS and x[1] < QSPI_END_ADDRESS:
            if qspi_end_address < x[1]:
                qspi_end_address = x[1]

    for i in range(flash_end_address - FLASH_START_ADDRESS):
        k = ih[FLASH_START_ADDRESS + i]
        fileFlash.write(bytes([k]))
    for i in range(qspi_end_address - QSPI_START_ADDRESS):
        k = ih[QSPI_START_ADDRESS + i]
        fileQspi.write(bytes([k]))

    fileFlash.close()
    fileQspi.close()

    # print(ih[0x8000000])
    # print(ih[0x8000100])
    print(hex(FLASH_START_ADDRESS))
    print(hex(flash_end_address))
    print(hex(QSPI_START_ADDRESS))
    print(hex(qspi_end_address))

