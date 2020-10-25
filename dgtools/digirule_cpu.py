from .dgcpu_base import DGMemorySpaceBase, DGCPU

class MemorySpaceDigirule(DGMemorySpaceBase):
    def __init__(self):
        super().DGMemorySpaceBase.__init__()
        self._mem_base = 3
        self._reg_map = {"Acc":0,
                         "SPEED":1,
                         "INPUT":253 + self._mem_base,
                         "ADDR_LED":254 + self._mem_base,
                         "DATA_LED":255 + self._mem_base,
                         "STATUS":252 + self._mem_base,
                         "PC":2}
        self._mem_len = 256
        self._mem = bytearray([0 for k in range(0, self._mem_len + self._mem_base)])
        
class Digirule2(CPU):
    def __init__(self):
        super().__init__()
        self._mem_space = MemorySpaceDigirule()
        self._pc_reg = "PC"
        self._ins_lookup={0:self._ins_halt}
        
    def _ins_halt(self):
        print("THE END");
