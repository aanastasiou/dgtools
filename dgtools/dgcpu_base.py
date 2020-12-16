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
        self._mem_len = 0
        
    def _mem_rd(self, offset, absolute=False):
        # TODO: HIGH, Needs offset checking and exception
        if absolute:
            return self._mem[offset]
        else:
            if issubclass(type(offset), slice):
                return list(self._mem[slice(self._mem_base + offset.start, self._mem_base + offset.stop, offset.step)])
            return self._mem[self._mem_base + offset]
    
    def _mem_wr(self, offset, value, absolute=False):
        # TODO: HIGH, Needs offset checking and exception
        if absolute:
            self._mem[offset] = value
        else:
            #if subclass(type(offset), slice):
            #    self._mem[slice(self._mem_base + offset.start, self._mem_base + offset.stop, offset.step)] = value
            self._mem[self._mem_base + offset] = value
        return self

    def _reg_rd(self, reg_name):
        # TODO: HIGH, Needs to check if reg_name exists and exception
        return self._mem_rd(self._reg_map[reg_name], absolute=True)
    
    def _reg_wr(self, reg_name, value):
        # TODO: HIGH, Needs to check if reg_name exists and if value is within the right range
        self._mem_wr(self._reg_map[reg_name],value, absolute=True)
        return self
    
    def _reg_rd_bit(self, reg_name, n_bit):
        # TODO: HIGH, needs reg_name checking and n_bit range checkint and exceptions
        test_bit = n_bit
        reg_val = self._reg_rd(reg_name)
        return ((reg_val & test_bit) == test_bit) & 0xFF
        
    def _reg_wr_bit(self, reg_name, n_bit, bit_value):
        # TODO: HIGH, needs reg_name, n_bit, bit_value range checks and exceptions
        test_bit = n_bit
        reg_val = self._reg_rd(reg_name)
        if bit_value:
            self._reg_wr(reg_name, reg_val | test_bit)
        else:
            self._reg_wr(reg_name, reg_val & (255 - test_bit))
        return self
            
    def __getitem__(self, idx):
        if issubclass(type(idx), tuple):
            return self._reg_rd_bit(idx[0], idx[1])
        if issubclass(type(idx), str):
            return self._reg_rd(idx)
        elif issubclass(type(idx), (int, slice)):
            return self._mem_rd(idx)
            
    def __setitem__(self, idx, a_value, n_bit=None):
        if issubclass(type(idx), tuple):
            return self._reg_wr_bit(idx[0], idx[1], a_value)
        if issubclass(type(idx), str):
            if n_bit is not None:
                return self._reg_wr_bit(idx, n_bit, a_value)
            return self._reg_wr(idx, a_value)
        elif issubclass(type(idx), (int, slice)):
            return self._mem_wr(idx, a_value)
        
            
    def load(self,a_program):
        self._mem = bytearray([0 for k in range(0, self._mem_len + self._mem_base)])
        self._mem[self._mem_base:self._mem_base+len(a_program)] = a_program
        
    def save(self):
        return self._mem
        

class DGCPU:
    def __init__(self):
        self._mem_space = None
        self._pc_reg = ""
        self._ins_lookup = {}
        
    @property
    def mem(self):
        return self._mem_space

    @property
    def pc(self):
        return self._mem_space._reg_rd(self._pc_reg)
    
    @pc.setter    
    def pc(self, value):
        self._mem_space._reg_wr(self._pc_reg, value)
        
    def _read_next(self):
        value = self._mem_space._mem_rd(self.pc)
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

