"""

Classes that support tracing Digirule hardware code

:author: Athanasios Anastasiou
:date: Jul 2020
"""

class DgSimulator:
    """
    The simulator object is responsible for orchestrating a specific simulation run.
    It gets associated with a digirule object and a visualiser for the same.
    """
    def __init__(self, digirule, dgb_archive, digirule_visualiser, max_n=200, trace_title=None, \
                 in_interactive_mode=False, extra_symbols=[], with_mem_dump=True):
        """
        
        :param digirule:
        :type digirule:
        :param dgb_archive:
        :type dgb_archive:
        :param digirule_visualiser:
        :type digirule_visualiser:
        :param max_n:
        :type max_n: int
        :param trace_title: 
        :type trace_title: str
        :param in_interactive_mode:
        :type in_interactive_mode:
        :param extra_symbols:
        :type extra_symbols:
        :param with_mem_dump:
        :type with_mem_dump:
        """
        
        self._digirule = digirule
        self._digirule_visualiser = digirule_visualiser
        self._max_n = max_n
        self._trace_title = trace_title
        self._in_interactive_mode = in_interactive_mode
        self._extra_symbols = []
        self._with_mem_dump = with_mem_dump
        pass
        
    def on_init(self):
        # Reset the hardware and load the program
        
        pass
        
    def on_step(self):
        pass
        
    def on_finalise(self):
        pass
        
    def __call__(self, output_file):
        n = 0
        self.on_init()
        
        while not done and n<self._max_n:
            try:
                machine._exec_next()
            except DgtoolsError as de:
                done = True
                halt_reason = de
                
            n+=1
        self.on_finalise()
        
                
