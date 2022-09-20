from .sky130hd import SKY130HDProcess
from .asap7 import ASAP7Process
from .gf180mcu import GF180MCUProcess
from .none import NoneProcess


class Tech:
    def get_tech(self, name):
        tech = NoneProcess
        if name:
            if name == 'none':
                tech = NoneProcess
            elif name == 'sky130hd':
                tech = SKY130HDProcess
            elif name == 'asap7':
                tech = ASAP7Process
            elif name == 'gf180mcu':
                tech = GF180MCUProcess
            else:
                raise Exception('Unknown Technology')
        return tech
