from emulator.cpu import CPU


def test_jmp_absolute():
    """JMP $0200 - Jump to absolute address"""
    cpu = CPU()

    # Opcode: 0x4C = JMP absolute
    cpu.memory.write_byte(0x0000, 0x4C)
    cpu.memory.write_byte(0x0001, 0x00)  # Jump to 0x0200
    cpu.memory.write_byte(0x0002, 0x02)

    cpu.step()

    assert cpu.program_counter.get() == 0x0200  # PC jumped!


def test_jmp_backward():
    """JMP can jump backward (for loops)"""
    cpu = CPU()
    cpu.program_counter.set(0x0100)

    # At 0x0100: JMP $0050 (jump backward)
    cpu.memory.write_byte(0x0100, 0x4C)
    cpu.memory.write_byte(0x0101, 0x50)
    cpu.memory.write_byte(0x0102, 0x00)

    cpu.step()

    assert cpu.program_counter.get() == 0x0050


def test_bne_branch_taken():
    """BNE - Branch when zero flag is clear"""
    cpu = CPU()
    cpu.alu.zero_flag = False  # Not zero

    # Opcode: 0xD0 = BNE relative
    # Branch offset: +10 bytes
    cpu.memory.write_byte(0x0000, 0xD0)
    cpu.memory.write_byte(0x0001, 0x0A)  # +10

    cpu.step()

    # PC = 0x0002 (after instruction) + 0x0A (offset) = 0x000C
    assert cpu.program_counter.get() == 0x000C


def test_bne_branch_not_taken():
    """BNE - Don't branch when zero flag is set"""
    cpu = CPU()
    cpu.alu.zero_flag = True  # Zero!

    cpu.memory.write_byte(0x0000, 0xD0)
    cpu.memory.write_byte(0x0001, 0x0A)

    cpu.step()

    # Branch not taken, just advance by 2
    assert cpu.program_counter.get() == 0x0002


def test_bne_branch_backward():
    """BNE can branch backward (negative offset)"""
    cpu = CPU()
    cpu.program_counter.set(0x0010)
    cpu.alu.zero_flag = False

    # Branch back 6 bytes (0xFA in two's complement = -6)
    cpu.memory.write_byte(0x0010, 0xD0)
    cpu.memory.write_byte(0x0011, 0xFA)  # -6

    cpu.step()

    # PC = 0x0012 - 6 = 0x000C
    assert cpu.program_counter.get() == 0x000C


def test_beq_branch_taken():
    """BEQ - Branch when zero flag is set"""
    cpu = CPU()
    cpu.alu.zero_flag = True  # Zero!

    # Opcode: 0xF0 = BEQ relative
    cpu.memory.write_byte(0x0000, 0xF0)
    cpu.memory.write_byte(0x0001, 0x05)  # +5

    cpu.step()

    assert cpu.program_counter.get() == 0x0007
