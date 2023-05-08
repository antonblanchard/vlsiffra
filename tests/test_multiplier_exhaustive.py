import math
import unittest
from amaranth.sim import Simulator, Settle

from vlsiffra.adder import BrentKung
from vlsiffra.multiplier import Multiplier, BoothRadix4, Dadda
from vlsiffra.tech.none import NoneProcess


class TestAdder(BrentKung, NoneProcess):
    pass


class TestMultiplier(Multiplier, BoothRadix4, Dadda, NoneProcess):
    pass


class TestCaseExhaustive8(unittest.TestCase):
    def setUp(self):
        self.bits = 8
        self.dut = TestMultiplier(adder=TestAdder, bits=self.bits)

    def do_one_comb(self, a, b):
        yield self.dut.a.eq(a)
        yield self.dut.b.eq(b)
        yield Settle()
        res = (yield self.dut.o)
        self.assertEqual(res, a * b)

    def test_exhaustive(self):
        def bench():
            for a in range(int(math.pow(self.bits, 2))):
                for b in range(int(math.pow(self.bits, 2))):
                    yield from self.do_one_comb(a, b)

        sim = Simulator(self.dut)
        sim.add_process(bench)
        with sim.write_vcd("multiplier_exhaustive8.vcd"):
            sim.run()


class TestCaseExhaustive7(unittest.TestCase):
    def setUp(self):
        self.bits = 7
        self.dut = TestMultiplier(adder=TestAdder, bits=self.bits)

    def do_one_comb(self, a, b):
        yield self.dut.a.eq(a)
        yield self.dut.b.eq(b)
        yield Settle()
        res = (yield self.dut.o)
        self.assertEqual(res, a * b)

    def test_exhaustive(self):
        def bench():
            for a in range(int(math.pow(self.bits, 2))):
                for b in range(int(math.pow(self.bits, 2))):
                    yield from self.do_one_comb(a, b)

        sim = Simulator(self.dut)
        sim.add_process(bench)
        with sim.write_vcd("multiplier_exhaustive7.vcd"):
            sim.run()


if __name__ == '__main__':
    unittest.main()
