"""

Classes that support tracing Digirule hardware code

:author: Athanasios Anastasiou
:date: Jul 2020
"""

from .exceptions import DgtoolsErrorProgramHalt, DgtoolsError
from .output_render_html import Output_Render_HTML

class DgSimulator:
    """
    The simulator object is responsible for orchestrating a specific simulation run.
    It gets associated with a digirule object and a visualiser for the same.
    """
    def __init__(self, digirule, digirule_visualiser, max_n=200):
        """
        :param digirule:
        :type digirule:
        :param digirule_visualiser:
        :type digirule_visualiser:
        :param max_n:
        :type max_n: int
        """
        
        self._digirule = digirule
        self._digirule_visualiser = digirule_visualiser
        self._max_n = max_n
        self._current_n = 0
        
    def on_init(self, rend_obj):
        """
        Called at the start of the trace procedure
        """
        self._digirule_visualiser.on_init(self._digirule, rend_obj)

    def on_step(self, rend_obj):
        self._digirule_visualiser.on_step(self._digirule, rend_obj)
        
    def on_finalise(self, rend_obj, halt_exception):
        # TODO: HIGH, Add similar type checking to the two points above
        if not issubclass(halt_exception, DgtoolsError):
            raise TypeError(f"Expected DgtoolsError, received {type(halt_exception)}")
        self._digirule_visualiser.on_finalise(self._digirule, rend_obj, halt_exception)
        
    def __call__(self, output_file):
        with Output_Render_HTML(output_file) as dgen:
            self.on_init(dgen)
            while not done:
                try:
                    if self._current_n == self._max_n:
                        raise DgtoolsErrorProgramHalt(f"Maximum number of execution steps reached ({self._current_n}).")
                    self._digirule._exec_next()
                    self.on_step(dgen)
                    self._current_n+=1
                except DgtoolsError as de:
                    self.on_finalise(dgen, de)
                    done = True
