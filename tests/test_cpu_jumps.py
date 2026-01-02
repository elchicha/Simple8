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