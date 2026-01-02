class Register8:
    """An 8-bit register for CPU operations"""

    def __init__(self):
        self._value = 0

    def get(self):
        """Get the current value of the register"""
        return self._value

    def set(self, value):
        """Set the value of the register to *value*"""
        self._value = value & 0xFF # Mask to ensure 8-bit value

class Register16:
    """A 16-bit register for CPU operations"""
    def __init__(self):
        self._value = 0

    def get(self):
        return self._value

    def set(self, value):
        self._value = value & 0xFFFF