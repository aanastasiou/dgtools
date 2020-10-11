"""
Preliminary tests with the Kenback

Sept 2020
"""

import pyparsing

def get_parser():
    lit_num = pyparsing.Regex("[+-]?[0-9]+")
    idf = pyparsing.Regex("[a-zA-Z_][a-zA-Z_0-9]+")
    
    lit_value = lit_num ^ idf
    mem_value = pyparsing.Suppress("[") + lit_value + pyparsing.Suppress("]")
    idc_value = pyparsing.Suppress("@[") + lit_value + pyparsing.Suppress("]")
    idx_value = pyparsing.Suppress("X[") + lit_value + pyparsing.Suppress("]")
    idcx_value = pyparsing.Suppress("@X[") + lit_value + pyparsing.Suppress("]")
    
    ins_halt = pyparsing.Group(pyparsing.Regex("HALT"))("0:1")
    ins_noop = pyparsing.Group(pyparsing.Regex("NOOP"))("127:1")
    # ADD
    ins_add_a_im = pyparsing.Group(pyparsing.Regex("ADD A") + lit_value)("3:1")
    ins_add_a_me = pyparsing.Group(pyparsing.Regex("ADD A") + mem_value)("4:1")
    ins_add_a_id = pyparsing.Group(pyparsing.Regex("ADD A") + idc_value)("5:1")
    ins_add_a_ix = pyparsing.Group(pyparsing.Regex("ADD A") + idx_value)("6:1")
    ins_add_a_idx = pyparsing.Group(pyparsing.Regex("ADD A") + idcx_value)("7:1")

    ins_add_b_im = pyparsing.Group(pyparsing.Regex("ADD B") + lit_value)("67:1")
    ins_add_b_me = pyparsing.Group(pyparsing.Regex("ADD B") + mem_value)("68:1")
    ins_add_b_id = pyparsing.Group(pyparsing.Regex("ADD B") + idc_value)("69:1")
    ins_add_b_ix = pyparsing.Group(pyparsing.Regex("ADD B") + idx_value)("70:1")
    ins_add_b_idx = pyparsing.Group(pyparsing.Regex("ADD B") + idcx_value)("71:1")

    ins_add_x_im = pyparsing.Group(pyparsing.Regex("ADD X") + lit_value)("131:1")
    ins_add_x_me = pyparsing.Group(pyparsing.Regex("ADD X") + mem_value)("132:1")
    ins_add_x_id = pyparsing.Group(pyparsing.Regex("ADD X") + idc_value)("133:1")
    ins_add_x_ix = pyparsing.Group(pyparsing.Regex("ADD X") + idx_value)("134:1")
    ins_add_x_idx = pyparsing.Group(pyparsing.Regex("ADD X") + idcx_value)("135:1")
    # SUB
    ins_sub_a_im = pyparsing.Group(pyparsing.Regex("SUB A") + lit_value)("11:1")
    ins_sub_a_me = pyparsing.Group(pyparsing.Regex("SUB A") + mem_value)("12:1")
    ins_sub_a_id = pyparsing.Group(pyparsing.Regex("SUB A") + idc_value)("13:1")
    ins_sub_a_ix = pyparsing.Group(pyparsing.Regex("SUB A") + idx_value)("14:1")
    ins_sub_a_idx = pyparsing.Group(pyparsing.Regex("SUB A") + idcx_value)("15:1")

    ins_sub_b_im = pyparsing.Group(pyparsing.Regex("SUB B") + lit_value)("75:1")
    ins_sub_b_me = pyparsing.Group(pyparsing.Regex("SUB B") + mem_value)("76:1")
    ins_sub_b_id = pyparsing.Group(pyparsing.Regex("SUB B") + idc_value)("77:1")
    ins_sub_b_ix = pyparsing.Group(pyparsing.Regex("SUB B") + idx_value)("78:1")
    ins_sub_b_idx = pyparsing.Group(pyparsing.Regex("SUB B") + idcx_value)("79:1")

    ins_sub_x_im = pyparsing.Group(pyparsing.Regex("SUB X") + lit_value)("139:1")
    ins_sub_x_me = pyparsing.Group(pyparsing.Regex("SUB X") + mem_value)("140:1")
    ins_sub_x_id = pyparsing.Group(pyparsing.Regex("SUB X") + idc_value)("141:1")
    ins_sub_x_ix = pyparsing.Group(pyparsing.Regex("SUB X") + idx_value)("142:1")
    ins_sub_x_idx = pyparsing.Group(pyparsing.Regex("SUB X") + idcx_value)("143:1")
    # LOAD
    ins_load_a_im = pyparsing.Group(pyparsing.Regex("LOAD A") + lit_value)("19:1")
    ins_load_a_me = pyparsing.Group(pyparsing.Regex("LOAD A") + mem_value)("20:1")
    ins_load_a_id = pyparsing.Group(pyparsing.Regex("LOAD A") + idc_value)("21:1")
    ins_load_a_ix = pyparsing.Group(pyparsing.Regex("LOAD A") + idx_value)("22:1")
    ins_load_a_idx = pyparsing.Group(pyparsing.Regex("LOAD A") + idcx_value)("23:1")

    ins_load_b_im = pyparsing.Group(pyparsing.Regex("LOAD B") + lit_value)("83:1")
    ins_load_b_me = pyparsing.Group(pyparsing.Regex("LOAD B") + mem_value)("84:1")
    ins_load_b_id = pyparsing.Group(pyparsing.Regex("LOAD B") + idc_value)("85:1")
    ins_load_b_ix = pyparsing.Group(pyparsing.Regex("LOAD B") + idx_value)("86:1")
    ins_load_b_idx = pyparsing.Group(pyparsing.Regex("LOAD B") + idcx_value)("87:1")

    ins_load_x_im = pyparsing.Group(pyparsing.Regex("LOAD X") + lit_value)("147:1")
    ins_load_x_me = pyparsing.Group(pyparsing.Regex("LOAD X") + mem_value)("148:1")
    ins_load_x_id = pyparsing.Group(pyparsing.Regex("LOAD X") + idc_value)("149:1")
    ins_load_x_ix = pyparsing.Group(pyparsing.Regex("LOAD X") + idx_value)("150:1")
    ins_load_x_idx = pyparsing.Group(pyparsing.Regex("LOAD X") + idcx_value)("151:1")
    # STORE
    ins_store_a_im = pyparsing.Group(pyparsing.Regex("STORE A") + lit_value)("27:1")
    ins_store_a_me = pyparsing.Group(pyparsing.Regex("STORE A") + mem_value)("28:1")
    ins_store_a_id = pyparsing.Group(pyparsing.Regex("STORE A") + idc_value)("29:1")
    ins_store_a_ix = pyparsing.Group(pyparsing.Regex("STORE A") + idx_value)("30:1")
    ins_store_a_idx = pyparsing.Group(pyparsing.Regex("STORE A") + idcx_value)("31:1")

    ins_store_b_im = pyparsing.Group(pyparsing.Regex("STORE B") + lit_value)("91:1")
    ins_store_b_me = pyparsing.Group(pyparsing.Regex("STORE B") + mem_value)("92:1")
    ins_store_b_id = pyparsing.Group(pyparsing.Regex("STORE B") + idc_value)("93:1")
    ins_store_b_ix = pyparsing.Group(pyparsing.Regex("STORE B") + idx_value)("94:1")
    ins_store_b_idx = pyparsing.Group(pyparsing.Regex("STORE B") + idcx_value)("95:1")

    ins_store_x_im = pyparsing.Group(pyparsing.Regex("STORE X") + lit_value)("155:1")
    ins_store_x_me = pyparsing.Group(pyparsing.Regex("STORE X") + mem_value)("156:1")
    ins_store_x_id = pyparsing.Group(pyparsing.Regex("STORE X") + idc_value)("157:1")
    ins_store_x_ix = pyparsing.Group(pyparsing.Regex("STORE X") + idx_value)("158:1")
    ins_store_x_idx = pyparsing.Group(pyparsing.Regex("STORE X") + idcx_value)("159:1")
    # AND
    ins_and_x_im = pyparsing.Group(pyparsing.Regex("AND X") + lit_value)("211:1")
    ins_and_x_me = pyparsing.Group(pyparsing.Regex("AND X") + mem_value)("212:1")
    ins_and_x_id = pyparsing.Group(pyparsing.Regex("AND X") + idc_value)("213:1")
    ins_and_x_ix = pyparsing.Group(pyparsing.Regex("AND X") + idx_value)("214:1")
    ins_and_x_idx = pyparsing.Group(pyparsing.Regex("AND X") + idcx_value)("215:1")
    # OR
    ins_or_x_im = pyparsing.Group(pyparsing.Regex("OR X") + lit_value)("195:1")
    ins_or_x_me = pyparsing.Group(pyparsing.Regex("OR X") + mem_value)("196:1")
    ins_or_x_id = pyparsing.Group(pyparsing.Regex("OR X") + idc_value)("197:1")
    ins_or_x_ix = pyparsing.Group(pyparsing.Regex("OR X") + idx_value)("198:1")
    ins_or_x_idx = pyparsing.Group(pyparsing.Regex("OR X") + idcx_value)("199:1")
    # LNEG
    ins_lneg_x_im = pyparsing.Group(pyparsing.Regex("LNEG X") + lit_value)("219:1")
    ins_lneg_x_me = pyparsing.Group(pyparsing.Regex("LNEG X") + mem_value)("220:1")
    ins_lneg_x_id = pyparsing.Group(pyparsing.Regex("LNEG X") + idc_value)("221:1")
    ins_lneg_x_ix = pyparsing.Group(pyparsing.Regex("LNEG X") + idx_value)("222:1")
    ins_lneg_x_idx = pyparsing.Group(pyparsing.Regex("LNEG X") + idcx_value)("223:1")
    


if __name__ == "__main__":
    
