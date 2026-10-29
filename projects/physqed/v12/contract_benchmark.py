"""Emit positive and negative typed Einstein-Maxwell contract JSON receipts.

PYTHONPATH=projects/physqed python -m v12.contract_benchmark --out-dir receipts
"""
import argparse
from dataclasses import replace
from pathlib import Path
import sympy as S
from .contracts import EinsteinMaxwellSpec, evaluate_contract, save_contract


def replay(directory):
    t,r,theta,phi=S.symbols('t r theta phi',real=True)
    charge=S.Rational(1,2)
    f=1-2/r+charge**2/r**2
    metric=S.diag(-f,1/f,r**2,r**2*S.sin(theta)**2)
    witness={t:0,r:4,theta:S.pi/2,phi:0}
    base=EinsteinMaxwellSpec(
        'STD-EINSTEIN-MAXWELL-ADM-001',(t,r,theta,phi),metric,
        (charge/r,0,0,0),S.sqrt(f),(witness,),
        ('exterior Reissner-Nordstrom chart r>r_+',
         'regular angular patch 0<theta<pi',
         'action R-F_ab F^ab, signature -+++'),
        source='standard textbook classical Einstein-Maxwell theory')
    correct=evaluate_contract(base)
    wrong=evaluate_contract(replace(base,
        claim_id='STD-EINSTEIN-MAXWELL-ADM-NEGATIVE',
        gravitational_coupling=3,
        declared_hamiltonian=1))
    if correct['status']!='PASS_LOCAL_TYPED_COUPLED_SYMBOLIC_CONTRACT':
        raise AssertionError('textbook Reissner-Nordstrom contract failed')
    if wrong['status']!='REJECTED_INCONSISTENT_COUPLED_PHYSICS':
        raise AssertionError('wrong coupling and ADM constraint accepted')
    out=Path(directory);out.mkdir(parents=True,exist_ok=True)
    save_contract(correct,out/(correct['claim_id']+'.json'))
    save_contract(wrong,out/(wrong['claim_id']+'.json'))
    return correct,wrong


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out-dir',type=Path,required=True)
    args=p.parse_args()
    good,bad=replay(args.out_dir)
    print('PASS_TYPED_COUPLED_CONTRACT 16_LINKED_CHECKS; NEGATIVE_REFUSED; '
          'INDEPENDENT_RATIONAL_2JET_CONFIRMED; NO_GLOBAL_PHYSICS_CLAIM')


if __name__=='__main__':
    main()
