"""

Contains all tests for the Digirule Virtual Machine.

The VM is perhaps THE most important class of ``dgtools`` since any deviation in its behaviour
would cause errors not only to the code itself but more importantly, errors in the files the 
VM simulates.
"""

from dgtools.digirule import Digirule
from dgtools.exceptions import DgtoolsErrorProgramHalt
import types
import base64
import pytest


def get_vm_hash(dg_vm):
    """
    Returns a hash of a VM's state.
    
    :param dg_vm: A Digirule object
    :type: dgtools.Digirule
    :returns: A hash that is derived by all variables that contribute to the VM's state.
    :rtype: int
    """
    hash_obj = list(dg_vm.mem._mem)
    #hash_obj.extend([dg_vm._acc,
    ##                 dg_vm._pc,
    #                 dg_vm._mem[252], 
    #                 dg_vm._mem[253], 
    #                 dg_vm._mem[254], 
    #                 dg_vm._mem[255]])
    hash_obj.extend(dg_vm._ppc)
    return hash(base64.b64encode(bytearray(hash_obj)))
    

def get_vm_hash_after_exec(a_program, use_this_vm=None):
    """
    Executes a_program and returns the hash of the VM at the end of that program.
    
    :param a_program: Compiled Digirule program
    :type a_program: list<int>
    :param use_this_vm: A pre-configured Digirule object.
    :type use_this_vm: Digirule
    :returns: The hash of the VM at the end of the program
    :rtype: int
    """
    if use_this_vm is None:
        vm = Digirule()
        vm.mem.load(a_program)
        # vm.mem.load(a_program)
        vm.pc = 0
    else:
        vm = use_this_vm
        
    with pytest.raises(DgtoolsErrorProgramHalt):
        vm.run()
    
    return get_vm_hash(vm)


def test_constants():
    """
    Ensures that the value of specific constants for this version of the VM are within specification.
    """
    vm = Digirule()
    
    assert vm._ZERO_FLAG_BIT == 1
    assert vm._CARRY_FLAG_BIT == 2
    assert vm._ADDRLED_FLAG_BIT == 4
    assert vm._interactive_callback is None

    
def test_HALT():
    """
    HALT stops execution, but other than this, it does not affect the state of the VM.
    
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected._pc = 1
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_NOP():
    """
    NOP does not perform ANY operation, does not affect the state of the VM.
    
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [1, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._pc = 2
    assert get_vm_hash(vm_expected) == vm_hash
    

def test_SPEED():
    """
    SPEED simply sets an internal variable, it does not affect the state of the VM.
    
    Program bytes used   : 2
    Status flags affected: None
    """
    test_program = [2, 3, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._pc = 3
    vm_expected._speed_setting = 3
    
    assert get_vm_hash(vm_expected) == vm_hash

    
def test_COPYLR():
    """
    COPYLR copies a literal to the specified RAM location.
    
    Program bytes used   : 3
    Status flags affected: None
    """
    test_program = [3, 42, 4, 0, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._pc = 4
    vm_expected.mem[4] = 42
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_COPYLA():
    """
    COPYLA copies a literal to the Accumulator.
    
    Program bytes used   : 2
    Status flags affected: None
    """
    test_program = [4, 42, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 42
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_COPYAR():
    """
    COPYAR copies the value of the Accumulator to the specified RAM location.
    
    Program bytes used   : 2
    Status flags affected: None 
    """
    test_program = [5, 3, 0, 42]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected.mem[3] = 0
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_COPYRA():
    """
    COPYRA copies the value of a memory location to the Accumulator.

    Program bytes used:  : 2
    Status flags affected: Zero
    """
    test_program = [6, 3, 0, 42]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 42
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_COPYRR():
    """
    COPYRR copies the value of a memory location to another.
    
    Program bytes used   : 3
    Status flags affected: Zero
    """
    test_program = [7, 4, 5, 0, 42, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected.mem[5] = 42
    vm_expected._pc = 4
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_ADDLA():
    """
    ADDLA Adds a literal to the Accumulator.
    
    Program bytes used   : 2
    Status flags affected: Zero, Carry
    """
    test_program = [8, 1, 0]
    vm = Digirule()
    vm.mem.load(test_program)
    vm._acc = 0xFF
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 0
    vm_expected.mem[252] = 3
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_ADDRA():
    """
    ADDRA Adds the value of a memory location to the Accumulator.
    
    Program bytes used   : 2
    Status flags affected: Zero, Carry
    """
    test_program = [9, 3, 0, 1]
    vm = Digirule()
    vm.mem.load(test_program)
    vm._acc = 0xFF
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 0
    vm_expected.mem[252] = 3
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash



def test_SUBLA():
    """
    SUBLA subtracts a literal from the Accumulator.
    
    Program bytes used   : 2
    Status flags affected: Zero, Carry
    """
    test_program = [10, 1, 0]
    
    # Test setting the zero flag
    vm = Digirule()
    vm.mem.load(test_program)
    vm._acc = 1
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 0
    vm_expected.mem[252] = 1
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash, "Failed the zero flag part of the test."
    
    # Run the same program once again, it takes the Accumulator to 0xFF and
    # sets the carry flag
    vm.goto(0)
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    vm_expected._acc = 0xFF
    vm_expected.mem[252] = 2

    assert get_vm_hash(vm_expected) == vm_hash, "Failed the carry flag part of the test."
    


def test_SUBRA():
    """
    SUBRA subtracts the value of a memory location from the Accumulator.
    
    Program bytes used   : 2
    Status flags affected: Zero, Carry
    """
    test_program = [11, 3, 0, 1]
    
    # Test setting the zero flag
    vm = Digirule()
    vm.mem.load(test_program)
    vm._acc = 1
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 0
    vm_expected.mem[252] = 1
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash, "Failed the zero flag part of the test."
    
    # Run the same program once again, it takes the Accumulator to 0xFF and
    # sets the carry flag
    vm.goto(0)
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    vm_expected._acc = 0xFF
    vm_expected.mem[252] = 2

    assert get_vm_hash(vm_expected) == vm_hash, "Failed the carry flag part of the test."


def test_ANDLA():
    """
    ANDLA applies bitwise AND between the Accumulator and a literal and returns the result
    to the Accumulator.
    
    Program bytes used   : 2
    Status flags affected: Zero
    """
    test_program = [12, 0xFF, 0]
    
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 0
    vm_expected.mem[252] = 1
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash
    

def test_ANDRA():
    """
    ANDRA applies bitwise AND between the Accumulator and the value of a memory location and returns the result
    to the Accumulator.

    Program bytes used   : 2
    Status flags affected: Zero    
    """
    test_program = [13, 3, 0, 0xFF]
    
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 0
    vm_expected.mem[252] = 1
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash
    

def test_ORLA():
    """
    ORLA applies bitwise OR between the Accumulator and a literal and returns the result
    to the Accumulator.

    Program bytes used   : 2
    Status flags affected: Zero    
    """
    test_program = [14, 0, 0]
    
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 0
    vm_expected.mem[252] = 1
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_ORRA():
    """
    ORRA applies bitwise OR between the Accumulator and the value of a memory location and returns the result
    to the Accumulator.

    Program bytes used   : 2
    Status flags affected: Zero    
    """
    test_program = [15, 3, 0, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 0
    vm_expected.mem[252] = 1
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash



def test_XORLA():
    """
    XORLA applies bitwise XOR between the Accumulator and the value of a memory location and returns the result
    to the Accumulator.

    Program bytes used   : 2
    Status flags affected: Zero    
    """
    test_program = [16, 0xFF, 0]
    
    vm = Digirule()
    vm.mem.load(test_program)
    vm._acc = 0xFF
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 0
    vm_expected.mem[252] = 1
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash



def test_XORRA():
    """
    XORRA applies bitwise XOR between the Accumulator and the value of a memory location and returns the result
    to the Accumulator.

    Program bytes used   : 2
    Status flags affected: Zero    
    """
    test_program = [17, 3, 0, 0xFF]
    
    vm = Digirule()
    vm.mem.load(test_program)
    vm._acc = 0xFF
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._acc = 0x00
    vm_expected.mem[252] = 1
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_DECR():
    """
    DECR decrements the value of a memory location.    
    
    Program bytes used   : 2
    Status flags affected: Zero    
    """
    test_program = [18, 3, 0, 0x01]
    
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected.mem[3] = 0
    vm_expected.mem[252] = 1
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_INCR():
    """
    INCR increments the value of a memory location.

    Program bytes used   : 2
    Status flags affected: Zero    
    """
    test_program = [19, 3, 0, 0xFF]
    
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected.mem[3] = 0
    vm_expected.mem[252] = 1
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_DECRJZ():
    """
    DECRJZ decrement the value of a memory location and increase PC by two if zero.     
    
    Program bytes used   : 2
    Status flags affected: Zero    
    """
    test_program = [20, 3, 0, 0x02, 0x00]
    
    vm = Digirule()
    vm.mem.load(test_program)
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    # Test normal execution without hitting zero
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected.mem[3] = 0x01
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash, "Failed to continue when condition not met."

    # Test execution after hitting zero.
    # Notice here, we resume execution without reloading the program. That would reset the memory state.
    
    vm.goto(0)
    with pytest.raises(DgtoolsErrorProgramHalt):
        vm.run()
    vm_hash = get_vm_hash(vm)
    vm_expected.mem[3] = 0x00
    vm_expected.mem[252] = 1
    vm_expected._pc = 5

    assert get_vm_hash(vm_expected) == vm_hash, "Failed in jumping when condition is met."
    
    
def test_INCRJZ():
    """
    INCRJZ increment the value of a memory location and increase PC by two if zero.

    Program bytes used   : 2
    Status flags affected: Zero    
    """
    test_program = [21, 3, 0, 0xFE, 0x00]
    
    vm = Digirule()
    vm.mem.load(test_program)
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    # Test normal execution without hitting zero
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected.mem[3] = 0xFF
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash, "Failed to continue when condition not met."
    
    vm.goto(0)
    with pytest.raises(DgtoolsErrorProgramHalt):
        vm.run()
    vm_hash = get_vm_hash(vm)
    vm_expected.mem[3] = 0x00
    vm_expected.mem[252] = 1
    vm_expected._pc = 5

    assert get_vm_hash(vm_expected) == vm_hash, "Failed in jumping when condition is met."


def test_SHIFTRL():
    """
    SHIFTRL Shifts the value of a memory location left by one through the carry flag.
    
    Program bytes used   : 2
    Status flags affected: Carry    
    """
    test_program = [22, 3, 0, 0x81]
    
    vm = Digirule()
    vm.mem.load(test_program)
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    # Test normal execution without hitting zero
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected.mem[3] = 0x02
    vm_expected.mem[252] = 0x02
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash
    

def test_SHIFTRR():
    """
    SHIFTRR Shifts the value of a memory location right by one through the carry flag.
    
    Program bytes used   : 2
    Status flags affected: Carry    
    """
    test_program = [23, 3, 0, 0x81]
    
    vm = Digirule()
    vm.mem.load(test_program)
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    # Test normal execution without hitting zero
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected.mem[3] = 0x40
    vm_expected.mem[252] = 0x02
    vm_expected._pc = 3
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_CBR():
    """
    CBR clears a specific bit in the value of a memory location.
    
    Program bytes used   : 3
    Status flags affected: None    
    """
    test_program = [24, 5, 4, 0, 0xFF]
    
    vm = Digirule()
    vm.mem.load(test_program)
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    # Test normal execution without hitting zero
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected.mem[4] = 0xDF
    vm_expected._pc = 4
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_SBR():
    """
    SBR sets a specific bit in the value of a memory location.
    
    Program bytes used   : 3
    Status flags affected: None    
    """
    test_program = [25, 5, 4, 0, 0x00]
    
    vm = Digirule()
    vm.mem.load(test_program)
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    # Test normal execution without hitting zero
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected.mem[4] = 32
    vm_expected._pc = 4
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_BCRSC():
    """
    BCRSC tests a specific bit in the value of a memory location and if it is CLEAR it adds 2 to the PC.
    
    Program bytes used   : 3
    Status flags affected: None    
    """
    test_program_bit_set = [26, 3, 6, 0, 0, 0, 0xFF]
    test_program_bit_clear = [26, 3, 6, 0, 0, 0, 0x00]
    
    vm_hash_when_clear = get_vm_hash_after_exec(test_program_bit_clear)
    vm_hash_when_set = get_vm_hash_after_exec(test_program_bit_set)
    
    vm_expected_clear = Digirule()
    vm_expected_clear.mem.load(test_program_bit_clear)
    vm_expected_clear._pc = 6
    
    vm_expected_set = Digirule()
    vm_expected_set.mem.load(test_program_bit_set)
    vm_expected_set._pc = 4
    
    assert vm_hash_when_clear == get_vm_hash(vm_expected_clear), "Failed when bit is clear."
    assert vm_hash_when_set == get_vm_hash(vm_expected_set), "Failed when bit is set."


def test_BCRSS():
    """
    BCRSS tests a specific bit in the value of a memory location and if it is SET it adds 2 to the PC.

    Program bytes used   : 3
    Status flags affected: None    
    """
    test_program_bit_set = [27, 3, 6, 0, 0, 0, 0xFF]
    test_program_bit_clear = [27, 3, 6, 0, 0, 0, 0x00]
    
    vm_hash_when_clear = get_vm_hash_after_exec(test_program_bit_clear)
    vm_hash_when_set = get_vm_hash_after_exec(test_program_bit_set)
    
    vm_expected_clear = Digirule()
    vm_expected_clear.mem.load(test_program_bit_clear)
    vm_expected_clear._pc = 4
    
    vm_expected_set = Digirule()
    vm_expected_set.mem.load(test_program_bit_set)
    vm_expected_set._pc = 6
    
    assert vm_hash_when_clear == get_vm_hash(vm_expected_clear), "Failed when bit is clear."
    assert vm_hash_when_set == get_vm_hash(vm_expected_set), "Failed when bit is set."


def test_JUMP():
    """
    JUMP jumps to a specific location in memory.

    Program bytes used   : 2
    Status flags affected: None    
    """
    test_program = [28, 3, 0, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._pc = 4
    
    assert vm_hash == get_vm_hash(vm_expected)


def test_CALL():
    """
    CALL jumps to a specific location in memory until it finds a RETURN.

    Program bytes used   : 2
    Status flags affected: None    
    """
    test_program = [29,3,0,0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    # Notice here, the test program calls the routine which immediately HALTs
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._ppc = [2]
    vm_expected._pc = 4
    
    assert vm_hash == get_vm_hash(vm_expected)


def test_RETLA():
    """
    CALL jumps to a specific location in memory until it finds a RETURN.

    Program bytes used   : 2
    Status flags affected: None    
    """
    test_program = [0,0,0,30,42]
    vm = Digirule()
    vm.mem.load(test_program)
    vm.goto(3)
    vm._ppc = [0]
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._pc = 1
    vm_expected._acc = 42
    
    assert vm_hash == get_vm_hash(vm_expected)


def test_RETURN():
    """
    RETURN returns from a CALL.

    Program bytes used   : 1
    Status flags affected: None    
    """
    test_program = [0,0,0,31]
    vm = Digirule()
    vm.mem.load(test_program)
    vm.goto(3)
    vm._ppc = [0]
    vm_hash = get_vm_hash_after_exec(test_program, vm)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._pc = 1
    
    assert vm_hash == get_vm_hash(vm_expected)


def test_ADDRPC():
    """
    ADDRPC adds the value of a ram location to the PC and jumps to that offset.

    Program bytes used   : 2
    Status flags affected: None    
    """
    test_program = [32, 2, 0, 0, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Digirule()
    vm_expected.mem.load(test_program)
    vm_expected._pc = 4
    
    assert vm_hash == get_vm_hash(vm_expected)
