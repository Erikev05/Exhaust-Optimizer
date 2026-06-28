"""
Bell's exhaust runner length formula
"""



def primary_length(RPM: float, T0: float, EVO: float) -> float:
    """
    Calculate optimal exhaust primary length using Bell's formula.

    Args:
        RPM:  Engine speed (rev/min)
        T0:   Exhaust gas temperature at port (K)
        EVO:  Exhaust valve opening angle (degrees BBDC)

    Returns:
        Primary pipe length (m)
    """

    return ((T0 * (360 - EVO) / RPM) - 3) * 25.4 / 1000