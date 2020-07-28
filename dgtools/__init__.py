"""

Basic imports to make Digirule and DGB_Archive available to other programs.

:author: Athanasios Anastasiou
:date: May 2020
"""
from .digirule import Digirule, Digirule2U
from .dgb_archive import DGB_Archive
from .lexer import DigiruleASMLexer
from .assembler import DgAssembler
from .exceptions import (DgtoolsErrorSymbolUndefined, DgtoolsErrorSymbolAlreadyDefined, 
                         DgtoolsErrorOpcodeNotSupported, DgtoolsErrorDgbarchiveCorrupted, 
                         DgtoolsErrorDgbarchiveVersionIncompatible, DgtoolsErrorProgramHalt,
                         DgtoolsErrorOutOfMemory, DgtoolsErrorASMSyntaxError, DgtoolsErrorStackUnderflow, 
                         DgtoolsErrorStackOverflow)
from .output_render_html import Output_Render_HTML
from .callbacks import (DigiruleCallbackComOutStdout, DigiruleCallbackComOutStoreMem, 
                        DigiruleCallbackComInUserInteraction, DigiruleCallbackInputUserInteraction)
from .lexer import DigiruleASMLexer
                                
BUILTIN_MODELS = {"2A":Digirule, "2U":Digirule2U}
