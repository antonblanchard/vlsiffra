import unittest
import random
from amaranth.sim import Simulator, Settle

from vlsi_arithmetic.adder import BrentKung
from vlsi_arithmetic.multiplier import Multiplier, BoothRadix4, Dadda
from vlsi_arithmetic.tech.none import NoneProcess


class TestAdder(BrentKung, NoneProcess):
    pass


class TestMultiplier(Multiplier, BoothRadix4, Dadda, NoneProcess):
    pass


class TestCaseRandom(unittest.TestCase):
    def setUp(self):
        self.bits = 32
        self.dut = TestMultiplier(adder=TestAdder, bits=self.bits)

    def do_one_comb(self, a, b):
        yield self.dut.a.eq(a)
        yield self.dut.b.eq(b)
        yield Settle()
        res = (yield self.dut.o)
        self.assertEqual(res, a * b)

    def test_random(self):
        def bench():
            for i in range(100):
                rand_a = random.getrandbits(self.bits)
                rand_b = random.getrandbits(self.bits)
                yield from self.do_one_comb(rand_a, rand_b)

        sim = Simulator(self.dut)
        sim.add_process(bench)
        with sim.write_vcd("multiplier_random.vcd"):
            sim.run()


if __name__ == '__main__':
    unittest.main()
