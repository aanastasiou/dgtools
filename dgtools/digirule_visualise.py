"""
Default visualisers for the Digirule2A and Digirule2U models.

:authors: Athanasios Anastasiou
:date: Jul 2020
"""

class DgVisualiseBase:
    """
    Digirule visualiser objects are responsible for generating human readable representations for the state 
    of the Digirule as it evolves through program execution.
    """
    def on_init(self, current_digirule, rend_obj):
        raise NotImplementedError("Cannot instantiate directly.")
        
    def on_step(self, current_digirule, rend_obj):
        raise NotImplementedError("Cannot instantiate directly.")
        
    def on_finalise(self, current_digirule, rend_obj, halt_exception):
        raise NotImplementedError("Cannot instantiate directly.")
        

class DgVisualiseDigirule2A(DgVisualiseBase):
    def __init__(self, trace_title="", extra_symbols=[], with_mem_dump=False):
        self._trace_title = trace_title
        self._extra_symbols = extra_symbols
        self._with_mem_dump = self._with_mem_dump
        
    def on_init(self, current_digirule, rend_obj):
        rend_obj.open_tag("article")
        rend_obj.open_tag("header")
        rend_obj.heading(f"Program Trace {self._trace_title}", 1)
        rend_obj.close_tag("header")
        
    def on_step(self, current_digirule, rend_obj):
        # Machine registers
        rend_obj.open_tag("section")
        rend_obj.named_anchor(f"n{n}")
        rend_obj.open_tag("header")
        rend_obj.heading(f"Machine State at n={n}",2)
        rend_obj.close_tag("header")
        
        rend_obj.open_tag("section")
        rend_obj.open_tag("header")
        rend_obj.heading(f"Machine Registers",3)
        rend_obj.close_tag("header")
        rend_obj.table_h(["Program Counter:","Accumulator:", "Status Reg:","Button Register:", "Addr.Led Register:",
                          "Data Led Register:", "Speed setting:", "Program counter stack:"],
                         [[f"0x{current_digirule._pc:02X}"], 
                          [current_digirule._acc],
                          [current_digirule._mem[current_digirule._status_reg_ptr]], 
                          [current_digirule._mem[current_digirule._bt_reg_ptr]], 
                          [current_digirule._mem[current_digirule._addrled_reg_ptr]], 
                          [current_digirule._mem[current_digirule._dataled_reg_ptr]], 
                         [current_digirule._speed_setting], 
                         # [machine._ppc]],
                         [",".join(list(map(lambda x:f"0x{x:02X}",current_digirule._ppc)))]],
                         attrs={"class":"table_machine_state"})
        rend_obj.close_tag("section")
        
        # Memory space
        if self._with_mem_dump:
            rend_obj.open_tag("section")
            rend_obj.open_tag("header")
            rend_obj.heading(f"Full memory dump:",3)
            rend_obj.close_tag("header")
            rend_obj.table_hv([[f"{current_digirule._mem[n]:02X}" for n in range(m,m+16)] for m in range(0,256,16)],
                              mem_space_heading_h, 
                              mem_space_heading_v,
                              attrs={"class":"table_memory_space"},
                              cell_attrs={(current_digirule._pc // 16,current_digirule._pc-(current_digirule._pc // 16)):{"class":"current_pc"}})
            rend_obj.close_tag("section")
        
        # Extra symbols
        if len(self._extra_symbols):
            rend_obj.open_tag("section")
            rend_obj.open_tag("header")
            rend_obj.heading(f"Specific Symbols",3)
            rend_obj.close_tag("header")
            
            symbol_values = []
            for a_symbol in extra_symbols:
                raw_bytes = current_digirule._mem[a_symbol[1]:(a_symbol[1]+a_symbol[2])]
                if len(raw_bytes)>1:
                    chr_bytes = "".join(map(lambda x:chr(x), raw_bytes))
                else:
                    chr_bytes = ""
                symbol_values.append([str(raw_bytes),chr_bytes])
            # dgen.table_h(symbol_names,symbol_values, attrs={"class":"table_spec_sym"})
            rend_obj.table_v(["Symbol","Offset","Value(s)", "Value as string"],
                             list(map(lambda x:[x[0][0],
                                                f"0x{x[0][1]:02X}",
                                                x[1][0],x[1][1]],
                                      zip(extra_symbols,symbol_values))), 
                             attrs={"class":"table_spec_sym"})
            rend_obj.close_tag("section")
        
        # Onboard IO
        rend_obj.open_tag("section")
        rend_obj.open_tag("header")
        rend_obj.heading("Onboard I/O",3)
        rend_obj.close_tag("header")
        rend_obj.table_h(["Address LEDs","Data LEDs","Button Switches"],
                         [current_digirule.addr_led, current_digirule.data_led, current_digirule.button_sw],
                         attrs={"class":"table_onboard_io"})
        rend_obj.close_tag("section")
        
        rend_obj.close_tag("section")
        rend_obj.ruler()
        
    def on_finalise(self, current_digirule, rend_obj, halt_exception):
        rend_obj.open_tag("section", {"class":"program_halt"})
        rend_obj.named_anchor(f"program_halt")
        rend_obj.open_tag("header")
        rend_obj.heading(f"Program stopped at n={n-1}",2)
        rend_obj.close_tag("header")
        if done:
            rend_obj._write_tag("p", str(halt_reason))
        else:
            rend_obj._write_tag("p", f"Program exceeded max_n of {max_n}")
        rend_obj.close_tag("section")
        
        rend_obj.close_tag("article")
    
        
class DgVisualiseDigirule2U:
    pass
