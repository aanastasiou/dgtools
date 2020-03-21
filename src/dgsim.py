#!/usr/bin/env python
"""

Usage: dgsim.py [OPTIONS] INPUT_FILE

  Command line program that produces a trace of a Digirule2 binary on
  simulated hardware.

Options:
  -otf, --output-trace_file PATH  Filename containing trace information in
                                  Markdown.

  -omf, --output-memdump_file PATH
                                  Filename containing final memory space.
  -t, --title TEXT                An optional title for the produced trace.
  -wd, --with-dump                Whether to include a complete dump of memory
                                  at every time step.

  -I, --interactive-mode          Whether to execute the program in
                                  interactive mode.

  -ts, --trace-symbol <TEXT INTEGER INTEGER>...
                                  Adds a symbol to be traced explicitly.
  -mn, --max-n INTEGER            Maximum number of time steps to allow the
                                  sim to run for.

  --help                          Show this message and exit.


:author: Athanasios Anastasiou
:date: Mar 2020.

"""

import sys
import pickle
import click
import os
import types

class Digirule:
    """
    Abstracts the Digirule 2 hardware.
    
    Maps all registers, flags and memory spaces accessible.
    
    Notes:
    
        * Functions that change the state of the VM but do not return values, should return `self`
        
    """
    def __init__(self):
        # Program counter
        self._pc = 0
        # Previous program counter (a stak where the pc is pushed during CALL/RETURN)
        # TODO: HIGH, There might be constraints in the depth of this stack. Not yet implemented.
        self._ppc = []
        # Accumulator
        self._acc = 0
        # The status reg contains the zero flag (bit 0) and the carry flag (bit 1)
        self._ZERO_FLAG_BIT = 1 << 0 # Directly convert bits to their binary representations here
        self._CARRY_FLAG_BIT = 1 << 1
        self._ADDRLED_FLAG_BIT = 1 << 2     
        # Certain registers are memory mapped (why not all?)
        # The following were obtained from the documentation
        self._status_reg_ptr = 252
        self._bt_reg_ptr = 253
        self._addrled_reg_ptr = 254
        self._dataled_reg_ptr = 255
        self._mem = [0 for k in range(0,256)]
        # The speed setting is just for visualisation
        # TODO: LOW, Make the speed setting functional
        self._speed_setting = 0
        # If the Digirule is in interactive mode and a program tries to read from the button register
        # it prompts the user for input
        self._interactive_mode = False
        self._interactive_callback = self._default_interactive_callback
        
    @staticmethod
    def _default_interactive_callback():
        """
        Prompts the user for (binary) button input.
        
        :returns: Type checked user input
        :rtype: uint8
        """
        done = False
        while not done:
            user_input = input("BT:")
            try:
                user_input_numeric = int(user_input, 2)
                if user_input_numeric>255:
                    raise ValueError("User input greater than 255")
                else:
                    done = True
            except ValueError as ve:
                sys.stdout.write(f"ERROR:{ve}\n")
                
        return user_input_numeric
        
    @property
    def interactive_mode(self):
        return self._interactive_mode
        
    @interactive_mode.setter
    def interactive_mode(self, new_mode):
        self._interactive_mode = new_mode
        
    @property 
    def interactive_callback(self):
        return self._interactive_callback
        
    @interactive_callback.setter
    def interactive_callback(self, new_callback):
        if type(new_callback) is not types.FunctionType:
            # TODO: HIGH, Raise exception "Object is not a callback"
            pass
        self._interactive_callback = new_callback
    
    @property
    def mem(self):
        return self._mem
        
    @property
    def speed(self):
        return self._speed_setting
        
    @speed.setter
    def speed(self, new_value):
        if type(new_value) is not int:
            # TODO: HIGH, Raise exception "new_value is not int"
            pass
        self._speed_setting = new_value & 0xFF
                
    def load_program(self, a_program, offset=0):
        """
        Loads a program starting from the specified address.
        
        Notes:
            * A program is basically an array of (most commonly) 256 values
            * Offset is the offset within the Digirule memory where the first
              byte of the program would reside.
        """
        if type(offset) is not int:
            # TODO: HIGH, Raise exception "offset is not int"
            pass
        if len(a_program)+offset>256:
            # TODO: HIGH, Raise exception "Memory range missmatch"
            pass
        for k in enumerate(a_program):
            self._mem[k[0]+offset] = k[1]            
        return self
        
    def set_button_register(self, new_value):
        """
        Sets the values of the button register to simulate key-presses.
        """
        if type(new_value) is not int:
            # TODO: HIGH, Raise exception "new_value is not int"
            pass
        self._wr_mem(self._bt_reg_ptr, new_value & 255)
        return self
        
    def _read_next(self):
        """
        The equivalent of "fetch".
        
        It fetches a byte from the current program counter and advances the program counter.
        """
        value = self._rd_mem(self._pc)
        self._incr_pc()
        return value
        
    def _get_pc(self):
        return self._pc
        
    def _set_pc(self, addr):
        self._pc = addr
        return self
        
    def _incr_pc(self):
        self._pc+=1
        return self
        
    def _set_acc_value(self, new_value):
        """
        Sets the accumulator value, taking care of the zero and carry flags.
        
        :param new_value: The value to set the Accumulator to.
        :type new_value: uint8
        """
        self._acc = new_value & 255
        if new_value == 0:
            self._set_status_reg(self._ZERO_FLAG_BIT, 1)
        else:
            self._set_status_reg(self._ZERO_FLAG_BIT, 0)
            
        if new_value > 255 or new_value < 0:
            self._set_status_reg(self._CARRY_FLAG_BIT, 1)
        else:
            self._set_status_reg(self._CARRY_FLAG_BIT, 0)
        
        return self
        
    def _get_acc_value(self):
        return self._acc
        
    def _set_status_reg(self, field_mask, value):
        current_value = self._mem[self._status_reg_ptr]
        self._mem[self._status_reg_ptr] ^= (-value ^ current_value) & field_mask
        return self
        
    def _get_status_reg(self, field_mask):
        return 1 if (self._mem[self._status_reg_ptr] & field_mask) == field_mask else 0
        
    def _get_zero_flag(self):
        return 1 if self._mem[self._status_reg_ptr] & self._ZERO_FLAG_BIT == self._ZERO_FLAG_BIT else 0
        
    def _wr_mem(self, addr, value):
        # TODO: MED, addr cannot go higher than 252 or it will overwrite peripherals. It should generate a warning.
        self._mem[addr & 0xFF] = value & 0xFF
        return self
        
    def _rd_mem(self, addr):
        """
        Reads memory from the specified address.
        
        Notes:
        
            * If the VM is in interactive mode and the button register is attempted to be read, it prompts the user 
              for input.
        """
        if addr == self._bt_reg_ptr and self._interactive_mode:
            self._mem[addr] = self._interactive_callback()
        return self._mem[addr]
                
    def _exec_next(self):
        """
        Fetches and executes an opcode from memory.
        
        :returns: 0 if a HALT is executed 1 otherwise.
        :rtype: int
        """
        # TODO: LOW, Obviously, each command can be abstracted in its own callback so that the VM becomes easily 
        #      extensible and re-usable.
        
        # Fetch...
        cmd = self._read_next()
        
        if cmd>32:
            # TODO: HIGH, Raise exception "opcode not supported"
            # TODO: LOW, These can be intercepted and re-interpreted. Package state along.
            pass
            
        # ...Execute    
        # HALT
        if cmd == 0:
            # TODO: HIGH, Raise exception HALT
            return 0 
        
        # NOP
        if cmd == 1:
            pass
        
        # SPEED
        if cmd == 2:
            self._speed_setting = self._read_next()            
        
        # COPYLR
        if cmd == 3:
            literal = self._read_next()
            self._wr_mem(self._read_next(), literal)
        
        # COPYLA
        if cmd == 4:
            literal = self._read_next()
            self._set_acc_value(literal)
            
        # COPYAR
        if cmd == 5:
            self._wr_mem(self._read_next(), self._get_acc_value())
            
        # COPYRA
        if cmd == 6:
            self._set_acc_value(self._rd_mem(self._read_next()))
        
        # COPYRR
        if cmd == 7:
            addr1 = self._read_next()
            value_addr1 = self._rd_mem(addr1)
            addr2 = self._read_next()
            self._wr_mem(addr2, value_addr1)
            if value_addr1==0:
                self._set_status_reg(self._ZERO_FLAG_BIT, 1)
            else:
                self._set_status_reg(self._ZERO_FLAG_BIT, 0)
            
        # ADDLA
        if cmd == 8:
            new_value = self._get_acc_value()+self._read_next()
            self._set_acc_value(new_value)           
            
        # ADDRA
        if cmd == 9:
            self._set_acc_value(self._get_acc_value() + self._rd_mem(self._read_next()))
            
        # SUBLA
        if cmd == 10:
            self._set_acc_value(self._get_acc_value() - self._read_next())
            
        # SUBRA
        if cmd == 11:
            self._set_acc_value(self._get_acc_value() - self._rd_mem(self._read_next()))
            
        # ANDLA
        if cmd == 12:
            self._set_acc_value(self._get_acc_value() & self._read_next())
            
        # ANDRA
        if cmd == 13:
            self._set_acc_value(self._get_acc_value() & self._rd_mem(self._read_next()))
            
        # ORLA
        if cmd == 14:
            self._set_acc_value(self._get_acc_value() | self._read_next())
            
        # ORRA
        if cmd == 15:
            self._set_acc_value(self._get_acc_value() | self._rd_mem(self._read_next()))
        
        # XORLA
        if cmd == 16:
            self._set_acc_value(self._get_acc_value() ^ self._read_next())
            
        # XORRA
        if cmd == 17:
            self._set_acc_value(self._get_acc_value() ^ self._rd_mem(self._read_next()))
        
        # DECR
        if cmd == 18:
            addr = self._read_next()
            value = self._rd_mem(addr)
            self._wr_mem(addr, value - 1)
        
        # INCR
        if cmd == 19:
            addr = self._read_next()
            value = self._rd_mem(addr)
            self._wr_mem(addr, value + 1)
            
        # DECRJZ
        if cmd == 20:
            addr = self._read_next()
            value = self._rd_mem(addr) - 1
            self._wr_mem(addr, value & 0xFF)
            if value == 0:
                self._set_status_reg(self._ZERO_FLAG_BIT,0)
                self._pc+=2
                
        # INCRJZ
        if cmd == 21:
            addr = self._read_next()
            value = self._rd_mem(addr) + 1
            self._wr_mem(addr, value & 0xFF)
            if value == 0:
                self._set_status_reg(self._ZERO_FLAG_BIT,1)
                self._pc += 2
            else:
                self._set_status_reg(self._ZERO_FLAG_BIT,0)

        # SHIFTRL
        if cmd == 22:
            addr = self._read_next()
            value = self._rd_mem(addr)
            next_carry_value = 1 if value & 128 == 128 else 0
            self._wr_mem(addr, ((value<<1) & 0xFF)|self._get_status_reg(self._CARRY_FLAG_BIT))
            self._set_status_reg(self._CARRY_FLAG_BIT,next_carry_value)

        # SHIFTRR
        if cmd == 23:
            addr = self._read_next()
            value = self._rd_mem(addr)
            next_carry_value = 1 if value & 1 == 1 else 0
            self._wr_mem(addr, ((value>>1) & 0xFF)|(self._get_status_reg(self._CARRY_FLAG_BIT) << 7))
            self._set_status_reg(self._CARRY_FLAG_BIT,next_carry_value)
            
        # CBR
        if cmd == 24:
            bit_to_clear = self._read_next()
            addr = self._read_next()
            new_value = self._rd_mem(addr) & (255 - (1<<bit_to_clear))
            self._wr_mem(addr, new_value)
                    
        # SBR
        if cmd == 25:
            # TODO: MED, In CBR and SBR, if the bit is zero, it should raise an error either at compilation time or 
            #       runtime. 
            bit_to_clear = self._read_next()
            addr = self._read_next()
            new_value = self._rd_mem(addr) | (255 - (1<<bit_to_clear))
            self._wr_mem(addr, new_value)
            
        # BCRSC
        if cmd == 26:
            bit_to_check_mask = 1 << self._read_next()
            addr = self._read_next()
            if (self._rd_mem(addr) & bit_to_check_mask) != bit_to_check_mask:
                self._pc+=2
            
        # BCRSS
        if cmd == 27:
            bit_to_check_mask = 1 << self._read_next()
            addr = self._read_next()
            if (self._rd_mem(addr) & bit_to_check_mask) == bit_to_check_mask:
                self._pc+=2

        # JUMP
        if cmd == 28:
            self._pc = self._read_next()
            
        # CALL
        if cmd == 29:
            self._ppc.append(self._pc + 1)
            self._pc = self._read_next()
            
        # RETLA
        if cmd == 30:
            self._acc = self._read_next()
            # But if you get a RETLA without first having called CALL, then it should throw an exception.
            self._pc = self._ppc.pop()
        
        # RETURN
        if cmd == 31:
            self._pc = self._ppc.pop()
        
        # ADDRPC
        if cmd == 32:
            self._pc += self._read_next()
            
        return 1
        
    def goto(self, offset):
        if type(offset) is not int:
            # TODO: HIGH, Raise exception "offset is not int"
            pass
        if offset<0 or offset>255:
            # TODO: HIGH, Raise exception "offset out of range"
            pass
        self._pc = offset
    
    def run(self, offset=0):
        """
        Executes commands from the current program counter until a HALT opcode.
        
        :param offset: The offset within `_mem` to start executing from.
        :type offset: int
        """
        self._pc = offset
        cnt = self._exec_next()
        while cnt:
            cnt = self._exec_next()
            
    def step(self):
        return self._exec_next()
        
    def __str__(self):
        """
        Returns a string representing the current state of the VM as it would be visible to a user.
        """
        return f"ADDR LED:{self._pc:08b}\n" \
               f"DATA LED:{self._rd_mem(self._dataled_reg_ptr):08b}\n"\
               f"  BTT SW:{self._mem[self._bt_reg_ptr]:08b}\n"


def mem_dump(mem, offset_from=0, offset_to=256, line_length=16):
    """
    Dumps memory in a hex-editor style view.
    
    :param mem: A memory block to hex dump.
    :type mem: list<uint8>[256]
    :param offset_from: Where to start the dump from
    :type offset_from: int
    :param offset_to: Where to end the dump at
    :type offset_to: int
    :param line_length: How many bytes per character to print in one line
    :type line_length: int
    :returns: A multiline string containing the hex dump.
    :rtype: str
    """
    char_map_from = "\n\a\t\r"
    char_map_to = "...."
    trans_tab = str.maketrans(char_map_from, char_map_to)
    to_ret = f"Offset (h)\t" + " ".join([format(k, "02X") for k in range(0,line_length)])+"\n"
    total_length = offset_to - offset_from
    n_lines = total_length // line_length
    remaining_chars = total_length % line_length
    for k in range(0, n_lines):
        # Memory page to visualise
        mem_page = [mem[u] for u in range(offset_from+k*line_length,offset_from+k*line_length+line_length)]
        # The same memory page in hex
        mem_page_hex = " ".join([f"{q:02X}" for q in mem_page])
        # The same memory page in chr depictions.
        # TODO: MED, The character translation table can be improved here to get rid of the >9 and clarify depictions.
        mem_page_char = "".join([chr(q) if q>9 else "." for q in mem_page]).translate(trans_tab)
        to_ret += f"\t\t{(offset_from+k*8):02X}\t{mem_page_hex} {mem_page_char}\n"        
    return to_ret
    
    
def trace_program(program, output_file, max_n=200, trace_title="", in_interactive_mode=False, extra_symbols=None, with_mem_dump=True):
    """
    Produces a detailed trace of program execution in Markdown format.
    
    :param program: A fully compiled Digirule2 binary.
    :type program: List<uint8>[256]
    :param output_file: The Markdown filename to generate.
    :type output_file: str
    :param max_n: Maximum number of steps to allow the VM to run for.
    :type max_n: int
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
    machine = Digirule()
    machine.load_program(program)
    if in_interactive_mode:
        machine.interactive_mode = True
    done = False
    n=0
    # This function could simply be returning a string with the Markdown format but for long programs, that might 
    # become too big too quickly. This is why the file is created on the fly right here.
    with open(output_file, "wt") as fd:
        fd.write(f"# Program Trace {trace_title} \n\n")
        while not done and n<max_n:
            fd.write(f"## Machine Registers at n={n} \n\n")
            fd.write(f"```\nProgram Counter:{machine._pc}\nAccumulator:{machine._acc}\nStatus Reg:{machine._mem[machine._status_reg_ptr]}\n"
                     f"Button Register:{machine._mem[machine._bt_reg_ptr]}\nAddr.Led Register:{machine._mem[machine._addrled_reg_ptr]}\n"
                     f"Data Led Register:{machine._mem[machine._dataled_reg_ptr]}\nSpeed setting:{machine._speed_setting} \n")
            fd.write(f"Program counter stack:{machine._ppc}\n```\n\n")
            if with_mem_dump:
                fd.write(f"## Full memory dump:\n```\n{mem_dump(machine._mem)}\n```\n\n")
            if extra_symbols is not None:
                fd.write(f"### Specific Symbols\n\n")
                symbols_paragraph = "\n".join(map(lambda x:f"{x[0]} {machine._mem[x[1]:(x[1]+x[2])]}",extra_symbols))
                fd.write(f"```\n{symbols_paragraph}\n```\n\n")
            fd.write(f"## Onboard I/O\n\n")
            fd.write(f"```\n{str(machine)}\n```\n\n")
            fd.write("-------------\n\n")
            done = not machine._exec_next()
            n+=1
            
    return machine

@click.command()
@click.argument("input-file", type=click.Path(exists=True))
@click.option("--output-trace_file","-otf", type=click.Path(), help="Filename containing trace information in Markdown.")
@click.option("--output-memdump_file", "-omf", type=click.Path(), help="Filename containing final memory space.")
@click.option("--title","-t", type=str, help="An optional title for the produced trace.", default="")
@click.option("--with-dump", "-wd", is_flag=True, help="Whether to include a complete dump of memory at every time step.")
@click.option("--interactive-mode", "-I", is_flag=True, help="Whether to execute the program in interactive mode.")
@click.option("--trace-symbol", "-ts", multiple=True, nargs=3, type=(str,int,int), help="Adds a symbol to be traced explicitly.")    
@click.option("--max-n","-mn", type=int, default=200, help="Maximum number of time steps to allow the sim to run for.")
def dgsim(input_file, output_trace_file, output_memdump_file, title, with_dump, interactive_mode, trace_symbol, max_n):
    """
    Command line program that produces a trace of a Digirule2 binary on simulated hardware.
    
    \f
    :param input_file: The `.dgb` file to simulate.
    :type input_file: str<Path>
    :param output_trace_file: The filename of the Markdown file containing human readable trace information.
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
    # TODO: HIGH, trace_symbol needs further validation
    # TODO: HIGH, The .dgb should also contain the machine state itself.
    if output_trace_file is None:
        output_trace_file = f"{os.path.splitext(input_file)[0]}_trace.md"
    
    if output_memdump_file is None:
        output_memdump_file = f"{os.path.splitext(input_file)[0]}_memdump.dgb"
        
    with open(input_file, "rb") as fd:
        compiled_program = pickle.load(fd)
    # TODO, HIGH: Check (at least) if the compiled_program is a dictionary with three known attributes.
    machine_after_execution = trace_program(compiled_program["program"], output_trace_file, max_n = max_n, trace_title = title, in_interactive_mode=interactive_mode, with_mem_dump=with_dump, extra_symbols=trace_symbol)
    compiled_program["program"] = machine_after_execution._mem
    with open(output_memdump_file, "wb") as fd:
        pickle.dump(compiled_program, fd)
        
if __name__ == "__main__":
    dgsim()
