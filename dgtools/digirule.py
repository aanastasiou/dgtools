"""

The main Digirule VM class.

:author: Athanasios Anastasiou
:date: Mar 2020
"""
from .exceptions import DgtoolsErrorOpcodeNotSupported, DgtoolsErrorProgramHalt
from .callbacks import DigiruleCallbackInputBase
import random

class Digirule:
    """
    Abstracts the Digirule 2A hardware.
    
    Maps all registers, flags and memory spaces accessible.
    
    Notes:
    
        * Functions that change the state of the VM but do not return values, should return `self`
        
    """
    def __init__(self):
        # Program counter
        self._pc = 0
        # Previous program counter (a stak where the pc is pushed during CALL/RETURN)
        # TODO: MED, There might be constraints in the depth of this stack. Not yet implemented.
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
        # To put the Digirule in interactive mode, set interactive_callback to an appropriate callback.
        # When a Digirule is in Interactive Mode and an instruction comes to read from the button register
        # it prompts the user for input
        self._interactive_callback = None
        # Instruction set lookup
        self._ins_lookup = {0:self._halt,
                            1:self._nop,
                            2:self._speed,
                            3:self._copylr,
                            4:self._copyla,
                            5:self._copyar,
                            6:self._copyra,
                            7:self._copyrr,
                            8:self._addla,
                            9:self._addra,
                           10:self._subla,
                           11:self._subra,
                           12:self._andla,
                           13:self._andra,
                           14:self._orla,
                           15:self._orra,
                           16:self._xorla,
                           17:self._xorra,
                           18:self._decr,
                           19:self._incr,
                           20:self._decrjz,
                           21:self._incrjz,
                           22:self._shiftrl,
                           23:self._shiftrr,
                           24:self._cbr,
                           25:self._sbr,
                           26:self._bcrsc,
                           27:self._bcrss,
                           28:self._jump,
                           29:self._call,
                           30:self._retla,
                           31:self._return,
                           32:self._addrpc}
        
    @property
    def addr_led(self):
        return f"{self._pc:08b}"
        
    @property
    def data_led(self):
        return f"{self._rd_mem(self._dataled_reg_ptr):08b}"
        
    @property
    def button_sw(self):
        return f"{self._mem[self._bt_reg_ptr]:08b}"

    @property 
    def interactive_callback(self):
        return self._interactive_callback
        
    @interactive_callback.setter
    def interactive_callback(self, new_callback):
        if not isinstance(new_callback, DigiruleCallbackInputBase):
            raise TypeError(f"interactive_callback() setter expected descendant of DigiruleCallbackInputBase, "
                            f"received {type(new_callback)}")
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
            raise TypeError(f".speed() setter expects int, received {type(new_value)}")
        self._speed_setting = new_value & 0xFF
                
    def load_program(self, a_program):
        """
        Loads a program starting from the specified address.
        
        Notes:
            * A program is basically an array of (most commonly) 256 values
            * Offset is the offset within the Digirule memory where the first
              byte of the program would reside.
        """
        if type(a_program) is not list:
            raise TypeError(f"Expected a_program as list received {type(a_program)}")
        
        if len(a_program) > 256:
            raise ValueError(f"Expected length of program to be at most 256, received {len(a_program)}")
            
        for k in enumerate(a_program):
            self._mem[k[0]] = k[1]            
        return self
        
    def set_button_register(self, new_value):
        """
        Sets the values of the button register to simulate key-presses.
        """
        if type(new_value) is not int:
            raise TypeError(f"Expected new_value as int, received {type(new_value)}")
            
        self._wr_mem(self._bt_reg_ptr, new_value & 0xFF)
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
        self._acc = new_value & 0xFF
        # self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        # self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))
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
        if addr == self._bt_reg_ptr and self._interactive_callback is not None:
            self._mem[addr] = self._interactive_callback()
        return self._mem[addr]
        
    def _halt(self):
        raise DgtoolsErrorProgramHalt()
        
    def _nop(self):
        pass
        
    def _speed(self):
        self._speed_setting = self._read_next()
        
    def _copylr(self):
        literal = self._read_next()
        self._wr_mem(self._read_next(), literal)
        
    def _copyla(self):
        literal = self._read_next()
        self._set_acc_value(literal)

    def _copyar(self):
        self._wr_mem(self._read_next(), self._get_acc_value())

    def _copyra(self):
        new_value = self._rd_mem(self._read_next())
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, new_value==0)

    def _copyrr(self):
        addr1 = self._read_next()
        value_addr1 = self._rd_mem(addr1) & 0xFF
        addr2 = self._read_next()
        self._wr_mem(addr2, value_addr1)
        self._set_status_reg(self._ZERO_FLAG_BIT,value_addr1==0)

    def _addla(self):
        new_value = self._get_acc_value()+self._read_next()
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

    def _addra(self):
        new_value = self._get_acc_value() + self._rd_mem(self._read_next())
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

    def _subla(self):
        new_value = self._get_acc_value() - self._read_next()
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

    def _subra(self):
        new_value = self._get_acc_value() - self._rd_mem(self._read_next())
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

    def _andla(self):
        new_value = self._get_acc_value() & self._read_next()
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)

    def _andra(self):
        new_value = self._get_acc_value() & self._rd_mem(self._read_next())
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)

    def _orla(self):
        new_value = self._get_acc_value() | self._read_next()
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)

    def _orra(self):
        new_value = self._get_acc_value() | self._rd_mem(self._read_next())
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)

    def _xorla(self):
        new_value = self._get_acc_value() ^ self._read_next()
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)

    def _xorra(self):
        new_value = self._get_acc_value() ^ self._rd_mem(self._read_next())
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)

    def _decr(self):
        addr = self._read_next()
        value = (self._rd_mem(addr) - 1) & 0xFF
        self._wr_mem(addr, value)
        self._set_status_reg(self._ZERO_FLAG_BIT,value==0)

    def _incr(self):
        addr = self._read_next()
        value = (self._rd_mem(addr) + 1) & 0xFF
        self._wr_mem(addr, value)
        self._set_status_reg(self._ZERO_FLAG_BIT,value==0)

    def _decrjz(self):
        addr = self._read_next()
        value = (self._rd_mem(addr) - 1) & 0xFF
        self._wr_mem(addr, value)
        self._set_status_reg(self._ZERO_FLAG_BIT,value==0)
        if value == 0:
            self._pc+=2

    def _incrjz(self):        
        addr = self._read_next()
        value = (self._rd_mem(addr) + 1) & 0xFF
        self._wr_mem(addr, value)
        self._set_status_reg(self._ZERO_FLAG_BIT,value==0)
        if value == 0:
            self._pc += 2
            
    def _shiftrl(self):
        addr = self._read_next()
        value = self._rd_mem(addr)
        next_carry_value = 1 if value & 128 == 128 else 0
        self._wr_mem(addr, ((value<<1) & 0xFF)|self._get_status_reg(self._CARRY_FLAG_BIT))
        self._set_status_reg(self._CARRY_FLAG_BIT,next_carry_value)

    def _shiftrr(self):
        addr = self._read_next()
        value = self._rd_mem(addr)
        next_carry_value = 1 if value & 1 == 1 else 0
        self._wr_mem(addr, ((value>>1) & 0xFF)|(self._get_status_reg(self._CARRY_FLAG_BIT) << 7))
        self._set_status_reg(self._CARRY_FLAG_BIT,next_carry_value)

    def _cbr(self):
        bit_to_clear = self._read_next()
        addr = self._read_next()
        new_value = self._rd_mem(addr) & (255 - (1<<bit_to_clear))
        self._wr_mem(addr, new_value)
        
    def _sbr(self):
        # TODO: MED, In CBR and SBR, if the bit is zero, it should raise an error at compile time.
        bit_to_clear = self._read_next()
        addr = self._read_next()
        new_value = self._rd_mem(addr) | (1<<bit_to_clear)
        self._wr_mem(addr, new_value)

    def _bcrsc(self):
        bit_to_check_mask = 1 << self._read_next()
        addr = self._read_next()
        if (self._rd_mem(addr) & bit_to_check_mask) != bit_to_check_mask:
            self._pc+=2
            
    def _bcrss(self):
        bit_to_check_mask = 1 << self._read_next()
        addr = self._read_next()
        if (self._rd_mem(addr) & bit_to_check_mask) == bit_to_check_mask:
            self._pc+=2

    def _jump(self):
        self._pc = self._read_next()
        
    def _call(self):
        self._ppc.append(self._pc + 1)
        self._pc = self._read_next()
        
    def _retla(self):
        self._acc = self._read_next()
        # TODO: MED, If you get a RETLA without first having called CALL, it should raise an exception at compile time.
        self._pc = self._ppc.pop()

    def _return(self):
        self._pc = self._ppc.pop()

    def _addrpc(self):
        self._pc += self._read_next()


    def _exec_next(self):
        """
        Fetches and executes an opcode from memory. Emulates the 2A firmware.
        """
        # Fetch...
        cmd = self._read_next()
        # Execute
        try:
            self._ins_lookup[cmd]()
        except KeyError as ke:
            raise DgtoolsErrorOpcodeNotSupported(f"Opcode {cmd} not understood")
        
    def goto(self, offset):
        if type(offset) is not int:
            raise TypeError(f"Expected offset as int, received {type(offset)}")
            
        if offset<0 or offset>255:
            raise ValueError(f"Expected 0<=offset<256, received {offset}")
            
        self._pc = offset
    
    def run(self, max_n=2500):
        """
        Executes commands from the current program counter until a HALT opcode.
        """
        cnt = self._exec_next()
        n = 0
        while n<2500:
            cnt = self._exec_next()
            n+=1
            
        raise DgtoolsErrorProgramHalt()
            
    def step(self):
        return self._exec_next()
        
    def __str__(self):
        """
        Returns a string representing the current state of the VM as it would be visible to a user.
        """
        return f"ADDR LED:{self._pc:08b}\n" \
               f"DATA LED:{self._rd_mem(self._dataled_reg_ptr):08b}\n"\
               f"  BTT SW:{self._mem[self._bt_reg_ptr]:08b}\n"
               
    @staticmethod
    def get_asm_parser():
        """
        Returns the assembly parser that the Digirule2A understands.
        
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
        asm_halt = pyparsing.Group(pyparsing.Regex(r"HALT")("cmd"))("0:0")
        asm_nop = pyparsing.Group(pyparsing.Regex(r"NOP")("cmd"))("1:0")
        asm_speed = pyparsing.Group(pyparsing.Regex(r"SPEED")("cmd") + literal_or_identifier("value"))("2:1")
        asm_copylr = pyparsing.Group(pyparsing.Regex("COPYLR")("cmd") + literal_or_identifier("value") + literal_or_identifier("addr"))("3:1")
        asm_copyla = pyparsing.Group(pyparsing.Regex(r"COPYLA")("cmd") + literal_or_identifier("value"))("4:1")
        asm_copyar = pyparsing.Group(pyparsing.Regex("COPYAR")("cmd") + literal_or_identifier("addr"))("5:1")
        asm_copyra = pyparsing.Group(pyparsing.Regex("COPYRA")("cmd") + literal_or_identifier("addr"))("6:1")
        asm_copyrr = pyparsing.Group(pyparsing.Regex("COPYRR")("cmd") + literal_or_identifier("addr_from") + literal_or_identifier("addr_to"))("7:2")
        asm_addla = pyparsing.Group(pyparsing.Regex("ADDLA")("cmd") + literal_or_identifier("value"))("8:1")
        asm_addra = pyparsing.Group(pyparsing.Regex("ADDRA")("cmd") + literal_or_identifier("addr"))("9:1")
        asm_subla = pyparsing.Group(pyparsing.Regex("SUBLA")("cmd") + literal_or_identifier("value"))("10:1")
        asm_subra = pyparsing.Group(pyparsing.Regex("SUBRA")("cmd") + literal_or_identifier("value"))("11:1")
        asm_andla = pyparsing.Group(pyparsing.Regex("ANDLA")("cmd") + literal_or_identifier("value"))("12:1")
        asm_andra = pyparsing.Group(pyparsing.Regex("ANDRA")("cmd") + literal_or_identifier("addr"))("13:1")
        asm_orla = pyparsing.Group(pyparsing.Regex("ORLA")("cmd") + literal_or_identifier("value"))("14:1")
        asm_orra = pyparsing.Group(pyparsing.Regex("ORRA")("cmd") + literal_or_identifier("addr"))("15:1")
        asm_xorla = pyparsing.Group(pyparsing.Regex("XORLA")("cmd") + literal_or_identifier("value"))("16:1")
        asm_xorra = pyparsing.Group(pyparsing.Regex("XORRA")("cmd") + literal_or_identifier("addr"))("17:1")
        asm_decr = pyparsing.Group(pyparsing.Regex("DECR")("cmd") + literal_or_identifier("addr"))("18:1")
        asm_incr = pyparsing.Group(pyparsing.Regex("INCR")("cmd") + literal_or_identifier("addr"))("19:1")
        asm_decrjz = pyparsing.Group(pyparsing.Regex("DECRJZ")("cmd") + literal_or_identifier("addr"))("20:1")
        asm_incrjz = pyparsing.Group(pyparsing.Regex("INCRJZ")("cmd") + literal_or_identifier("addr"))("21:1")
        asm_shiftrl = pyparsing.Group(pyparsing.Regex("SHIFTRL")("cmd") + literal_or_identifier("addr"))("22:1")
        asm_shiftrr = pyparsing.Group(pyparsing.Regex("SHIFTRR")("cmd") + literal_or_identifier("addr"))("23:1")
        asm_cbr = pyparsing.Group(pyparsing.Regex("CBR")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("24:2")
        asm_sbr = pyparsing.Group(pyparsing.Regex("SBR")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("25:2")
        asm_bcrsc = pyparsing.Group(pyparsing.Regex("BCRSC")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("26:2")
        asm_bcrss = pyparsing.Group(pyparsing.Regex("BCRSS")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("27:2")
        asm_jump = pyparsing.Group(pyparsing.Regex("JUMP")("cmd") + literal_or_identifier("addr"))("28:1")
        asm_call = pyparsing.Group(pyparsing.Regex("CALL")("cmd") + literal_or_identifier("addr"))("29:1")
        asm_retla = pyparsing.Group(pyparsing.Regex("RETLA")("cmd") + literal_or_identifier("value"))("30:1")
        asm_return = pyparsing.Group(pyparsing.Regex("RETURN")("cmd"))("31:0")
        asm_addrpc = pyparsing.Group(pyparsing.Regex("ADDRPC")("cmd") + literal_or_identifier("value"))("32:1")
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

               

class Digirule2U(Digirule):
    """
    Implements the Digirule 2U model.
    """
    
    def __init__(self):
        super().__init__()

        # Switch around RETLA and RETURN
        self._ins_lookup[30], self._ins_lookup[31] = self._ins_lookup[31], self._ins_lookup[30]  
        # Add the new commands
        self._ins_lookup.update({33:self._initsp,
                                 34:self._randa,
                                 35:self._swapra,
                                 36:self._swaprr,
                                 37:self._mul,
                                 38:self._div,
                                192:self._comout,
                                193:self._comin,
                                194:self._comrdy})
        self._comout_callback = None
        self._comin_callback = None
        
    @property 
    def comout_callback(self):
        return self._comout_callback
        
    @comout_callback.setter
    def comout_callback(self, new_callback):
        if not isinstance(new_callback, DigiruleCallbackInputBase):
            raise TypeError(f"comout_callback() setter expected descendant of DigiruleCallbackInputBase, "
                            f"received {type(new_callback)}")
        self._comout_callback = new_callback
        
    @property 
    def comin_callback(self):
        return self._comin_callback
        
    @comin_callback.setter
    def comin_callback(self, new_callback):
        if type(new_callback) is not types.FunctionType:
            raise TypeError(f"comin_callback() setter expected a function, received {type(new_callback)}")
        self._comin_callback = new_callback

    def _initsp(self):
        pass
        
    def _randa(self):
        self._acc = random.randint(0,255)
        
    def _swapra(self):
        mem_addr = self._read_next()
        mem_val = self._rd_mem(mem_addr)
        current_acc_value = self._acc
        self._acc = mem_val
        self._wr_mem(mem_addr, current_acc_value)

    def _swaprr(self):
        mem_addr_left = self._read_next()
        mem_addr_right = self._read_next()
        mem_val_left =  self._rd_mem(mem_addr_left)
        mem_val_right = self._rd_mem(mem_addr_right)
        self._wr_mem(mem_addr_left, mem_val_right)
        self._wr_mem(mem_addr_right, mem_val_left)
    
    def _mul(self):
        mem_addr_left = self._read_next()
        mem_val_left = self._rd_mem(mem_addr_left)
        mem_addr_right = self._read_next()
        mem_val_right = self._rd_mem(mem_addr_right)
        self._wr_mem(mem_addr_left,(mem_val_left * mem_val_right) & 0xFF)
        
    def _div(self):
        # TODO: MED, This can raise a divide by zero warning / exception too
        mem_addr_left = self._read_next()
        mem_val_left = self._rd_mem(mem_addr_left)
        mem_addr_right = self._read_next()
        mem_val_right = self._rd_mem(mem_addr_right)
        if mem_val_right == 0:
            # This is the default division by zero behaviour
            raise DgtoolsErrorProgramHalt()
        self._wr_mem(mem_addr_left, (mem_val_left // mem_val_right) & 0xFF)
        self._acc = (mem_val_left % mem_val_right) & 0xFF
        
    def _comout(self):
        if self._comout_callback is not None:
            self._comout_callback(self._acc)
        
    def _comin(self):
        if self._comin_callback is not None:
            self._comin_callback(self._acc)
        
    def _comrdy(self):
        # Comms is always "ready" in emulation.
        # TODO: MED, Maybe this can be matched to a more realistic behaviour once comout, comin are connected to real files.
        self._set_status_reg(self._ZERO_FLAG_BIT, 0)
