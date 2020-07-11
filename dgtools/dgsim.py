#!/usr/bin/env python
"""

Usage: dgsim.py [OPTIONS] INPUT_FILE

  Command line program that produces a trace of a Digirule2 binary on
  simulated hardware.

Options:
  -otf, --output-trace_file PATH  Filename containing trace information in
                                  HTML.

  -omf, --output-memdump_file PATH
                                  Filename containing final memory space.
  -t, --title TEXT                An optional title for the produced trace.
  -wd, --with-dump                Whether to include a complete dump of memory
                                  at every time step.

  -I, --interactive-mode          Whether to execute the program in
                                  interactive mode.

  -ts, --trace-symbol TEXT        Adds a symbol to be traced in every
                                  execution step. The format of TEXT
                                  is<Symbol>[:Length[:Offset]].  If only
                                  Symbol is provided, it must have been
                                  defined in the program for its offset to be
                                  automatically determined. In this case,
                                  Length will be 1 by default. If
                                  Symbol:Length is provided, it must have been
                                  defined in the program for its offset to be
                                  automatically determined. If
                                  Symbol:Length:Offset is provided, Symbol
                                  does not have to have beendefined in the ASM
                                  program. In this case, Symbol is just a name
                                  for a region of memory of Length bytes that
                                  starts at Offset.

  -mn, --max-n INTEGER            Maximum number of time steps to allow the
                                  sim to run for.

  --help                          Show this message and exit.


:author: Athanasios Anastasiou
:date: Mar 2020.

"""

import sys
import click
import os
import types
from dgtools import (DgtoolsErrorDgbarchiveCorrupted, 
                     DgtoolsErrorSymbolUndefined,
                     DGB_Archive,
                     DgSimulator, 
                     DgVisualiseDigirule2A,
                     BUILTIN_MODELS)
from dgtools.exceptions import DgtoolsError
    

def validate_trace_symbol(ctx, param, value):
    """
    Validates the Symbol[:Length[:Offset]] form of parameter ``trace_symbol``.
    """
    for a_value in value:
        value_params = a_value.split(":")
        if len(value_params)>3:
            raise click.BadParameter(f"format is <Symbol>[:Length[:Offset]], received {a_value}")
            
        if len(value_params)>=2:
            try:
                length = int(value_params[1]) & 0xFF
            except ValueError:
                raise click.BadParameter(f"When using the format Symbol:Length, Length must be an integer. "
                                         f"Received {a_value}")
            if length>255:
                raise click.BadParameter(f"When using the format Symbol:Length, it should be Length<=255. "
                                         f"Received {a_value}")

            if len(value_params)==3:
                try:
                    offset = int(value_params[2])
                except ValueError:
                    raise click.BadParameter(f"When using the format Symbol:Length:Offset, Offset must be an integer."
                                             f"Received {a_value}")
                if offset>255:
                    raise click.BadParameter(f"When using the format Symbol:Length:Offset, it should be Offset<=255. "
                                             f"Received {a_value}")
                
                if (offset+length)>255:
                    raise click.BadParameter(f"It should be Offset+Length<=255, received {a_value}")
    return value


@click.command()
@click.argument("input-file", type=click.Path(exists=True))
@click.option("--output-trace_file","-otf", type=click.Path(), 
              help="Filename containing trace information in HTML.")
@click.option("--output-memdump_file", "-omf", type=click.Path(), 
              help="Filename containing final memory space.")
@click.option("--title","-t", type=str, 
              help="An optional title for the produced trace.", default="")
@click.option("--with-dump", "-wd", is_flag=True, 
              help="Whether to include a complete dump of memory at every time step.")
@click.option("--interactive-mode", "-I", is_flag=True, 
              help="Whether to execute the program in interactive mode.")
@click.option("--trace-symbol", "-ts", multiple=True, nargs=1, type=str, callback=validate_trace_symbol, 
              help="Adds a symbol to be traced in every execution step. The format of TEXT is"
                   "<Symbol>[:Length[:Offset]]. \nIf only Symbol is provided, it must have been defined in the program "
                   "for its offset to be automatically determined. In this case, Length will be 1 by default.\nIf "
                   "Symbol:Length is provided, it must have been defined in the program for its offset to be " 
                   "automatically determined.\nIf Symbol:Length:Offset is provided, Symbol does not have to have been"
                   "defined in the ASM program. In this case, Symbol is just a name for a region of memory of Length "
                   "bytes that starts at Offset.")    
@click.option("--max-n","-mn", type=int, default=200, 
              help="Maximum number of time steps to allow the sim to run for.")
def dgsim(input_file, output_trace_file, output_memdump_file, title, with_dump, interactive_mode, trace_symbol, max_n):
    """
    Command line program that produces a trace of a Digirule2 binary on simulated hardware.
    
    \f
    :param input_file: The `.dgb` file to simulate.
    :type input_file: str<Path>
    :param output_trace_file: The filename of the HTML file containing human readable trace information.
    :type output_trace_file: str<Path>
    :param output_memdump_file: The filename of the `[]_memdump.dgb.` file containing the final machine memory state.
    :type output_memdump_file: str<Path>
    :param title: A human readable title for the trace.
    :type title: str
    :param with_dump: Whether to produce a memory dump at each timestep of code execution.
    :type with_dump: bool
    :param interactive_mode: Whether execution should be performed in interactive mode.
    :type interactive_mode: bool
    :param trace_symbol: A list of memory locations (name, offset, length) to explicitly track while producing the trace.
    :type trace_symbol: tuple<tuple<str, int, int>>
    :param max_n: The total number of timesteps to allow execution to run for.
    :type max_n:int
    """
    if output_trace_file is None:
        output_trace_file = f"{os.path.splitext(input_file)[0]}_trace.html"
    
    if output_memdump_file is None:
        output_memdump_file = f"{os.path.splitext(input_file)[0]}_memdump.dgb"
        
    try:
        compiled_program = DGB_Archive.load(input_file)       
    except DgtoolsErrorDgbarchiveCorrupted as e:
        print(e.args[0])
        sys.exit(1)

    symbols_to_trace = list(map(lambda x:x.split(":"), trace_symbol))
    # Validate trace_symbol if any
    # Create a set of autodiscovery symbols. The symbol is always element 0 and autodiscoverable symbols have a 
    # length <=2 (i.e. Either Symbol or Symbol:Length)
    symbols_to_validate = set(map(lambda x:x[0],filter(lambda x:len(x)<=2, symbols_to_trace)))
    # Check if there are any symbols that are undefined
    undefined_symbols = symbols_to_validate - set(compiled_program.labels)
    if len(undefined_symbols)>0:
        raise DgtoolsErrorSymbolUndefined(f"Symbol(s) undefined: {undefined_symbols}")
    # If all is well, format the table of TITLE:OFFSET:LENGTH to be sent to trace_program
    # Extra symbols is the union of all combinations of forms (just symbol, symbol:len, symbol:len:offset)
    # This is further "decoded" here, because extra_symbols only understands name,start_addr,stop_addr.
    # The resolution of symbols takes place externally.
    extra_symbols = list(map(lambda x:(x[0],compiled_program.labels[x[0]],1),
                             filter(lambda x:len(x)==1, symbols_to_trace))) + \
                    list(map(lambda x:(x[0],compiled_program.labels[x[0]], int(x[1])), 
                             filter(lambda x:len(x)==2, symbols_to_trace))) + \
                    list(map(lambda x:(x[0],compiled_program.labels[x[0]], int(x[1])), 
                             filter(lambda x:len(x)==3, symbols_to_trace)))
    # Create the visualiser
    dg_vis = BUILTIN_MODELS[compiled_program.version]["machine_vis"](title, extra_symbols, with_dump)
    # Create the machine    
    dg_machine = BUILTIN_MODELS[compiled_program.version]["machine_cls"]()
    # Load the program
    dg_machine.load_program(compiled_program.program)
    # Set interactive mode
    if interactive_mode:
        dg_machine.set_default_callbacks()
    
    # Finally, create the simulator
    dg_sim = DgSimulator(dg_machine, dg_vis, max_n)
    # Run the simulation
    dg_machine_final = dg_sim(output_trace_file)
    # Save the final machine state
    dg_machine_final_archive = DGB_Archive(dg_machine_final._mem, 
                                           compiled_program.labels, 
                                           version=compiled_program.version)
    dg_machine_final_archive.save(output_memdump_file)
        
if __name__ == "__main__":
    dgsim()
