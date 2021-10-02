"""
Base classes to define micro-CPUs.

:author: Athanasios Anastasiou
:date: Sept 2020
"""

class DGMemorySpaceBase:
    """
    Defines a generic memory space that can include registers and provides an interface to that memory space.
    
    :param _mem: The memory space including space for the registers
    :type _mem: bytearray
    :param _mem_base: The base address of the actual RAM space devoted to the CPU
    :type _mem_base: int
    :param _reg_map: A <str, int> mapping in which it is assumed that register name (str) of size 1 byte starts at ofset int.
    :type reg_map:dict
    :param _mem_len: The total length of RAM.
    :type _mem_len:int
    """
    def __init__(self):
        """
            Initialise the memory space.
        """
        self._mem = bytearray([])
        self._mem_base = 0
        self._reg_map = {}
        self._mem_len = 0
        
    def _mem_rd(self, offset, absolute=False):
        """
        Generic memory read.
        
        Note:
            * Memory reads can include slices.
        
        :param offset: The memory offset within the memory space to read one or more values from.
        :type offset: int or slice
        :param absolute: Whether this is an absolute memory read or relative to mem_base
        :param absolute:bool
        :returns: The byte value at a particular position in memory.
        :rtype: byte or list
        """
        # TODO: HIGH, Needs offset checking and exception
        if absolute:
            return self._mem[offset]
        else:
            if issubclass(type(offset), slice):
                return list(self._mem[slice(self._mem_base + offset.start, self._mem_base + offset.stop, offset.step)])
            return self._mem[self._mem_base + offset]
    
    def _mem_wr(self, offset, value, absolute=False):
        """
        Generic memory write.
        
        Note:
            * Memory writes can include slices.
        
        :param offset: The memory offset within the memory space to write one or more values to.
        :type offset: int or slice
        :param value: The actual value(s) to set the memory to.
        :param absolute: Whether this is an absolute memory read or relative to mem_base
        :param absolute:bool
        :returns: The byte value at a particular position in memory.
        :rtype: byte or list
        """
        # TODO: HIGH, Needs offset checking and exception
        # TODO: HIGH, Needs type checking on value
        if absolute:
            self._mem[offset] = value
        else:
            #if subclass(type(offset), slice):
            #    self._mem[slice(self._mem_base + offset.start, self._mem_base + offset.stop, offset.step)] = value
            self._mem[self._mem_base + offset] = value
        return self

    def _reg_rd(self, reg_name):
        """
        Register read.
        
        Note:
            * Registers are defined by name and assigned an offset within the memory space where they live.
            * This function handles all this translation from register name to actual position in memory
            
        :param reg_name: The register to read from
        :type reg_name: str
        :returns: The value of the register
        :rtype: byte
        """
        # TODO: HIGH, Needs to check if reg_name is str
        # TODO: HIGH, Needs to check if reg_name exists and exception
        return self._mem_rd(self._reg_map[reg_name], absolute=True)
    
    def _reg_wr(self, reg_name, value):
        """
        Register Write.
            
        :param reg_name: The register to write to
        :type reg_name: str
        :param value: The value to set the register to.
        :type value: byte
        :returns: Nothing
        """
        # TODO: HIGH, Needs to check if reg_name exists and if value is within the right range
        self._mem_wr(self._reg_map[reg_name],value, absolute=True)
        return self
    
    def _reg_rd_bit(self, reg_name, n_bit):
        """
        Register read bit.
        
        :param reg_name: The register to read a bit from
        :type reg_name: str
        :param n_bit: The n-th bit to read from. 
        :type n_bit: int
        :returns: The state of the chosen register's n-th bit.
        :rtype:int
        """
        # TODO: HIGH, needs reg_name checking and n_bit range checking and exceptions
        test_bit = n_bit
        reg_val = self._reg_rd(reg_name)
        return ((reg_val & test_bit) == test_bit) & 0xFF
        
    def _reg_wr_bit(self, reg_name, n_bit, bit_value):
        """
        Register write bit.
        
        :param reg_name: The register to read a bit from
        :type reg_name: str
        :param n_bit: The n-th bit to read from. 
        :type n_bit: int
        :param bit_value: The bit state to set to
        :type bit_value: int
        :returns: Nothing.
        """
        # TODO: HIGH, needs reg_name, n_bit, bit_value range checks and exceptions
        test_bit = n_bit
        reg_val = self._reg_rd(reg_name)
        if bit_value:
            self._reg_wr(reg_name, reg_val | test_bit)
        else:
            self._reg_wr(reg_name, reg_val & (255 - test_bit))
        return self
            
    def __getitem__(self, idx):
        """
        Universal memory space read.
        
        Notes:
            * [("A",3)] invokes `_reg_rd_bit`
            * ["A"] invokes `_reg_rd`
            * [120] invokes `_mem_rd`
            * [120:128] invokes `_mem_rd`
            
        :param idx: The index to read a value from
        :type idx: tuple, str, int, slice
        :returns: The value at a specific location in memory
        :rtype: byte
        """
        # TODO, HIGH: Needs an exception on final for not knowing how to handle a request type.
        if issubclass(type(idx), tuple):
            return self._reg_rd_bit(idx[0], idx[1])
        if issubclass(type(idx), str):
            return self._reg_rd(idx)
        elif issubclass(type(idx), (int, slice)):
            return self._mem_rd(idx)
            
    def __setitem__(self, idx, a_value, n_bit=None):
        """
        Universal memory space write.
        
        Notes:
            * [("A",3)]=1 invokes `_reg_wr_bit`
            * ["A"]=5 invokes `_reg_wr`
            * [120]=2 invokes `_mem_wr`
            * [120:128]=4 invokes `_mem_wr`
            
        :param idx: The index to read a value from
        :type idx: tuple, str, int, slice
        :returns: Nothing
        """
        # TODO, HIGH: Needs an exception on final for not knowing how to handle a request type.
        if issubclass(type(idx), tuple):
            return self._reg_wr_bit(idx[0], idx[1], a_value)
        if issubclass(type(idx), str):
            if n_bit is not None:
                return self._reg_wr_bit(idx, n_bit, a_value)
            return self._reg_wr(idx, a_value)
        elif issubclass(type(idx), (int, slice)):
            return self._mem_wr(idx, a_value)
        
            
    def load(self, a_program):
        """
        Loads a program to memory
        """
        self._mem = bytearray([0 for k in range(0, self._mem_len + self._mem_base)])
        self._mem[self._mem_base:(self._mem_base+len(a_program))] = a_program
        
    def save(self):
        """
        Simply returns the current state of the whole memory space.
        """
        return self._mem
        

class DGCPU:
    """
    An abstract dgtools CPU.
    
    :param _mem_space: The memory space of a given CPU.
    :type _mem_space: DGMemorySpaceBase
    :param _pc_reg: The label of the program counter for a given CPU.
    :type _pc_reg: str
    :param _ins_lookup: A mapping <int, function> that maps opcode (int) to the function that executes it (function)
    :type _ins_lookup: dict
    """
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
        while n < max_n:
            cnt = self._exec_next()
            n+=1
            
        raise DgtoolsErrorProgramHalt(f"Program exceeded preset max_n={max_n}.")
            
    def step(self):
        return self._exec_next()

