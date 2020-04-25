"""

Contains all tests for the Digirule Virtual Machine.

The VM is perhaps THE most important class of ``dgtools`` since any deviation in its behaviour
would cause errors not only to the code itself but more importantly, errors in the files the 
VM simulates.
"""

from dgtools.dgsim import Digirule
import types

import pdb


def get_vm_hash(dg_vm):
    """
    Returns a hash of a VM's state.
    
    :param dg_vm: A Digirule object
    :type: dgtools.Digirule
    :returns: A hash that is derived by all variables that contribute to the VM's state.
    :rtype: int
    """
    hash_obj = list(dg_vm._mem)
    hash_obj.extend([dg_vm._acc,
                     dg_vm._pc,
                     dg_vm._interactive_mode, 
                     dg_vm._mem[252], 
                     dg_vm._mem[253], 
                     dg_vm._mem[254], 
                     dg_vm._mem[255]])
    hash_obj.extend(dg_vm._ppc)
    return hash(bytearray(hash_obj).decode("utf-8"))
    

def get_vm_hash_after_exec(a_program):
    """
    Executes a_program and returns the hash of the VM at the end of that program.
    
    :param a_program: Compiled Digirule program
    :type a_program: list<int>
    :returns: The hash of the VM at the end of the program
    :rtype: int
    """
    vm = Digirule()
    vm.load_program(a_program)
    vm.goto(0)
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
    assert vm._status_reg_ptr == 252
    assert vm._bt_reg_ptr == 253
    assert vm._addrled_reg_ptr == 254
    assert vm._dataled_reg_ptr == 255
    assert vm._interactive_mode == False
    assert type(vm._interactive_callback) is types.FunctionType

    
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
    vm_expected.load_program(test_program)
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
    vm_expected.load_program(test_program)
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
    vm_expected.load_program(test_program)
    vm_expected._pc = 4
    vm_expected._mem[4] = 42
    
    assert get_vm_hash(vm_expected) == vm_hash


def test_COPYLA():
    """
    COPYLA copies a literal to the Accumulator.
    
    Program bytes used   : 2
    Status flags affected: None
    """
    vm = Digirule()
    vm.load_program([4, 42])
    vm.goto(0)
    run_res = vm._exec_next()
    
    vm_expected = Digirule()
    vm_expected.load_program([4,42])
    
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
    

def test_ANDRA():
    """
    ANDRA applies bitwise AND between the Accumulator and a memory location and returns the result
    to the accumulator, affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([13, 2, 4])
    vm._acc = 0x03
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 0
    assert vm._mem[252] & 0x01 == 1
    

def test_ORLA():
    """
    ORLA applies bitwise OR between the Accumulator and a literal and returns the result
    to the accumulator, affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([14, 3])
    vm._acc = 0x04
    vm._mem[252] = 1
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 7
    assert vm._mem[252] & 0x01 == 0


def test_ORRA():
    """
    ORRA applies bitwise OR between the Accumulator and a memory location and returns the result
    to the accumulator, affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([15, 2, 3])
    vm._acc = 0x04
    vm._mem[252] = 1
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 7
    assert vm._mem[252] & 0x01 == 0


def test_XORLA():
    """
    XORLA applies bitwise XOR between the Accumulator and a memory location and returns the result
    to the accumulator, affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([16, 0xFF])
    vm._acc = 0xFF
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 0
    assert vm._mem[252] & 0x01 == 1


def test_XORRA():
    """
    XORLA applies bitwise XOR between the Accumulator and a memory location and returns the result
    to the accumulator, affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([17, 2, 0xFF])
    vm._acc = 0xFF
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._acc == 0
    assert vm._mem[252] & 0x01 == 1


def test_DECR():
    """
    DECR decrements a memory location affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([18, 2, 0x01])
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._mem[2] == 0
    assert vm._mem[252] & 0x01 == 1


def test_INCR():
    """
    INCR increments a memory location affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([19, 2, 0xFF])
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    
    assert run_res == 1
    assert vm._mem[2] == 0
    assert vm._mem[252] & 0x01 == 1


def test_DECRJZ():
    """
    DECRJZ decrement the content of a memory location and jump if zero affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([20, 2, 0x01, 0x00,0x00])
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[2] == 0
    assert vm._mem[252] & 0x01 == 1
    assert vm._pc == 4
    
    vm._mem[2]=0x02
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[2] == 1
    assert vm._mem[252] & 0x01 == 0
    assert vm._pc == 2
    

def test_INCRJZ():
    """
    INCRJZ increment the content of a memory location and jump if zero affecting the zero flag.
    """
    vm = Digirule()
    vm.load_program([21, 2, 0xFF, 0x00,0x00])
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[2] == 0
    assert vm._mem[252] & 0x01 == 1
    assert vm._pc == 4
    
    vm._mem[2]=0x01
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[2] == 2
    assert vm._mem[252] & 0x01 == 0
    assert vm._pc == 2


def test_SHIFTRL():
    """
    SHIFTRL Shifts the contents of a memory location left by one through the carry flag.
    """
    vm = Digirule()
    vm.load_program([22, 2, 0x01])
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[2] == 2
    assert vm._mem[252] & 0x02 == 0
    
    vm._mem[2]=0x80
    vm._mem[252]=0
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[2] == 0
    assert vm._mem[252] & 0x02 == 0x02

    vm._mem[2]=0x00
    vm._mem[252]=2
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[2] == 1
    assert vm._mem[252] & 0x02 == 0

def test_SHIFTRR():
    """
    SHIFTRR Shifts the contents of a memory location right by one through the carry flag.
    """
    vm = Digirule()
    vm.load_program([23, 2, 0x01])
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[2] == 0
    assert vm._mem[252] & 0x02 == 0x02
    
    vm._mem[2]=0x80
    vm._mem[252]=0
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[2] == 0x40
    assert vm._mem[252] & 0x02 == 0

    vm._mem[2]=0x04
    vm._mem[252]=2
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[2] == 0x82
    assert vm._mem[252] & 0x02 == 0


def test_CBR():
    """
    CBR clears a specific bit.
    """
    vm = Digirule()
    vm.load_program([24, 0, 3, 0x01])
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[3] == 0
    assert vm._mem[252] == 0x00


def test_SBR():
    """
    SBR sets a specific bit.
    """
    vm = Digirule()
    vm.load_program([25, 0, 3, 0x00])
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._mem[3] == 1
    assert vm._mem[252] == 0x00


def test_BCRSC():
    """
    BCRSC tests a specific bit and if it is CLEAR it jumps over the next two bytes in mem.
    """
    vm = Digirule()
    vm.load_program([26, 1, 6, 0x00, 0x00, 0x00, 0x00])
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._pc == 0x05

    vm._mem[6]=2
    vm.goto(0)
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._pc == 0x03


def test_BCRSS():
    """
    BCRSS tests a specific bit and if it is SET it jumps over the next two bytes in mem.
    """
    vm = Digirule()
    vm.load_program([27, 1, 6, 0x00, 0x00, 0x00, 0x00])
    vm._mem[252] = 0
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._pc == 0x03

    vm._mem[6]=2
    vm.goto(0)
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._pc == 0x05


def test_JUMP():
    """
    JUMP jumps to a specific location in memory.
    """
    vm = Digirule()
    vm.load_program([28, 2, 0x00])
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._pc == 0x02


def test_CALL():
    """
    CALL jumps to a specific location in memory until it finds a RETURN.
    """
    vm = Digirule()
    vm.load_program([29, 2, 0x00])
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._pc == 0x02
    assert vm._ppc[0] == 0x02


def test_RETLA():
    """
    CALL jumps to a specific location in memory until it finds a RETURN.
    """
    vm = Digirule()
    vm.load_program([29, 2, 0x01, 30, 42])
    vm.goto(0)
    
    run_res = vm._exec_next()
    run_res = vm._exec_next()
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._pc == 0x02
    assert len(vm._ppc) == 0
    assert vm._acc==42


def test_RETURN():
    """
    RETURN returns from a CALL.
    """
    vm = Digirule()
    vm.load_program([29, 2, 0x01, 31])
    vm.goto(0)
    
    run_res = vm._exec_next()
    run_res = vm._exec_next()
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._pc == 0x02
    assert len(vm._ppc) == 0


def test_ADDRPC():
    """
    ADDRPC adds the contents of a ram location to the PC.
    """
    vm = Digirule()
    vm.load_program([32, 2, 0x03, 0x00])
    vm.goto(0)
    
    run_res = vm._exec_next()
    assert run_res == 1
    assert vm._pc == 0x03
