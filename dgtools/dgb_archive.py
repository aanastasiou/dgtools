"""

Archive to store Digirule2 binaries

:author: Athanasios Anastasiou
:date: April 2020
"""

import json
import base64
import copy

class DGB_Archive:
    def __init__(self, compiled_program, labels, symbols, version="1.0.0"):
        self._sections = {"program":compiled_program,"labels":labels,"symbols":symbols, "version":version}
        
    def save(self, filename):
        sections_to_save = copy.deepcopy(self._sections)
        # Does this really need to be base64 encoded?
        sections_to_save["program"] = base64.b64encode(bytearray(sections_to_save["program"])).decode("ascii")
        with open(filename, "wt") as fd:
            json.dump(sections_to_save, fd)
        return self

    @classmethod    
    def load(cls,filename):
        with open(filename, "rt") as fd:
            archive_sections = json.load(fd)
        if "version" not in archive_sections:
            archive_sections.update({"version":"1.0.0"})
        archive_sections["program"] = list(base64.b64decode(archive_sections["program"]))
        return cls(archive_sections["program"], archive_sections["labels"], archive_sections["symbols"], archive_sections["version"]) 
        
    @property
    def program(self):
        return self._sections["program"]
        
    @property
    def labels(self):
        return self._sections["labels"]
        
    @property
    def symbols(self):
        return self._sections["symbols"]
        
    @property
    def version(self):
        return self._sections["version"]
