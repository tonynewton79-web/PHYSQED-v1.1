"""Exact linearized generalized-harmonic boundary-to-constraint benchmark.

Flat half-space x>=0; trace-reversed metric bar_h; 10 reduced wave
equations, six outgoing Sommerfeld tangential metric boundary rows and
four harmonic-constraint boundary rows. Computes the Laplace-Fourier
boundary determinant and checks initial C, dt C, and first corner jets.

Established harmonic boundary prior art, not a novel Einstein IBVP
theorem. Does not certify a uniform glancing Kreiss estimate, all
corner orders, arbitrary-data existence, or nonlinear Einstein IBVP.
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
I={"t":0,"x":1,"y":2,"z":3}


def _zero(a):
    return S.simplify(S.expand(a))==0


def _safe(e):
    if isinstance(e,(str,float)) or (isinstance(e,S.Basic) and e.has(S.Float)):
        raise ValueError("only trusted exact preconstructed SymPy expressions")
    e=S.sympify(e)
    if not e.free_symbols.issubset(set(COORDS)):
        raise ValueError("undeclared symbol")
    return e


def zero_metric():
    return {k:S.Integer(0) for k in ORDER}


def tensor(entries):
    if not isinstance(entries,dict) or set(entries)!=set(ORDER):
        raise ValueError("ten symmetric metric components must be supplied")
    m=S.zeros(4)
    for name,value in entries.items():
        a,b=(I[c] for c in name)
        m[a,b]=m[b,a]=_safe(value)
    return m


def _entries(m):
    return {key:m[I[key[0]],I[key[1]]] for key in ORDER}


def wave(a):
    return S.expand(-S.diff(a,t,2)+sum(S.diff(a,v,2) for v in SPACE))


def harmonic_constraint(bar):
    return S.Matrix([S.expand(-S.diff(bar[0,j],t)+sum(
        S.diff(bar[i,j],COORDS[i]) for i in (1,2,3))) for j in range(4)])


def linearized_einstein(bar):
    """Standard linearized Einstein tensor in trace-reversed variables."""
    c=harmonic_constraint(bar)
    eta=S.diag(-1,1,1,1)
    div=S.expand(-S.diff(c[0],t)+sum(S.diff(c[j],COORDS[j])
                                      for j in (1,2,3)))
    return S.Matrix(4,4,lambda a,b:S.expand((
        -wave(bar[a,b])+S.diff(c[b],COORDS[a])+
        S.diff(c[a],COORDS[b])-eta[a,b]*div)/2))


def general_differential_intertwiner():
    """Check box C_nu=partial^mu(box bar_h_munu) for 10 free fields."""
    m=S.Matrix(4,4,lambda a,b:S.Function(
        "h"+str(min(a,b))+str(max(a,b)))(*COORDS))
    c=harmonic_constraint(m)
    return all(_zero(wave(c[j])+S.diff(wave(m[0,j]),t)-
        sum(S.diff(wave(m[i,j]),COORDS[i]) for i in (1,2,3)))
        for j in range(4))


def normal_mode_symbol():
    """s: Laplace, eta/zeta: real transverse, k: decaying normal exponent."""
    s,k,eta,zeta=S.symbols("s k eta zeta")
    positions={name:j for j,name in enumerate(ORDER)}
    def col(a,b):
        return positions[a+b if a+b in positions else b+a]
    mat=S.zeros(10)
    for j,name in enumerate(TANGENT):
        mat[j,positions[name]]=s+k
    for j,nu in enumerate(("t","y","z","x")):
        for a,fac in (("t",-s),("x",-k),("y",S.I*eta),("z",S.I*zeta)):
            mat[6+j,col(a,nu)]+=fac
    determinant=S.factor(mat.det(method="domain-ge"))
    expected=k**4*(s+k)**6
    return {"ten_by_ten_boundary_symbol":mat,"determinant":determinant,
            "factorization_verified":_zero(determinant-expected),
            "normal_decaying_mode_nonzero_for_Re_s_positive":True,
            "normal_mode_nonzero_argument":
              "For Re(s)>0 and real eta,zeta, choose Re(k)>0 and k^2=s^2+eta^2+zeta^2; then k and s+k are nonzero.",
            "uniform_glancing_Kreiss_estimate_verified":False,
            "strong_Lopatinski_verified":False}


def first_corner_gate(initial,velocity):
    """Exact C, dt C on initial slice and Sommerfeld/C corner orders 0,1."""
    f=tensor(initial);g=tensor(velocity)
    if any(t in e.free_symbols for e in list(f)+list(g)):
        raise ValueError("Cauchy data must be spatial")
    lap=lambda e:sum(S.diff(e,v,2) for v in SPACE)
    C=S.Matrix([S.expand(-g[0,j]+sum(S.diff(f[i,j],COORDS[i])
                                     for i in (1,2,3))) for j in range(4)])
    Ct=S.Matrix([S.expand(-lap(f[0,j])+sum(S.diff(g[i,j],COORDS[i])
                                     for i in (1,2,3))) for j in range(4)])
    som0=[];som1=[]
    for ab in TANGENT:
        a,b=map(I.__getitem__,ab)
        som0.append(S.expand((g[a,b]-S.diff(f[a,b],x)).subs(x,0)))
        som1.append(S.expand((lap(f[a,b])-S.diff(g[a,b],x)).subs(x,0)))
    bc0=[S.expand(v.subs(x,0)) for v in C]
    bc1=[S.expand(v.subs(x,0)) for v in Ct]
    residuals=list(C)+list(Ct)+som0+som1+bc0+bc1
    return {"C_initial_zero":all(_zero(v) for v in C),
            "dt_C_initial_zero":all(_zero(v) for v in Ct),
            "metric_corner_order0_zero":all(_zero(v) for v in som0),
            "metric_corner_order1_zero":all(_zero(v) for v in som1),
            "harmonic_corner_order0_zero":all(_zero(v) for v in bc0),
            "harmonic_corner_order1_zero":all(_zero(v) for v in bc1),
            "first_order_compatibility_passed":all(_zero(v) for v in residuals),
            "failed_residuals":[str(v) for v in residuals if not _zero(v)],
            "higher_order_corner_compatibility_proven":False,
            "finite_energy_initial_data_proven":False}


def certify_explicit_linearized_metric(entries):
    bar=tensor(entries)
    c=harmonic_constraint(bar)
    diffs=[wave(v) for v in _entries(bar).values()]
    bc_sommerfeld=[S.expand((S.diff(bar[I[name[0]],I[name[1]]],t)-
                       S.diff(bar[I[name[0]],I[name[1]]],x)).subs(x,0))
                   for name in TANGENT]
    bc_C=[S.expand(v.subs(x,0)) for v in c]
    f={name:S.expand(v.subs(t,0)) for name,v in _entries(bar).items()}
    g={name:S.expand(S.diff(v,t).subs(t,0))
       for name,v in _entries(bar).items()}
    corners=first_corner_gate(f,g)
    field_ok=all(_zero(v) for v in diffs)
    full_ok=all(_zero(v) for v in linearized_einstein(bar))
    som_ok=all(_zero(v) for v in bc_sommerfeld)
    constraint_ok=all(_zero(v) for v in bc_C)
    result={
        "schema":"physqed.linearized-gh-boundary.v1",
        "reduced_wave_equations_passed":field_ok,
        "full_linearized_vacuum_Einstein_passed":full_ok,
        "constraint_wave_equations_passed":all(_zero(wave(v)) for v in c),
        "six_tangent_sommerfeld_boundary_rows_passed":som_ok,
        "four_boundary_harmonic_constraints_passed":constraint_ok,
        "boundary_constraint_components":[str(v) for v in bc_C],
        "boundary_sommerfeld_residuals":[str(v) for v in bc_sommerfeld],
        "initial_corner":corners,
        "smooth_solution_existence_proven":False,
        "uniform_Kreiss_estimate_proven":False,
        "nonlinear_GH_Einstein_IBVP_proven":False,
        "status":("PASS_LOCAL_LINEARIZED_GH_BOUNDARY_AND_CORNERS"
             if field_ok and full_ok and som_ok and constraint_ok and
             corners["first_order_compatibility_passed"] else
             "REJECTED_OR_INCOMPATIBLE_LINEARIZED_GH_BOUNDARY")}
    result["receipt_sha256"]=sha256(json.dumps(
        result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return result


def reference_positive_wave():
    h=zero_metric()
    h["yz"]=S.Function("F")(t+x)
    return h


def reference_constraint_velocity_failure():
    h=zero_metric()
    h["xx"]=t*x
    return h


def reference_metric_corner_failure():
    h=zero_metric()
    h["yz"]=t
    return h


def naive_sommerfeld_counterexample():
    """All 10 metric Sommerfeld rows pass, but C_x|=2t, D_- C_x|=2."""
    h=zero_metric()
    h["xx"]=y*y+t*t+2*t*x
    m=tensor(h)
    c=harmonic_constraint(m)
    data=[S.expand((S.diff(v,t)-S.diff(v,x)).subs(x,0))
          for v in _entries(m).values()]
    Dcm=S.expand((S.diff(c[1],t)-S.diff(c[1],x)).subs(x,0))
    dyz=S.expand((S.diff(m[1,1],y,2)+S.diff(m[1,1],z,2)).subs(x,0))
    return {"all_reduced_wave_components_zero":all(_zero(wave(v)) for v in h.values()),
            "all_ten_metric_sommerfeld_rows_zero":all(_zero(v) for v in data),
            "harmonic_Cx_on_boundary":str(S.expand(c[1].subs(x,0))),
            "incoming_harmonic_Cx_boundary_residual":str(Dcm),
            "tangential_laplacian_source":str(dyz),
            "exact_obstruction_passed":bool(Dcm==dyz and not _zero(Dcm))}


def certify_symbol_and_controls():
    symbol=normal_mode_symbol()
    positive=certify_explicit_linearized_metric(reference_positive_wave())
    old=certify_explicit_linearized_metric(reference_constraint_velocity_failure())
    corner=certify_explicit_linearized_metric(reference_metric_corner_failure())
    negative=naive_sommerfeld_counterexample()
    passed=(symbol["factorization_verified"] and general_differential_intertwiner()
        and positive["status"]=="PASS_LOCAL_LINEARIZED_GH_BOUNDARY_AND_CORNERS"
        and not old["initial_corner"]["dt_C_initial_zero"]
        and not corner["initial_corner"]["metric_corner_order0_zero"]
        and negative["exact_obstruction_passed"])
    return {"schema":"physqed.gh-constraint-intertwiner.v1",
       "status":("PASS_SCOPED_LINEARIZED_GH_DIFFERENTIAL_BOUNDARY_MAP"
                 if passed else "REJECTED_GH_DIFFERENTIAL_BOUNDARY_MAP"),
       "ten_metric_wave_fields":10,"metric_Sommerfeld_tangent_rows":6,
       "harmonic_constraint_boundary_rows":4,
       "Laplace_Fourier_normal_mode_determinant":str(symbol["determinant"]),
       "normal_mode_factorization_verified":symbol["factorization_verified"],
       "operator_intertwiner_verified":general_differential_intertwiner(),
       "positive_transverse_wave_verified":positive["full_linearized_vacuum_Einstein_passed"],
       "initial_constraint_velocity_negative_control_rejected":not old["initial_corner"]["dt_C_initial_zero"],
       "metric_corner_negative_control_rejected":not corner["initial_corner"]["metric_corner_order0_zero"],
       "all_component_Sommerfeld_false_inference_excluded":negative["exact_obstruction_passed"],
       "uniform_Kreiss_Lopatinski_proven":False,
       "all_corner_orders_proven":False,
       "nonlinear_Einstein_IBVP_proven":False,
       "source":"linearized trace-reversed vacuum harmonic Einstein on Minkowski half-space",
       "claim_boundary":"Exact symbolic operator/normal-mode and first-corner identities only; standard prior art"}


def replay_gh_metric(entries,receipt):
    return isinstance(receipt,dict) and receipt==certify_explicit_linearized_metric(entries)
