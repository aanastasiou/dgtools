#!/usr/bin/env python
"""

Usage: dginspect.py [OPTIONS] INPUT_FILE

  Command line tool to inspect and modify .dgb files.

  If modifying the .dgb file, a backup (.bak) with the version prior to
  applying the modifications  is created automatically. To turn this
  functionality off, see option `--no-backup`

Options:
  -g, --get-mem TEXT              Gets the values of a memory range. The
                                  format of TEXT is <Symbol>[:Length[:Offset]].
                                  If only Symbol is provided, it must have
                                  been defined in the program for its offset
                                  to be automatically determined. In this
                                  case, Length will be 1 by default. If
                                  Symbol:Length is provided, it must have been
                                  defined in the program for its offset to be
                                  automatically determined. If
                                  Symbol:Length:Offset is provided, Symbol
                                  does not have to have beendefined in the ASM
                                  program. In this case, Symbol is just a name
                                  for a region of memory of Length bytes that
                                  starts at Offset.

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
from dgsim import mem_dump, validate_trace_symbol
from exceptions import DgtoolsErrorSymbolUndefined

@click.command()
@click.argument("input-file", type=click.Path(exists=True))
@click.option("--get-mem","-g", multiple=True, type=str, callback=validate_trace_symbol, 
              help="Gets the values of a memory range. The format of TEXT is "
                   "<Symbol>[:Length[:Offset]]. \nIf only Symbol is provided, it must have been defined in the program "
                   "for its offset to be automatically determined. In this case, Length will be 1 by default.\nIf "
                   "Symbol:Length is provided, it must have been defined in the program for its offset to be " 
                   "automatically determined.\nIf Symbol:Length:Offset is provided, Symbol does not have to have been"
                   "defined in the ASM program. In this case, Symbol is just a name for a region of memory of Length "
                   "bytes that starts at Offset.")
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
    # TODO: MID, DGBArchive can become a separate entity and reduce duplication of checks.
    with open(input_file, "rb") as fd:
        compiled_program = pickle.load(fd)
        
    # Validate the format of the .dgb archive
    if type(compiled_program) is not dict:
        raise DgtoolsErrorDgbarchiveCorrupted(f"Archive corrupted.")
    
    if len(set(compiled_program) - {"program", "labels", "symbols"}) != 0:
        raise DgtoolsErrorDgbarchiveCorrupted(f"Archive corrupted.")        
    
    # TODO: MID, Reduce code duplication by packaging this validation in a function
    # Validate any extra memory areas to "get"
    symbols_to_trace = list(map(lambda x:x.split(":"), get_mem))
    # Validate trace_symbol if any
    # Create a set of autodiscovery symbols. The symbol is always element 0 and autodiscoverable symbols have a 
    # length <=2 (i.e. Either Symbol or Symbol:Length)
    symbols_to_validate = set(map(lambda x:x[0],filter(lambda x:len(x)<=2, symbols_to_trace)))
    # Check if there are any symbols that are undefined
    undefined_symbols = symbols_to_validate - set(compiled_program["labels"])
    if len(undefined_symbols)>0:
        raise DgtoolsErrorSymbolUndefined(f"Symbol(s) undefined: {undefined_symbols}")
    # If all is well, format the table of TITLE:OFFSET:LENGTH to be sent to trace_program
    # Extra symbols is the union of all combinations of forms (just symbol, symbol:len, symbol:len:offset)
    # This is further "decoded" here, because extra_symbols only understands name,start_addr,stop_addr.
    # The resolution of symbols takes place externally.
    extra_symbols = list(map(lambda x:(x[0],compiled_program["labels"][x[0]],1),
                             filter(lambda x:len(x)==1, symbols_to_trace))) + \
                    list(map(lambda x:(x[0],compiled_program["labels"][x[0]], int(x[1])), 
                             filter(lambda x:len(x)==2, symbols_to_trace))) + \
                    list(map(lambda x:(x[0],compiled_program["labels"][x[0]], int(x[1])), 
                             filter(lambda x:len(x)==3, symbols_to_trace)))
                                 
    sys.stdout.write(f"Inspecting {input_file}\n")
    sys.stdout.write(f"Program:\n{compiled_program['program']}\n\n")
    sys.stdout.write(f"Label offsets:\n{compiled_program['labels']}\n\n")
    sys.stdout.write(f"Static symbol offsets:\n{compiled_program['symbols']}\n\n")
    
    if len(get_mem)>0:
        # Build the get mem symbols here
        mem_vals = ""
        for a_symbol in extra_symbols:
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
