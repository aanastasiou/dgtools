"""

The main Digirule VM class.

:author: Athanasios Anastasiou
:date: Mar 2020
"""
from dgtools.exceptions import DgtoolsErrorOpcodeNotSupported
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
    def addr_led(self):
        return f"{self._pc:08b}"
        
    @property
    def data_led(self):
        return f"{self._rd_mem(self._dataled_reg_ptr):08b}"
        
    @property
    def button_sw(self):
        return f"{self._mem[self._bt_reg_ptr]:08b}"

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
            raise TypeError(f"interactive_callback() setter expected a function, received {type(new_callback)}")
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
        if addr == self._bt_reg_ptr and self._interactive_mode:
            self._mem[addr] = self._interactive_callback()
        return self._mem[addr]
        
    def _exec_instruction(self, cmd):
        """
        Handles the execution of a specific instruction. Emulates the 2A firmware.
        
        :param cmd: The instruction code to execute 
        :type cmd: int
        :returns: 0 if HALT has been reached, 1 if the instruction was carried out succesfully.
        :rtype: int
        :raises: DgtoolsErrorOpcodeNotSupported 
        """
        if cmd>32:
            # TODO: LOW, Unsupported opcodes could be intercepted and re-interpreted?
            raise DgtoolsErrorOpcodeNotSupported(f"Opcode {cmd} not supported.")
            
        # ...Execute    
        # HALT
        if cmd == 0:
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
            new_value = self._rd_mem(self._read_next())
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, new_value==0)
        
        # COPYRR
        if cmd == 7:
            addr1 = self._read_next()
            value_addr1 = self._rd_mem(addr1) & 0xFF
            addr2 = self._read_next()
            self._wr_mem(addr2, value_addr1)
            self._set_status_reg(self._ZERO_FLAG_BIT,value_addr1==0)
            
        # ADDLA
        if cmd == 8:
            new_value = self._get_acc_value()+self._read_next()
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
            self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

        # ADDRA
        if cmd == 9:
            new_value = self._get_acc_value() + self._rd_mem(self._read_next())
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
            self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

        # SUBLA
        if cmd == 10:
            new_value = self._get_acc_value() - self._read_next()
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
            self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))

        # SUBRA
        if cmd == 11:
            new_value = self._get_acc_value() - self._rd_mem(self._read_next())
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
            self._set_status_reg(self._CARRY_FLAG_BIT, (new_value > 255 or new_value < 0))
            
        # ANDLA
        if cmd == 12:
            new_value = self._get_acc_value() & self._read_next()
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
            
        # ANDRA
        if cmd == 13:
            new_value = self._get_acc_value() & self._rd_mem(self._read_next())
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
            
        # ORLA
        if cmd == 14:
            new_value = self._get_acc_value() | self._read_next()
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
            
        # ORRA
        if cmd == 15:
            new_value = self._get_acc_value() | self._rd_mem(self._read_next())
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        
        # XORLA
        if cmd == 16:
            new_value = self._get_acc_value() ^ self._read_next()
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
            
        # XORRA
        if cmd == 17:
            new_value = self._get_acc_value() ^ self._rd_mem(self._read_next())
            self._set_acc_value(new_value)
            self._set_status_reg(self._ZERO_FLAG_BIT, self._acc==0)
        
        # DECR
        if cmd == 18:
            addr = self._read_next()
            value = (self._rd_mem(addr) - 1) & 0xFF
            self._wr_mem(addr, value)
            self._set_status_reg(self._ZERO_FLAG_BIT,value==0)
                
        # INCR
        if cmd == 19:
            addr = self._read_next()
            value = (self._rd_mem(addr) + 1) & 0xFF
            self._wr_mem(addr, value)
            self._set_status_reg(self._ZERO_FLAG_BIT,value==0)
            
        # DECRJZ
        if cmd == 20:
            addr = self._read_next()
            value = (self._rd_mem(addr) - 1) & 0xFF
            self._wr_mem(addr, value)
            self._set_status_reg(self._ZERO_FLAG_BIT,value==0)
            if value == 0:
                self._pc+=2
                
        # INCRJZ
        if cmd == 21:
            addr = self._read_next()
            value = (self._rd_mem(addr) + 1) & 0xFF
            self._wr_mem(addr, value)
            self._set_status_reg(self._ZERO_FLAG_BIT,value==0)
            if value == 0:
                self._pc += 2

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
            # TODO: MED, In CBR and SBR, if the bit is zero, it should raise an error at compile time.
            bit_to_clear = self._read_next()
            addr = self._read_next()
            new_value = self._rd_mem(addr) | (1<<bit_to_clear)
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
            # TODO: MED, If you get a RETLA without first having called CALL, it should raise an exception at compile time.
            self._pc = self._ppc.pop()
        
        # RETURN
        if cmd == 31:
            self._pc = self._ppc.pop()
        
        # ADDRPC
        if cmd == 32:
            self._pc += self._read_next()
            
        return 1
                
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
        return self._exec_instruction(cmd)
        
    def goto(self, offset):
        if type(offset) is not int:
            raise TypeError(f"Expected offset as int, received {type(offset)}")
            
        if offset<0 or offset>255:
            raise ValueError(f"Expected 0<=offset<256, received {offset}")
            
        self._pc = offset
    
    def run(self):
        """
        Executes commands from the current program counter until a HALT opcode.
        
        :param offset: The offset within `_mem` to start executing from.
        :type offset: int
        """
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
               

class Digirule2U(Digirule):
    """
    Implements the Digirule 2U model.
    """
    def _exec_instruction(self, cmd):
        """
        Handles the execution of a specific instruction. Emulates the 2U firmware.

        Note:
            * See also ``Digirule._exec_instruction()``.
        """

        # Check if this is a valid instruction
        if (cmd>38 and cmd<192) or cmd>194:
            raise DgtoolsErrorOpcodeNotSupported(f"Opcode {cmd} not supported.")

        
        # Switch around RETLA and RETURN
        if cmd == 30:
            return super()._exec_instruction(31)

        if cmd == 31:
            return super()._exec_instruction(30)
        
        # Handle the new instructions
        # INITSP
        if cmd == 33:
            # The stack pointer is initialised internally anyway.
            pass

        # RANDA
        if cmd == 34:
            self._acc = random.randint(0,255)

        # SWAPRA
        if cmd == 35:
            mem_addr = self._read_next()
            mem_val = self._rd_mem(mem_addr)
            current_acc_value = self._acc
            self._acc = mem_val
            self._wr_mem(mem_addr, current_acc_value)

        # SWAPRR
        if cmd == 36:
            mem_addr_left = self._read_next()
            mem_addr_right = self._read_next()
            mem_val_left =  self._rd_mem(mem_addr_left)
            mem_val_right = self._rd_mem(mem_addr_right)
            self._wr_mem(mem_addr_left, mem_val_right)
            self._wr_mem(mem_addr_right, mem_val_left)

        # MUL
        if cmd == 37:
            mem_addr_left = self._read_next()
            mem_val_left = self._rd_mem(mem_addr_left)
            mem_addr_right = self._read_next()
            mem_val_right = self._rd_mem(mem_addr_right)
            self._wr_mem(mem_addr_left,(mem_val_left * mem_val_right) & 0xFF
        
        # DIV
        if cmd == 38:
            # TODO: MED, This can raise a divide by zero warning / exception too
            mem_addr_left = self._read_next()
            mem_val_left = self._rd_mem(mem_addr_left)
            mem_addr_right = self._read_next()
            mem_val_right = self._rd_mem(mem_addr_right)
            if mem_val_right == 0:
                # This is the division by zero behaviour
                return 0
            self._wr_mem(mem_addr_left, (mem_val_left // mem_val_right) & 0xFF)
            self._acc = (mem_val_left % mem_val_right) & 0xFF

        # COMOUT
        if cmd == 192:
            pass
        
        # COMIN
        if cmd == 193:
            pass

        # COMRDY
        if cmd == 194:
            pass

        return 1
