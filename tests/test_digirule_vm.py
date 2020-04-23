"""

Contains all tests for the Digirule Virtual Machine.

The VM is perhaps THE most important class of ``dgtools`` since any deviation in its behaviour
would cause errors not only to the code itself but more importantly, errors in the files the 
VM simulates.
"""

from dgtools.dgsim import Digirule
import types

def get_vm_hash(dg_vm):
    """
    Returns a hash of the VM's state.
    """
    hash_obj = list(dg_vm._mem)
    hash_obj.extend([dg_vm._acc, 
                     dg_vm._interactive_mode, 
                     dg_vm._mem[252], 
                     dg_vm._mem[253], 
                     dg_vm._mem[254], 
                     dg_vm._mem[255]])
    hash_obj.extend(dg_vm._ppc)
    return hash(bytearray(hash_obj).decode("utf-8"))


def test_constants():
    """
    Ensures that the value of specific constants for this version of the VM are within specification.
    """
    vm = Digirule()
    assert vm._ZERO_FLAG_BIT == 1
    assert vm._CARRY_FLAG_BIT == 2
    assert vm._ADDRLED_FLAG_BIT == 4
    assert vm._status_reg_ptr == 252
    assert vm._bt_reg_ptr == 253
    assert vm._addrled_reg_ptr == 254
    assert vm._dataled_reg_ptr == 255
    assert vm._interactive_mode == False
    assert type(vm._interactive_callback) is types.FunctionType

    
def test_HALT():
    """
    HALT stops execution, but other than this, it does not affect the state of the VM.
    """
    vm = Digirule()
    vm.load_program([0])
    vm.goto(0)
    hash_before = get_vm_hash(vm)
    run_res = vm._exec_next()
    hash_after = get_vm_hash(vm)
    
    assert run_res == 0
    assert hash_before == hash_after


def test_NOP():
    """
    NOP does not affect the state of the VM.
    """
    vm = Digirule()
    vm.load_program([1])
    vm.goto(0)
    hash_before = get_vm_hash(vm)
    run_res = vm._exec_next()
    hash_after = get_vm_hash(vm)
    
    assert run_res == 1
    assert hash_before == hash_after
    
def test_SPEED():
    """
    SPEED simply sets an internal variable, it does not affect the state of the VM.
    """
    vm = Digirule()
    vm.load_program([2, 3])
    vm.goto(0)
    hash_before = get_vm_hash(vm)
    run_res = vm._exec_next()
    hash_after = get_vm_hash(vm)
    
    assert run_res == 1
    assert hash_before == hash_after
    assert vm._speed_setting == 3
    

def test_COPYLR():
    """
    COPYLR copies a literal to a memory location.
    """
    vm = Digirule()
    vm.load_program([3, 42, 3, 0])
    vm.goto(0)
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._mem[3] == 42


def test_COPYLA():
    """
    COPYLA copies a literal to the accumulator.
    """
    vm = Digirule()
    vm.load_program([4, 42])
    vm.goto(0)
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 42


def test_COPYAR():
    """
    COPYAR copies the value of the accumulator to a memory position.
    """
    vm = Digirule()
    vm.load_program([5, 2, 0])
    vm.goto(0)
    vm._acc = 42
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._mem[2] == 42


def test_COPYRA():
    """
    COPYRA copies the value of a memory position to the accumulator.
    If the accumulator is set to zero, so does the zero flag.
    """
    vm = Digirule()
    vm.load_program([6, 2, 42])
    vm._mem[252] = 1
    vm.goto(0)
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 42
    assert vm._mem[252] & 0x01 == 0


def test_COPYRR():
    """
    COPYRR copies the value of one memory position to another affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([7, 3, 4, 42, 0])
    vm._mem[252] = 1
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._mem[3] == vm._mem[4]
    assert vm._mem[252] & 0x01 == 0


def test_ADDLA():
    """
    ADDLA Adds a literal to the accumulator affecting the zero and carry flags
    """
    vm = Digirule()
    vm.load_program([8, 1])
    vm._acc = 0xFF
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 0
    assert vm._mem[252] & 0x01 == 1
    assert vm._mem[252] & 0x02 == 2


def test_ADDRA():
    """
    ADDRA Adds a memory location to the accumulator affecting the zero and carry flags
    """
    vm = Digirule()
    vm.load_program([9, 2, 1])
    vm._acc = 0xFF
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 0
    assert vm._mem[252] & 0x01 == 1
    assert vm._mem[252] & 0x02 == 2


def test_SUBLA():
    """
    SUBLA subtracts a literal from the accumulator affecting the zero and carry flags
    """
    vm = Digirule()
    vm.load_program([10, 1])
    vm._acc = 0x01
    vm._mem[252] = 3
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 0
    assert vm._mem[252] & 0x01 == 1
    assert vm._mem[252] & 0x02 == 0


def test_SUBRA():
    """
    SUBRA subtracts a memory location from the accumulator affecting the zero and carry flags
    """
    vm = Digirule()
    vm.load_program([11, 2, 1])
    vm._acc = 0x01
    vm._mem[252] = 3
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 0
    assert vm._mem[252] & 0x01 == 1
    assert vm._mem[252] & 0x02 == 0


def test_ANDLA():
    """
    ANDLA applies bitwise AND between the Accumulator and a literal and returns the result
    to the accumulator, affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([12, 4])
    vm._acc = 0x03
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 0
    assert vm._mem[252] & 0x01 == 1
