import sys

PRINT_BEEJ     = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4  # Save a value to a register
PRINT_REGISTER = 5  # Print a value from a register
ADD            = 6  # regA += regB

memory = [
  PRINT_BEEJ,
  SAVE, #instruction 4 -Save value 65 in register2
  65, #value 65
  2, #register number 2
  SAVE,
  20,
  3,
  ADD,
  2,
  3,
  PRINT_REGISTER, #print register 2
  2, #register number
  HALT
]

#an array of 8 zeros 
register = [0] * 8

pc = 0
running = True

while running:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1

    elif command == HALT:
        running = False
        pc += 1

    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2

    elif command == SAVE: #pc where instruction is
        num = memory[pc + 1]#value -pc+1 where value is
        reg = memory[pc + 2]#register number -pc+2 is register number
        register[reg] = num #at this undex, store this value
        pc += 3 # 3 byte instruction, add 3

    elif command == PRINT_REGISTER:
        reg = memory[pc + 1] #register number, memory directly after pc, next index down
        print(register[reg]) #print value in register
        pc += 2 #2 byte instruction

    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3

    else:
        print(f"Unknown instruction: {command}")
        sys.exit(1)



