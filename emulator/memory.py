class Memory:
    """Flat RAM with explicit bounds checking."""

    def __init__(self, size: int = 0x10000):
        self._data = bytearray(size)

    def _check_address(self, address: int) -> None:
        """Validate that *addr* lies within the allocated range."""
        if not 0 <= address < len(self._data):
            raise MemoryAccessError(f"Address {address:#06x} out of range")

    def write_byte(self, address: int, value: int) -> None:
        """Store the low 8-bits of *value* at *address*"""
        self._check_address(address)
        self._data[address] = value & 0xFF

    def read_byte(self, address: int) -> int:
        """Read and return the byte at *address*"""
        self._check_address(address)
        return self._data[address]

class MemoryAccessError(RuntimeError):
    """Raised when an address is outside the allocated RAM"""
    pass