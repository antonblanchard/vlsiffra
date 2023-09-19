from amaranth import Elaboratable, Instance


class GenericProcess(Elaboratable):

    """ Maps to a set of generic cell names. """

    def _PoweredInstance(self, *args, **kwargs):
        if self._powered:
            kwargs.update({
                "i_VDD": self.VPWR,
                "i_VSS": self.VGND,
            })
        return Instance(*args, **kwargs)

    def _generate_and(self, a, b, o):
        andgate = self._PoweredInstance(
            "and2",
            i_A1=a,
            i_A2=b,
            o_Z=o
        )

        self.m.submodules += andgate

    def _generate_xor(self, a, b, o):
        xorgate = self._PoweredInstance(
            "xor2",
            i_A1=a,
            i_A2=b,
            o_Z=o
        )

        self.m.submodules += xorgate

    def _generate_inv(self, a, o):
        invgate = self._PoweredInstance(
            "inv",
            i_I=a,
            o_ZN=o
        )

        self.m.submodules += invgate

    def _generate_full_adder(self, a, b, carry_in, sum_out, carry_out, name=None):
        fa = self._PoweredInstance(
            "addf",
            o_CO=carry_out,
            o_S=sum_out,
            i_A=a,
            i_B=b,
            i_CI=carry_in
        )
        if name:
            self.m.submodules[name] = fa
        else:
            self.m.submodules += fa

    def _generate_half_adder(self, a, b, sum_out, carry_out, name=None):
        ha = self._PoweredInstance(
            "addh",
            o_CO=carry_out,
            o_S=sum_out,
            i_A=a,
            i_B=b
        )

        if name:
            self.m.submodules[name] = ha
        else:
            self.m.submodules += ha

    # Used in adder
    def _generate_ao21(self, a1, a2, b1, o):
        """ 2-input AND into first input of 2-input OR. """
        ao21gate = self._PoweredInstance(
            "ao21",
            i_A1=a1,
            i_A2=a2,
            i_B=b1,
            o_Z=o
        )
        self.m.submodules += ao21gate

    # Used in multiplier
    def _generate_ao22(self, a1, a2, b1, b2, o):
        """ 2-input AND into both inputs of 2-input OR. """
        ao22gate = self._PoweredInstance(
            "ao22",
            i_A1=a1,
            i_A2=a2,
            i_B1=b1,
            i_B2=b2,
            o_Z=o
        )
        self.m.submodules += ao22gate

    # Used in multiplier
    def _generate_oai33(self, a1, a2, a3, b1, b2, b3, o):
        """ 2 3-input OR into 2-input NAND. """
        oai33gate = self._PoweredInstance(
            "oai33",
            i_A1=a1,
            i_A2=a2,
            i_A3=a3,
            i_B1=b1,
            i_B2=b2,
            i_B3=b3,
            o_ZN=o
        )

        self.m.submodules += oai33gate
