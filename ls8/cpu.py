"""CPU functionality."""

import sys
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101

SP = 7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
     #  Add list properties to the `CPU` class to hold 256 bytes of memory
    # and 8 general-purpose registers.
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256

    def load(self, filename):
        """Load a program into memory."""

     # sys.argv is a list in Python, which contains the command-line arguments passed to the script.
        try:
            address = 0
            # Open the file
            with open(sys.argv[1]) as f:
                # Read all the lines
                for line in f:
                    # Parse out the comments
                    comment_split = line.strip().split("#")
                    # Cast number strings to ints
                    value = comment_split[0].strip()
                    # Ignore blank lines
                    if value == "":
                        continue
                    instruction = int(value, 2)
                    # Populate a memory array
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    # In `CPU`, add method `ram_read()` and `ram_write()`
    # that access the RAM inside the `CPU` object.

  # `ram_read()` should accept the address to read and return the value stored there.

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

   
# `ram_write()` should accept a value to write, and the address to write it to.      

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
##An arithmetic logic unit (ALU)
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

              # LDI register immediate
            # Set the value of a register to an integer.
            # LDI 0b10000010 00000rrr iiiiiiii
            if IR == LDI:
                 #reg location
                self.reg[operand_a] = operand_b
                self.pc += 3

             # PRN
            # PRN register pseudo-instruction   
            elif IR == PRN:
            #Print numeric value stored in the given register
                print(self.reg[operand_a])
                self.pc += 2
            
            #MUL
            # MUL registerA registerB
            # Multiply the values in two registers together and store the result in registerA.

            elif IR == MUL:
                self.alu(IR, operand_a, operand_b)
                self.pc += 3

            #implement the System Stack and be able to run the stack.ls8 program
            #stack that can be used to store information temporarily.    
            #stack resides in main memory and typically starts at the top of memory
            #  (at a high address) and grows downward as things are pushed on.
             # PUSH register
            # Push the value in the given register on the stack.
            # PUSH 01000101 00000rrr

            elif IR == PUSH:
                # Grab the register argument
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                # Decrement the SP
                self.reg[SP] -= 1
                # Copy the value in the given register to the address pointed to by the SP.
                self.ram[self.reg[SP]] = val #stack pointer SP
                self.pc += 2

           # pop register
           # POP: "POP" the value from the top of the stack and store it in the PC.
            # pop 01000101 00000rrr
            elif IR == POP:
                # Grab the value from the top of the stack
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[SP]]
                # Copy the value from the address pointed to by SP to the given register.
                self.reg[reg] = val
                # Increment SP.
                self.reg[SP] += 1
                self.pc += 2
            
          


            # HLT
            # Halt the CPU (and exit the emulator).
            # HLT 0b00000001
            elif IR == HLT:
                sys.exit(0)
            else:
                print(f"I did not understand that command: {IR}")
                sys.exit(1)