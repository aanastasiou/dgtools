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
@click.option("--target", "-g", type=click.Choice(["2A","2B", "2U"],case_sensitive=False), default="2A")
def dgasm(input_file, output_file, target):
    """
    Command line tool to produce Digirule 2 binaries (.dgb).
    
    The script produces a `.dgb` file with the same name as the `.asm` in its input,
    see option `-o` to set the output file explicitly.
    
    \f
    :param input_file: The ASM file to process
    :type input_file: str<Path>
    :param output_file: The assembled .dgb file.
    :type output_file:str<Path>
    :param target: The Digirule model to generate code for, default is 2A.
    :type target: str [2A,2B,2U]
    """
    
    #TODO: HIGH, The model lookup table should be shared between dgasm, dgsim
    target_digirule = {"2A":Digirule}[target]
    
    if output_file is None:
        output_file = f"{os.path.splitext(input_file)[0]}.dgb"
    
    with open(input_file, "rt") as fd:
        asm_code_text = fd.read()
    
    parser = target_digirule.get_asm_parser()
    
    try:
        parsed_code = parser.parseString(asm_code_text, parseAll=True)
    except pyparsing.ParseException as e:
        print(f"  File \"{input_file}\", line {e.lineno}, col {e.col}")
        print(f"    {e.line}")
        print(f"Syntax Error: {e.args[2]}")
        sys.exit(1)
        
    asm_code_compiled = asm_ast_to_obj(parsed_code)
            
    dgb_archive = DGB_Archive(asm_code_compiled["program"], asm_code_compiled["labels"], version=target)
    dgb_archive.save(output_file)
        
if __name__ == "__main__":
    dgasm()
