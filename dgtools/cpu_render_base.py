class CPURenderBase:
    """
    Handles rendering of each CPUs state
    """
    def __init__(a_machine):
        self._sec2ren={}
        pass

    def get_sections():
        """
        Return a dictionary describing the sections required to render the state information for a given CPU

        Section information includes:
        (Section Title, section render method name)
        """
        pass

    def render_section(a_section_name, an_html_renderer):
        """
        Actually renders the contents of a section
        """
        self._sec2ren[a_section_name](an_html_renderer)

# Then write one method for each section to render

