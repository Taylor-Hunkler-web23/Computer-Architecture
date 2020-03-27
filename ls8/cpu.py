"""CPU functionality."""

import sys
# print(sys.argv, "arg")

#op codes, representing the bytes in memory
LDI = 0b10000010 #LDI: load "immediate", store a value in a register, or "set this register to this value".
PRN = 0b01000111 #print: : a pseudo-instruction that prints the numeric value stored in a register.
HLT = 0b00000001 #halt: halt the CPU and exit the emulator.
MUL = 0b10100010 #MUL: multipy registerA registerB
PUSH = 0b01000101 #PUSH:Push the value in the given register on the stack.
POP = 0b01000110 #POP:Pop the value at the top of the stack into the given register.
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111 #Compare the values in two registers
JMP= 0b01010100  #Jump to the address stored in the given register.
JEQ = 0b01010101 #If equal flag is set (true), jump to the address stored in the given register.
JNE = 0b01010110 #If E flag is clear (false, 0), jump to the address stored in the given register.





#stack pointer
SP=7




class CPU:
    """Main CPU class."""



    def __init__(self):
        """Construct a new CPU."""
        
    #Add list properties to the CPU class to hold 256 bytes of memory
        self.ram = [0] * 256

     # and 8 general-purpose registers
        self.reg =[0] * 8

        #Also add properties for any internal registers you need, e.g. PC.
        #program counter  
        self.pc = 0
        # self.sp=7

        #equal than flag
        self.equal = 0
        #less than flag
        self.lessThan = 0
        #greater than flag
        self.greaterThan = 0

        






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
            self.reg[reg_a] *= self.reg[reg_b]

#CMP- This is an instruction handled by the ALU.
#Compare the values in two registers.
        elif op == "CMP":

# If they are equal, set the Equal E flag to 1, otherwise set it to 0.
            if self.reg[reg_a] == self.reg[reg_b]:
                self.equal = 1

# If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
            if self.reg[reg_a] < self.reg[reg_b]:
                self.lessThan = 1

# If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
            if self.reg[reg_a] > self.reg[reg_b]:
                self.greaterThan = 1

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

            #shifts bits to read first two numbers of opcode
            # first2 = ir>>6
            
            

            #Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            opperand_a = self.ram_read(self.pc+1) #reg index
            # print(opperand_a,'A')
            opperand_b = self.ram_read(self.pc+2) # value 
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

            elif ir ==ADD:

                self.alu("ADD", opperand_a,opperand_b)
                self.pc +=3

        #CMP
            elif ir == CMP:
                self.alu("CMP", opperand_a, opperand_b)

                #3 byte instruction
                self.pc +=3
                
        #JMP
            elif ir == JMP:
            #Set the PC to the address stored in the given register.
                self.pc = self.reg[opperand_a]

        #JEQ
            elif ir == JEQ:
                #if the equal flag is set to true
                if self.equal == 1:
                #set the PC to the address stored in the given register
                    self.pc = self.reg[opperand_a]
                else:
                    #else increment by 2
                    self.pc +=2
               
        #JNE
            elif ir == JNE:
        # if the equal flag is false
                if self.equal == 0:
        #set the PC to the address stored in the given register
                    self.pc = self.reg[opperand_a]
                else:
                #else increment by 2
                    self.pc +=2
                  


            elif ir ==PRN:
               
                #Print numeric value stored in the given register.
                print(self.reg[opperand_a])
                
              #2 byte instruction
                self.pc +=2

            #storing on the stack
            elif ir == PUSH:
                # SP=self.sp
                #register number
                reg = self.ram[self.pc + 1]
                #value in register
                val = self.reg[reg]
                # Decrement the SP.
                self.reg[SP] -= 1
                # Copy the value in the given register to the address pointed to by SP.
                self.ram[self.reg[SP]] = val
                #2 byte instruction, add 2 program counter
                self.pc += 2
# 10101
# 10011 
# 10001 and
# 10111 or
# 00110 xor

        #removing from the stack
            elif ir == POP:
                #pop it into this register address
                reg = self.ram[self.pc + 1]
                #wherever stack pointer is pointing, get value out of memory
                val = self.ram[self.reg[SP]]
                # Copy the value from the address pointed to by SP to the given register.
                self.reg[reg] = val
                # Increment SP.
                self.reg[SP] += 1
                #2 byte instruction
                self.pc += 2


            elif ir == CALL:
                # The address of the instruction directly after CALL is pushed onto the stack.
                # This allows us to return to where we left off when the subroutine finishes executing.

                #decrement SP
                self.reg[SP] -= 1

                # push return address on stack, return address = pc+2
                self.ram[self.reg[SP]] = self.pc + 2

                # The PC is set to the address stored in the given register.
                # We jump to that location in RAM and execute the first instruction in the subroutine.
                # The PC can move forward or backwards from its current location.

                #set the pc to value in register
                reg = self.ram[self.pc + 1]
                #set pc to value in register
                self.pc = self.reg[reg]

            elif ir == RET:
                # Return from subroutine.
                # Pop the value from the top of the stack 
                self.pc = self.ram[self.reg[SP]]
                #and store it in the PC.
                self.reg[SP] += 1

            
            elif ir == HLT:
                print("Stop run")
                running = False
                sys.exit

            else:
                print("Unknown instruction")
                sys.exit

            #increments pc by first 2 numbers of op code +1
            # self.pc += first2 +1
