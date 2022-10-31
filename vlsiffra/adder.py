import math

from amaranth import Elaboratable, Module, Signal, Const


class AdderFramework(Elaboratable):
    def __init__(self, bits=64, register_input=False, register_output=False, powered=False):
        self.a = Signal(bits)
        self.b = Signal(bits)
        self.o = Signal(bits)

        if powered:
            self._powered = True
            self.VPWR = Signal()
            self.VGND = Signal()
        else:
            self._powered = False

        self._bits = bits
        self._register_input = register_input
        self._register_output = register_output

    def elaborate(self, platform):
        self.m = m = Module()

        a = Signal(self._bits, reset_less=True)
        b = Signal(self._bits, reset_less=True)
        if self._register_input:
            m.d.sync += [
                a.eq(self.a),
                b.eq(self.b),
            ]
        else:
            m.d.comb += [
                a.eq(self.a),
                b.eq(self.b),
            ]

        # Use arrays of 1 bit signals to make it easy to create
        # trees of p and g updates.
        self._p = [Signal() for i in range(self._bits)]
        self._g = [Signal() for i in range(self._bits)]

        for i in range(self._bits):
            self._generate_half_adder(a[i], b[i], self._p[i], self._g[i])

        # We need a copy of p
        p_tmp = [Signal() for i in range(self._bits)]
        for i in range(self._bits):
            m.d.comb += p_tmp[i].eq(self._p[i])

        self._calculate_pg()

        # g is the carry out signal. We need to shift it left one bit then
        # xor it with the sum (ie p_tmp). Since we have a list of 1 bit
        # signals, just insert a constant zero signal at the head of of the
        # list to shift g.
        self._g.insert(0, Const(0))

        o = Signal(self._bits)
        for i in range(self._bits):
            # This also flattens the list of bits when writing to o
            self._generate_xor(p_tmp[i], self._g[i], o[i])

        o2 = Signal(self._bits, reset_less=True)
        if self._register_output:
            m.d.sync += o2.eq(o)
        else:
            m.d.comb += o2.eq(o)

        m.d.comb += self.o.eq(o2)
        return m


class BrentKung(AdderFramework):
    def _calculate_pg(self):
        # Calculate the p and g for the odd bits
        for level in range(1, int(math.log(self._bits, 2)) + 1):
            for bit_to in range(2**level - 1, self._bits, 2**level):
                bit_from = bit_to - 2**(level - 1)
                p_new = Signal()
                g_new = Signal()
                self._generate_and(self._p[bit_to], self._p[bit_from], p_new)
                self._generate_ao21(self._p[bit_to], self._g[bit_from], self._g[bit_to], g_new)
                self._p[bit_to] = p_new
                self._g[bit_to] = g_new

        # Calculate g for the even bits
        for level in range(int(math.log(self._bits, 2)), 0, -1):
            for bit_to in range(2**level + 2**(level - 1) - 1, self._bits, 2**level):
                bit_from = bit_to - 2**(level - 1)
                g_new = Signal()
                self._generate_ao21(self._p[bit_to], self._g[bit_from], self._g[bit_to], g_new)
                self._g[bit_to] = g_new


class KoggeStone(AdderFramework):
    def _calculate_pg(self):
        # Calculate p and g
        for level in range(0, int(math.log(self._bits, 2))):
            # Iterate backwards, because we want p and g from the previous iteration
            # and we update them as we go in this loop
            for bit_from in range(self._bits - 2**level - 1, -1, -1):
                bit_to = bit_from + 2**level
                p_new = Signal()
                g_new = Signal()
                self._generate_and(self._p[bit_from], self._p[bit_to], p_new)
                self._generate_ao21(self._p[bit_to], self._g[bit_from], self._g[bit_to], g_new)
                self._p[bit_to] = p_new
                self._g[bit_to] = g_new


# Han Carlson is Kogge Stone on odd bits, with a final stage to calculate the even bits
class HanCarlson(AdderFramework):
    def _calculate_pg(self):
        # Calculate p and g
        for level in range(0, int(math.log(self._bits, 2))):
            # Iterate backwards, because we want p and g from the previous iteration
            # and we update them as we go in this loop
            for bit_from in range(self._bits - 2**level - 1, -1, -1):
                bit_to = bit_from + 2**level
                # Kogge Stone on odd bits only
                if (bit_to & 1) == 0:
                    continue
                p_new = Signal()
                g_new = Signal()
                self._generate_and(self._p[bit_from], self._p[bit_to], p_new)
                self._generate_ao21(self._p[bit_to], self._g[bit_from], self._g[bit_to], g_new)
                self._p[bit_to] = p_new
                self._g[bit_to] = g_new

        # Now do the even bits, again working backwards
        for bit_from in range(self._bits - 3, 0, -2):
            bit_to = bit_from + 1
            g_new = Signal()
            self._generate_ao21(self._p[bit_to], self._g[bit_from], self._g[bit_to], g_new)
            self._g[bit_to] = g_new


class Inferred(Elaboratable):
    def __init__(self, bits=64, register_input=False, register_output=False, powered=False):
        self.a = Signal(bits)
        self.b = Signal(bits)
        self.o = Signal(bits)

        self._bits = bits
        self._register_input = register_input
        self._register_output = register_output

    def elaborate(self, platform):
        self.m = m = Module()

        a = Signal(self._bits, reset_less=True)
        b = Signal(self._bits, reset_less=True)
        if self._register_input:
            m.d.sync += [
                a.eq(self.a),
                b.eq(self.b),
            ]
        else:
            m.d.comb += [
                a.eq(self.a),
                b.eq(self.b),
            ]

        o = Signal(self._bits)
        self.m.d.comb += o.eq(self.a + self.b)

        o2 = Signal(self._bits, reset_less=True)
        if self._register_output:
            m.d.sync += o2.eq(o)
        else:
            m.d.comb += o2.eq(o)

        m.d.comb += self.o.eq(o2)
        return m


class Ripple(Elaboratable):
    def __init__(self, bits=64, register_input=False, register_output=False,
                 carry_in=False, carry_out=False, powered=False):
        self.a = Signal(bits)
        self.b = Signal(bits)
        self.o = Signal(bits)

        if carry_in:
            self._carry_in = True
            self.carry_in = Signal()
        else:
            self._carry_in = False

        if carry_out:
            self._carry_out = True
            self.carry_out = Signal()
        else:
            self._carry_out = False

        if powered:
            self._powered = True
            self.VPWR = Signal()
            self.VGND = Signal()
        else:
            self._powered = False

        self._bits = bits
        self._register_input = register_input
        self._register_output = register_output

    def elaborate(self, platform):
        self.m = m = Module()

        a = Signal(self._bits, reset_less=True)
        b = Signal(self._bits, reset_less=True)
        o = Signal(self._bits, reset_less=True)
        ci = Signal(self._bits, reset_less=True)
        co = Signal(self._bits, reset_less=True)

        if self._register_input:
            m.d.sync += [
                a.eq(self.a),
                b.eq(self.b),
            ]
            if self._carry_in:
                m.d.sync += ci[0].eq(self.carry_in)

        else:
            m.d.comb += [
                a.eq(self.a),
                b.eq(self.b),
            ]
            if self._carry_in:
                m.d.comb += ci[0].eq(self.carry_in)

        for i in range(0, self._bits):
            if i == 0 and not self._carry_in:
                self._generate_half_adder(a[i], b[i], o[i], co[i])
            else:
                self._generate_full_adder(a[i], b[i], ci[i], o[i], co[i])

            # carry chain
            if i != 0:
                m.d.comb += ci[i].eq(co[i - 1])

        if self._carry_out:
            if self._register_output:
                m.d.sync += self.carry_out.eq(co[self._bits - 1])
            else:
                m.d.comb += self.carry_out.eq(co[self._bits - 1])

        o2 = Signal(self._bits, reset_less=True)
        if self._register_output:
            m.d.sync += o2.eq(o)
        else:
            m.d.comb += o2.eq(o)

        m.d.comb += self.o.eq(o2)
        return m
