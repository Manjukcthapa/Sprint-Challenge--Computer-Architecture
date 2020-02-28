"""CPU functionality."""
import sys
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
    #  Add list properties to the `CPU` class to hold 256 bytes of memory
    # and 8 general-purpose registers.
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 255
        self.sp = self.reg[7]
        self.flag = 0b00000000 #flag starts out as "0"
    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, address, value):
        self.ram[address] = value

    #  # op dictionary
    #     self.op_table = {}
    #     self.op_table[0b10000010] = self.op_ldi
    #     self.op_table[0b01000111] = self.op_prn
    #     self.op_table[0b00000001] = self.op_hlt
    #     self.op_table[0b01000101] = self.op_push
    #     self.op_table[0b01000110] = self.op_pop
    #     self.op_table[0b00010001] = self.op_ret
    #     self.op_table[0b01010000] = self.op_call
    #     self.op_table[0b01010100] = self.op_jmp
    #     self.op_table[0b01010101] = self.op_jeq
    #     self.op_table[0b01010110] = self.op_jne    


    def load(self):
        """Load a program into memory."""
    # sys.argv is a list in Python, which contains the command-line arguments passed to the script.
        address = 0
        if len(sys.argv) != 2:
            print(f"usage: {sys.argv[0]} filename")
            sys.exit(1)
        try:
          # Open the file
            with open(sys.argv[1]) as f:
                # Read all the lines
                for line in f:
                # Cast number strings to ints
                    value = line.split('#', 1)[0]
                    # Ignore blank lines
                    if value.strip() == '':
                        continue
                    self.ram[address] = int(value, 2)
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]  
            
        elif op == "CMP":
            value_1 = self.reg[reg_a]
            value_2 = self.reg[reg_b]
            if value_1 > value_2:
                self.flag = 0b00000010 #sets flag to "2"
            elif value_1 == value_2:
                self.flag = 0b00000001 #sets flag to "1"
            elif value_1 < value_2:
                self.flag = 0b00000100 #sets flag to "4"
        else:
            raise Exception("Unsupported ALU operation")
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()
    def run(self):
        """Run the CPU."""
        running = True
        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            number_of_operands = int(IR) >> 6
            self.pc += (1 + number_of_operands)

            # LDI: "LOAD IMMEDIATE" Set the value of a register to an integer.
            # Set the value of a register to an integer.
            # LDI 0b10000010 00000rrr iiiiiiii
            if IR == LDI:
                self.reg[operand_a] = operand_b

            # HLT: "HALT" the CPU.
            elif IR == HLT:
                running = False

            # PRN: "PRINT" numeric value stored in the given register.
             # PRN register pseudo-instruction
            elif IR == PRN:
                 #Print numeric value stored in the given register
                print( self.reg[operand_a] )

            # MUL: "MULTIPLY" the values in two registers together and store the result in registerA.
            elif IR == MUL:
                self.reg[operand_a] *= self.reg[operand_b]

            # PUSH: "PUSH" the value in the given register on the stack.
            elif IR == PUSH:
                self.sp = (self.sp % 257) - 1
                self.ram[self.sp] = self.reg[operand_a]

            # POP: "POP" the value from the top of the stack and store it in the PC.
            elif IR == POP:
                self.reg[operand_a] = self.ram[self.sp]
                self.sp = (self.sp % 257) + 1

            # CMP: "COMPARE" the results in memory and change the flag is accordance to the result
            elif IR == CMP:
                self.alu("CMP", operand_a, operand_b)

            # CALL: we "CALL" the location of the register in memory so we can jump to in the subroutine
            elif IR == CALL:
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2

            # RET: "RETURN" the procedure from the value from the top of the stack and store it in the PC.
            elif IR == RET:
                self.pc = self.ram[self.sp]

            # JMP: ALWAYS "JUMP" to the address stored in the given register
            elif IR == JMP:
                address = self.reg[operand_a]
                self.pc = address

            # JEQ: "JUMP IF EQUAL" If the flag result is == 0 then jump to the address stored in the given 
            # register
            elif IR == JEQ:
                if self.flag == 0b00000001:
                #n that flag is currently "0" and if it's equal to "1"
                #  it jumps here but this JEQ works when it's techically false
                # this "1" is currently the number for "HLT" 
                    address = self.reg[operand_a]
                    self.pc = address

            # JNE: "JUMP IF NOT EQUAL" if flag DOESN"T != 0 then jump to the address stored in the given 
            # register.
            elif IR == JNE:
                if self.flag & 0b00000001 == 0b00000000:
                    # opposite of the "JEQ" nad it worked but it should only jump 
                    # when it's NOT equal to "0" 
                    address = self.reg[operand_a]
                    self.pc = address