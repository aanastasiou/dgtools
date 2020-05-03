"""

:author: Athanasios Anastasiou
:date: May 2020
"""
from pygments.lexer import RegexLexer, words
from pygments.token import Keyword, Name, Number, Operator, Comment

from pygments import highlight
from pygments.formatters import HtmlFormatter

class DigiruleASMLexer(RegexLexer):
    name = 'DigiruleASM'
    aliases = ['dgasm']
    filenames = ['*.dsf']

    tokens = {
        'root': [
            (r'#.*?$', Comment),
            (words(("ADDLA", "ADDRA", "ADDRPC", "ANDLA", "ANDRA", "BCRSC", "BCRSS", "CALL", "CBR", "COPYAR", "COPYLA",
                    "COPYLR", "COPYRA", "COPYRR", "DECR", "DECRJZ", "HALT", "INCR", "INCRJZ", "JUMP", "NOP", "ORLA", 
                    "ORRA", "RETLA", "RETURN", "SBR", "SHIFTRL", "SHIFTRR", "SPEED", "SUBLA", "SUBRA", "XORLA", 
                    "XORRA"), suffix=r" ?"), Keyword.Reserved),
            (r'^[a-zA-Z_][a-zA-Z0-9_]*\:$', Name.Label),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name.Variable),
            (r'\.(DB|EQU) ?', Keyword.Declaration),
            (r' ?0b[0-1]{1,8},?', Number.Bin),
            (r' ?0x[0-9A-F]{1,2},?', Number.Hex),
            (r' ?[0-9]{1,3},?', Number.Integer),
            (r'=', Operator),          
        ]
    }
