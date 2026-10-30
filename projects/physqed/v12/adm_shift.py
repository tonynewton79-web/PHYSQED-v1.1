"""PHYSQED: shifted 3+1 Einstein--Maxwell constraints and Bianchi propagation.

Exact chart-local symbolic identities, signature (-+++), shift beta^i,
future unit normal n=(1/N,-beta^i/N), *positive* extrinsic curvature

    K_ij = (partial_t h_ij - (L_beta h)_ij)/(2N).

Einstein residual E_ab=G_ab+Lambda*g_ab-kappa*T_ab.
H=R(h)+K^2-K_ij K^ij-2Lambda-2kappa*rho = 2 E_nn.
M_i=D_j K^j_i-D_i K-kappa*T_ni = E_ni.

Writing A=H/2, B_i=M_i, C_ij=E_ij, J_n=n^b nabla^a E_ab,
J_i=nabla^a E_ai, a_i=D_i(log N), the OFF-SHELL projected
divergence identities imply

 (dt-L_beta) H = 2N[D_j M^j + 2 a_j M^j
                         -K H/2 -K^ij C_ij - J_n],
 (dt-L_beta) M_i = N[-K M_i + (H/2) a_i
                         +D^j C_ji +a^j C_ji -J_i].

If spatial Einstein evolution C_ij=0 and matter is conserved, J=0,
these are homogeneous constraint propagation relations. An identity
alone is NOT a PDE uniqueness, existence, global propagation,
regularity or formal proof-assistant theorem.

The implementation is restricted to explicit four-dimensional
coordinate metrics, symbolic SymPy and 1..4 exact rational-jet
witnesses. It does not infer domain assumptions.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from hashlib import sha256
from pathlib import Path
import json
import sympy as S
from .geometry import Geometry, ScopeError, zero
from .coupled import (maxwell_from_potential, maxwell_bianchi,
                      maxwell_equations, maxwell_stress,
                      covariant_divergence_stress)
from .contracts import _single_oracle


def _vector3(value, label):
    if not isinstance(value, (list,tuple,S.MatrixBase)) or len(value)!=3:
        raise ScopeError(label+" requires exactly three spatial components")
    return S.Matrix([S.sympify(v) for v in value])


def _lie_shift_metric(h, b, coordinates):
    x=tuple(coordinates)
    return S.Matrix(3,3,lambda i,j:S.simplify(
        sum(b[k]*S.diff(h[i,j],x[k])+
            h[i,k]*S.diff(b[k],x[j])+
            h[j,k]*S.diff(b[k],x[i]) for k in range(3))))


def _spatial_divergence_mixed(geo, X):
    C=geo.connection
    x=geo.x
    return tuple(S.simplify(
        sum(S.diff(X[j,i],x[j])+
            sum(C[j][j][k]*X[k,i]-C[k][j][i]*X[j,k]
                for k in range(3)) for j in range(3))
        ) for i in range(3))


def _lift_covariant_spatial(B, b):
    """B_t=beta^i B_i ensures B_mu n^mu=0."""
    return S.Matrix([sum(b[i]*B[i] for i in range(3)),*list(B)])


def _flatten(value):
    if isinstance(value,S.MatrixBase):
        return tuple(value)
    return tuple(value) if isinstance(value,(tuple,list)) else (value,)


def _node(name, value, group):
    entries=_flatten(value)
    fails=[i for i,v in enumerate(entries) if not zero(v)]
    return {"name":name,"category":group,"passed":not fails,
            "components":len(entries),
            "failed_component_indices":fails,
            "failed_residuals":[S.srepr(entries[i]) for i in fails[:4]]}


@dataclass(frozen=True)
class ShiftedEinsteinMaxwellSpec:
    claim_id: str
    coordinates: tuple
    spatial_metric: object
    lapse: object
    shift: tuple
    potential: tuple
    witnesses: tuple
    assumptions: tuple
    source: str = "standard textbook 3+1 Einstein-Maxwell"
    cosmological_constant: object = S.S.Zero
    gravitational_coupling: object = S.Integer(2)

    def validate(self):
        x=tuple(self.coordinates)
        if (len(x)!=4 or len(set(x))!=4 or
                any(not isinstance(v,S.Symbol) for v in x)):
            raise ScopeError("shifted ADM requires four distinct coordinate symbols")
        if not isinstance(self.claim_id,str) or not self.claim_id.strip():
            raise ScopeError("nonempty claim identifier required")
        if not isinstance(self.source,str) or not self.source.strip():
            raise ScopeError("model provenance is required")
        if not self.assumptions or any(not isinstance(a,str) or
                    not a.strip() for a in self.assumptions):
            raise ScopeError("explicit assumption strings are required")
        if not isinstance(self.potential,(tuple,list)) or len(self.potential)!=4:
            raise ScopeError("electromagnetic potential must be a four-one-form")
        h=S.Matrix(self.spatial_metric)
        if h.shape!=(3,3) or any(not zero(h[i,j]-h[j,i])
                                 for i,j in product(range(3),repeat=2)):
            raise ScopeError("symmetric 3x3 spatial metric required")
        b=_vector3(self.shift,"contravariant ADM shift")
        N=S.sympify(self.lapse)
        if zero(N):
            raise ScopeError("ADM lapse must be nonzero")
        if len(self.witnesses)<1 or len(self.witnesses)>4:
            raise ScopeError("1..4 rational witnesses required")
        for witness in self.witnesses:
            if not isinstance(witness,dict) or set(witness)!=set(x):
                raise ScopeError("witness must assign all spacetime coordinates")
            nv=S.simplify(N.subs(witness))
            if nv.is_positive is not True:
                raise ScopeError("positive lapse not established at witness")
            hs=h.subs(witness)
            for k in range(1,4):
                minor=S.simplify(hs[:k,:k].det())
                if minor.is_positive is not True:
                    raise ScopeError("spatial metric not positive-definite at witness")
        return h,b,N


def evaluate_shifted_einstein_maxwell(spec):
    """Verify full spatial/normal Einstein projections and propagation."""
    if not isinstance(spec,ShiftedEinsteinMaxwellSpec):
        raise ScopeError("typed shifted Einstein-Maxwell specification required")
    h,b,N=spec.validate()
    x=tuple(spec.coordinates)
    hgeo=Geometry(x[1:],h)
    g=S.zeros(4)
    g[0,0]=S.simplify(-N*N+(b.T*h*b)[0])
    for i,j in product(range(3),repeat=2):
        g[i+1,j+1]=h[i,j]
    for i in range(3):
        g[0,i+1]=S.simplify((h*b)[i])
        g[i+1,0]=g[0,i+1]
    full=Geometry(x,g)
    nn=S.Matrix([1/N]+[-v/N for v in b])
    nlower=(g*nn).applyfunc(S.simplify)
    F=maxwell_from_potential(x,spec.potential)
    T=maxwell_stress(full,F)
    lam=S.sympify(spec.cosmological_constant)
    kappa=S.sympify(spec.gravitational_coupling)
    E=(full.einstein+lam*g-kappa*T).applyfunc(S.simplify)
    Jm=maxwell_equations(full,F)
    divT=covariant_divergence_stress(full,T)
    divE=covariant_divergence_stress(full,E)

    K=((h.diff(x[0])-_lie_shift_metric(h,b,x[1:]))/(2*N)).applyfunc(S.simplify)
    hinv=hgeo.g_inv
    Km=(hinv*K).applyfunc(S.simplify)
    trK=S.simplify(S.trace(Km))
    rho=S.simplify((nn.T*T*nn)[0])
    mattermoment=S.Matrix([S.simplify((nn.T*T[:,i+1])[0]) for i in range(3)])
    H=S.simplify(hgeo.scalar+trK*trK-S.trace(Km*Km)-2*lam-2*kappa*rho)
    momg=_spatial_divergence_mixed(hgeo,Km)
    M=S.Matrix([S.simplify(momg[i]-S.diff(trK,x[i+1])-
                             kappa*mattermoment[i]) for i in range(3)])
    A=S.simplify((nn.T*E*nn)[0])
    B=S.Matrix([S.simplify((nn.T*E[:,i+1])[0]) for i in range(3)])
    C=S.Matrix(E[1:4,1:4])
    Cmix=(hinv*C).applyfunc(S.simplify)

    accel=S.Matrix([S.simplify(S.diff(N,x[i+1])/N) for i in range(3)])
    KdotC=S.simplify(S.trace(Km*Cmix))
    # Divergence of a spatial vector M^i, computed with h-compatible connection.
    raisedM=hinv*M
    CB=hgeo.connection
    divM=S.simplify(sum(S.diff(raisedM[i],x[i+1])+
          sum(CB[i][i][k]*raisedM[k] for k in range(3))
          for i in range(3)))
    divC=S.Matrix(_spatial_divergence_mixed(hgeo,Cmix))

    # Project full four-dimensional Bianchi divergence onto n and slice.
    Jn=S.simplify((nn.T*S.Matrix(divE))[0])
    Ji=S.Matrix(divE[1:4])
    DtnH=S.simplify(S.diff(H,x[0])-sum(b[j]*S.diff(H,x[j+1])
                                                        for j in range(3)))
    DtnM=S.Matrix([S.simplify(S.diff(M[i],x[0])-
             sum(b[j]*S.diff(M[i],x[j+1])+M[j]*S.diff(b[j],x[i+1])
                 for j in range(3))) for i in range(3)])
    accelM=S.simplify((accel.T*raisedM)[0])
    accelC=(Cmix.T*accel).applyfunc(S.simplify)
    PH=S.simplify(DtnH-2*N*(divM+2*accelM-trK*H/2-KdotC-Jn))
    PM=(DtnM-N*(-trK*M+H*accel/2+divC+accelC-Ji)).applyfunc(S.simplify)
    Hfree=S.simplify(DtnH-2*N*(divM+2*accelM-trK*H/2))
    Mfree=(DtnM-N*(-trK*M+H*accel/2)).applyfunc(S.simplify)

    nodes=(
        _node("normal_unit",(nn.T*g*nn)[0]+1,"geometry"),
        _node("normal_orthogonal",[(nn.T*g[:,i+1])[0] for i in range(3)],"geometry"),
        _node("maxwell_bianchi",maxwell_bianchi(F,x),"matter_identity"),
        _node("maxwell_equations",Jm,"matter_dynamics"),
        _node("matter_conservation",divT,"matter_dynamics"),
        _node("einstein_full",E,"gravity_dynamics"),
        _node("spatial_einstein_evolution",C,"evolution_equations"),
        _node("hamilton_constraint",H,"adm_constraint"),
        _node("momentum_constraint",M,"adm_constraint"),
        _node("gauss_hamiltonian_bridge",H-2*A,"off_shell_identity"),
        _node("codazzi_momentum_bridge",M-B,"off_shell_identity"),
        _node("einstein_stress_bianchi_bridge",[
            S.simplify(divE[i]+kappa*divT[i]) for i in range(4)],
            "off_shell_identity"),
        _node("hamiltonian_propagation_bridge",PH,"off_shell_identity"),
        _node("momentum_propagation_bridge",PM,"off_shell_identity"),
    )
    results=[v for v in nodes]
    independent=[{
        "witness":{str(k):str(v) for k,v in w.items()},
        "four_dimensional":_single_oracle(full,w),
        "three_dimensional":_single_oracle(hgeo,w)}
        for w in spec.witnesses]
    oracle_ok=all(w["four_dimensional"]["passed"] and
                  w["three_dimensional"]["passed"] for w in independent)
    fail=[v["name"] for v in results if not v["passed"]]
    off_shell_names={"gauss_hamiltonian_bridge","codazzi_momentum_bridge",
                     "einstein_stress_bianchi_bridge",
                     "hamiltonian_propagation_bridge","momentum_propagation_bridge"}
    off_shell_ok=all(v["passed"] for v in results if v["name"] in off_shell_names)
    evolution_ok=all(v["passed"] for v in results if v["name"] in
                      {"spatial_einstein_evolution","matter_conservation"})
    homogeneous_ok=(evolution_ok and off_shell_ok and
                    zero(Hfree) and all(zero(z) for z in Mfree))
    status=("PASS_SCOPED_SHIFTED_EINSTEIN_MAXWELL" if not fail and oracle_ok
            else "REJECTED_SHIFTED_EINSTEIN_MAXWELL")
    result={
        "schema":"physqed.shifted-adm.v1","claim_id":spec.claim_id,
        "source":spec.source,"assumptions":list(spec.assumptions),
        "conventions":{"signature":"-+++",
            "shift":"nonzero beta^i supported",
            "extrinsic_curvature":"K=(dt h-L_beta h)/(2N), positive",
            "stress_normalization":"E=G+Lambda*g-kappa*T",
            "gravitational_coupling":str(kappa),
            "cosmological_constant":str(lam)},
        "nodes":results,"independent_oracle":independent,
        "oracle_passed":oracle_ok,
        "off_shell_projection_and_propagation_identities_passed":off_shell_ok,
        "spatial_evolution_and_matter_conservation_passed":evolution_ok,
        "homogeneous_constraint_propagation_identities_passed":homogeneous_ok,
        "global_constraint_propagation_theorem_proven":False,
        "pde_well_posedness_proven":False,
        "assumption_domain_verified":False,
        "independent_formal_proof":False,
        "status":status,
        "failed_nodes":fail,
        "implementation_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    packed=json.dumps(result,sort_keys=True,separators=(",",":"))
    result["receipt_sha256"]=sha256(packed.encode()).hexdigest()
    return result


def replay_shifted_adm(spec,receipt):
    """Full deterministic recomputation rather than trusting a receipt hash."""
    return isinstance(receipt,dict) and json.dumps(
        evaluate_shifted_einstein_maxwell(spec),sort_keys=True) == json.dumps(
        receipt,sort_keys=True)
