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
        vm.pc = 0
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
    test_program = [0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.pc = 1
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_NOOP():
    """
    NOOP performs, no operation.
    
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [127,0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.pc = 2
        
    assert get_vm_hash(vm_expected) == vm_hash


def test_ADD():
    """
    Add performs, no operation.
    
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [134,0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.pc = 2
    
        
    assert get_vm_hash(vm_expected) == vm_hash

def test_LOAD():
    """
    Add performs, no operation.
    
    Program bytes used   : 1
    Status flags affected: None
    """
    test_program = [19,0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    vm_expected = Kenback()
    vm_expected.mem.load(test_program)
    vm_expected.pc = 2
    
    import pdb
    pdb.set_trace()
        
    assert get_vm_hash(vm_expected) == vm_hash
