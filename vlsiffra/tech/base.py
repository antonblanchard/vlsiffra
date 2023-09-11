from amaranth import Elaboratable

# The following shell command can be used to discover the usage;
# grep -R '_generate_'  | sed -e's/: */:/' -e's/(.*/(/' | sort | uniq | less


class Process(Elaboratable):
    """ Base class for process technologies. """

    def _PoweredInstance(self, *args, **kwargs):
        pass

    # Standard cells used in *both* `adders.py` and `multipliers.py`

    def _generate_and(self, a, b, o):
        """2 input AND gate.

        Used by both `adders.py` and `multipliers.py`.
        """
        raise NotImplementedError()

    def _generate_xor(self, a, b, o):
        """2 input XOR gate.

        Used by both `adders.py` and `multipliers.py`.
        """
        raise NotImplementedError()

    def _generate_full_adder(self, a, b, carry_in, sum_out, carry_out, name=None):
        """Full adder.

        Used by both `adders.py` and `multipliers.py`.
        """
        raise NotImplementedError()

    def _generate_half_adder(self, a, b, sum_out, carry_out, name=None):
        """Half adder.

        Used by both `adders.py` and `multipliers.py`.
        """
        raise NotImplementedError()

    # Standard cells used only in adders
    def _generate_ao21(self, a1, a2, b1, o):
        """2-input AND into first input of 2-input OR.

        Used by `adders.py`.
        """
        raise NotImplementedError()

    # Standard cells used only in `multipliers.py`
    def _generate_inv(self, a, o):
        """1-bit inverter.

        Used by `multipliers.py`.
        """
        raise NotImplementedError()

    def _generate_ao22(self, a1, a2, b1, b2, o):
        """2-input AND into both inputs of 2-input OR.

        Used by `multipliers.py`.
        """
        raise NotImplementedError()

    def _generate_ao32(self, a1, a2):
        """3-input AND into first input, and 2-input AND into 2nd input of 2-input OR.

        Used by `multipliers.py`.
        """
        raise NotImplementedError()

    def _generate_ao33(self, a1, a2, a3, b1, b2, b3, o):
        """3-input AND into both inputs of 2-input OR.

        Optional, a `oai33` cell can be provided instead.

        Used by `multipliers.py`.
        """
        raise AttributeError()

    def _generate_oai33(self, a1, a2, a3, b1, b2, b3, o):
        """3-input AND into both inputs of 2-input OR.

        Optional, can be provided instead of the `ao33` cell.

        Used by `multipliers.py`.
        """
        raise AttributeError()
