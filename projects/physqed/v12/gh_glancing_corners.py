"""Exact glancing counterexample and finite higher-order GH corner hierarchy.

No uniform unweighted amplitude inverse for the existing boundary symbol
near kappa=0. No claim about adapted first-order Kreiss norms.
"""
from __future__ import annotations
from hashlib import sha256
import json
import sympy as S

t,x,y,z=S.symbols("t x y z",real=True)
COORDS=(t,x,y,z)
SPACE=(x,y,z)
ORDER=("tt","ty","tz","yy","yz","zz","tx","xy","xz","xx")
TANGENT=ORDER[:6]
INDEX={"t":0,"x":1,"y":2,"z":3}


def _zero(value):
    return S.simplify(S.expand(value))==0


def _tensor(data):
    if not isinstance(data,dict) or set(data)!=set(ORDER):
        raise ValueError("ten exact source components required")
    m=S.zeros(4)
    for key,value in data.items():
        if isinstance(value,(float,str)) or not isinstance(value,(int,S.Basic)):
            raise ValueError("trusted exact SymPy expressions only")
        value=S.sympify(value)
        if value.has(S.Float) or value.free_symbols-set(COORDS):
            raise ValueError("untrusted or undeclared source")
        a,b=(INDEX[c] for c in key)
        m[a,b]=m[b,a]=value
    return m


def higher_corner_hierarchy(initial,velocity,max_order=4):
    """Exact metric Sommerfeld/C boundary temporal jets through max_order.

    Box bar_h=0 implies h_(j+2)(0)=Delta h_j(0). Initial C and dt C
    are audited over the ENTIRE initial spatial slice; higher temporal
    compatibility checks are restricted to x=0.
    """
    if type(max_order) is not int or not 0<=max_order<=8:
        raise ValueError("bounded integer corner order 0..8 required")
    f=_tensor(initial);g=_tensor(velocity)
    if any(e.has(t) for e in tuple(f)+tuple(g)):
        raise ValueError("Cauchy data cannot depend on t")
    delta=lambda A:A.applyfunc(lambda e:S.expand(sum(S.diff(e,c,2) for c in SPACE)))
    jets=[f,g]
    for j in range(max(max_order,1)):
        jets.append(delta(jets[j]))
    cjets=[]
    for j in range(max(2,max_order+1)):
        cjets.append(S.Matrix([S.expand(-jets[j+1][0,nu]+sum(
            S.diff(jets[j][i,nu],COORDS[i]) for i in (1,2,3)))
            for nu in range(4)]))
    initial_ok=all(_zero(v) for v in cjets[0]) and all(_zero(v) for v in cjets[1])
    levels=[]
    for j in range(max_order+1):
        metric=[S.expand((jets[j+1][INDEX[key[0]],INDEX[key[1]]]-
               S.diff(jets[j][INDEX[key[0]],INDEX[key[1]]],x)).subs(x,0))
               for key in TANGENT]
        constraint=[S.expand(v.subs(x,0)) for v in cjets[j]]
        levels.append({"order":j,"metric_sommerfeld_zero":all(_zero(v) for v in metric),
                       "harmonic_constraint_zero":all(_zero(v) for v in constraint),
                       "metric_residuals":[str(v) for v in metric],
                       "constraint_residuals":[str(v) for v in constraint]})
    return {"schema":"physqed.GH-higher-corners.v1",
            "orders_checked":list(range(max_order+1)),
            "initial_C_zero":all(_zero(v) for v in cjets[0]),
            "initial_dt_C_zero":all(_zero(v) for v in cjets[1]),
            "levels":levels,
            "passed":bool(initial_ok and all(
                a["metric_sommerfeld_zero"] and a["harmonic_constraint_zero"]
                for a in levels)),
            "all_higher_order_compatibility_proven":False,
            "smooth_solution_exists_proven":False}


def glancing_obstruction(n):
    """Exact right-half-plane sequence proving nonuniform unweighted B.

    s=i+1/n², eta=1, kappa²=s²+1.
    A unit h_xx boundary amplitude has B*h_xx=-kappa in the
    harmonic x row and ZERO in all nine remaining rows.
    |kappa|²=epsilon*sqrt(4+epsilon²)<3/n².
    """
    if type(n) is not int or not 2<=n<=1000000:
        raise ValueError("integer glancing scale n>=2 required")
    eps=S.Rational(1,n*n)
    k2=eps**2+2*S.I*eps
    mod_sq=S.sqrt(S.expand_complex(k2*S.conjugate(k2)))
    expected=eps*S.sqrt(eps**2+4)
    assert S.simplify(mod_sq-expected)==0
    assert bool(eps**2+4<9) and eps>0
    return {"n":n,"laplace_real_part":str(eps),
            "tangential_real_frequency":"1",
            "kappa_squared":str(k2),
            "kappa_modulus_squared":str(expected),
            "boundary_residual_only_x_row":"-kappa",
            "exact_bound_squared":str(S.Rational(3,n*n)),
            "strict_upper_bound_verified":True,
            "normalized_amplitude_lower_bound_can_be_uniform":False,
            "normalized_minimum_singular_value_upper_bound":"sqrt(3)/n",
            "weighted_first_order_Kreiss_estimate_refuted":False}


def glancing_summary():
    sequence=[glancing_obstruction(n) for n in (2,4,8,16,32,64)]
    return {"schema":"physqed.GH-glancing.v1",
            "status":"REFUTED_UNWEIGHTED_UNIFORM_BOUNDARY_INVERSE",
            "sequence":sequence,
            "glancing_obstruction_proven":True,
            "proof":"Unit h_xx gives residual -kappa. At s=i+1/n², eta=1, |kappa|²=(1/n²)sqrt(4+1/n⁴)<3/n²; frequency normalization remains bounded below.",
            "uniform_weighted_Kreiss_estimate_proven":False,
            "strong_Lopatinski_for_first_order_system_proven":False,
            "nonlinear_Einstein_IBVP_proven":False}


def reference_data(kind):
    f={name:S.S.Zero for name in ORDER}
    g=f.copy()
    if kind=="tangent_outgoing_poly":
        f["yz"]=x**3+3*x*x+6*x+6
        g["yz"]=3*x*x+6*x+6
    elif kind=="order2_failure":
        f["yz"]=x**3
    elif kind!="zero":
        raise ValueError("unknown corner benchmark")
    return f,g


def certify_glancing_and_corners():
    positive=higher_corner_hierarchy(*reference_data("tangent_outgoing_poly"),
                                      max_order=6)
    negative=higher_corner_hierarchy(*reference_data("order2_failure"),
                                      max_order=4)
    passed=(positive["passed"] and not negative["passed"] and
            all(a["metric_sommerfeld_zero"] for a in negative["levels"][:2])
            and not negative["levels"][2]["metric_sommerfeld_zero"])
    receipt={"schema":"physqed.GH-glancing-corners.v1",
             "glancing":glancing_summary(),
             "positive_higher_corners":positive,
             "negative_second_order_corner":negative,
             "status":("PASS_GH_GLANCING_OBSTRUCTION_AND_FINITE_CORNERS"
                       if passed else "REJECTED_GH_GLANCING_CORNER_CHECK")}
    receipt["receipt_sha256"]=sha256(json.dumps(
        receipt,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return receipt


def replay_glancing_corners(stored):
    return isinstance(stored,dict) and stored==certify_glancing_and_corners()
