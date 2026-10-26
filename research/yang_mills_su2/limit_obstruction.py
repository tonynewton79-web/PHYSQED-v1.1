"""Exact counterexample to a finite-positive-gap => continuum-gap inference.

This deliberately elementary family is not a lattice Yang–Mills spectrum.
"""

from fractions import Fraction


def collapsing_gap(n: int) -> dict[str, object]:
    if type(n) is not int or n < 1:
        raise ValueError("positive integer index required")
    spacing = Fraction(1, n)
    lattice_gap = spacing**2
    return {
        "lattice_spacing": spacing,
        "dimensionless_gap": lattice_gap,
        "physical_gap": lattice_gap / spacing,
        "status": "COUNTEREXAMPLE_TO_FINITE_GAP_INFERENCE",
        "scope": "abstract positive-gap sequence, not a Yang-Mills field theory",
    }
