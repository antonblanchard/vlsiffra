from amaranth import Instance
from .base import Process


"""
Skywater's 130nm process technology with Google open source PDK found at
https://github.com/google/skywater-pdk and https://skywater-pdk.readthedocs.io

The process technology offers `multiple standard cell libraries <libraries>`_
with different trade offs. The `Standard Cells Library Index Spreadsheet
<stdindex>`_ is useful to understand what cells exist in which libraries.

.. _libraries: https://skywater-pdk.readthedocs.io/en/main/contents/libraries/foundry-provided.html
.. _stdindex: https://docs.google.com/spreadsheets/d/1KMZ215M_7YQb0l-vCyVdzSsRzaSJN4VVGsTwf4wFK3k/edit#gid=139199577
"""


class SKY130Process(Process):
    LIBRARY = None

    def _PoweredInstance(self, *args, **kwargs):
        if self._powered:
            kwargs.update({
                "i_VPWR": self.VPWR,
                "i_VPB": self.VPWR,
                "i_VGND": self.VGND,
                "i_VNB": self.VGND
            })
        return Instance(*args, **kwargs)

    def _generate_and(self, a, b, o):
        andgate = self._PoweredInstance(
            self.LIBRARY + "__and2_1",
            i_A=a,
            i_B=b,
            o_X=o
        )

        self.m.submodules += andgate

    def _generate_xor(self, a, b, o):
        xorgate = self._PoweredInstance(
            self.LIBRARY + "__xor2_1",
            i_A=a,
            i_B=b,
            o_X=o
        )

        self.m.submodules += xorgate

    def _generate_inv(self, a, o):
        invgate = self._PoweredInstance(
            self.LIBRARY + "__inv_1",
            i_A=a,
            o_Y=o
        )

        self.m.submodules += invgate

    def _generate_full_adder(self, a, b, carry_in, sum_out, carry_out, name=None):
        fa = self._PoweredInstance(
            self.LIBRARY + "__fa_1",
            o_COUT=carry_out,
            o_SUM=sum_out,
            i_A=a,
            i_B=b,
            i_CIN=carry_in
        )
        if name:
            self.m.submodules[name] = fa
        else:
            self.m.submodules += fa

    def _generate_half_adder(self, a, b, sum_out, carry_out, name=None):
        ha = self._PoweredInstance(
            self.LIBRARY + "__ha_1",
            o_COUT=carry_out,
            o_SUM=sum_out,
            i_A=a,
            i_B=b
        )

        if name:
            self.m.submodules[name] = ha
        else:
            self.m.submodules += ha

    # Used in adder
    def _generate_ao21(self, a1, a2, b1, o):
        # 2-input AND into first input of 2-input OR
        a21o = self._PoweredInstance(
            self.LIBRARY + "__a21o_1",
            o_X=o,
            i_A1=a1,
            i_A2=a2,
            i_B1=b1
        )

        self.m.submodules += a21o

    # Used in multiplier
    def _generate_ao22(self, a1, a2, b1, b2, o):
        # 2-input AND into both inputs of 2-input OR
        a22ogate = self._PoweredInstance(
            self.LIBRARY + "__a22o_1",
            i_A1=a1,
            i_A2=a2,
            i_B1=b1,
            i_B2=b2,
            o_X=o
        )

        self.m.submodules += a22ogate

    # Used in multiplier
    def _generate_ao32(self, a1, a2, a3, b1, b2, o):
        # 3-input AND into first input, and 2-input AND into 2nd input of 2-input OR
        a32ogate = self._PoweredInstance(
            self.LIBRARY + "__a32o_1",
            i_A1=a1,
            i_A2=a2,
            i_A3=a3,
            i_B1=b1,
            i_B2=b2,
            o_X=o
        )

        self.m.submodules += a32ogate


class SKY130HSProcess(SKY130Process):
    """ SKY130 process technology with high speed standard cells.

    Libraries sky130_fd_sc_hs (high speed), sky130_fd_sc_ms (medium speed),
    sky130_fd_sc_ls (low speed), and sky130_fd_sc_lp (low power) are compatible
    in size, with a 0.48 x 3.33um site, equivalent to about 11 met1 tracks.

    The medium and low speed can be swapped in after place and route to reduce
    power consumption.
    """

    LIBRARY = "sky130_fd_sc_hs"


class SKY130HDProcess(SKY130Process):
    """ SKY130 process technology with high density standard cells.

    Libraries sky130_fd_sc_hd (high density) and sky130_fd_sc_hdll (high
    density, low leakage) contain standard cells that are smaller, utilizing a
    0.46 x 2.72um site, equivalent to 9 met1 tracks.
    """

    LIBRARY = "sky130_fd_sc_hd"


class SKY130HVLProcess(SKY130Process):
    """ SKY130 process technology with high voltage standard cells.

    The sky130_fd_sc_hvl (high voltage) library contains 5V devices and
    utilizes a 0.48 x 4.07um site, or 14 met1 tracks.

    The high voltage library is missing a number of standard cells,
     * a211o
     * a211oi
     * a21bo
     * xnor3
     * xor3
    """

    LIBRARY = "sky130_fd_sc_hvl"
