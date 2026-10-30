"""Sourced linearized harmonic Einstein: conservation and finite corner jets.

For wave equations -psi_tt+Delta psi=Fpi, time jets obey
J0=f, J1=g, J_(m+2)=Delta J_m-dt^m Fpi(0).
The adapted six metric Sommerfeld and four gauge-constraint
boundary conditions are checked as time-dependent nonhomogeneous
functions on the full transverse corner. Source divergence is audited
as a prerequisite to *homogeneous* harmonic constraint propagation.

These are compatibility identities, not PDE existence for arbitrary
source/boundary values or all corner orders.
"""
import sympy as S
from .gh_first_order_uniform import ORDER,P_COMBOS

COORDS=S.symbols("t x y z",real=True)
I={v:i for i,v in enumerate(("t","x","y","z"))}


def _matrix(data):
    if not isinstance(data,dict) or set(data)!=set(ORDER):
        raise ValueError("symmetric source requires ten metric components")
    m=S.zeros(4)
    for name,val in data.items():
        if isinstance(val,(str,float)):
            raise ValueError("trusted exact SymPy expressions required")
        val=S.sympify(val)
        if val.has(S.Float) or val.free_symbols-set(COORDS):
            raise ValueError("undeclared or inexact expression")
        a,b=I[name[0]],I[name[1]]
        m[a,b]=m[b,a]=val
    return m


def _as_ten(m):
    return S.Matrix([m[I[key[0]],I[key[1]]] for key in ORDER])


def check_sourced_harmonic_corners(initial,velocity,source,boundary_six,
                                  boundary_four,max_order=4):
    t,x,y,z=COORDS
    if type(max_order) is not int or not 0<=max_order<=6:
        raise ValueError("finite time corner order 0..6 required")
    f=_matrix(initial)
    g=_matrix(velocity)
    F=_matrix(source)
    if any(e.has(t) for m in (f,g) for e in m):
        raise ValueError("initial metric and velocity cannot depend on time")
    if not isinstance(boundary_six,(tuple,list)) or len(boundary_six)!=6:
        raise ValueError("exactly six prescribed Sommerfeld data needed")
    if not isinstance(boundary_four,(tuple,list)) or len(boundary_four)!=4:
        raise ValueError("exactly four prescribed harmonic boundary data needed")
    for item in list(boundary_six)+list(boundary_four):
        if isinstance(item,(str,float)) or S.sympify(item).has(S.Float) or (
           S.sympify(item).free_symbols-set(COORDS)):
            raise ValueError("untrusted boundary data")
    divergence=[S.simplify(-S.diff(F[0,j],t)+sum(
         S.diff(F[i,j],COORDS[i]) for i in (1,2,3))) for j in range(4)]
    def lap(mat):
        return mat.applyfunc(lambda e:S.expand(sum(S.diff(e,v,2)
                                                   for v in (x,y,z))))
    J=[f,g]
    for k in range(max(max_order,1)):
        J.append((lap(J[k])-F.diff(t,k).subs(t,0)).applyfunc(S.expand))
    def Cjet(k):
        return S.Matrix([S.expand(-J[k+1][0,j]+sum(
             S.diff(J[k][i,j],COORDS[i]) for i in (1,2,3)))
             for j in range(4)])
    c0,c1=Cjet(0),Cjet(1)
    P=S.zeros(6,10)
    for i,row in enumerate(P_COMBOS):
        for name,value in row.items():
            P[i,ORDER.index(name)]=value
    levels=[]
    for j in range(max_order+1):
        metric=S.Matrix([S.simplify(v.subs(x,0)) for v in
                            P*_as_ten(J[j+1]-J[j].diff(x))])
        gauges=S.Matrix([S.simplify(v.subs(x,0)) for v in Cjet(j)])
        requested_metric=[S.diff(S.sympify(v),t,j).subs(t,0)
                           for v in boundary_six]
        requested_gauges=[S.diff(S.sympify(v),t,j).subs(t,0)
                           for v in boundary_four]
        metric_res=[S.simplify(metric[k]-requested_metric[k]) for k in range(6)]
        gauge_res=[S.simplify(gauges[k]-requested_gauges[k]) for k in range(4)]
        levels.append({"order":j,
              "six_metric_residuals":[str(v) for v in metric_res],
              "four_constraint_residuals":[str(v) for v in gauge_res],
              "all_ten_corner_equations_passed":all(
                  v==0 for v in metric_res+gauge_res)})
    source_conserved=all(v==0 for v in divergence)
    zero_initial=all(S.simplify(v)==0 for v in c0) and all(
                                                  S.simplify(v)==0 for v in c1)
    zero_boundary_constraints=all(S.simplify(v)==0 for v in boundary_four)
    return {
       "schema":"physqed.GH-sourced-corners.v1",
       "source_divergence":[str(v) for v in divergence],
       "source_divergence_free":source_conserved,
       "initial_C_zero":all(S.simplify(v)==0 for v in c0),
       "initial_dt_C_zero":all(S.simplify(v)==0 for v in c1),
       "levels":levels,
       "requested_corner_orders_passed":all(
           row["all_ten_corner_equations_passed"] for row in levels),
       "conditional_harmonic_constraint_preservation":
           bool(source_conserved and zero_initial and zero_boundary_constraints),
       "all_corner_orders_proven":False,
       "smooth_solution_exists_proven":False,
       "Einstein_boundary_theorem_proven":False}


def sourced_wave_positive_control(*,bad_second_order=False,nonconserved=False):
    t,x,y,z=COORDS
    initial={key:0 for key in ORDER}
    velocity=initial.copy()
    source=initial.copy()
    source["yz"]=(t*t-2)*S.exp(-x)
    if nonconserved:
        source["tx"]=t*S.exp(-x)
    boundary_six=[0]*6
    boundary_six[4]=2*t+(0 if bad_second_order else t*t)
    boundary_four=[0]*4
    return check_sourced_harmonic_corners(
         initial,velocity,source,boundary_six,boundary_four,4)
