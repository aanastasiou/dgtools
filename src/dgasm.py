#!/usr/bin/env python
"""

Usage: dgasm.py [OPTIONS] INPUT_FILE

  Command line tool to produce Digirule 2 binaries (.dgb).

  The script produces a `.dgb` file with the same name as the `.asm` in its
  input, see option `-o` to set the output file explicitly.

Options:
  -o, --output-file PATH
  --help                  Show this message and exit.

:author: Athanasios Anastasiou
:date: Mar 2020

"""
import sys
import os
import pyparsing
import pickle
import click

def get_asm_parser():
    """
    Returns the Digirule2 Assembly parser.
    
    Notes:
        
        * See inline comments for specification of the grammar
    """
    # TODO: HIGH, This grammar can parse comments as well but they are not yet enabled. Enable them.
    # Action functions to convert valid string literals to numbers
    uchar2num = lambda toks:int(toks[0])
    buchar2num = lambda toks:int(toks[0],2)
    xuchar2num = lambda toks:int(toks[0],16)
    # An identifier for labels and symbols. It must be at least 1 character, start with a letter or number and
    # can include the underscore.
    identifier = pyparsing.Regex(r"[a-zA-Z_][a-zA-Z0-9_]*")
    # A literal can be a decimal number (4,14,52), a binary number (0b100, 0b1110, 0b110100) or a hexadecimal number
    # (0x4, 0x0E, 0x34). 
    literal_uchar = pyparsing.Regex(r"[-]?[0-9][0-9]?[0-9]?").setParseAction(uchar2num)
    literal_buchar = pyparsing.Regex(r"0b[0|1]+").setParseAction(buchar2num)
    literal_xuchar = pyparsing.Regex(r"0x[0-9A-F][0-9A-F]?").setParseAction(xuchar2num)
    literal = literal_uchar ^ literal_buchar ^ literal_xuchar
    # Opcodes can accept literals or identifiers (.EQU or labels) as opcodes.
    literal_or_identifier = pyparsing.Group(literal("literal") ^ identifier("symbol"))("value_type")
    # Digirule ASM commands
    # Each succesfully parsed command is tagged by its opcode.
    asm_halt = pyparsing.Group(pyparsing.Regex(r"HALT")("cmd"))("0")
    asm_nop = pyparsing.Group(pyparsing.Regex(r"NOP")("cmd"))("1")
    asm_speed = pyparsing.Group(pyparsing.Regex(r"SPEED")("cmd") + literal_or_identifier("value"))("2")
    asm_copylr = pyparsing.Group(pyparsing.Regex("COPYLR")("cmd") + literal_or_identifier("value") + literal_or_identifier("addr"))("3")
    asm_copyla = pyparsing.Group(pyparsing.Regex(r"COPYLA")("cmd") + literal_or_identifier("value"))("4")
    asm_copyar = pyparsing.Group(pyparsing.Regex("COPYAR")("cmd") + literal_or_identifier("addr"))("5")
    asm_copyra = pyparsing.Group(pyparsing.Regex("COPYRA")("cmd") + literal_or_identifier("addr"))("6")
    asm_copyrr = pyparsing.Group(pyparsing.Regex("COPYRR")("cmd") + literal_or_identifier("addr_from") + literal_or_identifier("addr_to"))("7")
    asm_addla = pyparsing.Group(pyparsing.Regex("ADDLA")("cmd") + literal_or_identifier("value"))("8")
    asm_addra = pyparsing.Group(pyparsing.Regex("ADDRA")("cmd") + literal_or_identifier("addr"))("9")
    asm_subla = pyparsing.Group(pyparsing.Regex("SUBLA")("cmd") + literal_or_identifier("value"))("10")
    asm_subra = pyparsing.Group(pyparsing.Regex("SUBRA")("cmd") + literal_or_identifier("value"))("11")
    asm_andla = pyparsing.Group(pyparsing.Regex("ANDLA")("cmd") + literal_or_identifier("value"))("12")
    asm_andra = pyparsing.Group(pyparsing.Regex("ANDRA")("cmd") + literal_or_identifier("addr"))("13")
    asm_orla = pyparsing.Group(pyparsing.Regex("ORLA")("cmd") + literal_or_identifier("value"))("14")
    asm_orra = pyparsing.Group(pyparsing.Regex("ORRA")("cmd") + literal_or_identifier("addr"))("15")
    asm_xorla = pyparsing.Group(pyparsing.Regex("XORLA")("cmd") + literal_or_identifier("value"))("16")
    asm_xorra = pyparsing.Group(pyparsing.Regex("XORRA")("cmd") + literal_or_identifier("addr"))("17")
    asm_decr = pyparsing.Group(pyparsing.Regex("DECR")("cmd") + literal_or_identifier("addr"))("18")
    asm_incr = pyparsing.Group(pyparsing.Regex("INCR")("cmd") + literal_or_identifier("addr"))("19")
    asm_decrjz = pyparsing.Group(pyparsing.Regex("DECRJZ")("cmd") + literal_or_identifier("addr"))("20")
    asm_incrjz = pyparsing.Group(pyparsing.Regex("INCRJZ")("cmd") + literal_or_identifier("addr"))("21")
    asm_shiftrl = pyparsing.Group(pyparsing.Regex("SHIFTRL")("cmd") + literal_or_identifier("addr"))("22")
    asm_shiftrr = pyparsing.Group(pyparsing.Regex("SHIFTRR")("cmd") + literal_or_identifier("addr"))("23")
    asm_cbr = pyparsing.Group(pyparsing.Regex("CBR")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("24")
    asm_sbr = pyparsing.Group(pyparsing.Regex("SBR")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("25")
    asm_bcrsc = pyparsing.Group(pyparsing.Regex("BCRSC")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("26")
    asm_bcrss = pyparsing.Group(pyparsing.Regex("BCRSS")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("27")
    asm_jump = pyparsing.Group(pyparsing.Regex("JUMP")("cmd") + literal_or_identifier("addr"))("28")
    asm_call = pyparsing.Group(pyparsing.Regex("CALL")("cmd") + literal_or_identifier("addr"))("29")
    asm_retla = pyparsing.Group(pyparsing.Regex("RETLA")("cmd") + literal_or_identifier("value"))("30")
    asm_return = pyparsing.Group(pyparsing.Regex("RETURN")("cmd"))("31")
    asm_addrpc = pyparsing.Group(pyparsing.Regex("ADDRPC")("cmd") + literal_or_identifier("value"))("32")
    asm_command = pyparsing.Group(asm_halt ^ asm_nop ^ asm_speed ^ asm_copylr ^ asm_copyla ^ asm_copyar ^ asm_copyra ^ asm_copyrr ^ \
              asm_addla ^ asm_addra ^ asm_subla ^ asm_subra ^ asm_andla ^ asm_andra ^ asm_subla ^ asm_subra ^ \
              asm_andla ^ asm_andra ^ asm_orla ^ asm_orra ^ asm_xorla ^ asm_xorra ^ asm_decr ^ asm_incr ^ \
              asm_decrjz ^ asm_incrjz ^ asm_shiftrl ^ asm_shiftrr ^ asm_cbr ^ asm_sbr ^ asm_bcrsc ^ asm_bcrss ^ \
              asm_jump ^ asm_call ^ asm_retla ^ asm_return ^ asm_addrpc)
    asm_statement = asm_command
    # Assembler directives
    # .DB A static space delimited list of byte defs
    # label: Defines a label
    # .EQU A "symbol" (that in the future would be able to evaluate to anything.
    dir_label = pyparsing.Group(identifier("idf") + pyparsing.Suppress(":"))("def_label")
    dir_db = pyparsing.Group(pyparsing.Regex(".DB")("cmd") + pyparsing.delimitedList(literal_or_identifier)("values"))("def_db")
    dir_equ = pyparsing.Group(pyparsing.Regex(".EQU")("cmd") + identifier("idf") + pyparsing.Suppress("=") + literal("value"))("def_equ")
    # Comments
    # A line of ASM code is either a comment or code with an optional inline comment
    #dir_comment = pyparsing.Group(pyparsing.Suppress("#") + pyparsing.Regex(r".*?\n")("text"))("def_comment")
    #program_statement = pyparsing.Group((asm_statement ^ pyparsing.Group(dir_label ^ dir_db ^ dir_equ ^ dir_comment)) + pyparsing.Optional(dir_comment))
    program = pyparsing.OneOrMore(asm_statement ^ pyparsing.Group(dir_label ^ dir_db ^ dir_equ))
    #program = pyparsing.OneOrMore(program_statement)
    # program.ignore(dir_comment)
    return program    
    
def asm2obj(asm):
    """
    Assembles a binary for the Digirule target architecture from an "asm" definition.
    
    :param asm: A string of ASM commands, just as it would be read from a text file.
    :type asm: str
    :returns: A dictionary of compiled code, symbols and variable offsets
    :rtype: dict<"program":list<uint8>, "labels":dict<str, int>>, "symbols":dict<str,int>>
    """
    parser = get_asm_parser()
    # TODO: HIGH, The parser needs to be flagging parse errors along with the locations where these happened.
    parsed_code = parser.parseString(asm)
    mem = [0 for k in range(0,256)]
    mem_ptr = 0
    labels = {}
    symbols = {}
    # Read through the code and load it to memory
    # While doing that, keep track of where labels and symbols appear. These will be substituted
    # in the second pass.
    for a_line in parsed_code:
        # TODO: HIGH, To enable comments, modify how the AST is interpreted here.
        command, arguments = list(a_line.items())[0]
        if command == "def_label":
            # Tie the label to where it points to
            labels[arguments["idf"]] = mem_ptr
        elif command == "def_db":
            # .DB simply defines raw data that are simply dumped where they appear. If a label is not set to a 
            # data block, it cannot be referenced.
            value_data = list(map(lambda x:x[0],arguments["values"]))
            mem[mem_ptr:mem_ptr+len(value_data)] = value_data
            mem_ptr+=len(value_data)
        elif command == "def_equ":
            symbols[arguments["idf"]] = arguments["value"]
        else:
            # It's a command. The opcode of the command has already been recognised, but we need to grab the operands
            # wherever they are available
            numeric_command = int(command)
            mem[mem_ptr] = numeric_command
            mem_ptr+=1
            # 3 Byte opcodes
            if numeric_command in [3,7,24,25,26,27]:
                mem[mem_ptr] = arguments[1][0]
                mem[mem_ptr + 1] = arguments[2][0]
                mem_ptr+=2
            # 2 Byte opcodes
            elif numeric_command not in [0,1,31]:
                mem[mem_ptr] = arguments[1][0] 
                mem_ptr+=1
    # The first pass produces an intermediate object that still contains symbolic references.
    # This second pass here substitutes those references and produces the final object.
    symbol_offsets = {}
    subst_entries = filter(lambda x:type(x[1]) is str, enumerate(mem))
    for an_entry in subst_entries:
        if an_entry[1] in labels:
            mem[an_entry[0]] = labels[an_entry[1]]
        elif an_entry[1] in symbols:
            # Note where the symbol is used
            if an_entry[1] not in symbol_offsets:
                symbol_offsets[an_entry[1]] = []
            if an_entry[0] not in symbol_offsets[an_entry[1]]:
                symbol_offsets[an_entry[1]].append(an_entry[0])
            # Make the substitution
            mem[an_entry[0]] = symbols[an_entry[1]]
        else:
            # TODO: HIGH, Raise exception Symbol Not Found
            pass
            
    # TODO: MED, Better if this returns an already initialised machine.
    return {"program":mem, "labels":labels, "symbols":symbol_offsets}
    
@click.command()
@click.argument("input-file",type=click.Path(exists=True))
@click.option("--output-file","-o", type=click.Path())
def dgasm(input_file, output_file):
    """
    Command line tool to produce Digirule 2 binaries (.dgb).
    
    The script produces a `.dgb` file with the same name as the `.asm` in its input,
    see option `-o` to set the output file explicitly.
    
    \f
    :param input_file: The ASM file to process
    :type input_file: str<Path>
    :param output_file: The assembled .dgb file.
    :type output_file:str<Path>
    """
    if output_file is None:
        output_file = f"{os.path.splitext(input_file)[0]}.dgb"
    with open(input_file, "rt") as fd:
        asm_code_text = fd.read()
    asm_code_compiled = asm2obj(asm_code_text)
    with open(output_file, "wb") as fd:
        pickle.dump(asm_code_compiled, fd)

if __name__ == "__main__":
    dgasm()