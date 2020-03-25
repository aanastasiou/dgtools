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
