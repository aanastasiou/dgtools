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

  -sn, --skip-n INTEGER           Number of steps to skip generating a dump
                                  for. For example, if --skip-n 10, the first
                                  10 steps will be executed and the HTML
                                  report will start at n=10

  -mn, --max-n INTEGER            Maximum number of time steps to allow the
                                  sim to run for.

  --theme TEXT                    Specifies the CSS theme to use (plain OR
                                  dgbeos)

  --help                          Show this message and exit.
  

:author: Athanasios Anastasiou
:date: Mar 2020.

"""

import sys
import click
import os
import types

from dgtools import (DgtoolsErrorOpcodeNotSupported, 
                     DgtoolsErrorDgbarchiveCorrupted, 
                     DgtoolsErrorSymbolUndefined,
                     DgtoolsErrorProgramHalt, 
                     Output_Render_HTML,
                     DGB_Archive,
                     DigiruleCallbackInputUserInteraction,
                     Digirule, 
                     Digirule2U, 
                     BUILTIN_MODELS)
import inspect
import shutil
from dgtools.exceptions import DgtoolsError
    

def trace_program(program, output_file, skip_n=0, max_n=200, trace_title="", 
                  in_interactive_mode=False, extra_symbols=[], with_mem_dump=True):
    """
    Produces a detailed trace of program execution in HTML form.
    
    :param program: A fully compiled Digirule2 binary.
    :type program: List<uint8>[256]
    :param output_file: The HTML filename.
    :type output_file: str
    :param skip_n: Number of execution steps to omit producing a report on.
    :type skip_n: int (>0)
    :param max_n: Maximum number of steps to allow the VM to run for.
    :type max_n: int (>0)
    :param trace_title: A very simple title for the trace.
    :type trace_title: str
    :param in_interactive_mode: Whether to execute the program in interactive mode.
    :type in_interactive_mode: bool
    :param with_mem_dump: Whether to be producing a full memory dump at each time step of execution.
    :param exra_symbols: A list of symbol name, offset, length to explicitly monitor during execution
    :type extra_symbols: List<str, int, int>
    :returns: A Digirule2 object at its final state when the last command was executed.
    :rtype: Digirule
    """
    # Setup the VM
    machine = BUILTIN_MODELS[program.version]()
    machine.load_program(program.program)
    
    if in_interactive_mode:
        machine.set_default_callbacks()
        
    done = False
    n=0
    # Headings for the memory space dump
    mem_space_heading_h = ["Offset (h)"]+[f"{x:02X}" for x in range(0,16)]
    mem_space_heading_v = [f"{x:02X}" for x in range(0,256,16)]
    # This function could simply be returning a data structure with all data required by a template to produce the 
    # actual output. But that would increase dependencies and possibly required memory too. This is why the file is 
    # created here on the fly.
    with Output_Render_HTML(output_file) as dgen:
        dgen.open_tag("article")
        dgen.open_tag("header")
        dgen.heading(f"Program Trace {trace_title}", 1)
        dgen.close_tag("header")
        while not done and n<max_n:
            if n>=skip_n:
                # Machine registers
                dgen.open_tag("section")
                dgen.named_anchor(f"n{n}")
                dgen.open_tag("header")
                dgen.heading(f"Machine State at n={n}",2)
                dgen.close_tag("header")
                
                dgen.open_tag("section")
                dgen.open_tag("header")
                dgen.heading(f"Machine Registers",3)
                dgen.close_tag("header")
                dgen.table_h(["Program Counter:","Accumulator:", "Status Reg:","Button Register:", "Addr.Led Register:",
                              "Data Led Register:", "Speed setting:", "Program counter stack:"],
                             [[f"0x{machine._pc:02X}"], 
                              [machine._acc],
                              [machine._mem[machine._status_reg_ptr]], 
                              [machine._mem[machine._bt_reg_ptr]], 
                              [machine._mem[machine._addrled_reg_ptr]], 
                              [machine._mem[machine._dataled_reg_ptr]], 
                              [machine._speed_setting], 
                              # [machine._ppc]],
                              [",".join(list(map(lambda x:f"0x{x:02X}",machine._ppc)))]],
                              attrs={"class":"table_machine_state"})
                dgen.close_tag("section")
                
                # Memory space
                if with_mem_dump:
                    dgen.open_tag("section")
                    dgen.open_tag("header")
                    dgen.heading(f"Full memory dump:",3)
                    dgen.close_tag("header")
                    dgen.table_hv([[f"{machine._mem[n]:02X}" for n in range(m,m+16)] for m in range(0,256,16)],
                                  mem_space_heading_h, 
                                  mem_space_heading_v,
                                  attrs={"class":"table_memory_space"},
                                  cell_attrs={(machine._pc // 16,machine._pc-(machine._pc // 16)):{"class":"current_pc"}})
                    dgen.close_tag("section")
                
                # Extra symbols
                if len(extra_symbols):
                    dgen.open_tag("section")
                    dgen.open_tag("header")
                    dgen.heading(f"Specific Symbols",3)
                    dgen.close_tag("header")
                    
                    # symbol_names = list(map(lambda x:x[0],extra_symbols))
                    
                    symbol_values = []
                    for a_symbol in extra_symbols:
                        raw_bytes = machine._mem[a_symbol[1]:(a_symbol[1]+a_symbol[2])]
                        if len(raw_bytes)>1:
                            chr_bytes = "".join(map(lambda x:chr(x), raw_bytes))
                        else:
                            chr_bytes = ""
                        symbol_values.append([str(raw_bytes),chr_bytes])
                    # dgen.table_h(symbol_names,symbol_values, attrs={"class":"table_spec_sym"})
                    dgen.table_v(["Symbol","Offset","Value(s)", "Value as string"],
                                 list(map(lambda x:[x[0][0],
                                                    f"0x{x[0][1]:02X}",
                                                    x[1][0],x[1][1]],
                                          zip(extra_symbols,symbol_values))), 
                                 attrs={"class":"table_spec_sym"})
                    dgen.close_tag("section")
                
                # Onboard IO
                dgen.open_tag("section")
                dgen.open_tag("header")
                dgen.heading("Onboard I/O",3)
                dgen.close_tag("header")
                dgen.table_h(["Address LEDs","Data LEDs","Button Switches"],
                             [machine.addr_led, machine.data_led, machine.button_sw],
                             attrs={"class":"table_onboard_io"})
                dgen.close_tag("section")
                
                dgen.close_tag("section")
                dgen.ruler()
            try:
                machine._exec_next()
            except DgtoolsError as de:
                done = True
                halt_reason = de
                
            n+=1
        # The program terminated for a reason at this point. Mention it
        dgen.open_tag("section", {"class":"program_halt"})
        dgen.named_anchor(f"program_halt")
        dgen.open_tag("header")
        dgen.heading(f"Program stopped at n={n-1}",2)
        dgen.close_tag("header")
        if done:
            dgen._write_tag("p", str(halt_reason))
        else:
            dgen._write_tag("p", f"Program exceeded max_n of {max_n}")
        dgen.close_tag("section")
        
        dgen.close_tag("article")
    return machine

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
@click.option("--skip-n", "-sn", type=int, default=0, 
              help="Number of steps to skip generating a dump for. For example, if --skip-n 10, the first 10 steps "
                   "will be executed and the HTML report will start at n=10")
@click.option("--max-n","-mn", type=int, default=200, 
              help="Maximum number of time steps to allow the sim to run for.")
@click.option("--theme",type=str, help="Specifies the CSS theme to use (plain OR dgbeos)")
def dgsim(input_file, output_trace_file, output_memdump_file, title, 
          with_dump, interactive_mode, trace_symbol, skip_n, max_n, theme):
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
    :param skip_n:
    :type skip_n:
    :param theme: A theme to apply to the output. Must be installed under [package]/css_data
    :type theme: str(path)
    """
    if output_trace_file is None:
        output_trace_file = f"{os.path.splitext(input_file)[0]}_trace.html"
    
    if output_memdump_file is None:
        output_memdump_file = f"{os.path.splitext(input_file)[0]}_memdump.dgb"
        
    try:
        compiled_program = DGB_Archive.load(input_file)       

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
                                 
        machine_after_execution = trace_program(compiled_program, 
                                                output_trace_file,
                                                skip_n = skip_n, 
                                                max_n = max_n, 
                                                trace_title = title, 
                                                in_interactive_mode=interactive_mode, 
                                                with_mem_dump=with_dump, 
                                                extra_symbols=extra_symbols)
                                                
        machine_after_execution_archive = DGB_Archive(machine_after_execution._mem, 
                                                      compiled_program.labels, version=compiled_program.version)
        
        machine_after_execution_archive.save(output_memdump_file)
    
    except Exception as e:
        print(f"dgsim: {str(e)}")
        sys.exit(1)

    # Take care of the theme specification
    if theme is not None:
        theme_source = f"{os.path.dirname(inspect.getfile(DGB_Archive))}/css_themes/{theme}.css"
        theme_destination = f"{os.path.dirname(output_trace_file) or '.'}/dgtheme.css"
        if not os.path.exists(theme_source):
            print(f"dgsim: Specified theme ({theme}) not installed.")
        else:
            shutil.copy(theme_source, theme_destination)

        
if __name__ == "__main__":
    dgsim()
