#!/usr/bin/env python
import pyparsing
import random
import click
import sys
import os
import functools

def get_superstack_parser():
    """
    Returns the complete brainfuck parser --> Digirule ASM.
    """
    def _get_label_tag(tag_chars="0123456789", N=12):
        return "".join([tag_chars[random.randint(0,len(tag_chars)-1)] for n in range(N)])
        
    def _push_literal(s, loc, toks):
        try:
            num = int(toks[0][0]) & 0xFF
        except ValueError:
            pass
        return {"statements":f"COPYLR {num} head_val\nCALL f_push\n", "dependencies":set()}
        
    def _add(s, loc, toks):
        return {"statements":"CALL f_pop\nCOPYRR head_val head_val_1\nCALL f_pop\nCOPYRA head_val_1\nCBR carry_bit status_reg\nADDRA head_val\nCOPYAR head_val\nCALL f_push\n",
                "dependencies":set()}
    
    def _sub(s, loc, toks):
        return {"statements":"CALL f_pop\nCOPYRR head_val head_val_1\nCALL f_pop\nCOPYRA head_val_1\nCBR carry_bit status_reg\nSUBRA head_val\nCOPYAR head_val\nCALL f_push\n",
                "dependencies":set()}

    def _mul(s, loc, toks):
        return {"statements":"CALL f_pop\nCOPYRR head_val head_val_1\nCALL f_pop\nMUL head_val head_val_1\nCALL f_push\n",
                "dependencies":set()}

    def _div(s, loc, toks):
        return {"statements":"CALL f_pop\nCOPYRR head_val head_val_1\nCALL f_pop\nDIV head_val head_val_1\nCALL f_push\n",
                "dependencies":set()}

    def _mod(s, loc, toks):
        return {"statements":"CALL f_pop\nCOPYRR head_val head_val_1\nCALL f_pop\nDIV head_val head_val_1\nCOPYAR head_val\nCALL f_push\n",
                "dependencies":set()}

    def _random(s, loc, toks):
        return {"statements":"CALL f_rand\nCALL f_push\n",
                "dependencies":{"f_rand"}}

    def _and(s, loc, toks):
        return {"statements":"CALL f_pop\nCOPYRR head_val head_val_1\nCALL f_pop\nCOPYRA head_val_1\nANDRA head_val\nCOPYAR head_val\nCALL f_push\n",
                "dependencies":set()}

    def _or(s, loc, toks):
        return {"statements":"CALL f_pop\nCOPYRR head_val head_val_1\nCALL f_pop\nCOPYRA head_val_1\nORRA head_val\nCOPYAR head_val\nCALL f_push\n",
                "dependencies":set()}

    def _xor(s, loc, toks):
        return {"statements":"CALL f_pop\nCOPYRR head_val head_val_1\nCALL f_pop\nCOPYRA head_val_1\nXORRA head_val\nCOPYAR head_val\nCALL f_push\n",
                "dependencies":set()}

    def _output(s, loc, toks):
        return {"statements":"CALL f_pop\nCOPYRR head_val out_dev\n",
                "dependencies":set()}

    def _input(s, loc, toks):
        return {"statements":"COPYRR in_dev head_val\nCALL f_push\n",
                "dependencies":set()}

    def _inputascii(s, loc, toks):
        return {"statements": "COMIN\nCOPYAR head_val\nCALL f_push\n",
                "dependencies": set()}

    def _outputascii(s, loc, toks):
        return {"statements": "CALL f_pop\nCOPYRA head_val\nCOMOUT\n",
                "dependencies": set()}

    def _pop(s, loc, toks):
        return {"statements": "CALL f_pop\n",
                "dependencies": set()}

    def _swap(s, loc, toks):
        return {"statements": "CALL f_pop\nCOPYRR head_val head_val_1\nCALL f_pop\nSWAPRR head_val head_val_1\nCALL f_push\nCOPYRR head_val_1 head_val\nCALL f_push\n",
                "dependencies": set()}

    def _dup(s, loc, toks):
        return {"statements": "CALL f_pop\nCALL f_push\nCALL f_push\n",
                "dependencies": set()}

    def _rev(s, loc, toks):
        return {"statements": "CALL f_rev\n", 
                "dependencies": {"f_rev"}}

    def _quit(s, loc, toks):
        return {"statements":"HALT\n",
                "dependencies": set()}
        
    def _iteration_block(s, loc, toks):
        label_tag = _get_label_tag()
        return {"statements":f"label_{label_tag}:\nCALL f_peek\nCOPYRA head_val_1\nBCRSC zero_bit status_reg\nJUMP label_continue_{label_tag}\n{''.join([s['statements'] for s in toks[0][1:-1]])}\nJUMP label_{label_tag}\nlabel_continue_{label_tag}:\n", 
                "dependencies":functools.reduce(lambda x,y:x.union(y["dependencies"]), toks[0][1:-1], set()).union({"f_peek"})}

    def _cycle(s, loc, toks):
        return {"statements": f"DECR head_ptr\nCOPYRR head_ptr head_val\nCOPYLR stack head_val_1\nCOPYLR 10 f_custom_ins\nCALL f_custom_ins\nINCR head_ptr\n",
                "dependencies": set()}

    def _rcycle(s, loc, toks):
        return {"statements": f"DECR head_ptr\nCOPYRR head_ptr head_val_1\nCOPYLR stack head_val\nCOPYLR 10 f_custom_ins\nCALL f_custom_ins\nINCR head_ptr\n",
                "dependencies": set()}
        
    def _emit_asm(s, loc, toks):
        precode = ".EQU status_reg=252\n.EQU in_dev=253\n.EQU out_dev=255\n.EQU zero_bit=0\n.EQU carry_bit=1\nCOPYLR stack head_ptr\nstart_program:\n"
        # postcode = "f_push:\nCOPYRI head_val head_ptr\nINCR head_ptr\nRETURN\n\nf_pop:\nDECR head_ptr\nCOPYIR head_ptr head_val\nRETURN\n\nf_custom_ins:\n.DB 0\nhead_val:\n.DB 0\nhead_val_1:\n.DB 0\nRETURN\nhead_ptr:\n.DB 0\nstack:\n.DB 0\n"
        postcode = "f_push:\nCOPYRA head_ptr\nSUBLA 253\nBCRSC zero_bit status_reg\nJUMP f_stack_error\nCOPYRI head_val head_ptr\nINCR head_ptr\nRETURN\n\nf_pop:\nCOPYRA head_ptr\nCBR carry_bit status_reg\nSUBLA stack\nBCRSC zero_bit status_reg\nJUMP f_stack_error\nDECR head_ptr\nCOPYIR head_ptr head_val\nRETURN\n\nf_stack_error:\nCOPYLR 0xFF out_dev\nJUMP f_stack_error\nf_custom_ins:\n.DB 0\nhead_val:\n.DB 0\nhead_val_1:\n.DB 0\nRETURN\nhead_ptr:\n.DB 0\nstack:\n.DB 0\n"
        deps_code = {"f_rand": "f_rand:\nRANDA\nCOPYAR head_val_1\nCOPYRA head_val\nCBR carry_bit status_reg\nSUBRA head_val_1\nBCRSC carry_bit status_reg\nJUMP f_rand\nCOPYRR head_val_1 head_val\nRETURN\n", 
                     "f_rev":"f_rev:\nCOPYRA head_ptr\nSUBLA stack\nSWAPRA head_ptr\nCBR carry_bit status_reg\nSHIFTRR head_ptr\nSWAPRA head_ptr\nCOPYRR head_ptr head_val\nDECR head_val\nCOPYLR stack head_val_1\nCOPYLR 16 f_custom_ins\nswap_again:\nCALL f_custom_ins\nCBR carry_bit status_reg\nSUBLA 1\nBCRSS zero_bit status_reg\nJUMP f_rev_adjust_and_loop\nRETURN\nf_rev_adjust_and_loop:\nDECR head_val\nINCR head_val_1\nJUMP swap_again\n",
                     "f_peek":"f_peek:\nDECR head_ptr\nCOPYIR head_ptr head_val_1\nINCR head_ptr\nRETURN\n"}
        # Collect dependencies and leave just compiled code
        deps = set()
        for a_tok in toks:
            deps = deps.union(a_tok["dependencies"])
                
        return precode + \
               f"{''.join([m['statements'] for m in toks])}" +\
               "HALT\n" + \
               "".join([deps_code[k] for k in deps])+ \
               postcode
        
    sust_literal = pyparsing.Group(pyparsing.Regex("[0-9]+"))("LITERAL").setParseAction(_push_literal)
    sust_add = pyparsing.Group(pyparsing.Regex("[Aa][Dd][Dd]"))("ADD").setParseAction(_add)
    sust_sub = pyparsing.Group(pyparsing.Regex("[Ss][Uu][Bb]"))("SUB").setParseAction(_sub)
    sust_mul = pyparsing.Group(pyparsing.Regex("[Mm][Uu][Ll]"))("MUL").setParseAction(_mul)
    sust_div = pyparsing.Group(pyparsing.Regex("[Dd][Ii][Vv]"))("DIV").setParseAction(_div)
    sust_mod = pyparsing.Group(pyparsing.Regex("[Mm][Oo][Dd]"))("MOD").setParseAction(_mod)
    sust_random = pyparsing.Group(pyparsing.Regex("[Rr][Aa][Nn][Dd][Oo][Mm]"))("RANDOM").setParseAction(_random)
    sust_and = pyparsing.Group(pyparsing.Regex("[Aa][Nn][Dd]"))("AND").setParseAction(_and)
    sust_or = pyparsing.Group(pyparsing.Regex("[Oo][Rr]"))("OR").setParseAction(_or)
    sust_xor = pyparsing.Group(pyparsing.Regex("[Xx][Oo][Rr]"))("XOR").setParseAction(_xor)
    sust_nand = pyparsing.Group(pyparsing.Regex("[Nn][Aa][Nn][Dd]"))("NAND")
    sust_not = pyparsing.Group(pyparsing.Regex("[Nn][Oo][Tt]"))("NOT")
    sust_output = pyparsing.Group(pyparsing.Regex("[Oo][Uu][Tt][Pp][Uu][Tt]"))("OUTPUT").setParseAction(_output)
    sust_input = pyparsing.Group(pyparsing.Regex("[Ii][Nn][Pp][Uu][Tt]"))("INPUT").setParseAction(_input)
    sust_outputascii = pyparsing.Group(pyparsing.Regex("[Oo][Uu][Tt][Pp][Uu][Tt][Aa][Ss][Cc][Ii][Ii]"))("OUTPUT_ASCII").setParseAction(_outputascii)
    sust_inputascii = pyparsing.Group(pyparsing.Regex("[Ii][Nn][Pp][Uu][Tt][Aa][Ss][Cc][Ii][Ii]"))("INPUT_ASCII").setParseAction(_inputascii)
    sust_pop = pyparsing.Group(pyparsing.Regex("[Pp][Oo][Pp]"))("POP").setParseAction(_pop)
    sust_swap = pyparsing.Group(pyparsing.Regex("[Ss][Ww][Aa][Pp]"))("SWAP").setParseAction(_swap)
    sust_cycle = pyparsing.Group(pyparsing.Regex("[Cc][Yy][Cc][Ll][Ee]"))("CYCLE").setParseAction(_cycle)
    sust_rcycle = pyparsing.Group(pyparsing.Regex("[Rr][Cc][Yy][Cc][Ll][Ee]"))("RCYCLE").setParseAction(_rcycle)
    sust_dup = pyparsing.Group(pyparsing.Regex("[Dd][Uu][Pp]"))("DUP").setParseAction(_dup)
    sust_rev = pyparsing.Group(pyparsing.Regex("[Rr][Ee][Vv]"))("REV").setParseAction(_rev)
    sust_quit = pyparsing.Group(pyparsing.Regex("[Qq][Uu][Ii][Tt]"))("QUIT").setParseAction(_quit)
    sust_debug = pyparsing.Group(pyparsing.Regex("[Dd][Ee][Bb][Uu][Gg]"))("DEBUG")
    sust_statement = pyparsing.Forward()
    sust_if_block = pyparsing.Group(pyparsing.Regex("[Ii][Ff]")+pyparsing.ZeroOrMore(sust_statement)+pyparsing.Regex("[Ff][Ii]")).setParseAction(_iteration_block)
    sust_statement << (sust_literal ^ sust_add ^ sust_sub ^ sust_mul ^ sust_div ^ sust_mod ^ sust_random ^ sust_and ^
                       sust_or ^ sust_xor ^ sust_nand ^ sust_not ^ sust_output ^ sust_input ^ sust_outputascii ^
                       sust_inputascii ^ sust_pop ^ sust_swap ^ sust_cycle ^ sust_rcycle ^ sust_dup ^ sust_rev ^  
                       sust_quit ^ sust_debug ^ sust_if_block)
    sust_program = pyparsing.OneOrMore(sust_statement).setParseAction(_emit_asm)
    sust_program.ignore(sust_debug)
    return sust_program
    
    
@click.command()
@click.argument("input_file", type=click.File("rt"))
def main(input_file):
    sust2asm_parser = get_superstack_parser()
    try:
        # parsed_pro = sust2asm_parser.parseString(input_file.read(), parseAll=True)
        dg_asm_text = sust2asm_parser.parseString(input_file.read(), parseAll=True)
        sys.stdout.write(dg_asm_text[0])
    except pyparsing.ParseException as pe:
        print(str(pe))
        sys.exit(-1)

if __name__ == "__main__":
    main()
