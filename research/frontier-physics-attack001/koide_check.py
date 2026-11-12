"""Exact algebra + decimal-data check of Koide's empirical mass relation.

Data: PDG 2025 update tau mass 1776.93 +/- 0.09 MeV, electron and muon
reference pole masses in MeV. These data are *not* a first-principles
flavor derivation; uncertainties and renormalization conventions matter.
"""
from decimal import Decimal, getcontext
import sympy as sp


def main():
    a,b,x=sp.symbols('a b x',positive=True)
    polynomial=sp.expand(3*(a*a+b*b+x*x)-2*(a+b+x)**2)
    assert sp.expand(polynomial-(a*a+b*b+x*x-4*(a*b+a*x+b*x)))==0
    branches=sp.solve(polynomial,x)
    positive_branch=2*(a+b)+sp.sqrt(3*(a*a+4*a*b+b*b))
    assert any(sp.simplify(v-positive_branch)==0 for v in branches)

    getcontext().prec=45
    me=Decimal('0.51099895')
    mm=Decimal('105.6583755')
    mt=Decimal('1776.93')
    A=me.sqrt(); B=mm.sqrt(); C=mt.sqrt()
    Q=(me+mm+mt)/(A+B+C)**2
    tau_pred=(2*(A+B)+(3*(me+4*A*B+mm)).sqrt())**2
    print('PASS Koide polynomial:', polynomial)
    print('PDG 2025-update inputs (MeV):',me,mm,mt,'tau uncertainty +/-0.09 MeV')
    print('empirical Q:',Q)
    print('Q - 2/3:',Q-Decimal(2)/3)
    print('predicted tau from e and mu assuming exact Q=2/3:',tau_pred)
    print('predicted minus reported tau (MeV):',tau_pred-mt)
    print('SCOPE: a one-constraint two-input mass relation, not an origin of masses')


if __name__ == '__main__':
    main()
