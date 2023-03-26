class CPUStateRendererBase:
    """
    Handles rendering of each CPUs state
    """
    def __init__(self, a_machine, prod_mem_dump=True):
        self._machine = a_machine
        self._prod_mem_dump = prod_mem_dump
        self._sec2ren={}

    @property
    def secdesc(self):
        """
        Section descriptions.
        """
        return self._sec2ren

    def render_section(self, a_section_name, an_html_renderer):
        """
        Actually renders the contents of a section
        """
        self._sec2ren[a_section_name](an_html_renderer)

# Then write one method for each section to render
class Digirule2UStateRenderer(CPUStateRendererBase):
    pass

class KenbackStateRenderer(CPUStateRendererBase):
    pass

class DigiruleStateRenderer(CPUStateRendererBase):
    """
    Renders all sections of a Digirule
    """
    def __init__(self, a_machine, prod_mem_dump):
        super().__init__(a_machine, prod_mem_dump)
        self._sec2ren={("Machine Registers", self._render_registers),
                       ("Full Memory Dump", self._render_memoryspace),
                       ("Onboard I/O",self._render_onboard_io)}

    def _render_registers(self, output_ren):
        # Machine registers 
        
        # Create the header of all attributes
        output_ren.table_h(",".join(list(self._machine.mem._reg_desc.values()) + ["Program counter stack"]), \
                     [[self._machine.mem._reg_rd(v)] for v in self._machine.mem._reg_desc] + [",".join(list(map(lambda x:f"0x{x:02X}",self._machine._ppc)))], \
                     attrs={"class":"table_machine_state"})
        output_ren.close_tag("section")

    def _render_memoryspace(self, output_ren):
        # Memory space
       if self._prod_mem_dump:
           # TODO: HIGH, Adapt to the CPUs memory
           output_ren.table_hv([[f"{self._machine.mem[n]:02X}" for n in range(m,m+16)] for m in range(0,256,16)],
                         mem_space_heading_h, 
                         mem_space_heading_v,
                         attrs={"class":"table_memory_space"},
                         cell_attrs={(self._machine.pc // 16,self._machine.pc-(self._machine.pc // 16)):{"class":"current_pc"}})
           dgen.close_tag("section")

    def _render_onboard_io(self, output_ren):
        # Onboard IO
        output_ren.table_h(["Address LEDs","Data LEDs","Button Switches"],
                     [[self._machine.mem["ADDR_LED"]], [self._machine.mem["DATA_LED"]], [self._machine.mem["INPUT"]]],
                     attrs={"class":"table_onboard_io"})
        output_ren.close_tag("section") 
        
