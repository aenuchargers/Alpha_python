
from intelhex import IntelHex

BINFILE_PAGE_SIZE = 256
BINFILE_ADR_IDENT = 512
FLASH_START_ADDRESS = 0x8000000
FLASH_END_ADDRESS = 0x8040000
EXTRAM_START_ADDRESS = 0x20000000
EXTRAM_END_ADDRESS = 0x20030000
SDRAM_START_ADDRESS = 0xC0200000
SDRAM_END_ADDRESS = 0xC0400000

if __name__ == '__main__':
    ih = IntelHex()
    ih.loadhex('Alpha_bootloader.hex')

    #  print(ih.addresses())

    # i = ih.segments()
    # print(ih.segments())
    fileFlash = open('bflash.bin', 'wb')
    fileExtram = open('bextram.bin', 'wb')
    fileSdram = open('bsdram.bin', 'wb')
    flash_end_address = 0
    extram_end_address = 0
    sdram_end_address = 0

    for x in ih.segments():
        # print(hex(x[0]))
        # print(hex(x[1]))
        if x[0] >= FLASH_START_ADDRESS and x[1] < FLASH_END_ADDRESS:
            if flash_end_address < x[1]:
                flash_end_address = x[1]
        if x[0] >= EXTRAM_START_ADDRESS and x[1] < EXTRAM_END_ADDRESS:
            if extram_end_address < x[1]:
                extram_end_address = x[1]
        if x[0] >= SDRAM_START_ADDRESS and x[1] < SDRAM_END_ADDRESS:
            if sdram_end_address < x[1]:
                sdram_end_address = x[1]

    for i in range(flash_end_address - FLASH_START_ADDRESS):
        k = ih[FLASH_START_ADDRESS + i]
        fileFlash.write(bytes([k]))
        if i < (BINFILE_ADR_IDENT + BINFILE_PAGE_SIZE):
            fileExtram.write(bytes([k]))
            fileSdram.write(bytes([k]))
    for i in range(extram_end_address - EXTRAM_START_ADDRESS):
        k = ih[EXTRAM_START_ADDRESS + i]
        fileExtram.write(bytes([k]))
    for i in range(sdram_end_address - SDRAM_START_ADDRESS):
        k = ih[SDRAM_START_ADDRESS + i]
        fileSdram.write(bytes([k]))

    fileFlash.close()
    fileExtram.close()
    fileSdram.close()

    # print(ih[0x8000000])
    # print(ih[0x8000100])
    print(hex(FLASH_START_ADDRESS))
    print(hex(flash_end_address))
    print(hex(EXTRAM_START_ADDRESS))
    print(hex(extram_end_address))
    print(hex(SDRAM_START_ADDRESS))
    print(hex(sdram_end_address))
