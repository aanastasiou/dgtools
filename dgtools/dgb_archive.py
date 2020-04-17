"""

Archive to store Digirule2 binaries

:author: Athanasios Anastasiou
:date: April 2020
"""

import json
import copy

class DGB_Archive:
    def __init__(self, compiled_program, labels, symbols, version="1.0.0"):
        self._sections = {"program":compiled_program,"labels":labels,"symbols":symbols, "version":version}
        
    def save(self, filename):
        with open(filename, "wt") as fd:
            json.dump(self._sections, fd)
        return self

    @classmethod
    def from_archive(cls, other_archive):
        self._sections = copy.deepcopy(other_archive._sections)
        return self
        
    @classmethod    
    def load(cls,filename):
        with open(filename, "rt") as fd:
            archive_sections = json.load(fd)
        # TODO: HIGH, Incorporate the following validations
        # # Validate the .dgb file
        # if type(compiled_program) is not dict:
            # raise DgtoolsErrorDgbarchiveCorrupted(f"Archive corrupted.")
        
        # if len(set(compiled_program) - {"program", "labels", "symbols"}) != 0:
            # raise DgtoolsErrorDgbarchiveCorrupted(f"Archive corrupted.")        

        if "version" not in archive_sections:
            archive_sections.update({"version":"1.0.0"})
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
