"""

Archive to store Digirule2 binaries

:author: Athanasios Anastasiou
:date: April 2020
"""

import sys
import json
import copy
from .exceptions import DgtoolsErrorDgbarchiveCorrupted

class DGB_Archive:
    """
    Implements functionality to store, modify and retrieve DGB archives.
    """
    def __init__(self, compiled_program, labels, version="2A"):
        """
        Initialisation
        
        :param compiled_program: The result of the assembling process
        :type compiled_program: list<int>
        :param labels: Lookup of labels and their offsets within the memory space
        :type labels: dict<str:int>
        :param version: The version of hardware this program is compiled for
        :type version: str
        """
        self._sections = {"program":compiled_program,"labels":labels, "version":version}
        
    def save(self, filename):
        with open(filename, "wt") as fd:
            json.dump(self._sections, fd, indent=4)
        return self

    @classmethod
    def from_archive(cls, other_archive):
        copied_sections = copy.deepcopy(other_archive._sections)
        if "version" in copied_sections:
            return cls(copied_sections["program"],copied_sections["labels"], copied_sections["version"])
        else:
            return cls(copied_sections["program"],copied_sections["labels"])
        
    @classmethod    
    def load(cls,filename):
        with open(filename, "rt") as fd:
            archive_sections = json.load(fd)

        if type(archive_sections) is not dict:
            raise DgtoolsErrorDgbarchiveCorrupted("DGB archive corrupted.")
            
        if not all(map(lambda field:field in archive_sections, ["program", "labels"])):
            raise DgtoolsErrorDgbarchiveCorrupted("DGB archive corrupted.")
                           
        if "version" not in archive_sections:
            archive_sections.update({"version":"2A"})
        return cls(archive_sections["program"], archive_sections["labels"], archive_sections["version"]) 
        
    @property
    def program(self):
        return self._sections["program"]
        
    @property
    def labels(self):
        return self._sections["labels"]
        
    @property
    def version(self):
        return self._sections["version"]
