"""

A very basic HTML renderer.

:author: Athanasios Anastasiou
:date: April 2020
"""

class Output_Render_HTML():
    def __init__(self, filename):
        self._filename = filename
        self._fd = None
        self._indent_level = 0
        
    @staticmethod
    def _get_attr_str(attrs):
        """
        Returns a properly formatted string containing the attributes of a tag (e.g. class, id, name, etc)
        
        :param attrs: Dictionary of attributes to be added to a tag
        :type attrs: dict
        :returns: A string with key="value" pairs unfolded.
        :rtype: str
        """
        attr_str = ""
        if attrs is not None:
            attr_str = " " + " ".join(map(lambda x:f'{x[0]}="{x[1]}"',attrs.items()))
        return attr_str
        
    def __enter__(self):
        self._fd = open(self._filename, "wt")
        self.doc_start()
        return self
        
    def __exit__(self, type, value, traceback):
        self.doc_end()
        self._fd.close()

    def _istr(self, x):
        return f"{chr(9)*self._indent_level}{x}"
            
    def _inc_indent(self):
        self._indent_level+=1
        return self
        
    def _dec_indent(self):
        self._indent_level-=1
        return self
                
    def _write_indented(self, payload):
        self._fd.write(self._istr(payload))
        return self
        
    def _write_raw(self, payload, with_breaks=False):
        if with_breaks:
            list(map(lambda x:self._write_indented(f"{x}\n"), payload.split("\n"))) 
        else:
            self._write_indented(f"{payload}")
        return self
            
    def _write_tag(self, tag, payload=None, attrs=None, autoclose=True):
        attr_str = self._get_attr_str(attrs)
        if payload is None:
            self._write_raw(f"<{tag}{attr_str}>")
            if autoclose:
                self._write_raw(f"</{tag}>\n")
            else:
                self._write_raw("\n")
        else:        
            is_multiline = payload.count("\n")>0
            if is_multiline:
                self._write_raw(f"<{tag}{attr_str}>\n")
                self._inc_indent()
                list(map(lambda x:self._write_raw(f"{x}\n"),payload.split("\n")))
                self._dec_indent()
                self._write_raw(f"</{tag}>\n")
            else:
                self._write_raw(f"<{tag}{attr_str}>{payload}</{tag}>\n")
        
        return self
        
    def doc_start(self):
        self._fd.write("<!DOCTYPE html>\n"
                       "<html>\n"
                       "\t<head>\n"
                       "\t<link rel=\"stylesheet\" type=\"text/css\" href=\"dgtheme.css\">"
                       "\t\t<meta charset=\"utf-8\" />\n"
                       "\t\t<title></title>\n"
                       "\t</head>\n"
                       "<body>\n")
        return self
        
    def doc_end(self):
        self._fd.write("</body>\n"
                       "</html>\n")
        return self
        
    def open_tag(self, tag, attrs=None):
        attr_str = self._get_attr_str(attrs)
        self._write_indented(f"<{tag}{attr_str}>\n")
        self._inc_indent()
        return self
        
    def close_tag(self, tag):
        self._dec_indent()
        self._write_indented(f"</{tag}>\n")
        return self

        
    def heading(self, text, level=1, attrs=None):
        self._write_tag(f"h{level}",text, attrs)
        return self
        
    def preformatted(self,text, attrs=None):
        self._write_tag("pre", text, attrs)
        return self
        
    def ruler(self):
        self._write_tag("hr", autoclose=False)
        
    def table_v(self, headings, contents, attrs=None):
        """
        Creates a vertical table. A vertical table has a row heading and column oriented content.
        """
        self.open_tag("table", attrs=attrs)
        # Write the headings
        self.open_tag("tr")
        list(map(lambda x:self._write_tag("th",x),headings))
        self.close_tag("tr")
        # Write the data
        for a_row in contents:
            self.open_tag("tr")
            for a_cell in a_row:
                self._write_tag("td", str(a_cell))
            self.close_tag("tr")
            
        self.close_tag("table")
        return self
        
    def table_h(self, headings, contents, attrs=None):
        """
        Creates a horizontal table. A horizontal table has a column heading and row oriented content.
        """
        self.open_tag("table", attrs=attrs)
        for a_row in enumerate(contents):
            # Write the heading
            self.open_tag("tr")
            self._write_tag("th",headings[a_row[0]])
            for a_cell in a_row[1]:
                self._write_tag("td", str(a_cell))
            self.close_tag("tr")
        self.close_tag("table")
        return self

    def table_hv(self,  contents, heading_h = None, heading_v = None, attrs=None, cell_attrs=None):
        """
        Creates a table that has headings both in horizontal and vertical dims and 
        lays out contents as a two dimensional table.
        
        :param contents: The actual contents of the table
        :type contents: list of lists of strings
        :param heading_h: The first row of headings
        :param heading_v: The first col of headings
        :param attrs: Attributes for the table element
        :param cell_attrs: Attributes for individual elements
        :type cell_attrs: Dictionary that maps offset in table to attribute dict
        :type cell_attrs: dict<int,dict>
        """
        self.open_tag("table", attrs=attrs)
        if heading_h is not None:
            self.open_tag("tr")
            for a_value in heading_h:
                self._write_tag("th",str(a_value))
            self.close_tag("tr")
        
        add_col_heads = heading_v is not None
        add_cell_attr = cell_attrs is not None        
        
        for a_row, a_row_v in enumerate(contents):
            self.open_tag("tr")
            if add_col_heads:
                self._write_tag("th", str(heading_v[a_row]))
            for a_col, a_col_v in enumerate(a_row_v):
                if add_cell_attr:
                    cell_coords = (a_row,a_col)
                    if cell_coords in cell_attrs:
                        self._write_tag("td",a_col_v, attrs=cell_attrs[cell_coords])
                    else:
                        self._write_tag("td", a_col_v)
                else:
                    self._write_tag("td",a_col_v)
            self.close_tag("tr")
                    
        self.close_tag("table")
        
    def named_anchor(self, anchor_name):
        self._write_tag("a",attrs={"id":anchor_name})
