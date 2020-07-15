import pyparsing

def get_bf_parser():
    bf_inc_data_p = pyparsing.Group(pyparsing.Suppress(">"))("INC_DP")
    bf_dec_data_p = pyparsing.Group(pyparsing.Suppress("<"))("DEC_DP")
    bf_inc_data_v = pyparsing.Group(pyparsing.Suppress("+"))("INC_DV")
    bf_dec_data_v = pyparsing.Group(pyparsing.Suppress("-"))("DEC_DV")
    bf_output = pyparsing.Group(pyparsing.Suppress("."))("OUT_DV")
    bf_input = pyparsing.Group(pyparsing.Suppress(","))("IN_DV")
    bf_jz = pyparsing.Group(pyparsing.Suppress("["))("JZ")
    bf_jnz = pyparsing.Group(pyparsing.Suppress("]"))("JNZ")
    bf_statement = pyparsing.Forward()
    bf_statement << (bf_inc_data_p ^ bf_dec_data_p ^ bf_inc_data_v ^ bf_dec_data_v ^ bf_output ^ bf_input ^  \
                    pyparsing.Group(bf_jz + pyparsing.ZeroOrMore(bf_statement) + bf_jnz)("BLOCK"))
    bf_program = pyparsing.OneOrMore(bf_statement)
    return bf_program
    
if __name__ == "__main__":
    program = "+>>+++++++++[<<[>++<-]>[<+>-]>-]<<"
    z = get_bf_parser()
    v = z.parseString(program)
    
