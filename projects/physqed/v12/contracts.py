"""PHYSQED v1.2: typed, fail-closed, coupled Einstein--Maxwell/ADM contract.

All conclusions are chart-local symbolic identities under explicit conventions.
Exact pointwise rational 2-jet curvature is computed by the separate stdlib
oracle. Pointwise agreement does NOT establish a global symbolic identity.
No input is evaluated as Python code; caller supplies constructed SymPy objects.

Conventions: signature (-,+,+,+), zero shift, future normal n=(1/N,0,0,0),
K_ij=+(1/(2N)) partial_t h_ij, action R-F_ab F^ab (kappa=2).
The Einstein residual is E_ab=G_ab + Lambda g_ab - kappa T_ab.
ADM Hamiltonian H = R3+K^2-Kij K^ij - 2 Lambda - 2 kappa rho
and momentum M_i=D_j K^j_i-D_i K - kappa T_0i/N.
The bridges are H=2 E_00/N^2 and M_i=E_0i/N.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from itertools import product
import json
import sympy as S
from .geometry import Geometry, ScopeError, zero
from .coupled import (maxwell_bianchi, maxwell_equations, maxwell_stress,
                      covariant_divergence_stress)
from .jet_oracle import curvature_from_jet

SCHEMA = 'physqed-v1.2-coupled-contract-1'


def _exact_zero(value):
    try:
        if zero(value):
            return True
        return S.simplify(S.cancel(S.together(S.trigsimp(S.expand_trig(value))))) == 0
    except (TypeError, ValueError, ZeroDivisionError, NotImplementedError):
        return False


def _flatten(value):
    if isinstance(value, S.MatrixBase):
        return list(value)
    if isinstance(value, S.NDimArray):
        return [value[index] for index in product(*(range(v) for v in value.shape))]
    if isinstance(value, (tuple,list)):
        out=[]
        for x in value:
            out.extend(_flatten(x))
        return out
    return [S.sympify(value)]


def _rational_at(expr, subs):
    value=S.simplify(S.sympify(expr).subs(subs))
    if value.free_symbols or value.is_Rational is not True:
        raise ScopeError('independent curvature oracle needs exact rational jet point')
    return str(value)


def _jet(coords, metric, witness):
    n=len(coords)
    g=S.Matrix(metric)
    return (
        [[_rational_at(g[i,j], witness) for j in range(n)] for i in range(n)],
        [[[_rational_at(S.diff(g[i,j],coords[k]), witness) for j in range(n)]
            for i in range(n)] for k in range(n)],
        [[[[_rational_at(S.diff(g[i,j],coords[k],coords[l]),witness)
              for j in range(n)] for i in range(n)]
              for l in range(n)] for k in range(n)])


def _sfrac(value):
    return S.Rational(value.numerator,value.denominator)


def _single_oracle(geometry, point):
    """Independent curvature at supplied exact rational 2-jet."""
    data=curvature_from_jet(*_jet(geometry.x,geometry.g,point))
    n=geometry.n
    errors=[]
    for i,j in product(range(n),repeat=2):
        if not _exact_zero(geometry.ricci[i,j].subs(point)-_sfrac(data['ricci'][i][j])):
            errors.append(f'Ricci[{i},{j}]')
        if not _exact_zero(geometry.einstein[i,j].subs(point)-_sfrac(data['einstein'][i][j])):
            errors.append(f'Einstein[{i},{j}]')
    if not _exact_zero(geometry.scalar.subs(point)-_sfrac(data['scalar'])):
        errors.append('scalar')
    return {'passed':not errors, 'errors':errors,
            'reference':'fractions.Fraction local metric 2-jet curvature',
            'component_count':2*n*n+1,
            'independent_numeric_curvature':True,
            'not_a_global_proof':True}


@dataclass(frozen=True)
class EinsteinMaxwellSpec:
    """Typed contract input: no field equations trusted as premises."""
    claim_id: str
    coordinates: tuple
    metric: object
    potential: tuple
    lapse: object
    witnesses: tuple
    assumptions: tuple
    cosmological_constant: object = S.S.Zero
    gravitational_coupling: object = S.Integer(2)
    source: str = 'standard textbook Einstein-Maxwell'
    declared_field_strength: object = None
    declared_stress: object = None
    declared_hamiltonian: object = None
    declared_momentum: object = None

    def validate(self):
        if not isinstance(self.claim_id,str) or not self.claim_id.strip():
            raise ScopeError('nonempty claim_id required')
        if not isinstance(self.source,str) or not self.source.strip():
            raise ScopeError('source provenance is required')
        x=tuple(self.coordinates)
        if (len(x)!=4 or len(set(x))!=4 or
                any(not isinstance(q,S.Symbol) for q in x)):
            raise ScopeError('four distinct coordinate symbols required')
        if len(self.potential)!=4:
            raise ScopeError('typed Maxwell one-form requires four components')
        if self.declared_field_strength is not None:
            declared=S.Matrix(self.declared_field_strength)
            if declared.shape!=(4,4):
                raise ScopeError('declared electromagnetic two-form must be 4x4')
            if any(not _exact_zero(declared[i,j]+declared[j,i])
                   for i,j in product(range(4),repeat=2)):
                raise ScopeError('declared electromagnetic field must be antisymmetric')
        if self.declared_stress is not None:
            declared=S.Matrix(self.declared_stress)
            if declared.shape!=(4,4):
                raise ScopeError('declared stress tensor must be 4x4')
            if any(not _exact_zero(declared[i,j]-declared[j,i])
                   for i,j in product(range(4),repeat=2)):
                raise ScopeError('declared stress tensor must be symmetric')
        if self.declared_momentum is not None and len(self.declared_momentum)!=3:
            raise ScopeError('declared momentum must contain three constraints')
        if not self.assumptions or any(not isinstance(a,str) or not a.strip() for a in self.assumptions):
            raise ScopeError('explicit nonempty domain assumptions required')
        if not self.witnesses:
            raise ScopeError('at least one exact rational metric-jet witness required')
        g=S.Matrix(self.metric)
        if g.shape!=(4,4):
            raise ScopeError('metric must be 4x4')
        N=S.sympify(self.lapse)
        if _exact_zero(N):
            raise ScopeError('zero lapse is forbidden')
        if not _exact_zero(g[0,0]+N*N):
            raise ScopeError('zero-shift lapse does not match g_00=-N^2')
        if any(not _exact_zero(g[0,i]) or not _exact_zero(g[i,0]) for i in range(1,4)):
            raise ScopeError('this ADM contract supports zero shift only')
        for witness in self.witnesses:
            if not isinstance(witness,dict) or not set(x).issubset(witness):
                raise ScopeError('complete coordinate witness map required')
            h=S.Matrix(g[1:4,1:4]).subs(witness)
            for i in range(1,4):
                principal=S.simplify(h[:i,:i].det())
                if principal.is_positive is not True:
                    raise ScopeError('spatial metric not proved positive at witness')
            ns=S.simplify(N.subs(witness))
            if ns.is_positive is not True:
                raise ScopeError('lapse must be positive at each witness')
            _jet(x,g,witness)
        if S.sympify(self.gravitational_coupling).is_zero is True:
            raise ScopeError('nonzero Einstein--matter coupling required')
        return g


@dataclass(frozen=True)
class ContractNode:
    name: str
    components: tuple
    category: str
    required: bool = True


def _node(name,value,category):
    return ContractNode(name,tuple(_flatten(value)),category)


def _spatial_divergence(geometry,Kmixed,trace_K):
    C=geometry.connection
    x=geometry.x
    n=3
    return tuple(S.simplify(
        sum(S.diff(Kmixed[j,i],x[j]) + sum(
            C[j][j][k]*Kmixed[k,i] - C[k][j][i]*Kmixed[j,k]
            for k in range(n)) for j in range(n))
        -S.diff(trace_K,x[i])) for i in range(n))


def _field_from_potential(spec):
    x=spec.coordinates
    return S.Matrix(4,4,lambda a,b:S.simplify(
        S.diff(spec.potential[b],x[a])-S.diff(spec.potential[a],x[b])))


def evaluate_contract(spec: EinsteinMaxwellSpec):
    """Compute all typed nodes; accept only if equations and bridges pass."""
    if not isinstance(spec,EinsteinMaxwellSpec):
        raise ScopeError('typed EinsteinMaxwellSpec required')
    g=spec.validate()
    x=spec.coordinates
    N=S.sympify(spec.lapse)
    lam=S.sympify(spec.cosmological_constant)
    kappa=S.sympify(spec.gravitational_coupling)
    full=Geometry(x,g)
    F_from_A=_field_from_potential(spec)
    F=(S.Matrix(spec.declared_field_strength) if
       spec.declared_field_strength is not None else F_from_A)
    T_derived=maxwell_stress(full,F)
    T=(S.Matrix(spec.declared_stress) if spec.declared_stress is not None
       else T_derived)
    E=(full.einstein+lam*g-kappa*T).applyfunc(S.simplify)
    J=maxwell_equations(full,F)
    B=maxwell_bianchi(F,x)
    divT=covariant_divergence_stress(full,T)
    lorentz_force=[S.simplify(sum(F[nu,a]*J[a] for a in range(4))) for nu in range(4)]
    energy_bridge=[S.simplify(divT[nu]-lorentz_force[nu]) for nu in range(4)]
    divE=covariant_divergence_stress(full,E)
    covariant_bridge=[S.simplify(divE[i]+kappa*divT[i]) for i in range(4)]
    h=S.Matrix(g[1:4,1:4])
    hs=h.inv()
    spatial=Geometry(x[1:4],h)
    K=(h.diff(x[0])/(2*N)).applyfunc(S.simplify)
    Kmixed=(hs*K).applyfunc(S.simplify)
    traceK=S.simplify(S.trace(Kmixed))
    Ksq=S.simplify(S.trace(Kmixed*Kmixed))
    rho=S.simplify(T[0,0]/N**2)
    H=S.simplify(spatial.scalar+traceK**2-Ksq-2*lam-2*kappa*rho)
    Momgeom=_spatial_divergence(spatial,Kmixed,traceK)
    M=tuple(S.simplify(Momgeom[i]-kappa*T[0,i+1]/N) for i in range(3))
    EH=S.simplify(2*E[0,0]/N**2)
    EM=tuple(S.simplify(E[0,i+1]/N) for i in range(3))
    Hbridge=S.simplify(H-EH)
    Mbridge=tuple(S.simplify(M[i]-EM[i]) for i in range(3))
    normal=S.simplify(g[0,0]/N**2+1)
    contracted=full.contracted_bianchi_residual()
    nodes=(
        _node('normal_unit',normal,'geometry'),
        _node('field_potential_consistency',F-F_from_A,'constitutive_bridge'),
        _node('maxwell_stress_constitutive',T-T_derived,'constitutive_bridge'),
        _node('electromagnetic_bianchi',B,'matter_bianchi'),
        _node('maxwell_euler_lagrange',J,'matter_dynamics'),
        _node('matter_noether_divergence',energy_bridge,'cross_law_identity'),
        _node('stress_conservation',divT,'matter_conservation'),
        _node('einstein_field_equation',E,'gravity_dynamics'),
        _node('einstein_contracted_bianchi',contracted,'gravity_bianchi'),
        _node('einstein_stress_divergence_bridge',covariant_bridge,'cross_law_identity'),
        _node('hamiltonian_constraint',H,'adm_constraint'),
        _node('momentum_constraints',M,'adm_constraint'),
        _node('hamiltonian_gauss_bridge',Hbridge,'cross_law_identity'),
        _node('momentum_codazzi_bridge',Mbridge,'cross_law_identity'),
        _node('claimed_hamiltonian_agreement',
              0 if spec.declared_hamiltonian is None else
              H-S.sympify(spec.declared_hamiltonian),'claimed_certificate'),
        _node('claimed_momentum_agreement',
              (0,0,0) if spec.declared_momentum is None else
              tuple(M[i]-S.sympify(spec.declared_momentum[i])
                    for i in range(3)),'claimed_certificate'),
    )
    results=[]
    for item in nodes:
        failed=[i for i,v in enumerate(item.components) if not _exact_zero(v)]
        results.append({'name':item.name,'category':item.category,
            'passed':len(failed)==0,'components':len(item.components),
            'failed_component_indices':failed,
            'residuals':[S.srepr(item.components[i]) for i in failed[:6]]})
    independent=[{'witness':{str(k):str(v) for k,v in w.items()},
                  'four_dimensional':_single_oracle(full,w),
                  'three_dimensional':_single_oracle(spatial,w)}
                 for w in spec.witnesses]
    all_oracles=all(w['four_dimensional']['passed'] and
                    w['three_dimensional']['passed'] for w in independent)
    accepted=all(r['passed'] for r in results) and all_oracles
    from pathlib import Path
    module_source=Path(__file__)
    oracle_source=Path(__file__).with_name('jet_oracle.py')
    receipt={'schema':SCHEMA,
        'contract_source_sha256':sha256(module_source.read_bytes()).hexdigest(),
        'oracle_source_sha256':sha256(oracle_source.read_bytes()).hexdigest(),
        'claim_id':spec.claim_id,'source':spec.source,
        'conventions':{'signature':'-+++','shift':'zero',
                       'extrinsic_curvature':'K_ij=+dt(h_ij)/(2N)',
                       'maxwell_action':'R-F_ab F^ab with kappa=2 by default',
                       'cosmological_constant':str(lam),
                       'gravitational_coupling':str(kappa)},
        'assumptions':list(spec.assumptions),'nodes':results,
        'independent_oracle':independent,
        'status':('PASS_LOCAL_TYPED_COUPLED_SYMBOLIC_CONTRACT' if accepted
                  else 'REJECTED_INCONSISTENT_COUPLED_PHYSICS'),
        'physical_truth_proven':False,'global_solution_proven':False,
        'independent_symbolic_proof':False,
        'independent_rational_curvature_witness_checked':all_oracles,
        'bounded_scope':'zero-shift four-dimensional Einstein-Maxwell, exact chart components',
        'replay_note':'Symbols/coordinate domains supplied by caller; rational witnesses alone cannot prove global identity'}
    encoding=json.dumps(receipt,sort_keys=True,separators=(',',':'))
    receipt['receipt_sha256']=sha256(encoding.encode()).hexdigest()
    return receipt


def save_contract(receipt,path):
    from pathlib import Path
    target=Path(path)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    return target


def replay_contract_receipt(spec: EinsteinMaxwellSpec, receipt):
    """Fail-closed full *recomputation*, not mere checksum comparison.

    The caller supplies the typed model again. Every node, curvature oracle
    comparison and current verifier-source hash is recomputed, then compared
    byte-for-byte under deterministic JSON. Modifying a stored receipt is
    refused unless the modified bytes match the current recomputation.
    This is not an independently trusted proof assistant/kernel.
    """
    fresh=evaluate_contract(spec)
    matched=(isinstance(receipt,dict) and
             json.dumps(receipt,sort_keys=True,separators=(',',':')) ==
             json.dumps(fresh,sort_keys=True,separators=(',',':')))
    return {'schema':'physqed-v1.2-contract-replay-1',
            'claim_id':spec.claim_id,
            'receipt_recomputed_and_matched':bool(matched),
            'fresh_status':fresh['status'],
            'positive_certificate_verified':bool(matched and
                fresh['status']=='PASS_LOCAL_TYPED_COUPLED_SYMBOLIC_CONTRACT'),
            'independent_symbolic_proof':False,
            'note':'Replays symbolic components and rational curvature oracle; not a global proof'}
