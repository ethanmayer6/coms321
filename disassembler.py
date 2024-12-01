# ADD
# ADDI
# AND
# ANDI
# B
# B.cond: This is a CB instruction in which the Rt field is not a register, but
#         a code that indicates the condition extension. These have the values
#         (base 16):
#         0: EQ
#         1: NE
#         2: HS
#         3: LO
#         4: MI
#         5: PL
#         6: VS
#         7: VC
#         8: HI
#         9: LS
#         a: GE
#         b: LT
#         c: GT
#         d: LE
# BL
# BR: The branch target is encoded in the Rn field.
# CBNZ
# CBZ
# EOR
# EORI
# LDUR
# LSL: This instruction uses the shamt field to encode the shift amount, while
#      Rm is unused.
# LSR: Same as LSL.
# ORR
# ORRI
# STUR
# SUB
# SUBI
# SUBIS
# SUBS
# MUL
# PRNT: This is an added instruction (part of our emulator, but not part of LEG
#       or ARM) that prints a register name and its contents in hex and
#       decimal.  This is an R instruction.  The opcode is 11111111101.  The
#       register is given in the Rd field.
# PRNL: This is an added instruction that prints a blank line.  This is an R
#       instruction.  The opcode is 11111111100.
# DUMP: This is an added instruction that displays the contents of all
#       registers and memory, as well as the disassembled program.  This is an
#       R instruction.  The opcode is 11111111110.
# HALT: This is an added instruction that triggers a DUMP and terminates the
#       emulator.  This is an R instruction.  The opcode is 11111111111




# sh run.sh legv8_binary_file

class Instruction():

    def __init__(self, binary, opcode, type, rd, rm, rn, shamt):
        self.binary = binary
        self.opcode = opcode
        self.type = type
        self.rd = rd
        self.rm = rm
        self.rn = rn
        self.shamt = shamt


def disassembler(filename):
    print("test")

def disassemble_instruction(Instruction i):

    print(i.getOpcode())

def binary_to_instruction(binary):

   i = Instruction(binary, opcode, type, rd, rm, rn, shamt)
    return i