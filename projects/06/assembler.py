import os, sys

# machine language translations of C-instructions (stored as dictionaries)

# comparison instructions
comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }


# destination instructions
dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }


# jump instructions
jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


# initialize a symbol table as a dictionary
symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    }

# add symbols to the symbol table (16-bit instruction) 
for i in range(0, 16):
    label = "R" + str(i)
    symbol_table[label] = i

next_available_mem = 16     # next available memory location has an offset of 16 from the base address
file_name = sys.argv[1]     # file to be translated


def strip_useless(file_line):
    """
    i/p :   takes a line of the input file as an argument
    o/p :   removes all trailing whitespaces and comments,
            which need to be ignored
    """
    char = file_line[0]    
    
    if char == "\n" or char == "/":
        return ""
    elif char == " ":
        return strip_useless(file_line[1:])          # ignore whitespaces
    else:
        return char + strip_useless(file_line[1:])   # otherwise


def normalize_c_ip(file_line):
    """
    i/p :   takes a line of the input file as an argument
    o/p :   add JMP and NULL destination fields in case they are
            unspecified
    """
    file_line = file_line[:-1]

    if not "=" in file_line:
        file_line = "null=" + file_line     # add NULL destination field
    if not ";" in file_line:
        file_line = file_line + ";null"     # specify JMP destination field

    return file_line


def allocate_mem(label):
    """
    i/p :   label
    o/p :   allocate memory location to variables if it hasn't
            been done already
    """
    global next_available_mem
    
    symbol_table[label] = next_available_mem       # take care of the offset value!
    next_available_mem += 1
    return symbol_table[label]


def translate_a_instr(file_line):
    """
    i/p :   takes a line of the input file as an argument
    o/p :   translated A instruction in machine language
    """
    
    if file_line[1].isalpha():
        label = file_line[1:-1]      # get instruction label
        alpha_val = symbol_table.get(label, -1)
        if alpha_val == -1:
            alpha_val = allocate_mem(label)
    else:
        alpha_val = int(file_line[1:])
    binary_val = bin(alpha_val)[2:].zfill(16)       # complete a 16-bit instruction
    return binary_val


def translate_c_instr(file_line):
    """
    i/p :   takes a line of the input file as an argument
    o/p :   translated C instruction in machine language
    """
    
    file_line = normalize_c_ip(file_line)
    temp = file_line.split("=")
    destination_code = dest.get(temp[0], "destFAIL")    # destination code translation
    temp = temp[1].split(";")
    comp_code = comp.get(temp[0], "compFAIL")           # comparison code translation
    jump_code = jump.get(temp[1], "jumpFAIL")           # jump code translation
    return comp_code, destination_code, jump_code



def a_vs_c(file_line):
    """
    i/p :   takes a line of the input file as an argument
    o/p :   calls appropriate function to translate either 
            A instructions or C instructions
    """

    if file_line[0] =="@":
        return translate_a_instr(file_line)
    else:
        instr_codes = translate_c_instr(file_line)
        return "111" + instr_codes[0] + instr_codes[1] + instr_codes[2]



def first_pass():
    """
    perform the first pass on the assembly code (add all 
    label symbols)
    """
    
    ip_file = open(file_name + ".asm")
    op_file = open(file_name + ".tmp", "w")

    line_number = 0
    for line in ip_file:
        stripped_line = strip_useless(line)
        if stripped_line != "":
            if stripped_line[0] == "(":
                label = stripped_line[1:-1]
                symbol_table[label] = line_number
                stripped_line = ""
            else:
                line_number += 1
                op_file.write(stripped_line + "\n")

    ip_file.close()
    op_file.close()


def assemble():
    """
    takes the '.tmp' file and translates it into '.hack'
    """
    ip_file = open(file_name + ".tmp")
    op_file = open(file_name + ".hack", "w")

    for line in ip_file:
        translated_line = a_vs_c(line)
        op_file.write(translated_line + "\n")

    ip_file.close()
    op_file.close()
    os.remove(file_name + ".tmp")


# literally just these two bad boys
first_pass()
assemble()
