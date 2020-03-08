import sys
import pdb
import pyparsing

import sys
import pdb

class Digirule:
    def __init__(self):
        self._pc = 0
        self._ppc = []
        self._acc = 0
        # The status reg contains the zero flag (bit 0) and the carry flag (bit 1)
        self._ZERO_FLAG_BIT = 1 << 0 # Directly convert bits to their binary representations here
        self._CARRY_FLAG_BIT = 1 << 1
        self._ADDRLED_FLAG_BIT = 1 << 2     
        self._status_reg_ptr = 252
        self._bt_reg_ptr = 253
        self._addrled_reg_ptr = 254
        self._dataled_reg_ptr = 255
        self._mem = [0 for k in range(0,256)]
        # The speed setting is just for visualisation
        self._speed_setting = 0
                
    def load_program(self, a_program, offset=0):
        for k in enumerate(a_program):
            self._mem[k[0]+offset] = k[1]            
        return self
        
    def set_button_register(self, new_value):
        self._wr_mem(self._bt_reg_ptr, new_value & 255)
        return self
        
    def _read_next(self):
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
        self._acc = new_value & 255
        if new_value == 0:
            self._set_status_reg(self._ZERO_FLAG_BIT, 1)
        else:
            self._set_status_reg(self._ZERO_FLAG_BIT, 0)
            
        if new_value > 255:
            self._set_status_reg(self._CARRY_FLAG_BIT, 1)
        else:
            self._set_status_reg(self._CARRY_FLAG_BIT, 0)
        
        return self
        
    def _get_acc_value(self):
        return self._acc
        
    def _set_status_reg(self, field_mask, value):
        self._mem[self._status_reg_ptr] |= (field_mask * value)
        return self
        
    def _get_status_reg(self, field_mask):
        return 1 if self._mem[self._status_reg_ptr] & field_mask == field_mask else 0
        
    def _get_zero_flag(self):
        return 1 if self._mem[self._status_reg_ptr] & self._ZERO_FLAG_BIT == self._ZERO_FLAG_BIT else 0
        
    def _wr_mem(self, addr, value):
        # TODO: HIGH, addr cannot go higher than 252
        # TODO: HIGH, value cannot go higher than 255
        # TODO: HIGH, addr cannot go lower than 0
        self._mem[addr] = value
        return self
        
    def _rd_mem(self, addr):
        return self._mem[addr]
                
    def _exec_next(self):
        """
        Executes a command
        """
        cmd = self._read_next()
        
        if cmd>32:
            # Throw an exception
            pass
            
        # HALT
        if cmd == 0:
            # TODO: HIGH, Throw exception
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
            addr2 = self._read_next()
            self._wr_mem(addr2, self._rd_mem(addr1))
            
        # ADDLA
        if cmd == 8:
            new_value = self._get_acc_value()+self._read_next()
            self._set_acc_value(new_value)           
            
        # ADDRA
        if cmd == 9:
            self._set_acc_value(self._get_acc_value()+self._rd_mem(self._read_next()))
            
        # SUBLA
        if cmd == 10:
            self._set_acc_value(self._get_acc_value()-self._read_next())
            
        # SUBRA
        if cmd == 11:
            self._set_acc_value(self._get_acc_value()-self._rd_mem(self._read_next()))
            
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
            self._wr_mem(addr, value)
            if value == 0:
                self._set_status_reg(self._ZERO_FLAG_BIT,0)
                self._pc+=2
                
        # INCRJZ
        if cmd == 21:
            addr = self._read_next()
            value = self._rd_mem(addr) + 1
            self._wr_mem(addr, value)
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
            self._wr_mem(addr, ((value<<1) & 255)|self._get_status_reg(self._CARRY_FLAG_BIT))
            self._set_status_reg(self._CARRY_FLAG_BIT,next_carry_value)

        # SHIFTRR
        if cmd == 23:
            addr = self._read_next()
            value = self._rd_mem(addr)
            next_carry_value = 1 if value & 1 == 1 else 0
            self._wr_mem(addr, ((value>>1) & 255)|(self._get_status_reg(self._CARRY_FLAG_BIT) << 7))
            self._set_status_reg(self._CARRY_FLAG_BIT,next_carry_value)
            
        # CBR
        if cmd == 24:
            bit_to_clear = self._read_next()
            addr = self._read_next()
            new_value = self._rd_mem(addr) & (255 - (1<<bit_to_clear))
            self._wr_mem(addr, new_value)
                    
        # SBR
        if cmd == 25:
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
        self._pc = offset
    
    def run(self, offset=0):
        """
        Executes commands from the current program counter until it meets HLT
        """
        self._pc = offset
        cnt = self._exec_next()
        while cnt:
            cnt = self._exec_next()
            
    def step(self):
        return self._exec_next()
        
    def __str__(self):
        return "ADDR LED:"+format(self._pc,"08b")+"\nDATA LED:"+format(self._rd_mem(self._pc), "08b")+"\nBTT SW  :"+format(self._rd_mem(self._bt_reg_ptr),"08b")

        
def get_asm_parser():
    """
    identifer = [a-zA-Z_][a-zA-Z_0-9]+
    program = statement+
    statement = asm_statement or assembler_directive
    asm_statement = asm_label or asm_keyword
    asm_label = ":" followed by an identifier
    asm_keyword = symbolic_def|data_segment
    symbolic_def = "%%define"
    data_segment = ".CODE" + symbolic_def+
    assembler_directive = "\t|at least 4 whitespace" followed by command_line
    command_line = keyword followed by parameter_list
    keyword = (one of the digirule keywords)
    parameter_list = space separated list of tokens at most 2 entries long
    """
    uchar2num = lambda toks:int(toks[0])
    buchar2num = lambda toks:int(toks[0],2)
    xuchar2num = lambda toks:int(toks[0],16)
    identifier = pyparsing.Regex(r"[a-zA-Z_][a-zA-Z0-9_]+")
    literal_uchar = pyparsing.Regex(r"[-]?[0-9][0-9]?[0-9]?").setParseAction(uchar2num)
    literal_buchar = pyparsing.Regex(r"0b[0|1]+").setParseAction(buchar2num)
    literal_xuchar = pyparsing.Regex(r"0x[0-9A-F][0-9A-F]?").setParseAction(xuchar2num)
    literal = literal_uchar ^ literal_buchar ^ literal_xuchar
    literal_or_identifier = pyparsing.Group(literal("literal") ^ identifier("symbol"))("value_type")
    # Digirule ASM commands
    asm_halt = pyparsing.Group(pyparsing.Regex(r"HALT")("cmd"))("0")
    asm_nop = pyparsing.Group(pyparsing.Regex(r"NOP")("cmd"))("1")
    asm_speed = pyparsing.Group(pyparsing.Regex(r"SPEED")("cmd") + literal_or_identifier("value"))("2")
    asm_copylr = pyparsing.Group(pyparsing.Regex("COPYLR")("cmd") + literal_or_identifier("value") + literal_or_identifier("addr"))("3")
    asm_copyla = pyparsing.Group(pyparsing.Regex(r"COPYLA")("cmd") + literal_or_identifier("value"))("4")
    asm_copyar = pyparsing.Group(pyparsing.Regex("COPYAR")("cmd") + literal_or_identifier("addr"))("5")
    asm_copyra = pyparsing.Group(pyparsing.Regex("COPYRA")("cmd") + literal_or_identifier("addr"))("6")
    asm_copyrr = pyparsing.Group(pyparsing.Regex("COPYRR")("cmd") + literal_or_identifier("addr_from") + literal_or_identifier("addr_to"))("7")
    asm_addla = pyparsing.Group(pyparsing.Regex("ADDLA")("cmd") + literal_or_identifier("value"))("8")
    asm_addra = pyparsing.Group(pyparsing.Regex("ADDRA")("cmd") + literal_or_identifier("addr"))("9")
    asm_subla = pyparsing.Group(pyparsing.Regex("SUBLA")("cmd") + literal_or_identifier("value"))("10")
    asm_subra = pyparsing.Group(pyparsing.Regex("SUBRA")("cmd") + literal_or_identifier("value"))("11")
    asm_andla = pyparsing.Group(pyparsing.Regex("ANDLA")("cmd") + literal_or_identifier("value"))("12")
    asm_andra = pyparsing.Group(pyparsing.Regex("ANDRA")("cmd") + literal_or_identifier("addr"))("13")
    asm_orla = pyparsing.Group(pyparsing.Regex("ORLA")("cmd") + literal_or_identifier("value"))("14")
    asm_orra = pyparsing.Group(pyparsing.Regex("ORRA")("cmd") + literal_or_identifier("addr"))("15")
    asm_xorla = pyparsing.Group(pyparsing.Regex("XORLA")("cmd") + literal_or_identifier("value"))("16")
    asm_xorra = pyparsing.Group(pyparsing.Regex("XORRA")("cmd") + literal_or_identifier("addr"))("17")
    asm_decr = pyparsing.Group(pyparsing.Regex("DECR")("cmd") + literal_or_identifier("addr"))("18")
    asm_incr = pyparsing.Group(pyparsing.Regex("INCR")("cmd") + literal_or_identifier("addr"))("19")
    asm_decrjz = pyparsing.Group(pyparsing.Regex("DECRJZ")("cmd") + literal_or_identifier("addr"))("20")
    asm_incrjz = pyparsing.Group(pyparsing.Regex("INCRJZ")("cmd") + literal_or_identifier("addr"))("21")
    asm_shiftrl = pyparsing.Group(pyparsing.Regex("SHIFTRL")("cmd") + literal_or_identifier("addr"))("22")
    asm_shiftrr = pyparsing.Group(pyparsing.Regex("SHIFTRR")("cmd") + literal_or_identifier("addr"))("23")
    asm_cbr = pyparsing.Group(pyparsing.Regex("CBR")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("24")
    asm_sbr = pyparsing.Group(pyparsing.Regex("SBR")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("25")
    asm_bcrsc = pyparsing.Group(pyparsing.Regex("BCRSC")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("26")
    asm_bcrss = pyparsing.Group(pyparsing.Regex("BCRSS")("cmd") + literal_or_identifier("n_bit") + literal_or_identifier("addr"))("27")
    asm_jump = pyparsing.Group(pyparsing.Regex("JUMP")("cmd") + literal_or_identifier("addr"))("28")
    asm_call = pyparsing.Group(pyparsing.Regex("CALL")("cmd") + literal_or_identifier("addr"))("29")
    asm_retla = pyparsing.Group(pyparsing.Regex("RETLA")("cmd") + literal_or_identifier("value"))("30")
    asm_return = pyparsing.Group(pyparsing.Regex("RETURN")("cmd"))("31")
    asm_addrpc = pyparsing.Group(pyparsing.Regex("ADDRPC")("cmd") + literal_or_identifier("value"))("32")
    asm_command = pyparsing.Group(asm_halt ^ asm_nop ^ asm_speed ^ asm_copylr ^ asm_copyla ^ asm_copyar ^ asm_copyra ^ asm_copyrr ^ \
              asm_addla ^ asm_addra ^ asm_subla ^ asm_subra ^ asm_andla ^ asm_andra ^ asm_subla ^ asm_subra ^ \
              asm_andla ^ asm_andra ^ asm_orla ^ asm_orra ^ asm_xorla ^ asm_xorra ^ asm_decr ^ asm_incr ^ \
              asm_decrjz ^ asm_incrjz ^ asm_shiftrl ^ asm_shiftrr ^ asm_cbr ^ asm_sbr ^ asm_bcrsc ^ asm_bcrss ^ \
              asm_jump ^ asm_call ^ asm_retla ^ asm_return ^ asm_addrpc)
    asm_statement = asm_command
    # Assembler directives
    # .DB A static list of byte defs
    # label: Defines a label
    dir_label = pyparsing.Group(identifier("idf") + pyparsing.Suppress(":"))("def_label")
    dir_db = pyparsing.Group(pyparsing.Regex(".DB")("cmd") + pyparsing.delimitedList(literal_or_identifier)("values"))("def_db")
    dir_equ = pyparsing.Group(pyparsing.Regex(".EQU")("cmd") + identifier("idf") + pyparsing.Suppress("=") + literal("value"))("def_equ")
    #dir_comment = pyparsing.Group(pyparsing.Suppress("#") + pyparsing.Regex(r".*?\n")("text"))("def_comment")
    #program_statement = pyparsing.Group((asm_statement ^ pyparsing.Group(dir_label ^ dir_db ^ dir_equ ^ dir_comment)) + pyparsing.Optional(dir_comment))
    program = pyparsing.OneOrMore(asm_statement ^ pyparsing.Group(dir_label ^ dir_db ^ dir_equ))
    #program = pyparsing.OneOrMore(program_statement)
    # program.ignore(dir_comment)
    return program    
    
def asm2obj(asm):
    """
    Puts together a binary for the Digirule target architecture from an "asm" definition
    """
    parser = get_asm_parser()
    parsed_code = parser.parseString(asm)
    mem = [0 for k in range(0,256)]
    mem_ptr = 0
    labels = {}
    symbols = {}
    # Read through the code and load it to memory
    # While doing that, keep track of where labels point and what symbols resolve to. These will be substituted
    # in the second pass.
    for a_line in parsed_code:
        command, arguments = list(a_line.items())[0]
        if command == "def_label":
            # Tie the label to where it points to
            labels[arguments["idf"]] = mem_ptr
        elif command == "def_db":
            # .DB simply defines raw data that are simply dumped where they appear. If a label is not set to a 
            # data block, it cannot be referenced.
            value_data = list(map(lambda x:x[0],arguments["values"]))
            mem[mem_ptr:mem_ptr+len(value_data)] = value_data
            mem_ptr+=len(value_data)
        elif command == "def_equ":
            symbols[arguments["idf"]] = arguments["value"]
        else:
            # It's a command. The opcode of the command has already been recognised, but we need to grab the operands
            # wherever they are available
            numeric_command = int(command)
            mem[mem_ptr] = numeric_command
            mem_ptr+=1
            if numeric_command in [3,7,24,25,26,27]:
                mem[mem_ptr] = arguments[1][0]
                mem[mem_ptr + 1] = arguments[2][0]
                mem_ptr+=2
            elif numeric_command not in [0,1,31]:
                mem[mem_ptr] = arguments[1][0] 
                mem_ptr+=1
    for k in range(0, len(mem)):
        if type(mem[k]) is str:
            if mem[k] in labels:
                mem[k] = labels[mem[k]]
            elif mem[k] in symbols:
                mem[k] = symbols[mem[k]]
    return mem, labels, symbols
    
def mem_dump(mem,n_page, page_length=8):
    offset = n_page*page_length
    for k in range(offset, offset+page_length):
        print(mem[k],"-",bin(mem[k]))
        
if __name__ == "__main__":
    # cpu = Digirule()
    # program = [0,0,2,15,0,3]
    # cpu.load_program(program)
    # z = get_asm_model()
    # z.setDefaultWhitespaceChars([" ","\n", "\t"])
    # f = z.parseFile("./first.asm")
    with open("./first.asm", "rt") as fd:
        data = fd.read()
    mem,l,s = asm2obj(data)
    machine = Digirule()
    machine.load_program(mem)
    machine.run()
    
    
