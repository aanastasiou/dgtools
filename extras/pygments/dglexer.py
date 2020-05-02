from pygments.lexer import RegexLexer, words
from pygments.token import *

# from pygments.lexers import load_lexer_from_file
from pygments import highlight
from pygments.formatters import HtmlFormatter
import sys

class CustomLexer(RegexLexer):
    name = 'DigiruleASM'
    aliases = ['dgasm']
    filenames = ['*.dsf']

    tokens = {
        'root': [
            (r'#.*?$', Comment),
            (words(("COPYLA","ADDLA"), suffix=r"\b"), Keyword)
        ]
    }

if __name__ == "__main__":
    with open("testdgasm.dsf", "rt") as df:
        sys.stdout.write(highlight(df.read(), CustomLexer(), HtmlFormatter()))
    
