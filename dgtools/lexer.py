"""

:author: Athanasios Anastasiou
:date: May 2020
"""
from pygments.lexer import RegexLexer, words
from pygments.token import Keyword, Name, Number, Operator, Comment, Punctuation

from pygments import highlight
from pygments.formatters import HtmlFormatter

class DigiruleASMLexer(RegexLexer):
    name = 'DigiruleASM'
    aliases = ['dgasm']
    filenames = ['*.dsf']

    tokens = {
        'root': [
            (r'#.*?$', Comment),
            (words(("HALT", "NOP", "SPEED", "INITSP", "COPYLA", "COPYLR", "COPYLI", "COPYAR", "COPYAI", "COPYRA", 
                    "COPYRR", "COPYRI", "COPYIA", "COPYIR", "COPYII", "SWAPRA", "SWAPRR", "ADDLA", "ADDRA", "SUBLA", 
                    "SUBRA", "MUL", "DIV", "ANDLA", "ANDRA", "ORLA", "ORRA", "XORLA", "XORRA", "DECR", "INCR", 
                    "DECRJZ", "INCRJZ", "SHIFTRL", "SHIFTRR", "CBR", "SBR", "BCRSC", "BCRSS", "JUMP", "JUMPI", "CALL", 
                    "CALLI", "RETURN", "RETLA", "ADDRPC", "RANDA", "COMOUT", "COMIN", 
                    "COMRDY","BCLR","BSET","BCHG", "PINOUT", "PININ", "PINDIR","BTSTSC", "BTSTSS"), suffix=r" ?"), 
             Keyword.Reserved),
            (r'^[a-zA-Z_][a-zA-Z0-9_]*\:$', Name.Label),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name.Variable),
            (r'\.(DB|EQU) ?', Keyword.Declaration),
            (r' ?0b[0-1]{1,8}', Number.Bin),
            (r' ?0x[0-9A-F]{1,2}', Number.Hex),
            (r' ?[0-9]{1,3}', Number.Integer),
            (r'=', Operator),
            (r'[ ,]', Punctuation),          
        ]
    }
