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
from dgtools.exceptions import DgtoolsErrorSymbolAlreadyDefined, DgtoolsErrorSymbolUndefined
from dgtools.dgb_archive import DGB_Archive
from dgtools import Digirule

def get_asm_parser():
    """
    Returns the Digirule2 Assembly parser.
    
    Notes:
        
        * See inline comments for specification of the grammar
    """
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
    prog_or_dir_statement = pyparsing.Group(asm_statement ^ pyparsing.Group(dir_label ^ dir_db ^ dir_equ))("prog_dir_statement")
    dir_comment = pyparsing.Group(pyparsing.Suppress("#") + pyparsing.Regex(r".*?\n")("text"))("def_comment")
    dir_code_comment = pyparsing.Group(dir_comment ^ (prog_or_dir_statement + pyparsing.Optional(dir_comment)))
    program = pyparsing.OneOrMore(dir_code_comment)
    # In the end, ignore the comments.
    program.ignore(dir_comment)
    return program 
       
def asm_ast_to_obj(parsed_code):
    """
    Transforms the parsed AST to a binary for the Digirule target architecture
    
    :param asm: Parsed ASM text, EXCLUDING COMMENT tags.
    :type asm: list<pyparsing.ParseElement>
    :returns: A dictionary of compiled code, symbols and variable offsets or the parsexception at failure
    :rtype: dict<"program":list<uint8>, "labels":dict<str, int>>, "symbols":dict<str,int>>, pyparsing.ParseException
    """
    mem = [0 for k in range(0,256)]
    mem_ptr = 0
    labels = {}
    symbols = {}
    # Read through the code and load it to memory
    # While doing that, keep track of where labels and symbols appear. These will be substituted
    # in the second pass.
    for a_line in parsed_code:
        command, arguments = list(a_line["prog_dir_statement"][0].items())[0]
        if command == "def_label":
            # Tie the label to where it points to
            if arguments["idf"] not in labels:
                labels[arguments["idf"]] = mem_ptr
            else:
                raise DgtoolsErrorSymbolAlreadyDefined(f"Label {arguments['idf']} is getting redefined.")
        elif command == "def_db":
            # .DB simply defines raw data that are simply dumped where they appear. If a label is not set to a 
            # data block, it cannot be referenced.
            value_data = list(map(lambda x:x[0],arguments["values"]))
            mem[mem_ptr:mem_ptr+len(value_data)] = value_data
            mem_ptr+=len(value_data)
        elif command == "def_equ":
            if arguments["idf"] not in symbols:
                symbols[arguments["idf"]] = arguments["value"]
            else:
                raise DgtoolsErrorSymbolAlreadyDefined(f"Symbol {arguments['idf']} is getting redefined")
        else:
            # It's an instruction. The opcode of the instruction has already been recognised, 
            # but we need to grab the operands wherever they are available
            inst_data = command.split(":")
            instruction_code = int(inst_data[0])
            instruction_num_op = int(inst_data[1])
                        
            mem[mem_ptr] = instruction_code
            mem_ptr+=1
            if instruction_num_op>0:
                mem[mem_ptr:(mem_ptr+instruction_num_op)] = list(map(lambda x:x[0], 
                                                                     arguments[1:(1+instruction_num_op)])) 
                mem_ptr+=instruction_num_op
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
            raise DgtoolsErrorSymbolUndefined(f"Symbol {an_entry[1]} not found.")
            
    return {"program":mem, "labels":labels}
    
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
    
    # parser = get_asm_parser()
    parser = Digirule.get_asm_parser()
    
    try:
        parsed_code = parser.parseString(asm_code_text, parseAll=True)
    except pyparsing.ParseException as e:
        print(f"  File \"{input_file}\", line {e.lineno}, col {e.col}")
        print(f"    {e.line}")
        print(f"Syntax Error: {e.args[2]}")
        sys.exit(1)
        
    asm_code_compiled = asm_ast_to_obj(parsed_code)
            
    dgb_archive = DGB_Archive(asm_code_compiled["program"], asm_code_compiled["labels"])
    dgb_archive.save(output_file)
        
if __name__ == "__main__":
    dgasm()
