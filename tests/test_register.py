from emulator.register import Register8


class TestRegister:
    def test_register_initializes_to_zero(self):
        """A new register should start with value 0"""
        register = Register8()
        assert register.get() == 0

    def test_register_can_store_value(self):
        """Register should store an 8-bit value"""
        register = Register8()
        register.set(0x2C)
        assert register.get() == 0x2C


    def test_register_wraps_on_overflow(self):
        """Values over 255 should wrap around to 0 (8-bit behavior)"""
        register = Register8()
        register.set(0x100)
        assert register.get() == 0

        register.set(0x101)
        assert register.get() == 1