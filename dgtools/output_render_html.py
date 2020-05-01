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
            
    def _write_tag(self, tag, payload=None):
        if payload is None:
            self._write_raw(f"<{tag}>\n")
        else:        
            is_multiline = payload.count("\n")>0
            if is_multiline:
                self._write_raw(f"<{tag}>\n")
                self._inc_indent()
                list(map(lambda x:self._write_raw(f"{x}\n"),payload.split("\n")))
                self._dec_indent()
                self._write_raw(f"</{tag}>\n")
            else:
                self._write_raw(f"<{tag}>{payload}</{tag}>\n")
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
        
    def open_tag(self, tag):
        self._write_indented(f"<{tag}>\n")
        self._inc_indent()
        return self
        
    def close_tag(self, tag):
        self._dec_indent()
        self._write_indented(f"</{tag}>\n")
        return self

        
    def heading(self, text, level=1):
        self._write_tag(f"h{level}",text)
        return self
        
    def preformatted(self,text):
        self._write_tag("pre", text)
        return self
        
    def ruler(self):
        self._write_tag("hr")
        
    def table_v(self, headings, contents):
        self._write_tag("table")
        self._inc_indent()
        # Write the headings
        self._write_tag("tr")
        self._inc_indent()
        list(map(lambda x:self._write_tag("th",x),headings))
        self._dec_indent()
        self._write_tag("/tr")
        # Write the data
        for a_row in contents:
            self._write_tag("tr")
            self._inc_indent()
            for a_cell in a_row:
                self._write_tag("td", str(a_cell))
            self._dec_indent()
            self._write_tag("/tr")
            
        self._dec_indent()
        self._write_tag("/table")
        return self
        
    def table_h(self, headings, contents):
        self._write_tag("table")
        self._inc_indent()
        for a_row in enumerate(contents):
            # Write the heading
            self._write_tag("tr")
            self._inc_indent()
            self._write_tag("th",headings[a_row[0]])
            for a_cell in a_row[1]:
                self._write_tag("td", str(a_cell))
            self._dec_indent()
            self._write_tag("/tr")
        self._dec_indent()
        self._write_tag("/table")
        return self
