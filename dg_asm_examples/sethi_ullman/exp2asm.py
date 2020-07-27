"""
TODO: Can compile down to a single expression or an autonomous program. Better to do it down to an autonomous program.
"""
import pyparsing

def gen_code(current_expression):
    # Translate table
    ops_lookup = {"*":"MUL",
                  "/":"DIV",
                  "%":"MOD",
                  "+":"SUM",
                  "-":"SUB"}
    to_ret =[]  
    k = 0
    while k<len(current_expression):
        a_tok = current_expression[k]
        if type(a_tok) is str and a_tok in ops_lookup:
            to_ret.append(current_expression[k+1])
            to_ret.append(ops_lookup[current_expression[k]])
            k+=1
        else:
            to_ret.append(a_tok)
        k+=1
    to_ret_2 = []
    for a_tok in to_ret:
        if type(a_tok) is pyparsing.ParseResults:
            to_ret_2.extend(gen_code(a_tok))
        else:
            to_ret_2.append(a_tok)
    return to_ret_2
    
    
def get_parser():
    """
    Returns the numeric program parser.
    
    A numeric program is one or more assignment statements
    """
        
    literal_dec = pyparsing.Regex("[0-9]+").setParseAction(lambda s,loc,toks:int(toks[0]))
    literal_bin = pyparsing.Regex("0b[01]+").setParseAction(lambda s,loc,toks:int(toks[0][2:],2))
    literal_hex = pyparsing.Regex("0x[0-9A-F]+").setParseAction(lambda s,loc,toks:int(toks[0][2:],16))
    literal = literal_dec^literal_bin^literal_hex
    
    logic_exp = pyparsing.Forward()
    identifier = pyparsing.Regex("[a-zA-Z_][a-zA-Z0-9_]*")
    operand = literal^identifier
    numeric_exp = pyparsing.infixNotation(operand,[(pyparsing.oneOf('* / %'),2,pyparsing.opAssoc.LEFT), 
                                                   (pyparsing.oneOf('+ -'),2,pyparsing.opAssoc.LEFT)])
    assignment_statement = pyparsing.Group(identifier("idf") + "=" + numeric_exp("nexp"))("STATEMENT")
    numeric_program = pyparsing.OneOrMore(assignment_statement)
    # return numeric_program
    return numeric_exp
        
if __name__ == "__main__":    
    numeric_exp = get_parser()
    # exp_stack = [numeric_exp.parseString("(3*(4/(6+a)+b)+c)*(6*(2+a))")]
    exp_stack = [numeric_exp.parseString("2*a+4*b+6*j")]
    # exp_stack = [numeric_exp.parseString("a")]
    
    # Working on this
    # exp_stack = [numeric_exp.parseString("a=2 b=4 x=2 c=0 y=a*x*x+b*x+c")]
    
    v = gen_code(exp_stack)
    # while len(exp_stack):
        # current_exp = exp_stack.pop()
        # print(current_exp)
        # for a_tok in current_exp:
            # if type(a_tok) is pyparsing.ParseResults:
                # exp_stack.append(a_tok)
                
    # logic_exp << pyparsing.infixNotation(numeric_exp,[(pyparsing.oneOf('& | > < == <= >= ^'),2,pyparsing.opAssoc.LEFT), (pyparsing.oneOf('!'),1,pyparsing.opAssoc.RIGHT)])
    # expr = pyparsing.Forward()
    # operand = (literal|identifier)
    # factor = operand^pyparsing.Group(pyparsing.Suppress("(") + expr + pyparsing.Suppress(")"))
    # mul_term = pyparsing.Group(factor + pyparsing.ZeroOrMore("*" + factor))
    # div_term = pyparsing.Group(mul_term + pyparsing.ZeroOrMore("/" + mul_term))
    # add_term = pyparsing.Group(div_term + pyparsing.ZeroOrMore("+" + div_term))
    # sub_term = pyparsing.Group(add_term + pyparsing.ZeroOrMore("-" + add_term))
    # expr<<sub_term
