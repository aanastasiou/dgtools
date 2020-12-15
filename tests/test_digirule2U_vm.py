"""

Contains all tests for the Digirule2U Virtual Machine.

"""

from dgtools.digirule import Digirule2U
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
        vm = Digirule2U()
        vm.mem.load(a_program)
        # vm.mem.load(a_program)
        vm.pc = 0
    else:
        vm = use_this_vm
        
    with pytest.raises(DgtoolsErrorProgramHalt):
        vm.run()
    
    return get_vm_hash(vm)
    

def test_CALLI():
    """
    CALLI jumps to a location in memory indicated by another location in memory...until it finds a RETURN.

    Program bytes used   : 2
    Status flags affected: None    
    """
    test_program = [43,2,3,0]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    # Notice here, the test program calls the routine which immediately HALTs
    vm_expected = Digirule2U()
    vm_expected.mem.load(test_program)
    vm_expected._ppc = [2]
    vm_expected.pc = 4
    
    assert vm_hash == get_vm_hash(vm_expected)

def test_SWAPRA():
    """
    SWAPRA Swaps the value of the Accumulator with the value of a memory location.

    Program bytes used   : 2
    Status flags affected: None    
    """
    test_program = [4, 9, 15, 5, 0, 42]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    # Notice here, the test program calls the routine which immediately HALTs
    vm_expected = Digirule2U()
    vm_expected.mem.load(test_program)
    vm_expected.pc = 5
    vm_expected.mem["Acc"] = 42
    vm_expected.mem[5] = 9
    
    assert vm_hash == get_vm_hash(vm_expected)

def test_SWAPRR():
    """
    SWAPRR Swaps the values of two memory locations.

    Program bytes used   : 3
    Status flags affected: None    
    """
    test_program = [16, 4, 5, 0, 42, 31]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    # Notice here, the test program calls the routine which immediately HALTs
    vm_expected = Digirule2U()
    vm_expected.mem.load(test_program)
    vm_expected.pc = 4
    vm_expected.mem[4] = 31
    vm_expected.mem[5] = 42
    
    
    assert vm_hash == get_vm_hash(vm_expected)


def test_MUL():
    """
    MUL Multiplies the content of two memory locations and returns the product in the first memory location.

    Program bytes used   : 3
    Status flags affected: None    
    """
    test_program = [21, 4, 5, 0, 4, 4]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    # Notice here, the test program calls the routine which immediately HALTs
    vm_expected = Digirule2U()
    vm_expected.mem.load(test_program)
    vm_expected.pc = 4
    vm_expected.mem[4] = 16
    
    assert vm_hash == get_vm_hash(vm_expected)


def test_DIV():
    """
    DIV Divides the content of two memory locations and returns the division in the first memory location and remainder
    in the Acc.

    Program bytes used   : 3
    Status flags affected: None    
    """
    test_program = [22, 4, 5, 0, 9, 2]
    vm_hash = get_vm_hash_after_exec(test_program)
    
    # Notice here, the test program calls the routine which immediately HALTs
    vm_expected = Digirule2U()
    vm_expected.mem.load(test_program)
    vm_expected.pc = 4
    vm_expected.mem[4] = 4
    vm_expected.mem["Acc"] = 1
    
    assert vm_hash == get_vm_hash(vm_expected)
