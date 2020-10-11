"""
Preliminary tests with the Kenback

Sept 2020
"""

import pyparsing

def get_parser():
    register_A = pyparsing.Literal("A").setParseAction(lambda s,loc,tok:0)
    register_B = pyparsing.Literal("B").setParseAction(lambda s,loc,tok:1)
    register_X = pyparsing.Literal("X").setParseAction(lambda s,loc,tok:2)
    register_P = pyparsing.Literal("P").setParseAction(lambda s,loc,tok:3)
    
    registers = register_A ^ register_B ^ register_X ^ register_P
    
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
    # JUMPS
    # Unconditional
    # The three LSb have to have specific values even in unconditional jumps
    # http://kenbak-1.net/index_files/PRM.pdf
    ins_jpd = pyparsing.Group(pyparsing.Regex("JPD") + lit_value)("228:1") 
    ins_jpi = pyparsing.Group(pyparsing.Regex("JPI") + idc_value)("236:1")
    ins_jmd = pyparsing.Group(pyparsing.Regex("JMD") + lit_value)("244:1")
    ins_jmi = pyparsing.Group(pyparsing.Regex("JMI") + idc_value)("252:1")
    # Conditional on A direct
    ins_jpd_a_nz = pyparsing.Group(pyparsing.Regex("JPDNZ A") + lit_value)
    ins_jpd_a_z = pyparsing.Group(pyparsing.Regex("JPDZ A") + lit_value)
    ins_jpd_a_ltz = pyparsing.Group(pyparsing.Regex("JPDLTZ A") + lit_value)
    ins_jpd_a_gez = pyparsing.Group(pyparsing.Regex("JPDGEZ A") + lit_value)
    ins_jpd_a_gz = pyparsing.Group(pyparsing.Regex("JPDGZ A") + lit_value)
    # Conditional on A indirect
    ins_jpi_a_nz = pyparsing.Group(pyparsing.Regex("JPINZ A") + idc_value)
    ins_jpi_a_z = pyparsing.Group(pyparsing.Regex("JPIZ A") + idc_value)
    ins_jpi_a_ltz = pyparsing.Group(pyparsing.Regex("JPILTZ A") + idc_value)
    ins_jpi_a_gez = pyparsing.Group(pyparsing.Regex("JPIGEZ A") + idc_value)
    ins_jpi_a_gz = pyparsing.Group(pyparsing.Regex("JPIGZ A") + idc_value)
    # Conditional on A mark direct
    ins_jmd_a_nz = pyparsing.Group(pyparsing.Regex("JMDNZ A") + lit_value)
    ins_jmd_a_z = pyparsing.Group(pyparsing.Regex("JMDZ A") + lit_value)
    ins_jmd_a_ltz = pyparsing.Group(pyparsing.Regex("JMDLTZ A") + lit_value)
    ins_jmd_a_gez = pyparsing.Group(pyparsing.Regex("JMDGEZ A") + lit_value)
    ins_jmd_a_gz = pyparsing.Group(pyparsing.Regex("JMDGZ A") + lit_value)
    # Conditional on A mark indirect
    ins_jmi_a_nz = pyparsing.Group(pyparsing.Regex("JMINZ A") + idc_value)
    ins_jmi_a_z = pyparsing.Group(pyparsing.Regex("JMIZ A") + idc_value)
    ins_jmi_a_ltz = pyparsing.Group(pyparsing.Regex("JMILTZ A") + idc_value)
    ins_jmi_a_gez = pyparsing.Group(pyparsing.Regex("JMIGEZ A") + idc_value)
    ins_jmi_a_gz = pyparsing.Group(pyparsing.Regex("JMIGZ A") + idc_value)
    
    # Conditional on B direct
    ins_jpd_b_nz = pyparsing.Group(pyparsing.Regex("JPDNZ B") + lit_value)
    ins_jpd_b_z = pyparsing.Group(pyparsing.Regex("JPDZ B") + lit_value)
    ins_jpd_b_ltz = pyparsing.Group(pyparsing.Regex("JPDLTZ B") + lit_value)
    ins_jpd_b_gez = pyparsing.Group(pyparsing.Regex("JPDGEZ B") + lit_value)
    ins_jpd_b_gz = pyparsing.Group(pyparsing.Regex("JPDGZ B") + lit_value)
    # Conditional on B indirect
    ins_jpi_b_nz = pyparsing.Group(pyparsing.Regex("JPINZ B") + idc_value)
    ins_jpi_b_z = pyparsing.Group(pyparsing.Regex("JPIZ B") + idc_value)
    ins_jpi_b_ltz = pyparsing.Group(pyparsing.Regex("JPILTZ B") + idc_value)
    ins_jpi_b_gez = pyparsing.Group(pyparsing.Regex("JPIGEZ B") + idc_value)
    ins_jpi_b_gz = pyparsing.Group(pyparsing.Regex("JPIGZ B") + idc_value)
    # Conditional on B mark direct
    ins_jmd_b_nz = pyparsing.Group(pyparsing.Regex("JMDNZ B") + lit_value)
    ins_jmd_b_z = pyparsing.Group(pyparsing.Regex("JMDZ B") + lit_value)
    ins_jmd_b_ltz = pyparsing.Group(pyparsing.Regex("JMDLTZ B") + lit_value)
    ins_jmd_b_gez = pyparsing.Group(pyparsing.Regex("JMDGEZ B") + lit_value)
    ins_jmd_b_gz = pyparsing.Group(pyparsing.Regex("JMDGZ B") + lit_value)
    # Conditional on B mark indirect
    ins_jmi_b_nz = pyparsing.Group(pyparsing.Regex("JMINZ B") + idc_value)
    ins_jmi_b_z = pyparsing.Group(pyparsing.Regex("JMIZ B") + idc_value)
    ins_jmi_b_ltz = pyparsing.Group(pyparsing.Regex("JMILTZ B") + idc_value)
    ins_jmi_b_gez = pyparsing.Group(pyparsing.Regex("JMIGEZ B") + idc_value)
    ins_jmi_b_gz = pyparsing.Group(pyparsing.Regex("JMIGZ B") + idc_value)

    # Conditional on X direct
    ins_jpd_x_nz = pyparsing.Group(pyparsing.Regex("JPDNZ X") + lit_value)
    ins_jpd_x_z = pyparsing.Group(pyparsing.Regex("JPDZ X") + lit_value)
    ins_jpd_x_ltz = pyparsing.Group(pyparsing.Regex("JPDLTZ X") + lit_value)
    ins_jpd_x_gez = pyparsing.Group(pyparsing.Regex("JPDGEZ X") + lit_value)
    ins_jpd_x_gz = pyparsing.Group(pyparsing.Regex("JPDGZ X") + lit_value)
    # Conditional on X indirect
    ins_jpi_x_nz = pyparsing.Group(pyparsing.Regex("JPINZ X") + idc_value)
    ins_jpi_x_z = pyparsing.Group(pyparsing.Regex("JPIZ X") + idc_value)
    ins_jpi_x_ltz = pyparsing.Group(pyparsing.Regex("JPILTZ X") + idc_value)
    ins_jpi_x_gez = pyparsing.Group(pyparsing.Regex("JPIGEZ X") + idc_value)
    ins_jpi_x_gz = pyparsing.Group(pyparsing.Regex("JPIGZ X") + idc_value)
    # Conditional on X mark direct
    ins_jmd_x_nz = pyparsing.Group(pyparsing.Regex("JMDNZ X") + lit_value)
    ins_jmd_x_z = pyparsing.Group(pyparsing.Regex("JMDZ X") + lit_value)
    ins_jmd_x_ltz = pyparsing.Group(pyparsing.Regex("JMDLTZ X") + lit_value)
    ins_jmd_x_gez = pyparsing.Group(pyparsing.Regex("JMDGEZ X") + lit_value)
    ins_jmd_x_gz = pyparsing.Group(pyparsing.Regex("JMDGZ X") + lit_value)
    # Conditional on X mark indirect
    ins_jmi_x_nz = pyparsing.Group(pyparsing.Regex("JMINZ X") + idc_value)
    ins_jmi_x_z = pyparsing.Group(pyparsing.Regex("JMIZ X") + idc_value)
    ins_jmi_x_ltz = pyparsing.Group(pyparsing.Regex("JMILTZ X") + idc_value)
    ins_jmi_x_gez = pyparsing.Group(pyparsing.Regex("JMIGEZ X") + idc_value)
    ins_jmi_x_gz = pyparsing.Group(pyparsing.Regex("JMIGZ X") + idc_value)
    
    # SKIPS
    # SKIP 0
    ins_skip_0_0 = pyparsing.Group(pyparsing.Regex("SKP 0 0") + mem_value)
    ins_skip_0_1 = pyparsing.Group(pyparsing.Regex("SKP 0 1") + mem_value)
    ins_skip_0_2 = pyparsing.Group(pyparsing.Regex("SKP 0 2") + mem_value)
    ins_skip_0_3 = pyparsing.Group(pyparsing.Regex("SKP 0 3") + mem_value)
    ins_skip_0_4 = pyparsing.Group(pyparsing.Regex("SKP 0 4") + mem_value)
    ins_skip_0_5 = pyparsing.Group(pyparsing.Regex("SKP 0 5") + mem_value)
    ins_skip_0_6 = pyparsing.Group(pyparsing.Regex("SKP 0 6") + mem_value)
    ins_skip_0_7 = pyparsing.Group(pyparsing.Regex("SKP 0 7") + mem_value)
    # SKIP 1
    ins_skip_1_0 = pyparsing.Group(pyparsing.Regex("SKP 1 0") + mem_value)
    ins_skip_1_1 = pyparsing.Group(pyparsing.Regex("SKP 1 1") + mem_value)
    ins_skip_1_2 = pyparsing.Group(pyparsing.Regex("SKP 1 2") + mem_value)
    ins_skip_1_3 = pyparsing.Group(pyparsing.Regex("SKP 1 3") + mem_value)
    ins_skip_1_4 = pyparsing.Group(pyparsing.Regex("SKP 1 4") + mem_value)
    ins_skip_1_5 = pyparsing.Group(pyparsing.Regex("SKP 1 5") + mem_value)
    ins_skip_1_6 = pyparsing.Group(pyparsing.Regex("SKP 1 6") + mem_value)
    ins_skip_1_7 = pyparsing.Group(pyparsing.Regex("SKP 1 7") + mem_value)

    # SET
    # SET 0
    ins_set_0_0 = pyparsing.Group(pyparsing.Regex("SET 0 0") + mem_value)
    ins_set_0_1 = pyparsing.Group(pyparsing.Regex("SET 0 1") + mem_value)
    ins_set_0_2 = pyparsing.Group(pyparsing.Regex("SET 0 2") + mem_value)
    ins_set_0_3 = pyparsing.Group(pyparsing.Regex("SET 0 3") + mem_value)
    ins_set_0_4 = pyparsing.Group(pyparsing.Regex("SET 0 4") + mem_value)
    ins_set_0_5 = pyparsing.Group(pyparsing.Regex("SET 0 5") + mem_value)
    ins_set_0_6 = pyparsing.Group(pyparsing.Regex("SET 0 6") + mem_value)
    ins_set_0_7 = pyparsing.Group(pyparsing.Regex("SET 0 7") + mem_value)
    # SKIP 1
    ins_set_1_0 = pyparsing.Group(pyparsing.Regex("SET 1 0") + mem_value)
    ins_set_1_1 = pyparsing.Group(pyparsing.Regex("SET 1 1") + mem_value)
    ins_set_1_2 = pyparsing.Group(pyparsing.Regex("SET 1 2") + mem_value)
    ins_set_1_3 = pyparsing.Group(pyparsing.Regex("SET 1 3") + mem_value)
    ins_set_1_4 = pyparsing.Group(pyparsing.Regex("SET 1 4") + mem_value)
    ins_set_1_5 = pyparsing.Group(pyparsing.Regex("SET 1 5") + mem_value)
    ins_set_1_6 = pyparsing.Group(pyparsing.Regex("SET 1 6") + mem_value)
    ins_set_1_7 = pyparsing.Group(pyparsing.Regex("SET 1 7") + mem_value)

    # SHIFT
    # LEFT A
    ins_sftl_a_1 = pyparsing.Group(pyparsing.Regex("SFTL A 1"))
    ins_sftl_a_2 = pyparsing.Group(pyparsing.Regex("SFTL A 2"))
    ins_sftl_a_3 = pyparsing.Group(pyparsing.Regex("SFTL A 3"))
    ins_sftl_a_4 = pyparsing.Group(pyparsing.Regex("SFTL A 4"))
    # RIGHT A
    ins_sftr_a_1 = pyparsing.Group(pyparsing.Regex("SFTR A 1"))
    ins_sftr_a_2 = pyparsing.Group(pyparsing.Regex("SFTR A 2"))
    ins_sftr_a_3 = pyparsing.Group(pyparsing.Regex("SFTR A 3"))
    ins_sftr_a_4 = pyparsing.Group(pyparsing.Regex("SFTR A 4"))
    # LEFT B
    ins_sftl_b_1 = pyparsing.Group(pyparsing.Regex("SFTL B 1"))
    ins_sftl_b_2 = pyparsing.Group(pyparsing.Regex("SFTL B 2"))
    ins_sftl_b_3 = pyparsing.Group(pyparsing.Regex("SFTL B 3"))
    ins_sftl_b_4 = pyparsing.Group(pyparsing.Regex("SFTL B 4"))
    # RIGHT B
    ins_sftr_b_1 = pyparsing.Group(pyparsing.Regex("SFTR B 1"))
    ins_sftr_b_2 = pyparsing.Group(pyparsing.Regex("SFTR B 2"))
    ins_sftr_b_3 = pyparsing.Group(pyparsing.Regex("SFTR B 3"))
    ins_sftr_b_4 = pyparsing.Group(pyparsing.Regex("SFTR B 4"))

    # ROTATE
    # LEFT A
    ins_rotl_a_1 = pyparsing.Group(pyparsing.Regex("ROTL A 1"))
    ins_rotl_a_2 = pyparsing.Group(pyparsing.Regex("ROTL A 2"))
    ins_rotl_a_3 = pyparsing.Group(pyparsing.Regex("ROTL A 3"))
    ins_rotl_a_4 = pyparsing.Group(pyparsing.Regex("ROTL A 4"))
    # RIGHT A
    ins_rotr_a_1 = pyparsing.Group(pyparsing.Regex("ROTR A 1"))
    ins_rotr_a_2 = pyparsing.Group(pyparsing.Regex("ROTR A 2"))
    ins_rotr_a_3 = pyparsing.Group(pyparsing.Regex("ROTR A 3"))
    ins_rotr_a_4 = pyparsing.Group(pyparsing.Regex("ROTR A 4"))
    # LEFT B
    ins_rotl_b_1 = pyparsing.Group(pyparsing.Regex("ROTL B 1"))
    ins_rotl_b_2 = pyparsing.Group(pyparsing.Regex("ROTL B 2"))
    ins_rotl_b_3 = pyparsing.Group(pyparsing.Regex("ROTL B 3"))
    ins_rotl_b_4 = pyparsing.Group(pyparsing.Regex("ROTL B 4"))
    # RIGHT B
    ins_rotr_b_1 = pyparsing.Group(pyparsing.Regex("ROTR B 1"))
    ins_rotr_b_2 = pyparsing.Group(pyparsing.Regex("ROTR B 2"))
    ins_rotr_b_3 = pyparsing.Group(pyparsing.Regex("ROTR B 3"))
    ins_rotr_b_4 = pyparsing.Group(pyparsing.Regex("ROTR B 4"))

if __name__ == "__main__":
    
