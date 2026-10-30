"""Independent exact-rational frozen ADM constraint-energy verifier.

For constant positive spatial metric h, lapse N>0, and shift beta on T^3,
checks the symmetric principal matrices, characteristic polynomial and
homogeneous constraint-energy flux. No SymPy or PHYSQED geometry imports.
The finite rational tests are evidence for, not a formalization of, the
periodic PDE energy argument; no claim of evolving Einstein solutions.
"""
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json


def rational(x):
    if type(x) is int or type(x) is str or isinstance(x,F):
        return F(x)
    raise ValueError("Exact rational strings/integers/Fraction required")


def matrix(x,n):
    if not isinstance(x,(list,tuple)) or len(x)!=n or any(
            not isinstance(r,(list,tuple)) or len(r)!=n for r in x):
        raise ValueError("Incorrect matrix shape")
    return [[rational(c) for c in row] for row in x]


def ident(n):
    return [[F(int(i==j)) for j in range(n)] for i in range(n)]


def mul(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),F(0))
             for j in range(len(B[0]))] for i in range(len(A))]


def det(A):
    n=len(A);a=[list(r) for r in A];d=F(1)
    for k in range(n):
        p=next((i for i in range(k,n) if a[i][k]),None)
        if p is None: return F(0)
        if p!=k: a[p],a[k]=a[k],a[p];d=-d
        x=a[k][k];d*=x
        for i in range(k+1,n):
            f=a[i][k]/x
            for j in range(k+1,n):a[i][j]-=f*a[k][j]
            a[i][k]=0
    return d


def inverse(A):
    n=len(A)
    m=[A[i][:]+ident(n)[i] for i in range(n)]
    for k in range(n):
        p=next((i for i in range(k,n) if m[i][k]),None)
        if p is None: raise ValueError("Singular spatial metric")
        m[p],m[k]=m[k],m[p]
        z=m[k][k]
        for j in range(2*n):m[k][j]/=z
        for i in range(n):
            if i==k:continue
            z=m[i][k]
            for j in range(2*n):m[i][j]-=z*m[k][j]
    return [row[n:] for row in m]


def positive(A):
    return all(det([r[:k] for r in A[:k]])>0 for k in range(1,len(A)+1))


def charpoly(A):
    """Characteristic coefficients by exact Faddeev-LeVerrier."""
    n=len(A);B=ident(n);cs=[F(1)]
    for k in range(1,n+1):
        AB=mul(A,B)
        c=-sum((AB[i][i] for i in range(n)),F(0))/k
        cs.append(c)
        B=[[AB[i][j]+(c if i==j else 0) for j in range(n)]
           for i in range(n)]
    return cs


def frozen_matrices(h,lapse,shift):
    h=matrix(h,3)
    if any(h[i][j]!=h[j][i] for i,j in product(range(3),repeat=2)):
        raise ValueError("Spatial metric must be symmetric")
    if not positive(h): raise ValueError("Spatial metric must be SPD")
    N=rational(lapse)
    if N<=0:raise ValueError("Strictly positive lapse required")
    if not isinstance(shift,(list,tuple)) or len(shift)!=3:
        raise ValueError("Three spatial shift components required")
    beta=[rational(x) for x in shift]
    hinv=inverse(h)
    S=[[F(0) for _ in range(4)] for _ in range(4)]
    S[0][0]=1
    for i,j in product(range(3),repeat=2):S[i+1][j+1]=4*hinv[i][j]
    if not positive(S):raise AssertionError("Symmetrizer not positive")
    A=[]
    for d in range(3):
        Ad=[[(-beta[d] if i==j else F(0)) for j in range(4)]
            for i in range(4)]
        for i in range(3):
            Ad[0][i+1]=-2*N*hinv[d][i]
            Ad[i+1][0]=-N*F(int(i==d))/2
        A.append(Ad)
    return h,hinv,N,beta,S,A


def characteristic_check(hinv,N,beta,A,xi):
    xi=[rational(x) for x in xi]
    if len(xi)!=3 or not any(xi):
        raise ValueError("Nonzero spatial covector required")
    symbol=[[sum((xi[d]*A[d][i][j] for d in range(3)),F(0))
             for j in range(4)] for i in range(4)]
    b=sum((beta[i]*xi[i] for i in range(3)),F(0))
    q=N*N*sum((hinv[i][j]*xi[i]*xi[j]
               for i,j in product(range(3),repeat=2)),F(0))
    actual=charpoly(symbol)
    expected=[F(1),4*b,6*b*b-q,4*b**3-2*q*b,b**4-q*b*b]
    return {"covector":[str(v) for v in xi],
            "charpoly_verified":actual==expected,
            "squared_normal_speed":str(q),
            "positive_squared_normal_speed":q>0,
            "shift_frequency":str(b)}


def flux_check(hinv,N,beta,H,M,dH,dM):
    H=rational(H);M=[rational(v) for v in M]
    dH=[rational(v) for v in dH]
    dM=[[rational(v) for v in row] for row in dM]
    if len(M)!=3 or len(dH)!=3 or len(dM)!=3 or any(len(row)!=3 for row in dM):
        raise ValueError("Flux test needs 3 spatial derivatives")
    raised=[sum((hinv[i][j]*M[j] for j in range(3)),F(0)) for i in range(3)]
    dtH=sum((beta[d]*dH[d] for d in range(3)),F(0))+2*N*sum(
        (hinv[d][j]*dM[d][j] for d,j in product(range(3),repeat=2)),F(0))
    dtM=[sum((beta[d]*dM[d][i] for d in range(3)),F(0))+N*dH[i]/2
         for i in range(3)]
    dtenergy=H*dtH+4*sum((hinv[i][j]*M[i]*dtM[j]
                          for i,j in product(range(3),repeat=2)),F(0))
    adv=sum((beta[d]*(H*dH[d]+4*sum(
        (hinv[i][j]*M[i]*dM[d][j]
         for i,j in product(range(3),repeat=2)),F(0)))
         for d in range(3)),F(0))
    flux=2*N*sum((dH[d]*raised[d]+H*sum(
        (hinv[d][j]*dM[d][j] for j in range(3)),F(0))
        for d in range(3)),F(0))
    return {"pointwise_exact_energy_flux_identity":dtenergy==adv+flux,
            "energy_time_derivative":str(dtenergy),
            "transport_plus_flux_divergence":str(adv+flux)}


def audit_frozen_adm(h,lapse,shift):
    h,hinv,N,beta,S,A=frozen_matrices(h,lapse,shift)
    sym=[mul(S,Ad) for Ad in A]
    symmetric=all(v[i][j]==v[j][i] for v in sym
                  for i,j in product(range(4),repeat=2))
    chars=[characteristic_check(hinv,N,beta,A,xi) for xi in
           ([1,0,0],[0,1,0],[0,0,1],[1,2,-1])]
    fluxes=[flux_check(hinv,N,beta,H,M,dH,dM)
            for H,M,dH,dM in (
              (F(2),[1,2,-3],[4,-2,1],[[1,2,3],[0,-1,2],[-4,0,1]]),
              (F(-3,2),[0,F(2,3),-1],[-3,0,5],[[2,1,-1],[4,2,0],[1,2,3]]))]
    passed=(symmetric and
            all(c["charpoly_verified"] and c["positive_squared_normal_speed"]
                for c in chars) and
            all(v["pointwise_exact_energy_flux_identity"] for v in fluxes))
    receipt={"schema":"physqed.frozen-adm-energy.v1",
      "status":("PASS_FROZEN_PERIODIC_CONSTRAINT_ENERGY_ALGEBRA"
                if passed else "REJECTED_FROZEN_CONSTRAINT_ENERGY_ALGEBRA"),
      "metric_spd_exact":True,"positive_lapse_exact":True,
      "symmetrizer_spd_exact":True,
      "all_three_principal_symbols_symmetrized":symmetric,
      "characteristic_trials":chars,"energy_flux_trials":fluxes,
      "energy_functional":"integral (H^2+4h^ij M_i M_j)/2 over T^3",
      "flux_identity":"dt e-beta^i partial_i e-2N partial_i(H M^i)=0",
      "frozen_periodic_zero_initial_implies_zero_if_smooth_solution":bool(passed),
      "general_variable_coefficient_energy_estimate_proven":False,
      "global_einstein_solution_proven":False,
      "independent_exact_arithmetic":True,
      "limitations":"Rational frozen coefficients; finitely many exact covectors and flux trials; periodic energy-uniqueness inference additionally uses smooth-solution calculus"}
    canon=json.dumps(receipt,sort_keys=True,separators=(",",":"))
    receipt["receipt_sha256"]=sha256(canon.encode()).hexdigest()
    return receipt
