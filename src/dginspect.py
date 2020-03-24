#!/usr/bin/env python
"""

Usage: dginspect.py [OPTIONS] INPUT_FILE

  Command line tool to inspect and modify .dgb files.

  If modifying the .dgb file, a backup (.bak) with the version prior to
  applying the modifications  is created automatically. To turn this
  functionality off, see option `--no-backup`

Options:
  -g, --get-mem <TEXT INTEGER INTEGER>...
                                  Get a memory range (defined as ADDR(INT)
                                  LENGTH(INT) in bytes and label it by TEXT.

  -s, --set-mem <INTEGER INTEGER>...
                                  Set a memory value (as Address, Value).
  -sy, --set-sym <TEXT INTEGER>...
                                  Set a symbol (Defined with .EQU) to a new
                                  value.

  -nb, --no-backup                If set then no backup file is created.
  --help                          Show this message and exit.


:author: Athanasios Anastasiou
:date: Mar 2020
"""

import sys
import os
import pickle
import click
from dgsim import mem_dump

@click.command()
@click.argument("input-file", type=click.Path(exists=True))
@click.option("--get-mem","-g", multiple=True, type=(str, int, int), nargs=3, 
              help="Get a memory range (defined as ADDR(INT) LENGTH(INT) in bytes and label it by TEXT.")
@click.option("--set-mem","-s",multiple=True, type=(int, int), nargs=2, 
              help="Set a memory value (as Address, Value).")
@click.option("--set-sym","-sy", multiple=True, type=(str, int), nargs=2, 
              help="Set a symbol (Defined with .EQU) to a new value.")
@click.option("--no-backup", "-nb", is_flag=True, 
              help="If set then no backup file is created.")
def dginspect(input_file, get_mem, set_mem, set_sym, no_backup):
    """
    Command line tool to inspect and modify .dgb files.
    
    If modifying the .dgb file, a backup (.bak) with the version prior to applying the modifications 
    is created automatically. To turn this functionality off, see option `--no-backup`
    
    \f
    :param input_file: The .dgb file to inspect
    :type input_file: str<Path>
    :param get_mem: Iterable of memory offset:length locations to retrieve, along with their names
    :type get_mem: tuple<tuple<str, int, int>>
    :param set_mem: Iterable of memory offset:value to modify in memory.
    :type set_mem: tuple<tuple<int,int>>
    :param set_sym: Iterable of symbol:value to modify in memory.
    :type set_sym: tuple<tuple<str,int>>
    :param no_backup: By default, this function creates a backup file if it were to modify memory. This option turns 
                     backups off.
    """
    # TODO: HIGH, get_mem, set_mem, set_sym needs further validation
    # TODO: LOW, DGBArchive can become a separate entity and reduce duplication of checks.
    with open(input_file, "rb") as fd:
        compiled_program = pickle.load(fd)
        
    if type(compiled_program) is not dict:
        raise DgtoolsErrorDgbarchiveCorrupted(f"Archive corrupted.")
    
    if len(set(compiled_program) - {"program", "labels", "symbols"}) != 0:
        raise DgtoolsErrorDgbarchiveCorrupted(f"Archive corrupted.")        

    sys.stdout.write(f"Inspecting {input_file}\n")
    sys.stdout.write(f"Program:\n{compiled_program['program']}\n\n")
    sys.stdout.write(f"Label offsets:\n{compiled_program['labels']}\n\n")
    sys.stdout.write(f"Static symbol offsets:\n{compiled_program['symbols']}\n\n")
    
    if len(get_mem)>0:
        # Build the get mem symbols here
        mem_vals = ""
        for a_symbol in get_mem:
            mem_vals+=f"{a_symbol[0]}: {compiled_program['program'][a_symbol[1]:(a_symbol[1]+a_symbol[2])]}\n"
        sys.stdout.write(f"Specific memory areas:\n{mem_vals}\n\n")
    
    if (len(set_mem) or len(set_sym)) > 0:
        if not no_backup:
            bak_file = f"{os.path.splitext(input_file)[0]}.bak"
            # First create a backup
            with open(bak_file, "wb") as fd:
                pickle.dump(compiled_program, fd)
        else:
            sys.stdout.write("Skipping backup file.\n\n")
                
        # Apply required modifications
        if set_mem is not None:
            for a_set_mem in set_mem:
                previous_value = compiled_program["program"][a_set_mem[0]]
                compiled_program["program"][a_set_mem[0] & 0xFF] = a_set_mem[1] & 0xFF
                sys.stdout.write(f"Modifying address {a_set_mem[0]} from {previous_value} to {a_set_mem[1]}\n")
            sys.stdout.write("\n")
            
        if set_sym is not None:
            for a_set_sym in set_sym:
                previous_value = compiled_program["program"][compiled_program["symbols"][a_set_sym[0]][0]]
                sys.stdout.write(f"Modifying symbol {set_sym[0]} from {previous_value} to {a_set_sym[1]}\n")
                compiled_program["program"][compiled_program["symbols"][a_set_sym[0]][0]] = a_set_sym[1] & 0xFF
                
        # Save the new dgb
        with open(input_file, "wb") as fd:
            pickle.dump(compiled_program,fd)
        sys.stdout.write(f"Saving changes to {input_file}\n\n")

if __name__ == "__main__":
    dginspect()
