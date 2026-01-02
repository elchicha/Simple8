from emulator.cpu import CPU

def test_simple_addition_program():
    """
    Program: Load 5, add 10, store result

    Assembly:
        LDA #$05    ; Load 5 into accumulator
        ADD #$0A    ; Add 10 to accumulator
        STA $0200   ; Store result at memory address $0200
    """
    cpu = CPU()

    # Write the program to memory
    cpu.memory.write_byte(0x0000, 0xA9) # LDA immediate
    cpu.memory.write_byte(0x0001, 0x05) # value: 5

    cpu.memory.write_byte(0x0002, 0x69) # ADD immediate
    cpu.memory.write_byte(0x0003, 0x0A) # value: 10

    cpu.memory.write_byte(0x0004, 0x8D) # STA
    cpu.memory.write_byte(0x0005, 0x00) # Low byte
    cpu.memory.write_byte(0x0006, 0x02) # High byte

    cpu.step() # LDA
    cpu.step() # ADD
    cpu.step() # STA $0200

    # Check results
    assert cpu.accumulator.get() == 0x0F  # 5 + 10 = 15
    assert cpu.memory.read_byte(0x0200) == 0x0F  # Stored in memory
    assert cpu.program_counter.get() == 0x07  # PC at next instruction


def test_accumulator_workflow():
    """
    Program: Multiple operations on accumulator

    Assembly:
        LDA #$20      ; Load 32
        ADD #$30      ; Add 48 (= 80)
        ADD #$50      ; Add 80 (= 160)
        STA $0300     ; Store result
    """
    cpu = CPU()

    # Program at 0x0000
    cpu.memory.write_byte(0x0000, 0xA9)  # LDA
    cpu.memory.write_byte(0x0001, 0x20)  # 32

    cpu.memory.write_byte(0x0002, 0x69)  # ADD
    cpu.memory.write_byte(0x0003, 0x30)  # 48

    cpu.memory.write_byte(0x0004, 0x69)  # ADD
    cpu.memory.write_byte(0x0005, 0x50)  # 80

    cpu.memory.write_byte(0x0006, 0x8D)  # STA
    cpu.memory.write_byte(0x0007, 0x00)  # low
    cpu.memory.write_byte(0x0008, 0x03)  # high (0x0300)

    # Execute
    cpu.step()  # A = 32
    assert cpu.accumulator.get() == 0x20

    cpu.step()  # A = 80
    assert cpu.accumulator.get() == 0x50

    cpu.step()  # A = 160
    assert cpu.accumulator.get() == 0xA0

    cpu.step()  # Store
    assert cpu.memory.read_byte(0x0300) == 0xA0


def test_overflow_handling():
    """
    Program: Test 8-bit overflow

    Assembly:
        LDA #$FF      ; Load 255
        ADD #$02      ; Add 2 (= 257, wraps to 1)
        STA $0400     ; Store result
    """
    cpu = CPU()

    cpu.memory.write_byte(0x0000, 0xA9)  # LDA
    cpu.memory.write_byte(0x0001, 0xFF)  # 255

    cpu.memory.write_byte(0x0002, 0x69)  # ADD
    cpu.memory.write_byte(0x0003, 0x02)  # 2

    cpu.memory.write_byte(0x0004, 0x8D)  # STA
    cpu.memory.write_byte(0x0005, 0x00)  # low
    cpu.memory.write_byte(0x0006, 0x04)  # high (0x0400)

    cpu.step()  # A = 255
    cpu.step()  # A = 1 (overflow!)
    cpu.step()  # Store

    assert cpu.accumulator.get() == 0x01  # Wrapped to 1
    assert cpu.memory.read_byte(0x0400) == 0x01
    assert cpu.alu.carry_flag == True  # Carry flag set!