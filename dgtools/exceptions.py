"""

Includes all exceptions raised by the software.

:author: Athanasios Anastasiou
:date: Mar 2020
"""

class DgtoolsError(Exception):
    """
    Base class for all dgtools specific errors
    """
    pass
    
    
class DgtoolsErrorSymbolUndefined(DgtoolsError):
    """
    Raised during the second pass of assembly if a label or symbol is requested that has not even been defined.
    """
    pass
    
    
class DgtoolsErrorSymbolAlreadyDefined(DgtoolsError):
    """
    Raised when a label or symbol is attempted to be redefined.
    """
    pass
    
    
class DgtoolsErrorOpcodeNotSupported(DgtoolsError):
    """
    Raised when an opcode is encountered that the VM does not know how to execute.
    """
    pass
    
    
class DgtoolsErrorDgbarchiveCorrupted(DgtoolsError):
    """
    Raised when a .dgb archive does not conform to its defined format.
    """
    pass
    
    
class DgtoolsErrorDgbarchiveVersionIncompatible(DgtoolsError):
    """
    Raised when a Digirule is attempting to load a DGBArchive whose version (firmware version) does not match that 
    of the hardware.
    """
    pass
    
    
class DgtoolsErrorProgramHalt(DgtoolsError):
    """
    Raised to signify that execution has halted for a specific reason (mentioned in the message of the exception)
    """
    pass

class DgtoolsErrorOutOfMemory(DgtoolsError):
    """
    Raised to signify that an operation has exhausted all available memory.
    """
    pass
    
    
class DgtoolsErrorASMSyntaxError(DgtoolsError):
    """
    Raised to signify a syntax error in the ASM code listing
    """
    pass
    
    
class DgtoolsErrorStack(DgtoolsError):
    """
    Base class to denote any stack related errors
    """
    pass
    
    
class DgtoolsErrorStackUnderflow(DgtoolsErrorStack):
    """
    Raised when a stack underflow error occurs.
    
    Note:
        * This exception can be raised by any stack (not only the program counter one).
    """
    pass
    

class DgtoolsErrorStackOverflow(DgtoolsErrorStack):
    """
    Raised when a stack overflow error occurs.
    
    Note:
        * This exception can be raised by any stack (not only the program counter one).
    """
    pass
