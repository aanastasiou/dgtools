#!/usr/bin/env python
import pyparsing
import random
import click
import sys
import os

def get_superstack_parser():
    """
    Returns the complete brainfuck parser --> Digirule ASM.
    """
    # def _get_label_tag(tag_chars="0123456789", N=12):
        # return "".join([tag_chars[random.randint(0,len(tag_chars)-1)] for n in range(N)])
        
    # def inc_dp(s, loc, toks):
        # reps = len(toks[0][0])
        # if reps>1:
            # return f"COPYRA dp\nADDLA {reps}\nCOPYAR dp\n" 
        # else:
            # return f"INCR dp\n"
    
    # def dec_dp(s, loc, toks):
        # reps = len(toks[0][0])
        # if reps>1:
            # return f"COPYRA dp\nSUBLA {reps}\nCOPYAR dp\n" 
        # else:
            # return f"DECR dp\n"
            
    # def inc_dv(s, loc, toks):
        # return f"COPYIA dp\nADDLA {len(toks[0][0])}\nCOPYAI dp\n" 
        
    # def dec_dv(s, loc, toks):
        # return f"COPYIA dp\nSUBLA {len(toks[0][0])}\nCOPYAI dp\n"        
    
    # def out_dv(s, loc, toks):
        # return f"COPYIR dp out_dev\n"
                
    # def in_dv(s, loc, toks):
        # return f"COPYRI in_dev dp\n"
        
    # def iteration_block(s, loc, toks):
        # label_tag = _get_label_tag()
        # return f"label_{label_tag}:\n{''.join(toks[0][1:-1])}COPYIA dp\nBCRSS zero_bit status_reg\nJUMP label_{label_tag}\n"
        
    # def emit_asm(s, loc, toks):
        # return f".EQU status_reg=252\n.EQU in_dev=253\n.EQU out_dev=255\n.EQU zero_bit=0\nCOPYLR tape dp\nstart_program:\n" \
               # f"{''.join([m for m in toks])}HALT\ndp:\n.DB 0\ntape:\n.DB 0"
        
    sust_literal = pyparsing.Group(pyparsing.Regex("[0-9]+"))("LITERAL")
    sust_add = pyparsing.Group(pyparsing.Regex("[Aa][Dd][Dd]"))("ADD")
    sust_sub = pyparsing.Group(pyparsing.Regex("[Ss][Uu][Bb]"))("SUB")
    sust_mul = pyparsing.Group(pyparsing.Regex("[Mm][Uu][Ll]"))("MUL")
    sust_div = pyparsing.Group(pyparsing.Regex("[Dd][Ii][Vv]"))("DIV")
    sust_mod = pyparsing.Group(pyparsing.Regex("[Mm][Oo][Dd]"))("MOD")
    sust_random = pyparsing.Group(pyparsing.Regex("[Rr][Aa][Nn][Dd][Oo][Mm]"))("RANDOM")
    sust_and = pyparsing.Group(pyparsing.Regex("[Aa][Nn][Dd]"))("AND")
    sust_or = pyparsing.Group(pyparsing.Regex("[Oo][Rr]"))("OR")
    sust_xor = pyparsing.Group(pyparsing.Regex("[Xx][Oo][Rr]"))("XOR")
    sust_nand = pyparsing.Group(pyparsing.Regex("[Nn][Aa][Nn][Dd]"))("NAND")
    sust_not = pyparsing.Group(pyparsing.Regex("[Nn][Oo][Tt]"))("NOT")
    sust_output = pyparsing.Group(pyparsing.Regex("[Oo][Uu][Tt][Pp][Uu][Tt]"))("OUTPUT")
    sust_input = pyparsing.Group(pyparsing.Regex("[Ii][Nn][Pp][Uu][Tt]"))("INPUT")
    sust_outputascii = pyparsing.Group(pyparsing.Regex("[Oo][Uu][Tt][Pp][Uu][Tt][Aa][Ss][Cc][Ii]"))("OUTPUT_ASCII")
    sust_inputascii = pyparsing.Group(pyparsing.Regex("[Ii][Nn][Pp][Uu][Tt][Aa][Ss][Cc][Ii]"))("INPUT_ASCII")
    sust_pop = pyparsing.Group(pyparsing.Regex("[Pp][Oo][Pp]"))("POP")
    sust_swap = pyparsing.Group(pyparsing.Regex("[Ss][Ww][Aa][Pp]"))("SWAP")
    sust_cycle = pyparsing.Group(pyparsing.Regex("[Cc][Yy][Cc][Ll][Ee]"))("CYCLE")
    sust_rcycle = pyparsing.Group(pyparsing.Regex("[Rr][Cc][Yy][Cc][Ll][Ee]"))("RCYCLE")
    sust_dup = pyparsing.Group(pyparsing.Regex("[Dd][Uu][Pp]"))("DUP")
    sust_rev = pyparsing.Group(pyparsing.Regex("[Rr][Ee][Vv]"))("REV")
    sust_quit = pyparsing.Group(pyparsing.Regex("[Qq][Uu][Ii][Tt]"))("QUIT")
    sust_debug = pyparsing.Group(pyparsing.Regex("[Dd][Ee][Bb][Uu][Gg]"))("DEBUG")
    sust_statement = pyparsing.Forward()
    sust_if_block = pyparsing.Group(pyparsing.Regex("[Ii][Ff]")+pyparsing.ZeroOrMore(sust_statement)+pyparsing.Regex("[Ff][Ii]"))
    sust_statement << (sust_literal ^ sust_add ^ sust_sub ^ sust_mul ^ sust_div ^ sust_mod ^ sust_random ^ sust_and ^
                       sust_or ^ sust_xor ^ sust_nand ^ sust_not ^ sust_output ^ sust_input ^ sust_outputascii ^
                       sust_inputascii ^ sust_pop ^ sust_swap ^ sust_cycle ^ sust_rcycle ^ sust_dup ^ sust_rev ^  
                       sust_quit ^ sust_debug ^ sust_if_block)
    sust_program = pyparsing.OneOrMore(sust_statement)
    return sust_program
    
    
@click.command()
@click.argument("input_file", type=click.File("rt"))
def main(input_file):
    sust2asm_parser = get_superstack_parser()
    try:
        parsed_pro = sust2asm_parser.parseString(input_file.read(), parseAll=True)
        # dg_asm_text = bf2asm_parser.parseString(input_file.read(), parseAll=True)
        # sys.stdout.write(dg_asm_text[0])
    except pyparsing.ParseException as pe:
        print(str(pe))
        sys.exit(-1)

if __name__ == "__main__":
    main()
