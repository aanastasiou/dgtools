from .dgcpu_base import DGMemorySpaceBase, DGCPU

from .exceptions import DgtoolsErrorOpcodeNotSupported, DgtoolsErrorProgramHalt, DgtoolsErrorOutOfMemory
from .callbacks import (DigiruleCallbackInputBase, DigiruleCallbackInputUserInteraction, DigiruleCallbackComOutStdout, 
                        DigiruleCallbackComInUserInteraction, DigiruleCallbackPinInUserInteraction)
import random
import pyparsing


class MemorySpaceDigirule(DGMemorySpaceBase):
    def __init__(self):
        super().__init__()
        self._mem_base = 3
        self._reg_map = {"Acc":0,
                         "SPEED":1,
                         "INPUT":253 + self._mem_base,
                         "ADDR_LED":254 + self._mem_base,
                         "DATA_LED":255 + self._mem_base,
                         "STATUS":252 + self._mem_base,
                         "PC":2}
        self._mem_len = 256
        self._mem = bytearray([0 for k in range(0, self._mem_len + self._mem_base)])
        
class Digirule(DGCPU):
    def __init__(self):
        super().__init__()
        self._mem_space = MemorySpaceDigirule()
        self._pc_reg = "PC"
        self._ppc = []
        # The status reg contains the zero flag (bit 0) and the carry flag (bit 1)
        self._ZERO_FLAG_BIT = 1 << 0 # Directly convert bits to their binary representations here
        self._CARRY_FLAG_BIT = 1 << 1
        self._ADDRLED_FLAG_BIT = 1 << 2     
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
    def interactive_callback(self):
        return self._interactive_callback
        
    @interactive_callback.setter
    def interactive_callback(self, new_callback):
        # if not isinstance(new_callback, DigiruleCallbackInputBase):
            # raise TypeError(f"interactive_callback() setter expected descendant of DigiruleCallbackInputBase, "
                            # f"received {type(new_callback)}")
        self._interactive_callback = new_callback
            
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
                
    def _push_pc(self):
        self._ppc.append(self.pc + 1)
        return self
        
    def _pop_pc(self):
        try:
            self._pc = self._ppc.pop()
        except IndexError:
            raise DgtoolsErrorStackUnderflow("Program stack underflow.")
        return self
        
    # def _set_acc_value(self, new_value):
        # """
        # Sets the accumulator value, taking care of the zero and carry flags.
        
        # :param new_value: The value to set the Accumulator to.
        # :type new_value: uint8
        # """
        # self._acc = new_value & 0xFF
        # return self
        
    # def _get_acc_value(self):
        # return self._acc
        
    # def _set_status_reg(self, field_mask, value):
        # current_value = self._mem[self._status_reg_ptr]
        # self._mem[self._status_reg_ptr] ^= (-value ^ current_value) & field_mask
        # return self
        
    # def _get_status_reg(self, field_mask):
        # return 1 if (self._mem[self._status_reg_ptr] & field_mask) == field_mask else 0
        
    # def _wr_mem(self, addr, value):
        # self._mem[addr & 0xFF] = value & 0xFF
        # return self
        
    # def _rd_mem(self, addr):
        # """
        # Reads memory from the specified address.
        
        # Notes:
        
            # * If the VM is in interactive mode and the button register is attempted to be read, it prompts the user 
              # for input.
        # """
        # if addr == self._bt_reg_ptr and self._interactive_callback is not None:
            # self._mem[addr] = self._interactive_callback()
        # return self._mem[addr]
        
    def _halt(self):
        raise DgtoolsErrorProgramHalt("Program terminated at HALT instruction.")
        
    def _nop(self):
        pass
        
    def _speed(self):
        self.mem["SPEED"] = self._read_next()
        
    def _copylr(self):
        literal = self._read_next()
        self.mem[self._read_next()] = literal
        
    def _copyla(self):
        literal = self._read_next()
        self.mem["Acc"] = literal

    def _copyar(self):
        self.mem[self._read_next()] = self.mem["Acc"]

    def _copyra(self):
        new_value = self.mem(self._read_next())
        self.mem["Acc"] = new_value
        self.mem["STATUS", self._ZERO_FLAG_BIT] = ((new_value==0) & 0xFF)

    def _copyrr(self):
        addr1 = self._read_next()
        value_addr1 = self.mem[addr1] & 0xFF
        addr2 = self._read_next()
        self.mem[addr2] = value_addr1
        self.mem["STATUS", self._ZERO_FLAG_BIT] = ((value_addr1==0) & 0xFF)

    def _addla(self):
        new_value = self.mem["Acc"] + self._read_next()
        self.mem["Acc"] = new_value
        self.mem["STATUS", self._ZERO_FLAG_BIT] = ((self._acc==0) & 0xFF)
        self.mem["STATUS", self._CARRY_FLAG_BIT] = ((new_value > 255 or new_value < 0) & 0xFF)

    def _addra(self):
        new_value = (self.mem["Acc"] + self._rd_mem(self._read_next())) & 0xFF
        self.mem["Acc"] = new_value 
        self.mem["STATUS", self._ZERO_FLAG_BIT] = ((new_value==0) & 0xFF)

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

