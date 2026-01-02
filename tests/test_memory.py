from emulator.memory import Memory, MemoryAccessError
import pytest

def test_write_and_read_back():
    ram = Memory(size=0x10000)               # 64 KiB address space
    ram.write_byte(0x1234, 0xAB)
    assert ram.read_byte(0x1234) == 0xAB

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


def test_memory_initializes_with_correct_size():
    """Memory should initialize with 64KB (65536 bytes)"""
    ram = Memory()
    assert ram.size() == 65536

def test_memory_initializes_to_zero():
    """Memory should initialize with all bytes set to zero"""
    ram = Memory()
    for address in range(ram.size()):
        assert ram.read_byte(address) == 0

def test_memory_read_write_consistency():
    """Reading and writing to the same address should return the written value"""
    ram = Memory()
    ram.write_byte(0x1000, 0xFF)
    assert ram.read_byte(0x1000) == 0xFF

def test_memory_wraps_values_to_8_bits():
    """Writing values larger than 8 bits should wrap them to fit within 8 bits"""
    ram = Memory()
    ram.write_byte(0x2000, 256)
    assert ram.read_byte(0x2000) == 0

def test_memory_wraps_values_to_8_bits_large_value():
    """Writing values larger than 8 bits should wrap them to fit within 8 bits"""
    ram = Memory()
    ram.write_byte(0x2000, 0xFFFF)
    assert ram.read_byte(0x2000) == 0xFF

def test_memory_rejects_negative_addresses():
    """Negative addresses should raise an error"""
    mem = Memory()
    with pytest.raises(MemoryAccessError):
        mem.read_byte(-1)
    with pytest.raises(MemoryAccessError):
        mem.write_byte(-1, 42)