from emulator.memory import Memory, MemoryAccessError
import pytest

def test_write_and_read_back():
    mem = Memory(size=0x10000)               # 64 KiB address space
    mem.write_byte(0x1234, 0xAB)
    assert mem.read_byte(0x1234) == 0xAB

def test_out_of_range_access_raises():
    """
    Accessing an address outside the allocated RAM should raise
    a dedicated MemoryAccessError, not a generic IndexError
    """
    ram = Memory(size=0x100)  # 256-byte RAM for the test
    # --- READ -------------
    with pytest.raises(MemoryAccessError):
        ram.read_byte(0x200)  # 0x200 > 0xFF -> error

    with pytest.raises(MemoryAccessError):
        ram.write_byte(0x300, 0x55)