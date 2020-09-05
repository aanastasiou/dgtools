#!/usr/bin/env python
"""

Usage: dgasm.py [OPTIONS] INPUT_FILE

    Command line tool to produce Digirule binaries (.dgb).

    The script produces a `.dgb` file with the same name as the `.asm` in its
    input, see option `-o` to set the output file explicitly.

Options:
    -o, --output-file PATH
    
    -g, --target [2A|2U]    Selects the target digirule model to generate code for

    --help                  Show this message and exit.

:author: Athanasios Anastasiou
:date: Mar 2020

"""
import sys
import os
import click
import intelhex
from dgtools import (DgtoolsError, DgtoolsErrorASMSyntaxError,
                     DGB_Archive, Digirule, Digirule2U, BUILTIN_MODELS, DgAssembler)
                     
@click.command()
@click.argument("input-file",type=click.Path(exists=True))
@click.option("--output-file","-o", type=click.Path())
@click.option("--target", "-g", type=click.Choice(["2A", "2U"],case_sensitive=False), default="2A",
              help="Selects the target digirule model to generate code for")
def dgasm(input_file, output_file, target):
    """
    Command line tool to produce Digirule binaries (.dgb).
    
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
    # Pick up the digirule model
    target_digirule = BUILTIN_MODELS[target]
    # Instantiate an assembler
    assembler = DgAssembler(target_digirule)
    
    if output_file is None:
        output_file = f"{os.path.splitext(input_file)[0]}.dgb"
    
    with open(input_file, "rt") as fd:
        asm_code_text = fd.read()
        
    # Parse
    try:
        asm_code_ast = assembler.text_to_ast(asm_code_text)
    except DgtoolsError as deas:
        print(f"dgasm: File {input_file}: {deas}")
        sys.exit(-1)
    
    # Compile    
    try:
        asm_code_compiled = assembler.asm_ast_to_obj(asm_code_ast)
    except DgtoolsError as dge:
        print(f"dgasm: File {input_file}: {dge}")
        sys.exit(-1)
    
    # Save     
    dgb_archive = DGB_Archive(asm_code_compiled["program"], asm_code_compiled["labels"], version=target)
    dgb_archive.save(output_file)

    if target == "2U":
        # Save the HEX binary too
        ihex = intelhex.IntelHex()
        for an_address, a_byte in enumerate(asm_code_compiled["program"]):
            ihex[an_address] = a_byte
        ihex.write_hex_file(f"{os.path.splitext(output_file)[0]}.hex")
        
if __name__ == "__main__":
    dgasm()
