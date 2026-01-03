from emulator.cpu import CPU


def test_cpu_has_x_and_y_registers():
    """X and Y are index registers for array/loop operations"""
    cpu = CPU()
    assert cpu.x_register.get() == 0x00
    assert cpu.y_register.get() == 0x00

def test_ldx_immediate():
    """LDX #$42 - Load X register with immediate value"""
    cpu = CPU()

    # Opcode: 0xA2 = LDX immediate
    cpu.memory.write_byte(0x0000, 0xA2)
    cpu.memory.write_byte(0x0001, 0x42)

    cpu.step()

    assert cpu.x_register.get() == 0x42


def test_ldy_immediate():
    """LDY #$33 - Load Y register with immediate value"""
    cpu = CPU()

    # Opcode: 0xA0 = LDY immediate
    cpu.memory.write_byte(0x0000, 0xA0)
    cpu.memory.write_byte(0x0001, 0x33)

    cpu.step()

    assert cpu.y_register.get() == 0x33
    assert cpu.program_counter.get() == 0x02


def test_stx_absolute():
    """STX $0200 - Store X register to memory"""
    cpu = CPU()
    cpu.x_register.set(0x99)

    # Opcode: 0x8E = STX absolute
    cpu.memory.write_byte(0x0000, 0x8E)
    cpu.memory.write_byte(0x0001, 0x00)
    cpu.memory.write_byte(0x0002, 0x02)

    cpu.step()

    assert cpu.memory.read_byte(0x0200) == 0x99
    assert cpu.program_counter.get() == 0x03


def test_sty_absolute():
    """STY $0300 - Store Y register to memory"""
    cpu = CPU()
    cpu.y_register.set(0x77)

    # Opcode: 0x8C = STY absolute
    cpu.memory.write_byte(0x0000, 0x8C)
    cpu.memory.write_byte(0x0001, 0x00)
    cpu.memory.write_byte(0x0002, 0x03)

    cpu.step()

    assert cpu.memory.read_byte(0x0300) == 0x77
    assert cpu.program_counter.get() == 0x03


def test_tax():
    """TAX - Transfer Accumulator to X"""
    cpu = CPU()
    cpu.accumulator.set(0x55)

    # Opcode: 0xAA = TAX
    cpu.memory.write_byte(0x0000, 0xAA)

    cpu.step()

    assert cpu.x_register.get() == 0x55
    assert cpu.accumulator.get() == 0x55  # A unchanged
    assert cpu.program_counter.get() == 0x01


def test_tay():
    """TAY - Transfer Accumulator to Y"""
    cpu = CPU()
    cpu.accumulator.set(0x66)

    # Opcode: 0xA8 = TAY
    cpu.memory.write_byte(0x0000, 0xA8)

    cpu.step()

    assert cpu.y_register.get() == 0x66
    assert cpu.accumulator.get() == 0x66  # A unchanged


def test_txa():
    """TXA - Transfer X to Accumulator"""
    cpu = CPU()
    cpu.x_register.set(0x88)

    # Opcode: 0x8A = TXA
    cpu.memory.write_byte(0x0000, 0x8A)

    cpu.step()

    assert cpu.accumulator.get() == 0x88
    assert cpu.x_register.get() == 0x88  # X unchanged


def test_tya():
    """TYA - Transfer Y to Accumulator"""
    cpu = CPU()
    cpu.y_register.set(0x99)

    # Opcode: 0x98 = TYA
    cpu.memory.write_byte(0x0000, 0x98)

    cpu.step()

    assert cpu.accumulator.get() == 0x99
    assert cpu.y_register.get() == 0x99  # Y unchanged