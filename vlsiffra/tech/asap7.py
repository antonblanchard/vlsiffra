from amaranth import Instance, Signal
from .base import Process


class ASAP7Process(Process):
    def _PoweredInstance(self, *args, **kwargs):
        if self._powered:
            kwargs.update({
                "i_VDD": self.VPWR,
                "i_VSS": self.VGND,
            })
        return Instance(*args, **kwargs)

    def _generate_and(self, a, b, o):
        andgate = self._PoweredInstance(
            "AND2x2_ASAP7_75t_R",
            i_A=a,
            i_B=b,
            o_Y=o
        )

        self.m.submodules += andgate

    def _generate_xor(self, a, b, o):
        xorgate = self._PoweredInstance(
            "XOR2x1_ASAP7_75t_R",
            i_A=a,
            i_B=b,
            o_Y=o
        )

        self.m.submodules += xorgate

    def _generate_inv(self, a, o):
        invgate = self._PoweredInstance(
            "INVx1_ASAP7_75t_R",
            i_A=a,
            o_Y=o
        )

        self.m.submodules += invgate

    def _generate_full_adder(self, a, b, carry_in, sum_out, carry_out, name=None):
        con = Signal()
        sn = Signal()

        fa = self._PoweredInstance(
            "FAx1_ASAP7_75t_R",
            o_CON=con,
            o_SN=sn,
            i_A=a,
            i_B=b,
            i_CI=carry_in
        )
        if name:
            self.m.submodules[name] = fa
        else:
            self.m.submodules += fa

        inv1 = self._PoweredInstance(
            "INVx1_ASAP7_75t_R",
            i_A=con,
            o_Y=carry_out
        )
        self.m.submodules += inv1

        inv2 = self._PoweredInstance(
            "INVx1_ASAP7_75t_R",
            i_A=sn,
            o_Y=sum_out
        )
        self.m.submodules += inv2

    def _generate_half_adder(self, a, b, sum_out, carry_out, name=None):
        con = Signal()
        sn = Signal()

        ha = self._PoweredInstance(
            "HAxp5_ASAP7_75t_R",
            o_CON=con,
            o_SN=sn,
            i_A=a,
            i_B=b
        )

        if name:
            self.m.submodules[name] = ha
        else:
            self.m.submodules += ha

        inv1 = self._PoweredInstance(
            "INVx1_ASAP7_75t_R",
            i_A=con,
            o_Y=carry_out
        )
        self.m.submodules += inv1

        inv2 = self._PoweredInstance(
            "INVx1_ASAP7_75t_R",
            i_A=sn,
            o_Y=sum_out
        )
        self.m.submodules += inv2

    # Used in adder
    def _generate_ao21(self, a1, a2, b1, o):
        """ 2-input AND into first input of 2-input OR. """
        a21o = self._PoweredInstance(
            "AO21x1_ASAP7_75t_R",
            o_Y=o,
            i_A1=a1,
            i_A2=a2,
            i_B=b1
        )

        self.m.submodules += a21o

    # Used in multiplier
    def _generate_ao22(self, a1, a2, b1, b2, o):
        """ 2-input AND into both inputs of 2-input OR. """
        a22ogate = self._PoweredInstance(
            "AO22x1_ASAP7_75t_R",
            i_A1=a1,
            i_A2=a2,
            i_B1=b1,
            i_B2=b2,
            o_Y=o
        )

        self.m.submodules += a22ogate

    # Used in multiplier
    def _generate_ao33(self, a1, a2, a3, b1, b2, b3, o):
        """ 3-input AND into both inputs of 2-input OR. """
        ao33gate = self._PoweredInstance(
            "AO33x2_ASAP7_75t_R",
            i_A1=a1,
            i_A2=a2,
            i_A3=a3,
            i_B1=b1,
            i_B2=b2,
            i_B3=b3,
            o_Y=o
        )

        self.m.submodules += ao33gate
