"""CPU functionality."""

import sys
print(sys.argv, "arg")
#op codes, representing the bytes in memory
LDI = 0b10000010 #LDI: load "immediate", store a value in a register, or "set this register to this value".
PRN = 0b01000111 #print: : a pseudo-instruction that prints the numeric value stored in a register.
HLT = 0b00000001 #halt: halt the CPU and exit the emulator.
MUL = 0b10100010
class CPU:
    """Main CPU class."""



    def __init__(self):
        """Construct a new CPU."""
        
    #Add list properties to the CPU class to hold 256 bytes of memory
        self.ram = [0] * 256

     # and 8 general-purpose registers
        self.reg =[0] * 8

        #Also add properties for any internal registers you need, e.g. PC.
        self.pc = 0






    def load(self, filename):

        
        """Load a program into memory."""
#address to write at
        address = 0
       

        
        try:

            with open(filename) as f:
                for line in f:

                    # Ignore comments
                    comment_split = line.split("#")

                    # Strip out whitespace
                    num = comment_split[0].strip()

                    # Ignore blank lines
                    if num == '':
                        continue

                    val = int(num, 2) #base 2
                    self.ram[address] = val
                    address += 1
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    # filename = sys.argv[1]
    # load(filename)


        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
#memory at the address
            


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        elif op == "MUL":
        #Multiply the values in two registers together and store the result in registerA.
            self.reg[reg_a] =(self.reg[reg_a] * self.reg[reg_b])
        else:
            raise Exception("Unsupported ALU operation")


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
#The MAR contains the address that is being read or written to. 
# The MDR contains the data that was read or the data to write.
#ram_read() should accept the address to read and return the value stored there.
    def ram_read(self,MAR):
        return self.ram[MAR]
        
        
#raw_write() should accept a value to write, and the address to write it to.   
# store data in address    
    def ram_write(self,MDR, MAR):
         self.ram[MAR] =MDR


    def run(self):   


        running =True
        while running:         
                   
            #It needs to read the memory address that’s stored in register PC, and store that result in IR,
            ir = self.ram_read(self.pc) #instruction register

            #Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            opperand_a = self.ram_read(self.pc+1) #reg index
            # print(opperand_a,'A')
            opperand_b = self.ram_read(self.pc+2) # value 8
            # print(opperand_b,'B')

            """Run the CPU."""
            if ir == LDI:
                #store 8 in reg index 0
                self.reg[opperand_a]= opperand_b
                #3 byte instruction
                self.pc +=3

            elif ir ==MUL:              
            #MUL
                self.alu("MUL", opperand_a,opperand_b)

            #3 byte instruction               
                self.pc +=3


            elif ir ==PRN:
               
                # reg=self.ram_read(self.pc+1) 
                #Print numeric value stored in the given register.
                print(self.reg[opperand_a])
              #2 byte instruction
                self.pc +=2

            elif ir == HLT:
                print("Stop run")
                running = False
                sys.exit

            else:
                print("Unknown instruction")
                sys.exit
