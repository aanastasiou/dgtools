"""

Digirule assembler support.

:author: Athanasios Anastasiou
:date: June 2020
"""

from .digirule import Digirule
from .exceptions import DgtoolsErrorSymbolAlreadyDefined, DgtoolsErrorSymbolUndefined, DgtoolsErrorASMSyntaxError
import pyparsing
import functools

class DgAssembler:
    
    def __init__(self, digirule_cls):
        if not issubclass(digirule_cls, Digirule):
            raise TypeError(f"Expected Digirule, received {type(digirule_cls)}")
        
        # Action functions to convert valid string literals to numbers
        char2num = lambda toks:ord(toks[0][1:-1])
        uchar2num = lambda toks:int(toks[0])
        buchar2num = lambda toks:int(toks[0],2)
        xuchar2num = lambda toks:int(toks[0],16)
        # An identifier for labels and symbols. It must be at least 1 character, start with a letter or number and
        # can include the underscore.
        identifier = pyparsing.Regex(r"[a-zA-Z_][a-zA-Z0-9_]*")
        # A literal can be: 
        #    * An integer (4, -14,52), 
        #    * A binary number (0b100, 0b1110, 0b110100) 
        #    * A hexadecimal number (0x4, 0x0E, 0x34)
        #    * A single character ("A","J","8", anything from space to tilde on the ascii table). 
        literal_char = pyparsing.Regex(r"\"[ -~]\"|'[ -~]'").setParseAction(char2num)
        # TODO: LOW, Rename uchar, as it is not a uchar anymore. This is a remnant.
        literal_uchar = pyparsing.Regex(r"[-]?[0-9][0-9]?[0-9]?").setParseAction(uchar2num)
        literal_buchar = pyparsing.Regex(r"0b[0|1]+").setParseAction(buchar2num)
        literal_xuchar = pyparsing.Regex(r"0x[0-9A-F][0-9A-F]?").setParseAction(xuchar2num)
        literal = literal_char ^ literal_uchar ^ literal_buchar ^ literal_xuchar
        # Opcodes can accept literals or identifiers (.EQU or labels) as opcodes.
        literal_or_identifier = pyparsing.Group(literal("literal") ^ identifier("symbol"))("value_type")
        
        existing_defs = {"identifier":identifier,
                         "literal_char":literal_char,
                         "literal_uchar":literal_uchar,
                         "literal_buchar":literal_buchar,
                         "literal_xuchar":literal_xuchar,
                         "literal":literal,
                         "literal_or_identifier":literal_or_identifier}
        # Existing defs are passed down in case the digirule ASM code needs to specialise instructions
        asm_statement = digirule_cls.get_asm_statement_def(existing_defs)
        
        # Assembler directives
        # label: Defines a label
        dir_label = pyparsing.Group(identifier("idf") + pyparsing.Suppress(":"))("def_label")
        
        # .DB A static coma delimited list of byte defs
        dir_db_str = pyparsing.quotedString().setParseAction(lambda s,loc,tok:[ord(u) for u in tok[0][1:-1]])
        dir_db_values = pyparsing.delimitedList(pyparsing.Group(literal("literal") ^ \
                                                                identifier("symbol") ^ \
                                                                dir_db_str("string")))
        dir_db = pyparsing.Group(pyparsing.Regex(".DB")("cmd") + dir_db_values("values"))("def_db")
        
        # .EQU A "symbol" (that in the future would be able to evaluate to a proper macro.
        dir_equ = pyparsing.Group(pyparsing.Regex(".EQU")("cmd") + \
                                  identifier("idf") + \
                                  pyparsing.Suppress("=") + \
                                  literal("value"))("def_equ")
        # A directive statement
        dir_statement = pyparsing.Group(dir_label ^ dir_db ^ dir_equ)
        # Comments
        # A line of ASM code is either a comment or code with an optional inline comment
        prog_or_dir_statement = pyparsing.Group(asm_statement ^ dir_statement)("prog_dir_statement")
        dir_comment = pyparsing.Group(pyparsing.Suppress("#") + pyparsing.restOfLine("text"))("def_comment")
        dir_code_comment = pyparsing.Group(dir_comment ^ (prog_or_dir_statement + pyparsing.Optional(dir_comment)))
        program = pyparsing.OneOrMore(dir_code_comment)
        # In the end, ignore the comments.
        program.ignore(dir_comment)
        
        self._parser = program
        
    
    def text_to_ast(self, asm_code_text):
        try:
            parsed_code = self._parser.parseString(asm_code_text, parseAll=True)
        except pyparsing.ParseException as e:
            raise DgtoolsErrorASMSyntaxError(f"line {e.lineno}, col {e.col}: "
                                             f"    {e.line}: "
                                             f"Syntax Error: {e.args[2]}")
                                             
        return parsed_code

    
    def asm_ast_to_obj(self, parsed_code):
        """
        Transforms the parsed AST to a binary for the Digirule target architecture
        
        :param asm: Parsed ASM text, EXCLUDING COMMENT tags.
        :type asm: list<pyparsing.ParseElement>
        :returns: A dictionary of compiled code, symbols and variable offsets or the parsexception at failure
        :rtype: dict<"program":list<uint8>, "labels":dict<str, int>>, "symbols":dict<str,int>>, pyparsing.ParseException
        """
        mem = []
        labels = {}
        symbols = {}
        # Read through the code and load it to memory
        # While doing that, keep track of where labels and symbols appear. These will be substituted
        # in the second pass.
        for a_line in parsed_code:
            command, arguments = list(a_line["prog_dir_statement"][0].items())[0]
            if command == "def_label":
                # Tie the label to where it points to
                if arguments["idf"] not in labels:
                    labels[arguments["idf"]] = len(mem)
                else:
                    raise DgtoolsErrorSymbolAlreadyDefined(f"Label {arguments['idf']} is getting redefined.")
            elif command == "def_db":
                # .DB defines raw data that are simply dumped where they appear. If a label is not set to a 
                # data block, it cannot be referenced.
                #value_data = list(map(lambda x:x[0] if "string" not in x else [u for u in x],arguments["values"]))
                #import pdb
                #pdb.set_trace()
                #mem.extend(value_data)
                for a_val in arguments["values"]:
                    mem.extend(a_val)
            elif command == "def_equ":
                if arguments["idf"] not in symbols:
                    symbols[arguments["idf"]] = arguments["value"]
                else:
                    raise DgtoolsErrorSymbolAlreadyDefined(f"Symbol {arguments['idf']} is getting redefined")
            else:
                # It's an instruction. The opcode of the instruction has already been recognised, 
                # but we need to grab the operands wherever they are available
                inst_data = command.split(":")
                instruction_code = int(inst_data[0])
                instruction_num_op = int(inst_data[1])
                            
                mem.append(instruction_code)
                mem.extend(list(map(lambda x:x[0], arguments[1:(1+instruction_num_op)]))) 
        # The first pass produces an intermediate object that still contains symbolic references.
        # This second pass here substitutes those references and produces the final object.
        symbol_offsets = {}
        subst_entries = filter(lambda x:type(x[1]) is str, enumerate(mem))
        for an_entry in subst_entries:
            if an_entry[1] in labels:
                mem[an_entry[0]] = labels[an_entry[1]]
            elif an_entry[1] in symbols:
                # Note where the symbol is used
                if an_entry[1] not in symbol_offsets:
                    symbol_offsets[an_entry[1]] = []
                if an_entry[0] not in symbol_offsets[an_entry[1]]:
                    symbol_offsets[an_entry[1]].append(an_entry[0])
                # Make the substitution
                mem[an_entry[0]] = symbols[an_entry[1]]
            else:
                raise DgtoolsErrorSymbolUndefined(f"Symbol {an_entry[1]} not found.")
        return {"program":mem, "labels":labels}
