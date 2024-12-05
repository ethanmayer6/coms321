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

import datetime
import sys

OPCODES = {
    0b10001011000: "ADD",     # R
    0b1001000100: "ADDI",     # I
    0b10001010000: "AND",     # R
    0b1001001000: "ANDI",     # I
    0b000101: "B",            # B
    0b100101: "BL",           # B
    0b11010110000: "BR",      # R
    0b10110101: "CBNZ",       # CB
    0b10110100: "CBZ",        # CB
    0b11001010000: "EOR",     # R
    0b1101001000: "EORI",     # I
    0b11111000010: "LDUR",    # D
    0b11010011011: "LSL",     # R
    0b11010011010: "LSR",     # R
    0b10101010000: "ORR",     # R
    0b1011001000: "ORRI",     # I
    0b11111000000: "STUR",    # D
    0b11001011000: "SUB",     # R
    0b1101000100: "SUBI",     # I
    0b1111000100: "SUBIS",    # I
    0b11101011000: "SUBS",    # R
    0b10011011000: "MUL",     # R
    0b11111111101: "PRNT",    # R
    0b11111111100: "PRNL",    # R
    0b11111111110: "DUMP",    # R
    0b11111111111: "HALT",    # R
}

OPCODE_TYPES = {
    0b10001011000: "R",
    0b1001000100: "I",
    0b10001010000: "R",
    0b1001001000: "I",
    0b000101: "B",
    0b100101: "B",
    0b11010110000: "R",
    0b10110101: "CB",
    0b10110100: "CB",
    0b11001010000: "R",
    0b1101001000: "I",
    0b11111000010: "D",
    0b11010011011: "R",
    0b11010011010: "R",
    0b10101010000: "R",
    0b1011001000: "I",
    0b11111000000: "D",
    0b11001011000: "R",
    0b1101000100: "I",
    0b1111000100: "I",
    0b11101011000: "R",
    0b10011011000: "R",
    0b11111111101: "R",
    0b11111111100: "R",
    0b11111111110: "R",
    0b11111111111: "R",
}


CONDITION_EXTENSIONS = {
    0b0: ".EQ",
    0b1: ".NE",
    0b10: ".HS",
    0b11: ".LO",
    0b100: ".MI",
    0b101: ".PL",
    0b110: ".VS",
    0b111: ".VC",
    0b1000: ".HI",
    0b1001: ".LS",
    0b1010: ".GE",
    0b1011: ".LT",
    0b1100: ".GT",
    0b1101: ".LE",
}
# sh run.sh legv8_binary_file

labels = []

class Instruction():

    def __init__(self, binary, opcode, type, rd, rm, rn, rt, shamt, immediate, address, op, label, condition_extension):
        self.binary = binary
        self.opcode = opcode
        self.type = type
        self.rd = rd
        self.rm = rm
        self.rn = rn
        self.rt = rt
        self.shamt = shamt
        self.immediate = immediate
        self.address = address
        self.op = op
        self.label = label
        self.condition_extension = condition_extension

    def __init__(self, binary):
        self.binary = binary
        self.opcode = None
        self.type = None
        self.rd = None
        self.rm = None
        self.rn = None
        self.rt = None
        self.shamt = None
        self.immediate = None
        self.address = None
        self.op = None
        self.label = None
        self.condition_extension = None



    def printFormat(self, instruction_count):

        type = self.type

        if (type == "R"):
            if(self.opcode == "PRNT" or self.opcode == "PRNL" or self.opcode == "DUMP" or self.opcode == "HALT"):
                return str(self.opcode) + "\n"
            if (self.opcode == "BR"):
                return str(self.opcode) + " X" + str(self.rn) + "\n"
            if(self.shamt is not None):
                return str(self.opcode) + " X" + str(self.rd) + ", X" + str(self.rn) + ", #" + str(self.shamt) + "\n"
            return str(self.opcode) + " X" + str(self.rd) + ", X" + str(self.rn) + ", X" + str(self.rm) + "\n"
        elif (type == "I"):
            return str(self.opcode) + " X" + str(self.rd) + ", X" + str(self.rn) + ", #" + str(self.immediate) + "\n"
        elif (type == "D"):
            return str(self.opcode) + " X" + str(self.rt) + ", [X" + str(self.rn) + ", #" + str(self.address) + "]\n"
        elif (type == "B"):
            return str(self.opcode) + " " + str(self.address + instruction_count) + "\n"
        elif (type == "CB"):
            return str(self.opcode) + "." + str(self.condition_extension) + " " + str(self.address) + "\n"

        return "--error"


def find_opcode(instruction):
    i = 1
    while i <= 12:
        opcode = (instruction.binary >> (32 - i)) & ((1 << i) - 1)
        print(opcode)
        if opcode in OPCODES:
            print("Found opcode in OPCODES: " + str(OPCODES[opcode]))
            instruction.opcode = OPCODES[opcode]
        i += 1

def find_type(instruction):
    i = 1
    while i <= 12:
        opcode = (instruction.binary >> (32 - i)) & ((1 << i) - 1)
        print(opcode)
        if opcode in OPCODE_TYPES:
            print("Found type: " + str(OPCODE_TYPES[opcode]))
            instruction.type = OPCODE_TYPES[opcode]
        i += 1


def disassemble_instructions(instructions):

    for instruction in instructions:
        print(instruction.binary)
        find_opcode(instruction)
        find_type(instruction)

        if(instruction.type == "R"):
            instruction.rm = (instruction.binary >> 16) & 0b11111
            instruction.shamt = (instruction.binary >> 10) & 0b111111
            instruction.rn = (instruction.binary >> 5) & 0b11111
            instruction.rd = (instruction.binary >> 0) & 0b11111
        elif(instruction.type == "I"):
            instruction.immediate = (instruction.binary >> 10) & 0b1111111111111
            instruction.rn = (instruction.binary >> 5) & 0b11111
            instruction.rd = (instruction.binary >> 0) & 0b11111
        elif(instruction.type == "D"):
            instruction.address = (instruction.binary >> 12) & 0b111111111
            instruction.op = (instruction.binary >> 10) & 0b11
            instruction.rn = (instruction.binary >> 5) & 0b11111
            instruction.rt = (instruction.binary >> 0) & 0b11111
        elif(instruction.type == "B"):
            instruction.address = (instruction.binary >> 0) & 0b11111111111111111111111111
            # for label in labels:
            #     if(instruction.address == label[0]):
            #         instruction.label = label[1]
            # if(instruction.label == None):
            #     labels.append((instruction.address, "L" + str(len(labels))))
            #     instruction.label = labels[len(labels) - 1][1]
            if(instruction.address >= 33554432):
                instruction.address = instruction.address - 67108864

        elif(instruction.type == "CB"):
            instruction.address = (instruction.binary >> 5) & 0b1111111111111111111
            instruction.rt = (instruction.binary >> 0) & 0b11111
            if(instruction.opcode == 0b01010100):
                instruction.condition_extension = CONDITION_EXTENSIONS[instruction.rt]

def test_case():

    instr = []
    instruction_r = Instruction(0b10001011000001010000000101001111)
    instruction_i = Instruction(0b10010001000000101010100101001001)
    instruction_d = Instruction(0b11111000010000010000000001000001)
    instruction_b = Instruction(0b00010100000000000000100000000000)
    instruction_cb =Instruction(0b10110100000000000000100000000001)
    instr.append(instruction_r)
    instr.append(instruction_i)
    instr.append(instruction_d)
    instr.append(instruction_b)
    instr.append(instruction_cb)

    disassemble_instructions(instr)

def debug_results(instructions):

    for i in instructions:
        if(i.type == "R"):
            print(i.binary)
            print(i.opcode)
            print(i.type)
            print(i.rm)
            print(i.shamt)
            print(i.rn)
            print(i.rd)
        elif(i.type == "I"):
            print(i.binary)
            print(i.opcode)
            print(i.type)
            print(i.immediate)
            print(i.rn)
            print(i.rd)
        elif(i.type == "D"):
            print(i.binary)
            print(i.opcode)
            print(i.type)
            print(i.address)
            print(i.op)
            print(i.rn)
            print(i.rt)
        elif(i.type == "B"):
            print(i.binary)
            print(i.opcode)
            print(i.type)
            print(i.address)
        elif(i.type == "CB"):
            print(i.binary)
            print(i.opcode)
            print(i.type)
            print(i.address)
            print(i.rt)
        else:
            print("Type not accounted for!!")

def assembly_writer(instructions):
    with open("disassembler_output.legv8asm", "x") as f:
        instruction_count = 0
        for instruction in instructions:
            instruction_count += 1
            f.write(instruction.printFormat(instruction_count))


def disassembler(filename):

    instructions = []

    with open(filename, 'rb') as f:
        while True:
            try:
                read_in = f.read(4)
                if not read_in:
                    break
                instruction_binary = int.from_bytes(read_in, 'big')
                instructions.append(Instruction(instruction_binary))
                print("Instruction added")
            except Exception as e:
                print("Ruh roh Raggy")

    disassemble_instructions(instructions)

    #debug_results(instructions)
    instruction_count = 0
    for i in instructions:
        instruction_count += 1
        print(i.printFormat(instruction_count))

    assembly_writer(instructions)


#disassembler("assignment1.legv8asm.machine")
disassembler(sys.argv[1])
