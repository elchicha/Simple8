from emulator.cpu import CPU


def test_countdown_loop():
    """
    Program: Count down from 5 to 0

    Assembly:
        LDA #$05    ; Start at 5
    LOOP:
        SUB #$01    ; Decrement A
        STA $0200   ; Store current value
        BNE LOOP    ; Loop if A is not zero
    """

    cpu = CPU()

    # Address 0x0000: LDA #$05
    cpu.memory.write_byte(0x0000, 0xA9)
    cpu.memory.write_byte(0x0001, 0x05)

    # Address 0x0002: SUB #$01 (we need to implement SUB!)
    # For now, let's use ADD #$FF (which is like subtracting 1)
    cpu.memory.write_byte(0x0002, 0x69)  # ADD immediate
    cpu.memory.write_byte(0x0003, 0xFF)  # value: -1 (wraps to 255)

    # Address 0x0004: STA $0200
    cpu.memory.write_byte(0x0004, 0x8D)  # STA absolute
    cpu.memory.write_byte(0x0005, 0x00)  # low byte
    cpu.memory.write_byte(0x0006, 0x02)  # high byte

    # Address 0x0007: BNE -7 (back to 0x0002)
    # Offset calculation: from 0x0009 back to 0x0002 = -7
    cpu.memory.write_byte(0x0007, 0xD0)  # BNE
    cpu.memory.write_byte(0x0008, 0xF9)  # -7 in two's complement

    # Execute!
    cpu.step()  # LDA #$05 → A = 5

    # Loop iteration 1
    cpu.step()  # ADD #$FF → A = 4
    cpu.step()  # STA $0200 → mem[0x0200] = 4
    cpu.step()  # BNE → branch back (zero_flag = False)

    # Loop iteration 2
    cpu.step()  # ADD #$FF → A = 3
    cpu.step()  # STA $0200 → mem[0x0200] = 3
    cpu.step()  # BNE → branch back

    # Loop iteration 3
    cpu.step()  # ADD #$FF → A = 2
    cpu.step()  # STA $0200 → mem[0x0200] = 2
    cpu.step()  # BNE → branch back

    # Loop iteration 4
    cpu.step()  # ADD #$FF → A = 1
    cpu.step()  # STA $0200 → mem[0x0200] = 1
    cpu.step()  # BNE → branch back

    # Loop iteration 5 (final)
    cpu.step()  # ADD #$FF → A = 0, zero_flag = True!
    cpu.step()  # STA $0200 → mem[0x0200] = 0
    cpu.step()  # BNE → DON'T branch (zero_flag = True)

    # Verify final state
    assert cpu.accumulator.get() == 0x00
    assert cpu.memory.read_byte(0x0200) == 0x00
    assert cpu.program_counter.get() == 0x0009  # Exited loop


def test_simple_infinite_loop_with_counter():
    """
    Program: Loop exactly 3 times then stop

    Assembly:
        LDA #$03      ; Counter = 3
    LOOP:
        SUB #$01      ; Counter--
        BNE LOOP      ; Loop if counter != 0
        NOP           ; Exit point
    """
    cpu = CPU()

    # LDA #$03
    cpu.memory.write_byte(0x0000, 0xA9)
    cpu.memory.write_byte(0x0001, 0x03)

    # ADD #$FF (subtract 1)
    cpu.memory.write_byte(0x0002, 0x69)
    cpu.memory.write_byte(0x0003, 0xFF)

    # BNE -4 (back to 0x0002)
    cpu.memory.write_byte(0x0004, 0xD0)
    cpu.memory.write_byte(0x0005, 0xFC)  # -4

    # NOP (exit point)
    cpu.memory.write_byte(0x0006, 0xEA)

    # Execute
    cpu.step()  # LDA → A = 3

    # Iteration 1: A = 3 → 2
    cpu.step()  # ADD → A = 2
    cpu.step()  # BNE → branch

    # Iteration 2: A = 2 → 1
    cpu.step()  # ADD → A = 1
    cpu.step()  # BNE → branch

    # Iteration 3: A = 1 → 0
    cpu.step()  # ADD → A = 0, zero_flag = True
    cpu.step()  # BNE → DON'T branch!

    # After loop
    cpu.step()  # NOP

    assert cpu.accumulator.get() == 0x00
    assert cpu.program_counter.get() == 0x0007  # After NOP