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
                         DgtoolsErrorASMSyntaxError, DgtoolsErrorStackUnderflow, DgtoolsErrorStackOverflow)
from .output_render_html import Output_Render_HTML
from .callbacks import (DigiruleCallbackComOutStdout, DigiruleCallbackComOutStoreMem, 
                        DigiruleCallbackComInUserInteraction, DigiruleCallbackInputUserInteraction)
from .lexer import DigiruleASMLexer
from .digirule_visualise import *
from .simulator import *
                                


BUILTIN_MODELS = {"2A":{"machine_cls":Digirule, "machine_vis":DgVisualiseDigirule2A},  
                  "2U":{"machine_cls":Digirule2U, "machine_vis":DgVisualiseDigirule2U}}
