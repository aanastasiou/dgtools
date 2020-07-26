import pyparsing

if __name__ == "__main__":
    nodes = {}
    edges = []
    
    literal_dec = pyparsing.Regex("[0-9]+").setParseAction(lambda s,loc,toks:int(toks[0]))
    literal_bin = pyparsing.Regex("0b[01]+").setParseAction(lambda s,loc,toks:int(toks[0][2:],2))
    literal_hex = pyparsing.Regex("0x[0-9A-F]+").setParseAction(lambda s,loc,toks:int(toks[0][2:],16))
    literal = literal_dec^literal_bin^literal_hex
    
    logic_exp = pyparsing.Forward()
    identifier = pyparsing.Regex("[a-zA-Z_][a-zA-Z0-9_]*")("id")
    operand = literal^identifier
    numeric_exp = pyparsing.infixNotation(operand,[(pyparsing.oneOf('* / %'),2,pyparsing.opAssoc.LEFT), (pyparsing.oneOf('+ -'),2,pyparsing.opAssoc.LEFT)])

    # logic_exp << pyparsing.infixNotation(numeric_exp,[(pyparsing.oneOf('& | > < == <= >= ^'),2,pyparsing.opAssoc.LEFT), (pyparsing.oneOf('!'),1,pyparsing.opAssoc.RIGHT)])
    # expr = pyparsing.Forward()
    # operand = (literal|identifier)
    # factor = operand^pyparsing.Group(pyparsing.Suppress("(") + expr + pyparsing.Suppress(")"))
    # mul_term = pyparsing.Group(factor + pyparsing.ZeroOrMore("*" + factor))
    # div_term = pyparsing.Group(mul_term + pyparsing.ZeroOrMore("/" + mul_term))
    # add_term = pyparsing.Group(div_term + pyparsing.ZeroOrMore("+" + div_term))
    # sub_term = pyparsing.Group(add_term + pyparsing.ZeroOrMore("-" + add_term))
    # expr<<sub_term
    
    
