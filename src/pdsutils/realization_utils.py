import math

def _determine_prefix(prefix: str, reals: int) -> str:
    """Counts the number of digits in an integer using logarithm.
    """

    digits = 1
    if reals == 0:
        digits = 1
    else:
        digits = math.floor(math.log10(abs(reals))) + 1

    if digits == 1:
        return prefix + "0" + ("" if prefix == "Case" else "0")

    if digits == 2:
        return prefix + "" + ("" if prefix == "Case" else "0")

    return prefix