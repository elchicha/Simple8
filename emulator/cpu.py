from emulator.alu import ALU
from emulator.memory import Memory
from emulator.register import Register8, Register16


class CPU:
    def __init__(self):
        self.accumulator = Register8()
        self.program_counter = Register16()
        self.stack_pointer = Register8()

        self.memory = Memory()
        self.alu = ALU()
        self.stack_pointer.set(0xFF)


    def step(self):
        """Execute one CPU instruction (Fetch, Decode, Execute)"""
        pc = self.program_counter.get()
        opcode = self.memory.read_byte(pc)

        if opcode == 0xA9:
            self._execute_lda_immediate()
        elif opcode == 0x8D:
            self._execute_sta_absolute()
        elif opcode == 0x69:
            self._execute_add_immediate()
        elif opcode == 0x4C:
            self._execute_jmp_absolute()
        elif opcode == 0xEA:
            self._execute_nop()
        elif opcode == 0xD0:
            self._execute_bne()
        elif opcode == 0xF0:
            self._execute_beq()
        else:
            raise NotImplementedError(f"Opcode {opcode:02X} not implemented")

    def _execute_lda_immediate(self):
        """Load Accumulator with immediate value"""
        # Format: [0x49, value]
        # Read the value from PC+1
        pc = self.program_counter.get()
        value = self.memory.read_byte(pc + 1)
        self.accumulator.set(value)

        self.program_counter.set(pc + 2)

    def _execute_sta_absolute(self):
        """Store accumulator value to absolute address"""
        pc = self.program_counter.get()

        addr_low = self.memory.read_byte(pc + 1)
        addr_high = self.memory.read_byte(pc + 2)
        address = (addr_high << 8) | addr_low

        value = self.accumulator.get()
        self.memory.write_byte(address, value)

        self.program_counter.set(pc + 3)

    def _execute_add_immediate(self):
        """ADD #$10 - Add immediate value to accumulator"""
        pc = self.program_counter.get()
        operand = self.memory.read_byte(pc + 1)
        accumulator_value = self.accumulator.get()
        result = self.alu.add(accumulator_value, operand)
        self.accumulator.set(result)
        self.program_counter.set(pc + 2)

    def _execute_nop(self):
        """NOP - No operation, just advance PC"""
        pc = self.program_counter.get()
        self.program_counter.set(pc + 1)

    def _execute_jmp_absolute(self):
        """JMP $0200 - Jump to absolute address"""
        pc = self.program_counter.get()

        addr_low = self.memory.read_byte(pc + 1)
        addr_high = self.memory.read_byte(pc + 2)
        target_address = (addr_high << 8) | addr_low

        self.program_counter.set(target_address)

    def _execute_bne(self):
        """BNE $nn - Branch if Not Equal (zero flag clear)"""
        pc = self.program_counter.get()
        offset = self.memory.read_byte(pc + 1)

        if offset >= 0x80:
            offset -= 0x100 # Convert to negative

        pc = pc + 2 # Move past the BNE instruction

        if not self.alu.zero_flag:
            pc += offset

        self.program_counter.set(pc)

    def _execute_beq(self):
        """BNE $nn - Branch if Equal (zero flag true)"""
        pc = self.program_counter.get()
        offset = self.memory.read_byte(pc + 1)

        if offset >= 0x80:
            offset -= 0x100  # Convert to negative

        pc = pc + 2  # Move past the BNE instruction

        if self.alu.zero_flag:
            pc += offset

        self.program_counter.set(pc)

    def test_beq_branch_not_taken():
        """BEQ - Don't branch when zero flag is clear"""
        cpu = CPU()
        cpu.alu.zero_flag = False

        cpu.memory.write_byte(0x0000, 0xF0)
        cpu.memory.write_byte(0x0001, 0x05)

        cpu.step()

        assert cpu.program_counter.get() == 0x0002