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
