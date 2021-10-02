from .dgcpu_base import DGMemorySpaceBase, DGCPU
from .exceptions import DgtoolsErrorProgramHalt

class MemorySpaceKenback(DGMemorySpaceBase):
    def __init__(self):
        super().__init__()
        self._mem_base = 0
        self._reg_map = {"A":0,
                         "B":1,
                         "X":2,
                         "P":3,
                         "OUTPUT":0O200,
                         "OC_A":0O201,
                         "OC_B":0O202,
                         "OC_X":0O203,
                         "INPUT":0O377}
        self._mem_len = 256
        self._mem = bytearray([0 for k in range(0, self._mem_len)])
        
        
class Kenback(DGCPU):
    def __init__(self):
        super().__init__()
        self._mem_space = MemorySpaceKenback()
        self._pc_reg = "P"
        self._ins_lookup={0:self._halt,
                          127: self._nop,
                          3:self._add,
                          4:self._add,
                          5:self._add,
                          6:self._add,
                          7:self._add,
                          67:self._add,
                          68:self._add,
                          69:self._add,
                          70:self._add,
                          71:self._add,
                          131:self._add,
                          132:self._add,
                          133:self._add,
                          134:self._add,
                          135:self._add,
                          # SUB
                          11:self._sub,
                          12:self._sub,
                          13:self._sub,
                          14:self._sub,
                          15:self._sub,
                          75:self._sub,
                          76:self._sub,
                          77:self._sub,
                          78:self._sub,
                          79:self._sub,
                          139:self._sub,
                          140:self._sub,
                          141:self._sub,
                          142:self._sub,
                          143:self._sub,
                          # LOAD
                          19:self._load,
                          20:self._load,
                          21:self._load,
                          22:self._load,
                          23:self._load,
                          83:self._load,
                          84:self._load,
                          85:self._load,
                          86:self._load,
                          87:self._load,
                          147:self._load,
                          148:self._load,
                          149:self._load,
                          150:self._load,
                          151:self._load,
                          # STORE
                          27:self._store,
                          28:self._store,
                          29:self._store,
                          30:self._store,
                          31:self._store,
                          91:self._store,
                          92:self._store,
                          93:self._store,
                          94:self._store,
                          95:self._store,
                          155:self._store,
                          156:self._store,
                          157:self._store,
                          158:self._store,
                          159:self._store,
                          # LOGIC
                          # AND
                          211:self._and,
                          212:self._and,
                          213:self._and,
                          214:self._and,
                          215:self._and,
                          # OR
                          195:self._or,
                          196:self._or,
                          197:self._or,
                          198:self._or,
                          199:self._or,
                          # LNEG
                          219:self._lneg,
                          220:self._lneg,
                          221:self._lneg,
                          222:self._lneg,
                          223:self._lneg,
                          # JUMPS
                          # Unconditional
                          228:self._jpd,
                          236:self._jpi,
                          244:self._jmd,
                          252:self._jmi,
                          # Conditional on A direct
                          0O073:self._jpdnz,
                          0O074:self._jpdz,
                          0O075:self._jpdltz,
                          0O076:self._jpdgez,
                          0O077:self._jpdgz,
                          0O053:self._jpinz,
                          0O054:self._jpiz,
                          0O055:self._jpiltz,
                          0O056:self._jpigez,
                          0O057:self._jpigz,
                          # Conditional on A mark direct
                          0O063:self._jmdnz,
                          0O064:self._jmdz,
                          0O065:self._jmdltz,
                          0O066:self._jmdgez,
                          0O067:self._jmdgz,
                          # Conditional on A mark indirect
                          0b00111011:self._jminz,
                          0b00111100:self._jmiz,
                          0b00111101:self._jmiltz,
                          0b00111110:self._jmigez,
                          0b00111111:self._jmigz,
                          # Conditional on B direct
                          0b01100011:self._jpdnz,
                          0b01100100:self._jpdz,
                          0b01100101:self._jpdltz,
                          0b01100110:self._jpdgez,
                          0b01100111:self._jpdgz,
                          # Conditional on B indirect
                          0b01101011:self._jpinz,
                          0b01101100:self._jpiz,
                          0b01101101:self._jpiltz,
                          0b01101110:self._jpigez,
                          0b01101111:self._jpigz,
                          # Conditional on B mark direct
                          0b01110011:self._jmdnz,
                          0b01110100:self._jmdz,
                          0b01110101:self._jmdltz,
                          0b01110110:self._jmdgez,
                          0b01110111:self._jmdgz,
                          # Conditional on B mark indirect
                          0b01111011:self._jminz,
                          0b01111100:self._jmiz,
                          0b01111101:self._jmiltz,
                          0b01111110:self._jmigez,
                          0b01111111:self._jmigz,
                          # Conditional on X direct
                          0b10100011:self._jpdnz,
                          0b10100100:self._jpdz,
                          0b10100101:self._jpdltz,
                          0b10100110:self._jpdgez,
                          0b10100111:self._jpdgz,
                          # Conditional on X indirect
                          0b10101011:self._jpinz,
                          0b10101100:self._jpiz,
                          0b10101101:self._jpiltz,
                          0b10101110:self._jpigez,
                          0b10101111:self._jpigz,
                          # Conditional on X mark direct
                          0b10110011:self._jmdnz,
                          0b10110100:self._jmdz,
                          0b10110101:self._jmdltz,
                          0b10110110:self._jmdgez,
                          0b10110111:self._jmdgz,
                          # Conditional on X mark indirect
                          0b10111011:self._jminz,
                          0b10111100:self._jmiz,
                          0b10111101:self._jmiltz,
                          0b10111110:self._jmigez,
                          0b10111111:self._jmigz,
                          # SKIPS
                          # SKIP 0
                          0b10000010:self._skp,
                          0b10001010:self._skp,
                          0b10010010:self._skp,
                          0b10011010:self._skp,
                          0b10100010:self._skp,
                          0b10101010:self._skp,
                          0b10110010:self._skp,
                          0b10111010:self._skp,
                          # SKIP 1
                          0b11000010:self._skp,
                          0b11001010:self._skp,
                          0b11010010:self._skp,
                          0b11011010:self._skp,
                          0b11100010:self._skp,
                          0b11101010:self._skp,
                          0b11110010:self._skp,
                          0b11111010:self._skp,
                          # SET
                          # SET 0
                          0b00000010:self._set,
                          0b00001010:self._set,
                          0b00010010:self._set,
                          0b00011010:self._set,
                          0b00100010:self._set,
                          0b00101010:self._set,
                          0b00110010:self._set,
                          0b00111010:self._set,
                          # SET 1
                          0b01000010:self._set,
                          0b01001010:self._set,
                          0b01010010:self._set,
                          0b01011010:self._set,
                          0b01100010:self._set,
                          0b01101010:self._set,
                          0b01110010:self._set,
                          0b01111010:self._set,
                          # SHIFT
                          # LEFT A
                          0b10001001:self._sft,
                          0b10010001:self._sft,
                          0b10011001:self._sft,
                          0b10000001:self._sft,
                          # RIGHT A
                          0b00001001:self._sft,
                          0b00010001:self._sft,
                          0b00011001:self._sft,
                          0b00000001:self._sft,
                          # LEFT B
                          0b10101001:self._sft,
                          0b10110001:self._sft,
                          0b10111001:self._sft,
                          0b10100001:self._sft,
                          # RIGHT B
                          0b00101001:self._sft,
                          0b00110001:self._sft,
                          0b00111001:self._sft,
                          0b00100001:self._sft,
                          # ROTATE
                          # LEFT A
                          0b11001001:self._rot,
                          0b11010001:self._rot,
                          0b11011001:self._rot,
                          0b11000001:self._rot,
                          # RIGHT A
                          0b01001001:self._rot,
                          0b01011001:self._rot,
                          0b01010001:self._rot,
                          0b01000001:self._rot,
                          # LEFT B
                          0b11101001:self._rot,
                          0b11110001:self._rot,
                          0b11111001:self._rot,
                          0b11100001:self._rot,
                          # RIGHT B
                          0b01101001:self._rot,
                          0b01110001:self._rot,
                          0b01111001:self._rot,
                          0b01100001:self._rot,}
        
    def _halt(self):
        """
        Halt terminates execution.
        """
        raise DgtoolsErrorProgramHalt("Program terminated at HALT instruction.")
        
    def _nop(self):
        """
        No operation.
        """
        pass
        
    def _add(self):
        inst_add = self.mem[self.pc - 1]
        operand = self._read_next()        
        reg, stat_reg = {0:("A", "OC_A"),
                         1:("B", "OC_B"),
                         2:("X", "OC_X")}[inst_add >> 6]
        addr_mode = inst_add & 7
        
        a = self.mem._reg_rd(reg)
        
        # Constant
        if addr_mode == 3:
            b = operand
        # Memory
        if addr_mode == 4:
            b = self.mem._mem_rd(operand, absolute=True)
        # Indirect
        if addr_mode == 5:
            b = self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), absolute=True)
        # Indexed
        if addr_mode == 6:
            b = self.mem._mem_rd(self.mem._reg_rd("X") + operand, absolute=True)
        # Indirect Indexed
        if addr_mode == 7:
            b = self.mem._mem_rd(self.mem._reg_rd("X") + \
                                 self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), \
                                                  absolute=True), \
                                 absolute=True)

        result = a + b
        v_flag = int(result < -127 or result>127)
        c_flag = int(result < 0 or result>255)
        
        self.mem._reg_wr(reg, result & 0xFF)
        self.mem._reg_wr(stat_reg, v_flag + (c_flag << 1))
        
        
    def _sub(self):
        inst_sub = self.mem[self.pc - 1]
        operand = self._read_next()        
        reg, stat_reg = {0:("A", "OC_A"),
                         1:("B", "OC_B"),
                         2:("X", "OC_X")}[inst_sub >> 6]
        addr_mode = inst_sub & 7
        
        a = self.mem._reg_rd(reg)
        
        # Constant
        if addr_mode == 3:
            b = operand
        # Memory
        if addr_mode == 4:
            b = self.mem._mem_rd(operand, absolute=True)
        # Indirect
        if addr_mode == 5:
            b = self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), absolute=True)
        # Indexed
        if addr_mode == 6:
            b = self.mem._mem_rd(self.mem._reg_rd("X") + operand, absolute=True)
        # Indirect Indexed
        if addr_mode == 7:
            b = self.mem._mem_rd(self.mem._reg_rd("X") + \
                                 self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), \
                                                  absolute=True), \
                                 absolute=True)

        result = a - b
        v_flag = int(result < -127 or result>127)
        c_flag = int(result < 0 or result>255)
        
        self.mem._reg_wr(reg, result & 0xFF)
        self.mem._reg_wr(stat_reg, v_flag + (c_flag << 1))
        
        
    def _load(self):
        # Load a register with a value that can come from various sources.
        
        inst_load = self.mem[self.pc - 1]
        operand = self._read_next()        
        reg = {0:"A",
               1:"B",
               2:"X"}[inst_load >> 6]
        addr_mode = inst_load & 7
                    
        # Constant
        if addr_mode == 3:
            self.mem._reg_wr(reg, operand)
        # Memory
        if addr_mode == 4:
            self.mem._reg_wr(reg, self.mem._mem_rd(operand, absolute=True))
        # Indirect
        if addr_mode == 5:
            self.mem._reg_wr(reg, self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), absolute=True))
        # Indexed
        if addr_mode == 6:
            self.mem._reg_wr(reg, self.mem._mem_rd(self.mem._reg_rd("X") + operand, absolute=True))
        # Indirect Indexed
        if addr_mode == 7:
            self.mem._reg_wr(reg, self.mem._mem_rd(self.mem._reg_rd("X") + self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), absolute=True), absolute=True))
        
    def _store(self):
        # The opposite of LOAD
        
        inst_store = self.mem[self.pc - 1]
        store_loc = self._read_next()        
        reg = {0:"A",
               1:"B",
               2:"X"}[inst_store >> 6]
        addr_mode = inst_store & 7
                    
        # Constant
        if addr_mode == 3:
            self.mem._mem_wr(store_loc, self.mem._reg_rd(reg), absolute=True)
        # Memory
        if addr_mode == 4:
            self.mem._mem_wr(self.mem._mem_rd(store_loc, absolute=True), self.mem._reg_rd(reg), absolute=True)
        # Indirect
        if addr_mode == 5:
            self.mem._mem_wr(self.mem._mem_rd(self.mem._mem_rd(store_loc, absolute=True), \
                                              self.mem._reg_rd(reg), absolute=True))
        # Indexed
        if addr_mode == 6:
            self.mem._mem_wr(self.mem._mem_rd(self.mem._reg_rd("X") + store_loc, absolute=True), \
                                              self.mem._reg_rd(reg), absolute=True)
        # Indirect Indexed
        if addr_mode == 7:
            self.mem._mem_wr(self.mem._mem_rd(self.mem._reg_rd("X") + \
                                              self.mem._mem_rd(self.mem._mem_rd(store_loc, \
                                                                                absolute=True), \
                                                                absolute=True), \
                                              absolute=True), self.mem._reg_rd(reg), absolute=True)
        pass
        
    def _and(self):
        inst_and = self.mem[self.pc - 1]
        operand = self._read_next()        
        addr_mode = inst_and & 7
        
        a = self.mem._reg_rd("A")
        
        # Constant
        if addr_mode == 3:
            b = operand
        # Memory
        if addr_mode == 4:
            b = self.mem._mem_rd(operand, absolute=True)
        # Indirect
        if addr_mode == 5:
            b = self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), absolute=True)
        # Indexed
        if addr_mode == 6:
            b = self.mem._mem_rd(self.mem._reg_rd("X") + operand, absolute=True)
        # Indirect Indexed
        if addr_mode == 7:
            b = self.mem._mem_rd(self.mem._reg_rd("X") + \
                                 self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), \
                                                  absolute=True), \
                                 absolute=True)

        result = a & b
        self.mem._reg_wr("A", result & 0xFF)
        
    def _or(self):
        inst_or = self.mem[self.pc - 1]
        operand = self._read_next()        
        addr_mode = inst_or & 7
        
        a = self.mem._reg_rd("A")
        
        # Constant
        if addr_mode == 3:
            b = operand
        # Memory
        if addr_mode == 4:
            b = self.mem._mem_rd(operand, absolute=True)
        # Indirect
        if addr_mode == 5:
            b = self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), absolute=True)
        # Indexed
        if addr_mode == 6:
            b = self.mem._mem_rd(self.mem._reg_rd("X") + operand, absolute=True)
        # Indirect Indexed
        if addr_mode == 7:
            b = self.mem._mem_rd(self.mem._reg_rd("X") + \
                                 self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), \
                                                  absolute=True), \
                                 absolute=True)

        result = a | b
        self.mem._reg_wr("A", result & 0xFF)
        
    def _lneg(self):
        inst_lneg = self.mem[self.pc - 1]
        operand = self._read_next()        
        addr_mode = inst_lneg & 7
        
        
        # Constant
        if addr_mode == 3:
            b = operand
        # Memory
        if addr_mode == 4:
            b = self.mem._mem_rd(operand, absolute=True)
        # Indirect
        if addr_mode == 5:
            b = self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), absolute=True)
        # Indexed
        if addr_mode == 6:
            b = self.mem._mem_rd(self.mem._reg_rd("X") + operand, absolute=True)
        # Indirect Indexed
        if addr_mode == 7:
            b = self.mem._mem_rd(self.mem._reg_rd("X") + \
                                 self.mem._mem_rd(self.mem._mem_rd(operand, absolute=True), \
                                                  absolute=True), \
                                 absolute=True)

        result = 0xFF ^ b
        self.mem._reg_wr("A", result & 0xFF)
        
        # TODO: HIGH, Need to determine the status of overflow too.
        
        
    def _jpd(self):
        pass
        
    def _jpi(self):
        pass
        
    def _jmi(self):
        pass
    
    def _jmd(self):
        pass
        
    def _jpdnz(self):
        pass

    def _jpdz(self):
        pass

    def _jpdltz(self):
        pass

    def _jpdgez(self):
        pass

    def _jpdgz(self):
        pass

    def _jpinz(self):
        pass

    def _jpiz(self):
        pass

    def _jpiltz(self):
        pass

    def _jpigez(self):
        pass

    def _jpigz(self):
        pass

    def _jmdnz(self):
        pass

    def _jmdz(self):
        pass

    def _jmdltz(self):
        pass

    def _jmdgez(self):
        pass

    def _jmdgz(self):
        pass

    def _jminz(self):
        pass

    def _jmiz(self):
        pass

    def _jmiltz(self):
        pass

    def _jmigez(self):
        pass

    def _jmigz(self):
        pass
        
    def _skp(self):
        pass

    def _set(self):
        inst_set = self.mem[self.pc - 1]
        set_to = (inst_set & 0b01000000) >> 6
        set_nth = (inst_set & 0b00111000) >> 3
        op_mem_offset = self._read_next()
        
        bit_mask = 1 << set_nth
        
        if set_to:
            result = self.mem._mem_rd(op_mem_offset) | bit_mask
        else:
            result = self.mem._mem_rd(op_mem_offset) & (0xFF ^ bit_mask)
        
        self.mem._mem_wr(op_mem_offset, result)
        
    def _sft(self):
        inst_sft = self.mem[self.pc - 1]
        shift_direction = (inst_sft & 0b10000000) >> 7
        reg = {0:"A",
               1:"B"}[(inst_sft & 0b0010000) >> 6]
        shift_operand = (inst_sft & 0b00011000) >> 3
        
        if shift_operand == 0:
            shift_operand = 4
        
        if shift_direction:
            # Shift left
            result = self.mem._reg_rd(reg) << shift_operand
        else:
            # Shift right (replicates the bit value)
            result = self.mem._reg_rd(reg)
            for reps in range(0, shift_operand):
                last_value = result & 0b10000000
                result = (result >> 1) | last_value

        self.mem._reg_wr(reg, result & 0xFF)
        

    def _rot(self):
        inst_rot = self.mem[self.pc - 1]
        rotate_direction = (inst_rot & 0b10000000) >> 7
        reg = {0:"A",
               1:"B"}[(inst_rot & 0b0010000) >> 6]
        rotate_operand = (inst_rot & 0b00011000) >> 3
        
        if rotate_operand == 0:
            rotate_operand = 4
        
        result = self.mem._reg_rd(reg)
        
        if rotate_direction:
            # Rotate left
            for reps in range(0, rotate_operand):
                last_value = (result & 0b10000000) >> 7
                result = (result << 1) | last_value
        else:
            # Rotate right (replicates the bit value)
            for reps in range(0, rotate_operand):
                last_value = (result & 0b00000001) << 7
                result = (result >> 1) | last_value

        self.mem._reg_wr(reg, result & 0xFF)


    def _rotl(self):
        pass

    def _rotr(self):
        pass

    @staticmethod
    def get_asm_statement_def(existing_defs):
        """
        Returns the assembly parser that the Kenback understands.
        
        Notes:
            
            * See inline comments for specification of the grammar
        """
        
        #register_A = pyparsing.Literal("A").setParseAction(lambda s,loc,tok:0)
        #register_B = pyparsing.Literal("B").setParseAction(lambda s,loc,tok:1)
        #register_X = pyparsing.Literal("X").setParseAction(lambda s,loc,tok:2)
        #register_P = pyparsing.Literal("P").setParseAction(lambda s,loc,tok:3)
        #
        #registers = register_A ^ register_B ^ register_X ^ register_P
        
        lit_num = pyparsing.Regex("[+-]?[0-9]+")
        idf = pyparsing.Regex("[a-zA-Z_][a-zA-Z_0-9]+")
        
        lit_value = lit_num ^ idf
        mem_value = pyparsing.Suppress("[") + lit_value + pyparsing.Suppress("]")
        idc_value = pyparsing.Suppress("@[") + lit_value + pyparsing.Suppress("]")
        idx_value = pyparsing.Suppress("X[") + lit_value + pyparsing.Suppress("]")
        idcx_value = pyparsing.Suppress("@X[") + lit_value + pyparsing.Suppress("]")
        
        ins_halt = pyparsing.Group(pyparsing.Regex("HALT"))("0:1")
        ins_noop = pyparsing.Group(pyparsing.Regex("NOOP"))("127:1")
        # ADD
        ins_add_a_im = pyparsing.Group(pyparsing.Regex("ADD A") +lit_value)("3:1")
        ins_add_a_me = pyparsing.Group(pyparsing.Regex("ADD A") + mem_value)("4:1")
        ins_add_a_id = pyparsing.Group(pyparsing.Regex("ADD A") + idc_value)("5:1")
        ins_add_a_ix = pyparsing.Group(pyparsing.Regex("ADD A") + idx_value)("6:1")
        ins_add_a_idx = pyparsing.Group(pyparsing.Regex("ADD A") + idcx_value)("7:1")

        ins_add_b_im = pyparsing.Group(pyparsing.Regex("ADD B") + lit_value)("67:1")
        ins_add_b_me = pyparsing.Group(pyparsing.Regex("ADD B") + mem_value)("68:1")
        ins_add_b_id = pyparsing.Group(pyparsing.Regex("ADD B") + idc_value)("69:1")
        ins_add_b_ix = pyparsing.Group(pyparsing.Regex("ADD B") + idx_value)("70:1")
        ins_add_b_idx = pyparsing.Group(pyparsing.Regex("ADD B") + idcx_value)("71:1")

        ins_add_x_im = pyparsing.Group(pyparsing.Regex("ADD X") + lit_value)("131:1")
        ins_add_x_me = pyparsing.Group(pyparsing.Regex("ADD X") + mem_value)("132:1")
        ins_add_x_id = pyparsing.Group(pyparsing.Regex("ADD X") + idc_value)("133:1")
        ins_add_x_ix = pyparsing.Group(pyparsing.Regex("ADD X") + idx_value)("134:1")
        ins_add_x_idx = pyparsing.Group(pyparsing.Regex("ADD X") + idcx_value)("135:1")
        # SUB
        ins_sub_a_im = pyparsing.Group(pyparsing.Regex("SUB A") + lit_value)("11:1")
        ins_sub_a_me = pyparsing.Group(pyparsing.Regex("SUB A") + mem_value)("12:1")
        ins_sub_a_id = pyparsing.Group(pyparsing.Regex("SUB A") + idc_value)("13:1")
        ins_sub_a_ix = pyparsing.Group(pyparsing.Regex("SUB A") + idx_value)("14:1")
        ins_sub_a_idx = pyparsing.Group(pyparsing.Regex("SUB A") + idcx_value)("15:1")

        ins_sub_b_im = pyparsing.Group(pyparsing.Regex("SUB B") + lit_value)("75:1")
        ins_sub_b_me = pyparsing.Group(pyparsing.Regex("SUB B") + mem_value)("76:1")
        ins_sub_b_id = pyparsing.Group(pyparsing.Regex("SUB B") + idc_value)("77:1")
        ins_sub_b_ix = pyparsing.Group(pyparsing.Regex("SUB B") + idx_value)("78:1")
        ins_sub_b_idx = pyparsing.Group(pyparsing.Regex("SUB B") + idcx_value)("79:1")

        ins_sub_x_im = pyparsing.Group(pyparsing.Regex("SUB X") + lit_value)("139:1")
        ins_sub_x_me = pyparsing.Group(pyparsing.Regex("SUB X") + mem_value)("140:1")
        ins_sub_x_id = pyparsing.Group(pyparsing.Regex("SUB X") + idc_value)("141:1")
        ins_sub_x_ix = pyparsing.Group(pyparsing.Regex("SUB X") + idx_value)("142:1")
        ins_sub_x_idx = pyparsing.Group(pyparsing.Regex("SUB X") + idcx_value)("143:1")
        # LOAD
        ins_load_a_im = pyparsing.Group(pyparsing.Regex("LOAD A") + lit_value)("19:1")
        ins_load_a_me = pyparsing.Group(pyparsing.Regex("LOAD A") + mem_value)("20:1")
        ins_load_a_id = pyparsing.Group(pyparsing.Regex("LOAD A") + idc_value)("21:1")
        ins_load_a_ix = pyparsing.Group(pyparsing.Regex("LOAD A") + idx_value)("22:1")
        ins_load_a_idx = pyparsing.Group(pyparsing.Regex("LOAD A") + idcx_value)("23:1")

        ins_load_b_im = pyparsing.Group(pyparsing.Regex("LOAD B") + lit_value)("83:1")
        ins_load_b_me = pyparsing.Group(pyparsing.Regex("LOAD B") + mem_value)("84:1")
        ins_load_b_id = pyparsing.Group(pyparsing.Regex("LOAD B") + idc_value)("85:1")
        ins_load_b_ix = pyparsing.Group(pyparsing.Regex("LOAD B") + idx_value)("86:1")
        ins_load_b_idx = pyparsing.Group(pyparsing.Regex("LOAD B") + idcx_value)("87:1")

        ins_load_x_im = pyparsing.Group(pyparsing.Regex("LOAD X") + lit_value)("147:1")
        ins_load_x_me = pyparsing.Group(pyparsing.Regex("LOAD X") + mem_value)("148:1")
        ins_load_x_id = pyparsing.Group(pyparsing.Regex("LOAD X") + idc_value)("149:1")
        ins_load_x_ix = pyparsing.Group(pyparsing.Regex("LOAD X") + idx_value)("150:1")
        ins_load_x_idx = pyparsing.Group(pyparsing.Regex("LOAD X") + idcx_value)("151:1")
        # STORE
        ins_store_a_im = pyparsing.Group(pyparsing.Regex("STORE A") + lit_value)("27:1")
        ins_store_a_me = pyparsing.Group(pyparsing.Regex("STORE A") + mem_value)("28:1")
        ins_store_a_id = pyparsing.Group(pyparsing.Regex("STORE A") + idc_value)("29:1")
        ins_store_a_ix = pyparsing.Group(pyparsing.Regex("STORE A") + idx_value)("30:1")
        ins_store_a_idx = pyparsing.Group(pyparsing.Regex("STORE A") + idcx_value)("31:1")

        ins_store_b_im = pyparsing.Group(pyparsing.Regex("STORE B") + lit_value)("91:1")
        ins_store_b_me = pyparsing.Group(pyparsing.Regex("STORE B") + mem_value)("92:1")
        ins_store_b_id = pyparsing.Group(pyparsing.Regex("STORE B") + idc_value)("93:1")
        ins_store_b_ix = pyparsing.Group(pyparsing.Regex("STORE B") + idx_value)("94:1")
        ins_store_b_idx = pyparsing.Group(pyparsing.Regex("STORE B") + idcx_value)("95:1")

        ins_store_x_im = pyparsing.Group(pyparsing.Regex("STORE X") + lit_value)("155:1")
        ins_store_x_me = pyparsing.Group(pyparsing.Regex("STORE X") + mem_value)("156:1")
        ins_store_x_id = pyparsing.Group(pyparsing.Regex("STORE X") + idc_value)("157:1")
        ins_store_x_ix = pyparsing.Group(pyparsing.Regex("STORE X") + idx_value)("158:1")
        ins_store_x_idx = pyparsing.Group(pyparsing.Regex("STORE X") + idcx_value)("159:1")
        # AND
        ins_and_x_im = pyparsing.Group(pyparsing.Regex("AND X") + lit_value)("211:1")
        ins_and_x_me = pyparsing.Group(pyparsing.Regex("AND X") + mem_value)("212:1")
        ins_and_x_id = pyparsing.Group(pyparsing.Regex("AND X") + idc_value)("213:1")
        ins_and_x_ix = pyparsing.Group(pyparsing.Regex("AND X") + idx_value)("214:1")
        ins_and_x_idx = pyparsing.Group(pyparsing.Regex("AND X") + idcx_value)("215:1")
        # OR
        ins_or_x_im = pyparsing.Group(pyparsing.Regex("OR X") + lit_value)("195:1")
        ins_or_x_me = pyparsing.Group(pyparsing.Regex("OR X") + mem_value)("196:1")
        ins_or_x_id = pyparsing.Group(pyparsing.Regex("OR X") + idc_value)("197:1")
        ins_or_x_ix = pyparsing.Group(pyparsing.Regex("OR X") + idx_value)("198:1")
        ins_or_x_idx = pyparsing.Group(pyparsing.Regex("OR X") + idcx_value)("199:1")
        # LNEG
        ins_lneg_x_im = pyparsing.Group(pyparsing.Regex("LNEG X") + lit_value)("219:1")
        ins_lneg_x_me = pyparsing.Group(pyparsing.Regex("LNEG X") + mem_value)("220:1")
        ins_lneg_x_id = pyparsing.Group(pyparsing.Regex("LNEG X") + idc_value)("221:1")
        ins_lneg_x_ix = pyparsing.Group(pyparsing.Regex("LNEG X") + idx_value)("222:1")
        ins_lneg_x_idx = pyparsing.Group(pyparsing.Regex("LNEG X") + idcx_value)("223:1")
        # JUMPS
        # Unconditional
        # The three LSb have to have specific values even in unconditional jumps
        # http://kenbak-1.net/index_files/PRM.pdf
        ins_jpd = pyparsing.Group(pyparsing.Regex("JPD") + lit_value)("228:1") 
        ins_jpi = pyparsing.Group(pyparsing.Regex("JPI") + idc_value)("236:1")
        ins_jmd = pyparsing.Group(pyparsing.Regex("JMD") + lit_value)("244:1")
        ins_jmi = pyparsing.Group(pyparsing.Regex("JMI") + idc_value)("252:1")
        # Conditional on A direct
        ins_jpd_a_nz = pyparsing.Group(pyparsing.Regex("JPDNZ A") + lit_value)(f"{0O073}:1")
        ins_jpd_a_z = pyparsing.Group(pyparsing.Regex("JPDZ A") + lit_value)(f"{0O074}:1")
        ins_jpd_a_ltz = pyparsing.Group(pyparsing.Regex("JPDLTZ A") + lit_value)(f"{0O075}:1")
        ins_jpd_a_gez = pyparsing.Group(pyparsing.Regex("JPDGEZ A") + lit_value)(f"{0O076}:1")
        ins_jpd_a_gz = pyparsing.Group(pyparsing.Regex("JPDGZ A") + lit_value)(f"{0O077}:1")
        # Conditional on A indirect
        ins_jpi_a_nz = pyparsing.Group(pyparsing.Regex("JPINZ A") + idc_value)(f"{0O053}:1")
        ins_jpi_a_z = pyparsing.Group(pyparsing.Regex("JPIZ A") + idc_value)(f"{0O054}:1")
        ins_jpi_a_ltz = pyparsing.Group(pyparsing.Regex("JPILTZ A") + idc_value)(f"{0O055}:1")
        ins_jpi_a_gez = pyparsing.Group(pyparsing.Regex("JPIGEZ A") + idc_value)(f"{0O056}:1")
        ins_jpi_a_gz = pyparsing.Group(pyparsing.Regex("JPIGZ A") + idc_value)(f"{0O057}:1")
        # Conditional on A mark direct
        ins_jmd_a_nz = pyparsing.Group(pyparsing.Regex("JMDNZ A") + lit_value)(f"{0O063}:1")
        ins_jmd_a_z = pyparsing.Group(pyparsing.Regex("JMDZ A") + lit_value)(f"{0O064}:1")
        ins_jmd_a_ltz = pyparsing.Group(pyparsing.Regex("JMDLTZ A") + lit_value)(f"{0O065}:1")
        ins_jmd_a_gez = pyparsing.Group(pyparsing.Regex("JMDGEZ A") + lit_value)(f"{0O066}:1")
        ins_jmd_a_gz = pyparsing.Group(pyparsing.Regex("JMDGZ A") + lit_value)(f"{0O067}:1")
        # Conditional on A mark indirect
        ins_jmi_a_nz = pyparsing.Group(pyparsing.Regex("JMINZ A") + idc_value)(f"{0b00111011}:1")
        ins_jmi_a_z = pyparsing.Group(pyparsing.Regex("JMIZ A") + idc_value)(f"{0b00111100}:1")
        ins_jmi_a_ltz = pyparsing.Group(pyparsing.Regex("JMILTZ A") + idc_value)(f"{0b00111101}:1")
        ins_jmi_a_gez = pyparsing.Group(pyparsing.Regex("JMIGEZ A") + idc_value)(f"{0b00111110}:1")
        ins_jmi_a_gz = pyparsing.Group(pyparsing.Regex("JMIGZ A") + idc_value)(f"{0b00111111}:1")
        
        # Conditional on B direct
        ins_jpd_b_nz = pyparsing.Group(pyparsing.Regex("JPDNZ B") + lit_value)(f"{0b01100011}:1")
        ins_jpd_b_z = pyparsing.Group(pyparsing.Regex("JPDZ B") + lit_value)(f"{0b01100100}:1")
        ins_jpd_b_ltz = pyparsing.Group(pyparsing.Regex("JPDLTZ B") + lit_value)(f"{0b01100101}:1")
        ins_jpd_b_gez = pyparsing.Group(pyparsing.Regex("JPDGEZ B") + lit_value)(f"{0b01100110}:1")
        ins_jpd_b_gz = pyparsing.Group(pyparsing.Regex("JPDGZ B") + lit_value)(f"{0b01100111}:1")
        # Conditional on B indirect
        ins_jpi_b_nz = pyparsing.Group(pyparsing.Regex("JPINZ B") + idc_value)(f"{0b01101011}:1")
        ins_jpi_b_z = pyparsing.Group(pyparsing.Regex("JPIZ B") + idc_value)(f"{0b01101100}:1")
        ins_jpi_b_ltz = pyparsing.Group(pyparsing.Regex("JPILTZ B") + idc_value)(f"{0b01101101}:1")
        ins_jpi_b_gez = pyparsing.Group(pyparsing.Regex("JPIGEZ B") + idc_value)(f"{0b01101110}:1")
        ins_jpi_b_gz = pyparsing.Group(pyparsing.Regex("JPIGZ B") + idc_value)(f"{0b01101111}:1")
        # Conditional on B mark direct
        ins_jmd_b_nz = pyparsing.Group(pyparsing.Regex("JMDNZ B") + lit_value)(f"{0b01110011}:1")
        ins_jmd_b_z = pyparsing.Group(pyparsing.Regex("JMDZ B") + lit_value)(f"{0b01110100}:1")
        ins_jmd_b_ltz = pyparsing.Group(pyparsing.Regex("JMDLTZ B") + lit_value)(f"{0b01110101}:1")
        ins_jmd_b_gez = pyparsing.Group(pyparsing.Regex("JMDGEZ B") + lit_value)(f"{0b01110110}:1")
        ins_jmd_b_gz = pyparsing.Group(pyparsing.Regex("JMDGZ B") + lit_value)(f"{0b01110111}:1")
        # Conditional on B mark indirect
        ins_jmi_b_nz = pyparsing.Group(pyparsing.Regex("JMINZ B") + idc_value)(f"{0b01111011}:1")
        ins_jmi_b_z = pyparsing.Group(pyparsing.Regex("JMIZ B") + idc_value)(f"{0b01111100}:1")
        ins_jmi_b_ltz = pyparsing.Group(pyparsing.Regex("JMILTZ B") + idc_value)(f"{0b01111101}:1")
        ins_jmi_b_gez = pyparsing.Group(pyparsing.Regex("JMIGEZ B") + idc_value)(f"{0b01111110}:1")
        ins_jmi_b_gz = pyparsing.Group(pyparsing.Regex("JMIGZ B") + idc_value)(f"{0b01111111}:1")

        # Conditional on X direct
        ins_jpd_x_nz = pyparsing.Group(pyparsing.Regex("JPDNZ X") + lit_value)(f"{0b10100011}:1")
        ins_jpd_x_z = pyparsing.Group(pyparsing.Regex("JPDZ X") + lit_value)(f"{0b10100100}:1")
        ins_jpd_x_ltz = pyparsing.Group(pyparsing.Regex("JPDLTZ X") + lit_value)(f"{0b10100101}:1")
        ins_jpd_x_gez = pyparsing.Group(pyparsing.Regex("JPDGEZ X") + lit_value)(f"{0b10100110}:1")
        ins_jpd_x_gz = pyparsing.Group(pyparsing.Regex("JPDGZ X") + lit_value)(f"{0b10100111}:1")
        # Conditional on X indirect
        ins_jpi_x_nz = pyparsing.Group(pyparsing.Regex("JPINZ X") + idc_value)(f"{0b10101011}:1")
        ins_jpi_x_z = pyparsing.Group(pyparsing.Regex("JPIZ X") + idc_value)(f"{0b10101100}:1")
        ins_jpi_x_ltz = pyparsing.Group(pyparsing.Regex("JPILTZ X") + idc_value)(f"{0b10101101}:1")
        ins_jpi_x_gez = pyparsing.Group(pyparsing.Regex("JPIGEZ X") + idc_value)(f"{0b10101110}:1")
        ins_jpi_x_gz = pyparsing.Group(pyparsing.Regex("JPIGZ X") + idc_value)(f"{0b10101111}:1")
        # Conditional on X mark direct
        ins_jmd_x_nz = pyparsing.Group(pyparsing.Regex("JMDNZ X") + lit_value)(f"{0b10110011}:1")
        ins_jmd_x_z = pyparsing.Group(pyparsing.Regex("JMDZ X") + lit_value)(f"{0b10110100}:1")
        ins_jmd_x_ltz = pyparsing.Group(pyparsing.Regex("JMDLTZ X") + lit_value)(f"{0b10110101}:1")
        ins_jmd_x_gez = pyparsing.Group(pyparsing.Regex("JMDGEZ X") + lit_value)(f"{0b10110110}:1")
        ins_jmd_x_gz = pyparsing.Group(pyparsing.Regex("JMDGZ X") + lit_value)(f"{0b10110111}:1")
        # Conditional on X mark indirect
        ins_jmi_x_nz = pyparsing.Group(pyparsing.Regex("JMINZ X") + idc_value)(f"{0b10111011}:1")
        ins_jmi_x_z = pyparsing.Group(pyparsing.Regex("JMIZ X") + idc_value)(f"{0b10111100}:1")
        ins_jmi_x_ltz = pyparsing.Group(pyparsing.Regex("JMILTZ X") + idc_value)(f"{0b10111101}:1")
        ins_jmi_x_gez = pyparsing.Group(pyparsing.Regex("JMIGEZ X") + idc_value)(f"{0b10111110}:1")
        ins_jmi_x_gz = pyparsing.Group(pyparsing.Regex("JMIGZ X") + idc_value)(f"{0b10111111}:1")
        
        # SKIPS
        # SKIP 0
        ins_skip_0_0 = pyparsing.Group(pyparsing.Regex("SKP 0 0") + mem_value)(f"{0b10000010}:1")
        ins_skip_0_1 = pyparsing.Group(pyparsing.Regex("SKP 0 1") + mem_value)(f"{0b10001010}:1")
        ins_skip_0_2 = pyparsing.Group(pyparsing.Regex("SKP 0 2") + mem_value)(f"{0b10010010}:1")
        ins_skip_0_3 = pyparsing.Group(pyparsing.Regex("SKP 0 3") + mem_value)(f"{0b10011010}:1")
        ins_skip_0_4 = pyparsing.Group(pyparsing.Regex("SKP 0 4") + mem_value)(f"{0b10100010}:1")
        ins_skip_0_5 = pyparsing.Group(pyparsing.Regex("SKP 0 5") + mem_value)(f"{0b10101010}:1")
        ins_skip_0_6 = pyparsing.Group(pyparsing.Regex("SKP 0 6") + mem_value)(f"{0b10110010}:1")
        ins_skip_0_7 = pyparsing.Group(pyparsing.Regex("SKP 0 7") + mem_value)(f"{0b10111010}:1")
        # SKIP 1
        ins_skip_1_0 = pyparsing.Group(pyparsing.Regex("SKP 1 0") + mem_value)(f"{0b11000010}:1")
        ins_skip_1_1 = pyparsing.Group(pyparsing.Regex("SKP 1 1") + mem_value)(f"{0b11001010}:1")
        ins_skip_1_2 = pyparsing.Group(pyparsing.Regex("SKP 1 2") + mem_value)(f"{0b11010010}:1")
        ins_skip_1_3 = pyparsing.Group(pyparsing.Regex("SKP 1 3") + mem_value)(f"{0b11011010}:1")
        ins_skip_1_4 = pyparsing.Group(pyparsing.Regex("SKP 1 4") + mem_value)(f"{0b11100010}:1")
        ins_skip_1_5 = pyparsing.Group(pyparsing.Regex("SKP 1 5") + mem_value)(f"{0b11101010}:1")
        ins_skip_1_6 = pyparsing.Group(pyparsing.Regex("SKP 1 6") + mem_value)(f"{0b11110010}:1")
        ins_skip_1_7 = pyparsing.Group(pyparsing.Regex("SKP 1 7") + mem_value)(f"{0b11111010}:1")

        # SET
        # SET 0
        ins_set_0_0 = pyparsing.Group(pyparsing.Regex("SET 0 0") + mem_value)(f"{0b00000010}:1")
        ins_set_0_1 = pyparsing.Group(pyparsing.Regex("SET 0 1") + mem_value)(f"{0b00001010}:1")
        ins_set_0_2 = pyparsing.Group(pyparsing.Regex("SET 0 2") + mem_value)(f"{0b00010010}:1")
        ins_set_0_3 = pyparsing.Group(pyparsing.Regex("SET 0 3") + mem_value)(f"{0b00011010}:1")
        ins_set_0_4 = pyparsing.Group(pyparsing.Regex("SET 0 4") + mem_value)(f"{0b00100010}:1")
        ins_set_0_5 = pyparsing.Group(pyparsing.Regex("SET 0 5") + mem_value)(f"{0b00101010}:1")
        ins_set_0_6 = pyparsing.Group(pyparsing.Regex("SET 0 6") + mem_value)(f"{0b00110010}:1")
        ins_set_0_7 = pyparsing.Group(pyparsing.Regex("SET 0 7") + mem_value)(f"{0b00111010}:1")
        # SET 1
        ins_set_1_0 = pyparsing.Group(pyparsing.Regex("SET 1 0") + mem_value)(f"{0b01000010}:1")
        ins_set_1_1 = pyparsing.Group(pyparsing.Regex("SET 1 1") + mem_value)(f"{0b01001010}:1")
        ins_set_1_2 = pyparsing.Group(pyparsing.Regex("SET 1 2") + mem_value)(f"{0b01010010}:1")
        ins_set_1_3 = pyparsing.Group(pyparsing.Regex("SET 1 3") + mem_value)(f"{0b01011010}:1")
        ins_set_1_4 = pyparsing.Group(pyparsing.Regex("SET 1 4") + mem_value)(f"{0b01100010}:1")
        ins_set_1_5 = pyparsing.Group(pyparsing.Regex("SET 1 5") + mem_value)(f"{0b01101010}:1")
        ins_set_1_6 = pyparsing.Group(pyparsing.Regex("SET 1 6") + mem_value)(f"{0b01110010}:1")
        ins_set_1_7 = pyparsing.Group(pyparsing.Regex("SET 1 7") + mem_value)(f"{0b01111010}:1")

        # SHIFT
        # LEFT A
        ins_sftl_a_1 = pyparsing.Group(pyparsing.Regex("SFTL A 1"))(f"{0b10001001}:1")
        ins_sftl_a_2 = pyparsing.Group(pyparsing.Regex("SFTL A 2"))(f"{0b10010001}:1")
        ins_sftl_a_3 = pyparsing.Group(pyparsing.Regex("SFTL A 3"))(f"{0b10011001}:1")
        ins_sftl_a_4 = pyparsing.Group(pyparsing.Regex("SFTL A 4"))(f"{0b10000001}:1")
        # RIGHT A
        ins_sftr_a_1 = pyparsing.Group(pyparsing.Regex("SFTR A 1"))(f"{0b00001001}:1")
        ins_sftr_a_2 = pyparsing.Group(pyparsing.Regex("SFTR A 2"))(f"{0b00010001}:1")
        ins_sftr_a_3 = pyparsing.Group(pyparsing.Regex("SFTR A 3"))(f"{0b00011001}:1")
        ins_sftr_a_4 = pyparsing.Group(pyparsing.Regex("SFTR A 4"))(f"{0b00000001}:1")
        # LEFT B
        ins_sftl_b_1 = pyparsing.Group(pyparsing.Regex("SFTL B 1"))(f"{0b10101001}:1")
        ins_sftl_b_2 = pyparsing.Group(pyparsing.Regex("SFTL B 2"))(f"{0b10110001}:1")
        ins_sftl_b_3 = pyparsing.Group(pyparsing.Regex("SFTL B 3"))(f"{0b10111001}:1")
        ins_sftl_b_4 = pyparsing.Group(pyparsing.Regex("SFTL B 4"))(f"{0b10100001}:1")
        # RIGHT B
        ins_sftr_b_1 = pyparsing.Group(pyparsing.Regex("SFTR B 1"))(f"{0b00101001}:1")
        ins_sftr_b_2 = pyparsing.Group(pyparsing.Regex("SFTR B 2"))(f"{0b00110001}:1")
        ins_sftr_b_3 = pyparsing.Group(pyparsing.Regex("SFTR B 3"))(f"{0b00111001}:1")
        ins_sftr_b_4 = pyparsing.Group(pyparsing.Regex("SFTR B 4"))(f"{0b00100001}:1")

        # ROTATE
        # LEFT A
        ins_rotl_a_1 = pyparsing.Group(pyparsing.Regex("ROTL A 1"))(f"{0b11001001}:1")
        ins_rotl_a_2 = pyparsing.Group(pyparsing.Regex("ROTL A 2"))(f"{0b11010001}:1")
        ins_rotl_a_3 = pyparsing.Group(pyparsing.Regex("ROTL A 3"))(f"{0b11011001}:1")
        ins_rotl_a_4 = pyparsing.Group(pyparsing.Regex("ROTL A 4"))(f"{0b11000001}:1")
        # RIGHT A
        ins_rotr_a_1 = pyparsing.Group(pyparsing.Regex("ROTR A 1"))(f"{0b01001001}:1")
        ins_rotr_a_2 = pyparsing.Group(pyparsing.Regex("ROTR A 2"))(f"{0b01011001}:1")
        ins_rotr_a_3 = pyparsing.Group(pyparsing.Regex("ROTR A 3"))(f"{0b01010001}:1")
        ins_rotr_a_4 = pyparsing.Group(pyparsing.Regex("ROTR A 4"))(f"{0b01000001}:1")
        # LEFT B
        ins_rotl_b_1 = pyparsing.Group(pyparsing.Regex("ROTL B 1"))(f"{0b11101001}:1")
        ins_rotl_b_2 = pyparsing.Group(pyparsing.Regex("ROTL B 2"))(f"{0b11110001}:1")
        ins_rotl_b_3 = pyparsing.Group(pyparsing.Regex("ROTL B 3"))(f"{0b11111001}:1")
        ins_rotl_b_4 = pyparsing.Group(pyparsing.Regex("ROTL B 4"))(f"{0b11100001}:1")
        # RIGHT B
        ins_rotr_b_1 = pyparsing.Group(pyparsing.Regex("ROTR B 1"))(f"{0b01101001}:1")
        ins_rotr_b_2 = pyparsing.Group(pyparsing.Regex("ROTR B 2"))(f"{0b01110001}:1")
        ins_rotr_b_3 = pyparsing.Group(pyparsing.Regex("ROTR B 3"))(f"{0b01111001}:1")
        ins_rotr_b_4 = pyparsing.Group(pyparsing.Regex("ROTR B 4"))(f"{0b01100001}:1")
        
        program = pyparsing.OneOrMore(ins_halt ^ ins_noop ^ ins_add_a_im ^ ins_add_a_me ^ ins_add_a_id ^ ins_add_a_ix ^ \
                                      ins_add_a_idx ^ ins_add_b_im ^ ins_add_b_me ^ ins_add_b_id ^ ins_add_b_ix ^ \
                                      ins_add_b_idx ^ ins_add_x_im ^ ins_add_x_me ^ ins_add_x_id ^ ins_add_x_ix ^ \
                                      ins_add_x_idx ^ ins_sub_a_im ^ ins_sub_a_me ^ ins_sub_a_id ^ ins_sub_a_ix ^ \
                                      ins_sub_a_idx ^ ins_sub_b_im ^ ins_sub_b_me ^ ins_sub_b_id ^ ins_sub_b_ix ^ \
                                      ins_sub_b_idx ^ ins_sub_x_im ^ ins_sub_x_me ^ ins_sub_x_id ^ ins_sub_x_ix ^ \
                                      ins_sub_x_idx ^ ins_load_a_im ^ ins_load_a_me ^ ins_load_a_id ^ ins_load_a_ix ^ \
                                      ins_load_a_idx ^ ins_load_b_im ^ ins_load_b_me ^ ins_load_b_id ^ ins_load_b_ix ^ \
                                      ins_load_b_idx ^ ins_load_x_im ^ ins_load_x_me ^ ins_load_x_id ^ ins_load_x_ix ^ \
                                      ins_load_x_idx ^ ins_store_a_im ^ ins_store_a_me ^ ins_store_a_id ^ ins_store_a_ix ^ \
                                      ins_store_a_idx ^ ins_store_b_im ^ ins_store_b_me ^ ins_store_b_id ^ \
                                      ins_store_b_ix ^ ins_store_b_idx ^ ins_store_x_im ^ ins_store_x_me ^ \
                                      ins_store_x_id ^ ins_store_x_ix ^ ins_store_x_idx ^ ins_and_x_im ^ ins_and_x_me ^ \
                                      ins_and_x_id ^ ins_and_x_ix ^ ins_and_x_idx ^ ins_or_x_im ^ ins_or_x_me ^ \
                                      ins_or_x_id ^ ins_or_x_ix ^ ins_or_x_idx ^ ins_lneg_x_im ^ ins_lneg_x_me ^ \
                                      ins_lneg_x_id ^ ins_lneg_x_ix ^ ins_lneg_x_idx ^ ins_jpd ^ ins_jpi ^ ins_jmd ^ \
                                      ins_jmi ^ ins_jpd_a_nz ^ ins_jpd_a_z ^ ins_jpd_a_ltz ^ ins_jpd_a_gez ^ ins_jpd_a_gz ^\
                                      ins_jpi_a_nz ^ ins_jpi_a_z ^ ins_jpi_a_ltz ^ ins_jpi_a_gez ^ ins_jpi_a_gz ^ \
                                      ins_jmd_a_nz ^ ins_jmd_a_z ^ ins_jmd_a_ltz ^ ins_jmd_a_gez ^ ins_jmd_a_gz ^ \
                                      ins_jmi_a_nz ^ ins_jmi_a_z ^ ins_jmi_a_ltz ^ ins_jmi_a_gez ^ ins_jmi_a_gz ^ \
                                      ins_jpd_b_nz ^ ins_jpd_b_z ^ ins_jpd_b_ltz ^ ins_jpd_b_gez ^ ins_jpd_b_gz ^ \
                                      ins_jpi_b_nz ^ ins_jpi_b_z ^ ins_jpi_b_ltz ^ ins_jpi_b_gez ^ ins_jpi_b_gz ^ \
                                      ins_jmd_b_nz ^ ins_jmd_b_z ^ ins_jmd_b_ltz ^ ins_jmd_b_gez ^ ins_jmd_b_gz ^ ins_jmi_b_nz ^ ins_jmi_b_z ^ ins_jmi_b_ltz ^ ins_jmi_b_gez ^ ins_jmi_b_gz ^ ins_jpd_x_nz ^ ins_jpd_x_z ^ ins_jpd_x_ltz ^ ins_jpd_x_gez ^ ins_jpd_x_gz ^ ins_jpi_x_nz ^ ins_jpi_x_z ^ ins_jpi_x_ltz ^ ins_jpi_x_gez ^ ins_jpi_x_gz ^ ins_jmd_x_nz ^ ins_jmd_x_z ^ ins_jmd_x_ltz ^ ins_jmd_x_gez ^ ins_jmd_x_gz ^ ins_jmi_x_nz ^ ins_jmi_x_z ^ ins_jmi_x_ltz ^ ins_jmi_x_gez ^ ins_jmi_x_gz ^ ins_skip_0_0 ^ ins_skip_0_1 ^ ins_skip_0_2 ^ ins_skip_0_3 ^ ins_skip_0_4 ^ ins_skip_0_5 ^ ins_skip_0_6 ^ ins_skip_0_7 ^ ins_skip_1_0 ^ ins_skip_1_1 ^ ins_skip_1_2 ^ ins_skip_1_3 ^ ins_skip_1_4 ^ ins_skip_1_5 ^ ins_skip_1_6 ^ ins_skip_1_7 ^ ins_set_0_0 ^ ins_set_0_1 ^ ins_set_0_2 ^ ins_set_0_3 ^ ins_set_0_4 ^ ins_set_0_5 ^ ins_set_0_6 ^ ins_set_0_7 ^ ins_set_1_0 ^ ins_set_1_1 ^ ins_set_1_2 ^ ins_set_1_3 ^ ins_set_1_4 ^ ins_set_1_5 ^ ins_set_1_6 ^ ins_set_1_7 ^ ins_sftl_a_1 ^ ins_sftl_a_2 ^ ins_sftl_a_3 ^ ins_sftl_a_4 ^ ins_sftr_a_1 ^ ins_sftr_a_2 ^ ins_sftr_a_3 ^ ins_sftr_a_4 ^ ins_sftl_b_1 ^ ins_sftl_b_2 ^ ins_sftl_b_3 ^ ins_sftl_b_4 ^ ins_sftr_b_1 ^ ins_sftr_b_2 ^ ins_sftr_b_3 ^ ins_sftr_b_4 ^ ins_rotl_a_1 ^ ins_rotl_a_2 ^ ins_rotl_a_3 ^ ins_rotl_a_4 ^ ins_rotr_a_1 ^ ins_rotr_a_2 ^ ins_rotr_a_3 ^ ins_rotr_a_4 ^ ins_rotl_b_1 ^ ins_rotl_b_2 ^ ins_rotl_b_3 ^ ins_rotl_b_4 ^ ins_rotr_b_1 ^ ins_rotr_b_2 ^ ins_rotr_b_3 ^ ins_rotr_b_4)
        return program

# if __name__ == "__main__":
    # pro = "LOAD A 1\nADD A 1\nHALT"
    # r = get_parser().parseString(pro, parseAll=True)
    
