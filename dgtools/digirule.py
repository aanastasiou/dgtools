"""

Built-in Digirule models supported by dgtools.

:author: Athanasios Anastasiou
:date: Mar 2020
"""
from .exceptions import DgtoolsErrorOpcodeNotSupported, DgtoolsErrorProgramHalt, DgtoolsErrorOutOfMemory
from .callbacks import (DigiruleCallbackInputBase, DigiruleCallbackInputUserInteraction, DigiruleCallbackComOutStdout, 
                        DigiruleCallbackComInUserInteraction, DigiruleCallbackPinInUserInteraction)
import random
import pyparsing

class Digirule:
    """
    Abstracts the Digirule 2 hardware.
    Maps all registers, flags and memory spaces accessible.
    
    Notes:
        * Functions that change the state of the VM but do not return values, should return `self`
        
    """
    # TODO: MED, Need to add randa on the 2A 
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
                
    def set_default_callbacks(self):
        """
        Sets the callbacks that are used to link a Digirule object to the outside world, to a 
        reasonable set of defaults
        """
        self._interactive_callback = DigiruleCallbackInputUserInteraction("Binary button Input (e.g. '010010' wihout " 
                                                                          "quotes):")

    def clear_callbacks(self):
        """
        Completely resets any callbacks to None.
        """
        self._interactive_callback = None
        
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
            raise DgtoolsErrorOutOfMemory(f"Expected length of program to be at most 256, received {len(a_program)}")
            
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
        
    def _push_pc(self):
        self._ppc.append(self._pc + 1)
        return self
        
    def _pop_pc(self):
        # TODO: HIGH, add the underflow exception
        try:
            self._pc = self._ppc.pop()
        except IndexError:
            raise DgtoolsErrorStackUnderflow("Program stack underflow.")
        return self
        
    def _set_acc_value(self, new_value):
        """
        Sets the accumulator value, taking care of the zero and carry flags.
        
        :param new_value: The value to set the Accumulator to.
        :type new_value: uint8
        """
        self._acc = new_value & 0xFF
        return self
        
    def _get_acc_value(self):
        return self._acc
        
    def _set_status_reg(self, field_mask, value):
        current_value = self._mem[self._status_reg_ptr]
        self._mem[self._status_reg_ptr] ^= (-value ^ current_value) & field_mask
        return self
        
    def _get_status_reg(self, field_mask):
        return 1 if (self._mem[self._status_reg_ptr] & field_mask) == field_mask else 0
        
    def _wr_mem(self, addr, value):
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
        raise DgtoolsErrorProgramHalt("Program terminated at HALT instruction.")
        
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
        new_value = self._get_acc_value() + self._read_next()
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

    def _addra(self):
        new_value = self._get_acc_value() + self._rd_mem(self._read_next())
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)

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
        self._push_pc()
        self._pc = self._read_next()
        
    def _retla(self):
        self._acc = self._read_next()
        # TODO: MED, If you get a RETLA without first having called CALL, it should raise an exception at compile time.
        self._pop_pc()

    def _return(self):
        self._pop_pc()
        
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
            
        raise DgtoolsErrorProgramHalt(f"Program exceeded preset max_n={max_n}.")
            
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
    def get_asm_statement_def(existing_defs):
        """
        Returns the assembly parser that the Digirule2A understands.
        
        Notes:
            
            * See inline comments for specification of the grammar
        """
        # Digirule ASM instructions
        # Each succesfully parsed instruction is tagged by its opcode:num operands.
        asm_halt = pyparsing.Group(pyparsing.Regex(r"HALT")("cmd"))("0:0")
        asm_nop = pyparsing.Group(pyparsing.Regex(r"NOP")("cmd"))("1:0")
        asm_speed = pyparsing.Group(pyparsing.Regex(r"SPEED")("cmd") + existing_defs["literal_or_identifier"]("value"))("2:1")
        asm_copylr = pyparsing.Group(pyparsing.Regex("COPYLR")("cmd") + existing_defs["literal_or_identifier"]("value") + existing_defs["literal_or_identifier"]("addr"))("3:2")
        asm_copyla = pyparsing.Group(pyparsing.Regex(r"COPYLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("4:1")
        asm_copyar = pyparsing.Group(pyparsing.Regex("COPYAR")("cmd") + existing_defs["literal_or_identifier"]("addr"))("5:1")
        asm_copyra = pyparsing.Group(pyparsing.Regex("COPYRA")("cmd") + existing_defs["literal_or_identifier"]("addr"))("6:1")
        asm_copyrr = pyparsing.Group(pyparsing.Regex("COPYRR")("cmd") + existing_defs["literal_or_identifier"]("addr_from") + existing_defs["literal_or_identifier"]("addr_to"))("7:2")
        asm_addla = pyparsing.Group(pyparsing.Regex("ADDLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("8:1")
        asm_addra = pyparsing.Group(pyparsing.Regex("ADDRA")("cmd") + existing_defs["literal_or_identifier"]("addr"))("9:1")
        asm_subla = pyparsing.Group(pyparsing.Regex("SUBLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("10:1")
        asm_subra = pyparsing.Group(pyparsing.Regex("SUBRA")("cmd") + existing_defs["literal_or_identifier"]("value"))("11:1")
        asm_andla = pyparsing.Group(pyparsing.Regex("ANDLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("12:1")
        asm_andra = pyparsing.Group(pyparsing.Regex("ANDRA")("cmd") + existing_defs["literal_or_identifier"]("addr"))("13:1")
        asm_orla = pyparsing.Group(pyparsing.Regex("ORLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("14:1")
        asm_orra = pyparsing.Group(pyparsing.Regex("ORRA")("cmd") + existing_defs["literal_or_identifier"]("addr"))("15:1")
        asm_xorla = pyparsing.Group(pyparsing.Regex("XORLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("16:1")
        asm_xorra = pyparsing.Group(pyparsing.Regex("XORRA")("cmd") + existing_defs["literal_or_identifier"]("addr"))("17:1")
        asm_decr = pyparsing.Group(pyparsing.Regex("DECR")("cmd") + existing_defs["literal_or_identifier"]("addr"))("18:1")
        asm_incr = pyparsing.Group(pyparsing.Regex("INCR")("cmd") + existing_defs["literal_or_identifier"]("addr"))("19:1")
        asm_decrjz = pyparsing.Group(pyparsing.Regex("DECRJZ")("cmd") + existing_defs["literal_or_identifier"]("addr"))("20:1")
        asm_incrjz = pyparsing.Group(pyparsing.Regex("INCRJZ")("cmd") + existing_defs["literal_or_identifier"]("addr"))("21:1")
        asm_shiftrl = pyparsing.Group(pyparsing.Regex("SHIFTRL")("cmd") + existing_defs["literal_or_identifier"]("addr"))("22:1")
        asm_shiftrr = pyparsing.Group(pyparsing.Regex("SHIFTRR")("cmd") + existing_defs["literal_or_identifier"]("addr"))("23:1")
        asm_cbr = pyparsing.Group(pyparsing.Regex("CBR")("cmd") + existing_defs["literal_or_identifier"]("n_bit") + existing_defs["literal_or_identifier"]("addr"))("24:2")
        asm_sbr = pyparsing.Group(pyparsing.Regex("SBR")("cmd") + existing_defs["literal_or_identifier"]("n_bit") + existing_defs["literal_or_identifier"]("addr"))("25:2")
        asm_bcrsc = pyparsing.Group(pyparsing.Regex("BCRSC")("cmd") + existing_defs["literal_or_identifier"]("n_bit") + existing_defs["literal_or_identifier"]("addr"))("26:2")
        asm_bcrss = pyparsing.Group(pyparsing.Regex("BCRSS")("cmd") + existing_defs["literal_or_identifier"]("n_bit") + existing_defs["literal_or_identifier"]("addr"))("27:2")
        asm_jump = pyparsing.Group(pyparsing.Regex("JUMP")("cmd") + existing_defs["literal_or_identifier"]("addr"))("28:1")
        asm_call = pyparsing.Group(pyparsing.Regex("CALL")("cmd") + existing_defs["literal_or_identifier"]("addr"))("29:1")
        asm_retla = pyparsing.Group(pyparsing.Regex("RETLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("30:1")
        asm_return = pyparsing.Group(pyparsing.Regex("RETURN")("cmd"))("31:0")
        asm_addrpc = pyparsing.Group(pyparsing.Regex("ADDRPC")("cmd") + existing_defs["literal_or_identifier"]("value"))("32:1")
        asm_statement = pyparsing.Group(asm_halt ^ asm_nop ^ asm_speed ^ asm_copylr ^ asm_copyla ^ asm_copyar ^ asm_copyra ^ asm_copyrr ^ \
                  asm_addla ^ asm_addra ^ asm_subla ^ asm_subra ^ asm_andla ^ asm_andra ^ asm_subla ^ asm_subra ^ \
                  asm_andla ^ asm_andra ^ asm_orla ^ asm_orra ^ asm_xorla ^ asm_xorra ^ asm_decr ^ asm_incr ^ \
                  asm_decrjz ^ asm_incrjz ^ asm_shiftrl ^ asm_shiftrr ^ asm_cbr ^ asm_sbr ^ asm_bcrsc ^ asm_bcrss ^ \
                  asm_jump ^ asm_call ^ asm_retla ^ asm_return ^ asm_addrpc)

        return asm_statement


class Digirule2U(Digirule):
    """
    Implements the Digirule 2U model.
    """
    
    def __init__(self):
        super().__init__()

        # Add the new commands
        self._ins_lookup.update({3:self._initsp,
                                 4:self._copyla,
                                 5:self._copylr,
                                 6:self._copyli,
                                 7:self._copyar,
                                 8:self._copyai,
                                 9:self._copyra,
                                10:self._copyrr,
                                11:self._copyri,
                                12:self._copyia,
                                13:self._copyir,
                                14:self._copyii,
                                15:self._swapra,
                                16:self._swaprr,
                                17:self._addla,
                                18:self._addra,
                                19:self._subla,
                                20:self._subra,
                                21:self._mul,
                                22:self._div,
                                23:self._andla,
                                24:self._andra,
                                25:self._orla,
                                26:self._orra,
                                27:self._xorla,
                                28:self._xorra,
                                29:self._decr,
                                30:self._incr,
                                31:self._decrjz,
                                32:self._incrjz,
                                33:self._shiftrl,
                                34:self._shiftrr,
                                35:self._cbr,
                                36:self._sbr,
                                37:self._bchg,
                                38:self._bcrsc,
                                39:self._bcrss,
                                40:self._jump,
                                41:self._jumpi,
                                42:self._call,
                                43:self._calli,
                                44:self._return,
                                45:self._retla,
                                46:self._addrpc,
                                47:self._randa,
                               192:self._comout,
                               193:self._comin,
                               194:self._comrdy,
                               196:self._pinout,
                               197:self._pinin,
                               198:self._pindir})
                               
        self._comout_callback = None
        self._comin_callback = None
        self._pin_in_callback = None
        self._pin_out_callback = None
        
    def set_default_callbacks(self):
        super().set_default_callbacks()
        self._comin_callback = DigiruleCallbackComInUserInteraction("Serial Input <-")
        self._pin_in_callback = DigiruleCallbackPinInUserInteraction("Pin Input <-")
        self._comout_callback = DigiruleCallbackComOutStdout("Serial Output ->")
        self._pin_out_callback = DigiruleCallbackComOutStdout("Pin Output ->")
        
    def clear_callbacks(self):
        super().clear_callbacks()
        self._comin_callback = None
        self._comout_callback = None
        self._pin_in_callback = None
        self._pin_out_callback = None
        
    @property 
    def comout_callback(self):
        return self._comout_callback
        
    @comout_callback.setter
    def comout_callback(self, new_callback):
        if not isinstance(new_callback, DigiruleCallbackOutputBase):
            raise TypeError(f"comout_callback() setter expected descendant of DigiruleCallbackOutputBase, "
                            f"received {type(new_callback)}")
        self._comout_callback = new_callback
        
    @property 
    def comin_callback(self):
        return self._comin_callback
        
    @comin_callback.setter
    def comin_callback(self, new_callback):
        if not isinstance(new_callback, DigiruleCallbackInputBase):
            raise TypeError(f"comin_callback() setter expected descendant of DigiruleCallbackInputBase, "
                            f"received {type(new_callback)}")
        self._comin_callback = new_callback

    @property
    def pin_in_callback(self):
            return self._pin_in_callback
            
    @pin_in_callback.setter
    def pin_in_callback(self, new_callback):
        if not isinstance(new_callback, DigiruleCallbackInputBase):
            raise TypeError(f"pin_in_callback() setter expected descendant of DigiruleCallbackInputBase, "
                            f"received {type(new_callback)}")
        self._pin_in_callback = new_callback
    
    @property
    def pin_out_callback(self):
        return self._pin_out_callback
    
    @pin_out_callback.setter
    def pin_out_callback(self, new_callback):
        if not isinstance(new_callback, DigiruleCallbackInputBase):
            raise TypeError(f"comin_callback() setter expected descendant of DigiruleCallbackInputBase, "
                            f"received {type(new_callback)}")
        self._pin_out_callback = new_callback
            
    def _initsp(self):
        self._ppc = []
        
    def _bchg(self):
        # Bit toggling
        bit_to_toggle = self._read_next()
        addr = self._read_next()
        new_value = (self._rd_mem(addr) ^ (1<<bit_to_toggle)) & 0xFF
        self._wr_mem(addr, new_value)  
        
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
        
    def _addla(self):
        new_value = self._get_acc_value() + self._read_next()
        if self._get_status_reg(self._CARRY_FLAG_BIT):
            new_value+=1
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

    def _addra(self):
        new_value = self._get_acc_value() + self._rd_mem(self._read_next())
        if self._get_status_reg(self._CARRY_FLAG_BIT):
            new_value+=1
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

    def _subla(self):
        new_value = self._get_acc_value() - self._read_next()
        if self._get_status_reg(self._CARRY_FLAG_BIT):
            new_value-=1
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

    def _subra(self):
        new_value = self._get_acc_value() - self._rd_mem(self._read_next())
        if self._get_status_reg(self._CARRY_FLAG_BIT):
            new_value-=1
        self._set_acc_value(new_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))
    
    def _mul(self):
        mem_addr_left = self._read_next()
        mem_val_left = self._rd_mem(mem_addr_left)
        mem_addr_right = self._read_next()
        mem_val_right = self._rd_mem(mem_addr_right)
        product = mem_val_left * mem_val_right
        self._wr_mem(mem_addr_left,product & 0xFF)
        self._set_status_reg(self._CARRY_FLAG_BIT, product > 255)
        self._set_status_reg(self._ZERO_FLAG_BIT, (product & 0xFF) == 0)
        
    def _div(self):
        # TODO: MED, This can raise a divide by zero warning / exception too
        mem_addr_left = self._read_next()
        mem_val_left = self._rd_mem(mem_addr_left)
        mem_addr_right = self._read_next()
        mem_val_right = self._rd_mem(mem_addr_right)
        if mem_val_right == 0:
            # This is the default division by zero behaviour
            raise DgtoolsErrorProgramHalt("Division by zero.")
        div_res = mem_val_left // mem_val_right
        self._wr_mem(mem_addr_left, div_res & 0xFF)
        self._set_acc_value(mem_val_left % mem_val_right)
        self._set_status_reg(self._ZERO_FLAG_BIT, (div_res & 0xFF) == 0)
        self._set_status_reg(self._CARRY_FLAG_BIT, self._get_acc_value() == 0) 
        
    def _copyli(self):
        literal = self._read_next()
        i_addr = self._read_next()
        self._wr_mem(self._rd_mem(i_addr), literal)
        self._set_status_reg(self._ZERO_FLAG_BIT, literal == 0)
        
    def _copyai(self):
        i_addr = self._read_next()
        self._wr_mem(self._rd_mem(i_addr), self._get_acc_value())
        self._set_status_reg(self._ZERO_FLAG_BIT, self._get_acc_value() == 0)
        
    def _copyia(self):
        i_addr = self._read_next()
        self._set_acc_value(self._rd_mem(self._rd_mem(i_addr)))
        self._set_status_reg(self._ZERO_FLAG_BIT, self._get_acc_value() == 0)

    def _copyri(self):
        mem_addr = self._read_next()
        mem_addr_value = self._rd_mem(mem_addr)
        i_addr = self._read_next()
        #self._wr_mem(self._rd_mem(self._rd_mem(i_addr)), mem_addr_value)
        self._wr_mem(self._rd_mem(i_addr), mem_addr_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, mem_addr_value == 0) 
        
    def _copyir(self):
        i_addr = self._read_next()
        mem_addr = self._read_next()
        i_addr_value = self._rd_mem(self._rd_mem(i_addr))
        self._wr_mem(mem_addr,i_addr_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, i_addr_value == 0)
    
    def _copyii(self):
        i_addr_l = self._read_next()
        i_addr_r = self._read_next()
        i_addr_l_value = self._rd_mem(self._rd_mem(i_addr_l))
        self._wr_mem(self._rd_mem(i_addr_r), i_addr_l_value)
        self._set_status_reg(self._ZERO_FLAG_BIT, i_addr_l_value == 0)
        
    def _calli(self):
        self._push_pc()
        i_addr = self._read_next()
        self._pc = self._rd_mem(i_addr)
        
    def _jumpi(self):
        i_addr = self._read_next()
        self._pc = self._rd_mem(i_addr)
        
    def _comout(self):
        if self._comout_callback is not None:
            self._comout_callback(self._acc)
        
    def _comin(self):
        if self._comin_callback is not None:
            self._set_acc_value(self._comin_callback())
        
    def _comrdy(self):
        # Comms is always "ready" in emulation.
        # TODO: MED, Maybe this can be matched to a more realistic behaviour once comout, comin are connected to real files.
        self._set_status_reg(self._ZERO_FLAG_BIT, 0)
        
    # TODO: MID, Reduce code duplication in _comin, _comout
    def _pinout(self):
        # Send ACC n bit to n_pin.
        # The n_pin is a mask
        n_pin = self._read_next()
        if n_pin>=1 and n_pin<=3:
            if self._pin_out_callback is not None:
                if n_pin != 3:
                    # Only one pin is sent to the output
                    pin_label = f"(PIN {n_pin}) "
                    self._pin_out_callback.label=f"{pin_label}{self._pin_out_callback.label}"
                    self._pin_out_callback(48 + ((self._get_acc_value() & n_pin)>>(n_pin-1)))
                    self._pin_out_callback.label = self._pin_out_callback.label.replace(pin_label,"")
                else:
                    # Both pins are sent to the output
                    pin_label = f"(PIN 1) "
                    self._pin_out_callback.label=f"{pin_label}{self._pin_out_callback.label}"
                    self._pin_out_callback(48 + (self._get_acc_value() & 1))
                    self._pin_out_callback.label = self._pin_out_callback.label.replace(pin_label,"")
                    
                    pin_label = f"(PIN 2) "
                    self._pin_out_callback.label=f"{pin_label}{self._pin_out_callback.label}"
                    self._pin_out_callback(48 + ((self._get_acc_value() & 2)>>1))
                    self._pin_out_callback.label = self._pin_out_callback.label.replace(pin_label,"")
        
    def _pinin(self):
        # Read ACC n bit to n_pin (1-3)
        # The n_pin is a mask if n_pin<3. If n_pin is 3 then the operation is carried out on both pins
        n_pin = self._read_next()
        if n_pin>=1 and n_pin<=3:
            if self._pin_in_callback is not None:
                if n_pin != 3:
                    # Only one pin is read
                    # TODO: LOW, Improve the way the label is modified externally
                    pin_label = f"(PIN {n_pin}) "
                    self._pin_in_callback.label=f"{pin_label}{self._pin_in_callback.label}"
                    self._set_acc_value((self._get_acc_value() & ~n_pin) | self._pin_in_callback())
                    self._pin_in_callback.label = self._pin_in_callback.label.replace(pin_label,"")
                else:
                    # Both pins are read
                    pin_label = f"(PIN 1) "
                    self._pin_in_callback.label=f"{pin_label}{self._pin_in_callback.label}"
                    self._set_acc_value((self._get_acc_value() & ~1) | self._pin_in_callback())
                    self._pin_in_callback.label = self._pin_in_callback.label.replace(pin_label,"")
                    
                    pin_label = f"(PIN 2) "
                    self._pin_in_callback.label=f"{pin_label}{self._pin_in_callback.label}"
                    self._set_acc_value((self._get_acc_value() & ~2) | (self._pin_in_callback()<<1))
                    self._pin_in_callback.label = self._pin_in_callback.label.replace(pin_label,"")
        
    def _pindir(self):
        # Set the pin I/O direction
        # The n_pin is a mask
        n_pin = self._read_next()
        

    @staticmethod
    def get_asm_statement_def(existing_defs):
        """
        Returns the assembly parser that the Digirule2U understands.
        
        Notes:
            
            * See inline comments for specification of the grammar
        """
        # NOTE: The instruction set on the 2U is so different that it is more practical to 
        #       write the whole definition as if from scratch.
        
        # Digirule 2U ASM instructions
        asm_halt = pyparsing.Group(pyparsing.Regex(r"HALT")("cmd"))("0:0")
        asm_nop = pyparsing.Group(pyparsing.Regex(r"NOP")("cmd"))("1:0")
        asm_speed = pyparsing.Group(pyparsing.Regex(r"SPEED")("cmd") + existing_defs["literal_or_identifier"]("value"))("2:1")
        asm_initsp = pyparsing.Group(pyparsing.Regex(r"INITSP")("cmd"))("3:0")
        asm_copyla = pyparsing.Group(pyparsing.Regex(r"COPYLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("4:1")
        asm_copylr = pyparsing.Group(pyparsing.Regex("COPYLR")("cmd") + existing_defs["literal_or_identifier"]("value") + existing_defs["literal_or_identifier"]("addr"))("5:2")
        asm_copyli = pyparsing.Group(pyparsing.Regex("COPYLI")("cmd") + existing_defs["literal_or_identifier"]("value") + existing_defs["literal_or_identifier"]("iaddr"))("6:2")
        asm_copyar = pyparsing.Group(pyparsing.Regex("COPYAR")("cmd") + existing_defs["literal_or_identifier"]("addr"))("7:1")
        asm_copyai = pyparsing.Group(pyparsing.Regex("COPYAI")("cmd") + existing_defs["literal_or_identifier"]("iaddr"))("8:1")
        asm_copyra = pyparsing.Group(pyparsing.Regex("COPYRA")("cmd") + existing_defs["literal_or_identifier"]("addr"))("9:1")
        asm_copyrr = pyparsing.Group(pyparsing.Regex("COPYRR")("cmd") + existing_defs["literal_or_identifier"]("addr_from") + existing_defs["literal_or_identifier"]("addr_to"))("10:2")
        asm_copyri = pyparsing.Group(pyparsing.Regex("COPYRI")("cmd") + existing_defs["literal_or_identifier"]("addr_from") + existing_defs["literal_or_identifier"]("iaddr_to"))("11:2")
        asm_copyia = pyparsing.Group(pyparsing.Regex("COPYIA")("cmd") + existing_defs["literal_or_identifier"]("iaddr_from"))("12:1")
        asm_copyir = pyparsing.Group(pyparsing.Regex("COPYIR")("cmd") + existing_defs["literal_or_identifier"]("iaddr_from") + existing_defs["literal_or_identifier"]("addr_to"))("13:2")
        asm_copyii = pyparsing.Group(pyparsing.Regex("COPYII")("cmd") + existing_defs["literal_or_identifier"]("iaddr_from") + existing_defs["literal_or_identifier"]("iaddr_to"))("14:2")
        asm_swapra = pyparsing.Group(pyparsing.Regex("SWAPRA")("cmd") + existing_defs["literal_or_identifier"]("addr_from"))("15:1")
        asm_swaprr = pyparsing.Group(pyparsing.Regex("SWAPRR")("cmd") + existing_defs["literal_or_identifier"]("addr_from") + existing_defs["literal_or_identifier"]("addr_to"))("16:2")
        asm_addla = pyparsing.Group(pyparsing.Regex("ADDLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("17:1")
        asm_addra = pyparsing.Group(pyparsing.Regex("ADDRA")("cmd") + existing_defs["literal_or_identifier"]("addr"))("18:1")
        asm_subla = pyparsing.Group(pyparsing.Regex("SUBLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("19:1")
        asm_subra = pyparsing.Group(pyparsing.Regex("SUBRA")("cmd") + existing_defs["literal_or_identifier"]("value"))("20:1")
        asm_mul = pyparsing.Group(pyparsing.Regex("MUL")("cmd") + existing_defs["literal_or_identifier"]("addr_left") + existing_defs["literal_or_identifier"]("addr_right"))("21:2")
        asm_div = pyparsing.Group(pyparsing.Regex("DIV")("cmd") + existing_defs["literal_or_identifier"]("addr_left") + existing_defs["literal_or_identifier"]("addr_right"))("22:2")
        asm_andla = pyparsing.Group(pyparsing.Regex("ANDLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("23:1")
        asm_andra = pyparsing.Group(pyparsing.Regex("ANDRA")("cmd") + existing_defs["literal_or_identifier"]("addr"))("24:1")
        asm_orla = pyparsing.Group(pyparsing.Regex("ORLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("25:1")
        asm_orra = pyparsing.Group(pyparsing.Regex("ORRA")("cmd") + existing_defs["literal_or_identifier"]("addr"))("26:1")
        asm_xorla = pyparsing.Group(pyparsing.Regex("XORLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("27:1")
        asm_xorra = pyparsing.Group(pyparsing.Regex("XORRA")("cmd") + existing_defs["literal_or_identifier"]("addr"))("28:1")
        asm_decr = pyparsing.Group(pyparsing.Regex("DECR")("cmd") + existing_defs["literal_or_identifier"]("addr"))("29:1")
        asm_incr = pyparsing.Group(pyparsing.Regex("INCR")("cmd") + existing_defs["literal_or_identifier"]("addr"))("30:1")
        asm_decrjz = pyparsing.Group(pyparsing.Regex("DECRJZ")("cmd") + existing_defs["literal_or_identifier"]("addr"))("31:1")
        asm_incrjz = pyparsing.Group(pyparsing.Regex("INCRJZ")("cmd") + existing_defs["literal_or_identifier"]("addr"))("32:1")
        asm_shiftrl = pyparsing.Group(pyparsing.Regex("SHIFTRL")("cmd") + existing_defs["literal_or_identifier"]("addr"))("33:1")
        asm_shiftrr = pyparsing.Group(pyparsing.Regex("SHIFTRR")("cmd") + existing_defs["literal_or_identifier"]("addr"))("34:1")
                
        asm_cbr = pyparsing.Group(pyparsing.Regex("CBR|BCLR")("cmd") + existing_defs["literal_or_identifier"]("n_bit") + existing_defs["literal_or_identifier"]("addr"))("35:2")
        asm_sbr = pyparsing.Group(pyparsing.Regex("SBR|BSET")("cmd") + existing_defs["literal_or_identifier"]("n_bit") + existing_defs["literal_or_identifier"]("addr"))("36:2")
        asm_bchg = pyparsing.Group(pyparsing.Regex("BCHG")("cmd") + existing_defs["literal_or_identifier"]("n_bit") + existing_defs["literal_or_identifier"]("addr"))("37:2")
        
        asm_bcrsc = pyparsing.Group(pyparsing.Regex("BCRSC|BTSTSC")("cmd") + existing_defs["literal_or_identifier"]("n_bit") + existing_defs["literal_or_identifier"]("addr"))("38:2")
        asm_bcrss = pyparsing.Group(pyparsing.Regex("BCRSS|BTSTSS")("cmd") + existing_defs["literal_or_identifier"]("n_bit") + existing_defs["literal_or_identifier"]("addr"))("39:2")
        asm_jump = pyparsing.Group(pyparsing.Regex("JUMP")("cmd") + existing_defs["literal_or_identifier"]("addr"))("40:1")
        asm_jumpi = pyparsing.Group(pyparsing.Regex("JUMPI")("cmd") + existing_defs["literal_or_identifier"]("iaddr"))("41:1")
        asm_call = pyparsing.Group(pyparsing.Regex("CALL")("cmd") + existing_defs["literal_or_identifier"]("addr"))("42:1")
        asm_calli = pyparsing.Group(pyparsing.Regex("CALLI")("cmd") + existing_defs["literal_or_identifier"]("iaddr"))("43:1")
        asm_return = pyparsing.Group(pyparsing.Regex("RETURN")("cmd"))("44:0")
        asm_retla = pyparsing.Group(pyparsing.Regex("RETLA")("cmd") + existing_defs["literal_or_identifier"]("value"))("45:1")
        asm_addrpc = pyparsing.Group(pyparsing.Regex("ADDRPC")("cmd") + existing_defs["literal_or_identifier"]("value"))("46:1")
        asm_randa = pyparsing.Group(pyparsing.Regex("RANDA")("cmd"))("47:0")
        asm_comout = pyparsing.Group(pyparsing.Regex("COMOUT")("cmd"))("192:0")
        asm_comin = pyparsing.Group(pyparsing.Regex("COMIN")("cmd"))("193:0")
        asm_comrdy = pyparsing.Group(pyparsing.Regex("COMRDY")("cmd"))("194:0")
        asm_pinout = pyparsing.Group(pyparsing.Regex("PINOUT")("cmd") + existing_defs["literal_or_identifier"]("value"))("196:1")
        asm_pinin = pyparsing.Group(pyparsing.Regex("PININ")("cmd") + existing_defs["literal_or_identifier"]("value"))("197:1")
        asm_pindir = pyparsing.Group(pyparsing.Regex("PINDIR")("cmd") + existing_defs["literal_or_identifier"]("value"))("198:1")
        
        asm_statement = pyparsing.Group(asm_halt ^ asm_nop ^ asm_speed ^ asm_initsp ^ asm_copyla ^ asm_copylr ^ \
                                        asm_copyli ^ asm_copyar ^ asm_copyai ^ asm_copyra ^ asm_copyrr ^ asm_copyri ^ \
                                        asm_copyia ^ asm_copyir ^ asm_copyii ^ asm_swapra ^ asm_swaprr ^ asm_addla ^ \
                                        asm_addra ^ asm_subla ^ asm_subra ^ asm_mul ^ asm_div ^ asm_andla ^ \
                                        asm_andra ^ asm_orla ^ asm_orra ^ asm_xorla ^ asm_xorra ^ asm_decr ^ \
                                        asm_incr ^ asm_decrjz ^ asm_incrjz ^ asm_shiftrl ^ asm_shiftrr ^ asm_cbr ^ \
                                        asm_sbr ^ asm_bchg ^ asm_bcrsc ^ asm_bcrss ^ \
                                        asm_jump ^ asm_jumpi ^ asm_call ^ asm_calli ^ asm_return ^ asm_retla ^ \
                                        asm_addrpc ^ asm_randa ^ asm_comout ^ asm_comin ^ asm_comrdy ^ \
                                        asm_pinout ^ asm_pinin ^ asm_pindir)

        return asm_statement
