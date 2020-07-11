"""
Default visualisers for the Digirule2A and Digirule2U models.

:authors: Athanasios Anastasiou
:date: Jul 2020
"""

class DgVisualiseBase:
    """
    Generates human readable representations given the state of a Digirule.
    
    Notes:
        * A program trace document has three parts: Beginning, Main, End
        * Each part is composed of one or more sections
        * Each section can be composed of different parts
        * The way parts are arranged in a section makes its layout.
        
        * The visualiser is meant to be initialised with all its parameters and then 
          "called" with the current simulation parameters (e.g. current simulation step 
          and machine state) and produce its output.
    """
    def __init__(self):
        self._init_layout = []
        self._step_layout = []
        self._final_layout = []
        self.on_setup_layouts()
        
    def on_setup_layouts(self):
        """
        Sets up the layout for each section.
        
        A section layout is a list of class functions that are identical, in terms of signature, to 
        init, step, finalise and each one is supposed to handle a part of the output.
        """
        pass
        
    def _render_section_layout(self, a_section_layout, current_n, current_digirule, rend_obj, halt_exception=None):
        # TODO: LOW, Need to revise the parameter passing here
        for a_layout in a_section_layout:
            if halt_exception:
                a_layout(current_n, current_digirule, rend_obj, halt_exception)
            else:
                a_layout(current_n, current_digirule, rend_obj)
        
    def on_init(self, current_n, current_digirule, rend_obj):
        self._render_section_layout(self._init_layout, current_n, current_digirule, rend_obj)
                
    def on_step(self, current_n, current_digirule, rend_obj):
        self._render_section_layout(self._step_layout, current_n, current_digirule, rend_obj)
        
    def on_finalise(self, current_n, current_digirule, rend_obj, halt_exception):
        self._render_section_layout(self._final_layout, current_n, current_digirule, rend_obj, halt_exception)
        

class DgVisualiseDigirule2A(DgVisualiseBase):
    """
    Renders the state of a Digirule2A.
    """
    def __init__(self, trace_title="", extra_symbols=[], with_mem_dump=False):
        super().__init__()
        self._trace_title = trace_title
        self._extra_symbols = extra_symbols
        self._with_mem_dump = with_mem_dump
        
    def on_setup_layouts(self):
        self._init_layout = [self.start_trace]
        self._step_layout = [self.step_heading, 
                             self.step_machine_registers, 
                             self.step_mem_space, 
                             self.step_extra_symbols,
                             self.step_onboard_io]
        self._final_layout = [self.end_trace]
        
        
    def start_trace(self, current_n, current_digirule, rend_obj):
        """
        Begins the trace document with the supplied title of the trace.
        """
        rend_obj.open_tag("article")
        rend_obj.open_tag("header")
        rend_obj.heading(f"Program Trace {self._trace_title}", 1)
        rend_obj.close_tag("header")
        
    def step_heading(self, current_n, current_digirule, rend_obj):
        """
        Produces the heading of each main execution step within the main section.
        """
        rend_obj.open_tag("section")
        rend_obj.named_anchor(f"n{current_n}")
        rend_obj.open_tag("header")
        rend_obj.heading(f"Machine State at n={current_n}",2)
        rend_obj.close_tag("header")
        
    def step_machine_registers(self, current_n, current_digirule, rend_obj):
        """
        Produces the "Machine Registers" part of the main section.
        """
        # Machine registers
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
        
    def step_mem_space(self, current_n, current_digirule, rend_obj):
        """
        Produces the mem-dump part of the main section (if enabled)
        """
        # If this section is not "enabled" then immediately return.
        if not self._with_mem_dump:
            return
            
        mem_space_heading_h = ["Offset (h)"]+[f"{x:02X}" for x in range(0,16)]
        mem_space_heading_v = [f"{x:02X}" for x in range(0,256,16)]

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

    def step_extra_symbols(self, current_n, current_digirule, rend_obj):
        """
        Produces the "Extra Symbols" part of the main section
        """
        # Extra symbols
        # If there are no extra symbols specified then return immediately.
        if len(self._extra_symbols) == 0:
            return
            
        rend_obj.open_tag("section")
        rend_obj.open_tag("header")
        rend_obj.heading(f"Specific Symbols",3)
        rend_obj.close_tag("header")
        
        symbol_values = []
        for a_symbol in self._extra_symbols:
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
                                  zip(self._extra_symbols,symbol_values))), 
                         attrs={"class":"table_spec_sym"})
        rend_obj.close_tag("section")

    def step_onboard_io(self, current_n, current_digirule, rend_obj):
        """
        Produces the "Onboard IO" section of the main part.
        """
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
        
    def end_trace(self, current_n, current_digirule, rend_obj, halt_exception):
        """
        Produces the ending section which usually includes the reason for program termination.
        """
        rend_obj.open_tag("section", {"class":"program_halt"})
        rend_obj.named_anchor(f"program_halt")
        rend_obj.open_tag("header")
        rend_obj.heading(f"Program stopped at n={current_n-1}",2)
        rend_obj.close_tag("header")
        rend_obj._write_tag("p", str(halt_exception))
        rend_obj.close_tag("section")
        
        rend_obj.close_tag("article")
    
        
class DgVisualiseDigirule2U:
    pass
