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


