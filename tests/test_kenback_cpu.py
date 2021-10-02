"""

Contains all tests for the Kenback.

:author: Athanasios Anastasiou
:date: Dec 2020 

"""

# TODO: HIGH, Need to include all possible test cases
# TODO: HIGH, Reduce code duplication between the tests

from dgtools.kenback import Kenback
from dgtools.exceptions import DgtoolsErrorProgramHalt
import types
import base64
import pytest


def get_vm_hash(dg_vm):
    """
    Returns a hash of a VM's state.
    
    :param dg_vm: A Kenback object
    :type: dgtools.kenback.Kenback
    :returns: A hash that is derived by all variables that contribute to the VM's state.
    :rtype: int
    """
    hash_obj = list(dg_vm.mem._mem)
    return hash(base64.b64encode(bytearray(hash_obj)))
    

def get_vm_hash_after_exec(a_program, use_this_vm=None):
    """
    Executes a_program and returns the hash of the VM at the end of that program.
    
    :param a_program: Compiled Kenback program
    :type a_program: list<int>
    :param use_this_vm: A pre-configured Kenback object.
    :type use_this_vm: dgtools.kenback.Kenback
    :returns: The hash of the VM at the end of the program
    :rtype: int
    """
    if use_this_vm is None:
        vm = Kenback()
        vm.mem.load(a_program)
    else:
        vm = use_this_vm
        
    with pytest.raises(DgtoolsErrorProgramHalt):
        vm.run()
    
    return get_vm_hash(vm)
    

def test_HALT():
    """
    HALT stops execution, but other than this, it does not affect the state of the VM.
    
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [0, 0, 0, 4, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.pc = 5
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_NOOP():
    """
    NOOP performs, no operation.
    
    Program bytes used   : 1
    Status flags affected: None
    """
    
    # Notice the program here, it is 127 followed by 0. So 127 is no-op but the following HALT is what 
    # gracefully stops the CPU, so the program counter advances two cells in this cas rather than the one
    # that would be expected from just the noop.
    test_program = [0, 0, 0, 4, 127,0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.pc = 6
        
    assert get_vm_hash(vm_expected) == vm_hash


def test_ADD():
    """
    Add performs, no operation.
    
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [1, 0, 0, 4, 3, 1, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem["A"] = 2
    vm_expected.pc = 7
        
    assert get_vm_hash(vm_expected) == vm_hash

def test_SUB():
    """
    Add performs, no operation.
    
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [1, 0, 0, 4, 11, 1, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem["A"] = 0
    vm_expected.pc = 7
        
    assert get_vm_hash(vm_expected) == vm_hash

def test_LOAD():
    """
    Add performs, no operation.
    
    Program bytes used   : 1
    Status flags affected: None
    """
    # TODO: HIGH, add all the programs that check all the branches of execution
    test_program = [0, 0, 0, 4, 19, 2]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._reg_wr("A",2)
    vm_expected.pc = 7
    
    assert get_vm_hash(vm_expected) == vm_hash

def test_STORE():
    """
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [0, 0, 0, 4, 27, 8, 0, 120, 120]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._reg_wr("A",0)
    vm_expected.mem[8]=0
    vm_expected.pc = 7
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_AND():
    """
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [3, 0, 0, 4, 211, 2, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._reg_wr("A",3 & 2)
    vm_expected.pc = 7
    
    assert get_vm_hash(vm_expected) == vm_hash

def test_OR():
    """
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [0x0F, 0, 0, 4, 195, 0xF0, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._reg_wr("A",0x0F | 0xF0)
    vm_expected.pc = 7
    
    assert get_vm_hash(vm_expected) == vm_hash

def test_LNEG():
    """
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [0, 0, 0, 4, 219, 0xF0, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._reg_wr("A",0x0F)
    vm_expected.pc = 7
    
    assert get_vm_hash(vm_expected) == vm_hash

def test_SHIFT_LEFT():
    """
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [3, 0, 0, 4, 0b10001001, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._reg_wr("A",3 << 1)
    vm_expected.pc = 6
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_SHIFT_RIGHT():
    """
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [128, 0, 0, 4, 0b00001001, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._reg_wr("A",128 + 64)
    vm_expected.pc = 6
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_ROTATE_LEFT():
    """
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [129, 0, 0, 4, 0b11001001, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._reg_wr("A",3)
    vm_expected.pc = 6
    
    assert get_vm_hash(vm_expected) == vm_hash

def test_ROTATE_RIGHT():
    """
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [3, 0, 0, 4, 0b01001001, 0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._reg_wr("A",129)
    vm_expected.pc = 6
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_SET_ZERO_ZERO():
    """
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [0, 0, 0, 4, 0b00000010, 7, 0, 0xFF]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._mem_wr(7,0xFE)
    vm_expected.pc = 7
    
    assert get_vm_hash(vm_expected) == vm_hash

def test_SET_ONE_ZERO():
    """
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [0, 0, 0, 4, 0b01000010, 7, 0, 0xFE]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.mem._mem_wr(7,0xFF)
    vm_expected.pc = 7
    
    assert get_vm_hash(vm_expected) == vm_hash
