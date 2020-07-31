#!/usr/bin/env python
import pyparsing
import random
import click
import sys
import os

def get_bf_parser():
    """
    Returns the complete brainfuck parser --> Digirule ASM.
    """
    def _get_label_tag(tag_chars="0123456789", N=12):
        return "".join([tag_chars[random.randint(0,len(tag_chars)-1)] for n in range(N)])
        
    def inc_dp(s, loc, toks):
        reps = len(toks[0][0])
        if reps>1:
            return f"COPYRA dp\nADDLA {reps}\nCOPYAR dp\n" 
        else:
            return f"INCR dp\n"
    
    def dec_dp(s, loc, toks):
        reps = len(toks[0][0])
        if reps>1:
            return f"COPYRA dp\nSUBLA {reps}\nCOPYAR dp\n" 
        else:
            return f"DECR dp\n"
            
    def inc_dv(s, loc, toks):
        reps = len(toks[0][0])
        if reps>1:
            return f"COPYIA dp\nADDLA {reps}\nCOPYAI dp\n" 
        else:
            return f"COPYLR 30 handle_dv_i\nCALL handle_dv_i\n"
            
    def dec_dv(s, loc, toks):
        reps = len(toks)
        if reps>1:
            return f"COPYIA dp\nSUBLA {len(toks[0][0])}\nCOPYAI dp\n"        
        else:
            return f"COPYLR 29 handle_dv_i\nCALL handle_dv_i\n"
            
    def out_dv(s, loc, toks):
        return f"COPYIR dp out_dev\n"
                
    def in_dv(s, loc, toks):
        return f"COPYRI in_dev dp\n"
        
    def iteration_block(s, loc, toks):
        label_tag = _get_label_tag()
        #return f"label_{label_tag}:\n{''.join(toks[0][1:-1])}COPYIA dp\nBCRSS zero_bit status_reg\nJUMP label_{label_tag}\n"
        return f"label_{label_tag}:\nCOPYIA dp\nBCRSC zero_bit status_reg\nJUMP label_continue_{label_tag}\n{''.join(toks[0][1:-1])}JUMP label_{label_tag}\nlabel_continue_{label_tag}:\n"
        
    def emit_asm(s, loc, toks):
        return f".EQU status_reg=252\n.EQU in_dev=253\n.EQU out_dev=255\n.EQU zero_bit=0\nCOPYLR tape dp\nstart_program:\n" \
               f"{''.join([m for m in toks])}HALT\nhandle_dv_i:\n.DB 0\ndp:\n.DB 0\nRETURN\ntape:\n.DB 0"
        
    bf_inc_data_p = pyparsing.Group(pyparsing.Regex("[>]+"))("INC_DP").setParseAction(inc_dp)
    bf_dec_data_p = pyparsing.Group(pyparsing.Regex("[<]+"))("DEC_DP").setParseAction(dec_dp)
    bf_inc_data_v = pyparsing.Group(pyparsing.Regex("[+]+"))("INC_DV").setParseAction(inc_dv)
    bf_dec_data_v = pyparsing.Group(pyparsing.Regex("[-]+"))("DEC_DV").setParseAction(dec_dv)
    bf_output = pyparsing.Group(pyparsing.Suppress("."))("OUT_DV").setParseAction(out_dv)
    bf_input = pyparsing.Group(pyparsing.Suppress(","))("IN_DV").setParseAction(in_dv)
    bf_jz = pyparsing.Group(pyparsing.Suppress("["))("JZ")
    bf_jnz = pyparsing.Group(pyparsing.Suppress("]"))("JNZ")
    bf_statement = pyparsing.Forward()
    bf_statement << (bf_inc_data_p ^ bf_dec_data_p ^ bf_inc_data_v ^ bf_dec_data_v ^ bf_output ^ bf_input ^  \
                    pyparsing.Group(bf_jz + pyparsing.ZeroOrMore(bf_statement) + bf_jnz)("ITERATION").setParseAction(iteration_block))
    bf_program = pyparsing.OneOrMore(bf_statement).setParseAction(emit_asm)
    return bf_program
    
    
@click.command()
@click.argument("input_file", type=click.File("rt"))
def main(input_file):
    bf2asm_parser = get_bf_parser()
    try:
        dg_asm_text = bf2asm_parser.parseString(input_file.read(), parseAll=True)
        sys.stdout.write(dg_asm_text[0])
    except pyparsing.ParseException as pe:
        print(str(pe))
        sys.exit(-1)

if __name__ == "__main__":
    main()
    # program = "+>>+++++++++[<<[>++<-]>[<+>-]>-]<<"
    
        
    
