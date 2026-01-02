from emulator.cpu import CPU


def test_cpu_initialization_with_registers():
    """CPU should have accumulator, PC, and SP registers"""
    cpu = CPU()
    assert cpu.accumulator.get() == 0x00
    assert cpu.program_counter.get() == 0x00
    assert cpu.stack_pointer.get() == 0xFF

def test_cpu_has_memory():
    """CPU should have accessible memory"""
    cpu = CPU()
    cpu.memory.write_byte(0x0100, 0x42)
    assert cpu.memory.read_byte(0x0100) == 0x42

def test_cpu_lda_immediate():
    """
    CPU should be able to load accumulator with immediate value.
    (e.g. LDA #$42)
    """
    cpu = CPU()
    # Opcode: 0xA9 = LDA immediate
    # Format: [opcode, immediate_value]
    cpu.memory.write_byte(0x0000, 0xA9) # LDA opcode
    cpu.memory.write_byte(0x0001, 0x42) # value

    cpu.step()

    assert cpu.accumulator.get() == 0x42
    assert cpu.program_counter.get() == 0x02 # PC advanced by 2 bytes


def test_cpu_sta_absolute():
    """STA $0200 - Store accumulator to absolute memory address"""
    cpu = CPU()
    cpu.accumulator.set(0x99)

    # Opcode: 0x8D = STA absolute
    # Format: [0x8D, low_byte, high_byte]
    cpu.memory.write_byte(0x0000, 0x8D) # STA opcode
    cpu.memory.write_byte(0x0001, 0x00) # address low byte
    cpu.memory.write_byte(0x0002, 0x02) # address high byte (0x0200)

    cpu.step()

    assert cpu.memory.read_byte(0x0200) == 0x99
    assert cpu.program_counter.get() == 0x03 # PC advanced by 3 bytes


def test_cpu_add_immediate():
    """ADD #$10 - Add immediate value to accumulator"""
    cpu = CPU()
    cpu.accumulator.set(0x05)

    # Opcode: 0x69 = ADD immediate (we define this)
    cpu.memory.write_byte(0x0000, 0x69)
    cpu.memory.write_byte(0x0001, 0x10)

    cpu.step()

    assert cpu.accumulator.get() == 0x15
    assert cpu.program_counter.get() == 0x02

def test_cpu_nop():
    """NOP - No operation, just advance PC"""
    cpu = CPU()

    cpu.memory.write_byte(0x0000, 0xEA)
    cpu.step()

    assert cpu.program_counter.get() == 0x01