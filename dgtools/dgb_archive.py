"""

Archive to store Digirule2 binaries

:author: Athanasios Anastasiou
:date: April 2020
"""

import sys
import json
import copy
from dgtools.exceptions import DgtoolsErrorDgbarchiveCorrupted

class DGB_Archive:
    """
    Implements functionality to store, modify and retrieve DGB archives.
    """
    def __init__(self, compiled_program, labels, symbols, version="1.0.0"):
        """
        Initialisation
        
        :param compiled_program: The result of the assembling process
        :type compiled_program: list<int>
        :param labels: Lookup of labels and their offsets within the memory space
        :type labels: dict<str:int>
        :param symbols: Lookup of symbols and the offset within the code the symbol appears in
        :type symbols: dict<str:int>
        :param version: The version of hardware this program is compiled for
        :type version: str
        """
        self._sections = {"program":compiled_program,"labels":labels,"symbols":symbols, "version":version}
        
    def save(self, filename):
        with open(filename, "wt") as fd:
            json.dump(self._sections, fd, indent=4)
        return self

    @classmethod
    def from_archive(cls, other_archive):
        self._sections = copy.deepcopy(other_archive._sections)
        return self
        
    @classmethod    
    def load(cls,filename):
        with open(filename, "rt") as fd:
            archive_sections = json.load(fd)

        if type(archive_sections) is not dict:
            raise DgtoolsErrorDgbarchiveCorrupted("DGB archive corrupted.")
            
        if not all(map(lambda field:field in archive_sections, ["program", "labels", "symbols"])):
            raise DgtoolsErrorDgbarchiveCorrupted("DGB archive corrupted.")
                           
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
