"""
Base classes to define micro-CPUs.

:author: Athanasios Anastasiou
:date: Sept 2020
"""

class DGMemorySpaceBase:
    """
    Defines a generic memory space that can be shared with registers.
    """
    def __init__(self):
        self._mem = bytearray([])
        self._mem_base = 0
        self._reg_map = {}
        self._mem_len = 256
        
    def _mem_rd(self, offset, absolute=False):
        if absolute:
            return self._mem[offset]
        else:
            return self._mem[self._mem_base + offset]
    
    def _mem_wr(self, offset, value, absolute=False):
        if absolute:
            self._mem[offset] = value
        else:
            self._mem[self._mem_base + offset] = value

    def _reg_rd(self, reg_name):
        self._mem_rd(self._reg_map[reg_name], absolute=True)
    
    def _reg_wr(self, reg_name, value):
        self._mem_wr(self._reg_map[reg_name],value, absolute=True)
    
    def _reg_rd_bit(self, reg_name, n_bit):
        test_bit = 1 << n_bit
        reg_val = self._reg_rd(reg_name)
        return ((reg_val & test_bit) == test_bit) & 0xFF
        
    def _reg_wr_bit(self, reg_name, n_bit, bit_value):
        test_bit = 1 << n_bit
        reg_val = self._reg_rd(reg_name)
        if bit_value:
            self._reg_wr(reg_name, reg_val | test_bit)
        else:
            self._reg_wr(reg_name, reg_val & (255 - test_bit))
            
    def load(self,a_program):
        self._mem = bytearray(a_program)
        
    def save(self):
        return self._mem
        

class DGCPU:
    def __init__(self):
        self._mem_space = None
        self._pc_reg = ""
        self._ins_lookup = {}
        
    @property
    def pc(self):
        return self._mem_space._reg_rd(self._pc_reg)
    
    @pc.setter    
    def pc(self, value):
        self._mem_space._reg_wr(self._pc_reg, value)
        
    def _read_next(self):
        value = self._mem_space._mem_rd(self.pc, absolute=True)
        self.pc+=1
        return value
        
    def _exec_next(self):
        # Fetch...
        cmd = self._read_next()
        # Execute
        try:
            self._ins_lookup[cmd]()
        except KeyError as ke:
            #raise DgtoolsErrorOpcodeNotSupported(f"Opcode {cmd} not understood")
            pass
