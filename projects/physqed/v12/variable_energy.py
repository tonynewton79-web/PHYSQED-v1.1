"""Exact variable-coefficient symmetric-hyperbolic energy-balance verifier.

For U_t + A^j U_j + B U = f and symmetric S with S A^j
symmetric, verifies e_t + div F = U^T R U/2 + U^T S f,
R=S_t+div(S A^j)-S B-B^T S.

This is an algebraic identity. It does NOT establish uniform SPD,
coefficient boundedness, global domain regularity, boundary flux or
well-posedness on a spacetime.
"""
import sympy as S


class ScopeError(ValueError):
    pass


def _zero(v):
    return S.simplify(S.cancel(S.together(v))) == 0


def _matrix_zero(M):
    return all(_zero(e) for e in M)


def audit_matrix_energy(coords,symmetrizer,principal,lower_order,source=None):
    coords=tuple(coords)
    if not 2<=len(coords)<=4 or len(set(coords))!=len(coords):
        raise ScopeError("Need one time and 1..3 spatial coordinates")
    Sm=S.Matrix(symmetrizer)
    n=Sm.rows
    if not 1<=n<=6 or Sm.shape!=(n,n):
        raise ScopeError("Supported system dimension is 1..6")
    if len(principal)!=len(coords)-1:
        raise ScopeError("Principal matrix count incorrect")
    A=[S.Matrix(a) for a in principal]
    B=S.Matrix(lower_order)
    if B.shape!=(n,n) or any(a.shape!=(n,n) for a in A):
        raise ScopeError("Matrix shapes differ")
    if not _matrix_zero(Sm-Sm.T):
        raise ScopeError("Symmetrizer must be symmetric")
    if any(not _matrix_zero(Sm*a-(Sm*a).T) for a in A):
        raise ScopeError("Principal symbol fails symmetrizer identity")
    f=S.zeros(n,1) if source is None else S.Matrix(source)
    if f.shape!=(n,1):
        raise ScopeError("Source vector shape differs")
    U=S.Matrix([S.Function("u"+str(i))(*coords) for i in range(n)])
    e=S.expand((U.T*Sm*U)[0]/2)
    flux=[S.expand((U.T*Sm*a*U)[0]/2) for a in A]
    R=(Sm.diff(coords[0])+sum(
        ((Sm*A[i]).diff(coords[i+1]) for i in range(len(A))),
        S.zeros(n,n))-Sm*B-B.T*Sm).applyfunc(S.simplify)
    pde_rhs= -sum((A[i]*U.diff(coords[i+1])
                   for i in range(len(A))),S.zeros(n,1))-B*U+f
    time_derivs={
        S.Derivative(U[i],coords[0]):pde_rhs[i] for i in range(n)}
    lhs=S.diff(e,coords[0])+sum(
        (S.diff(flux[i],coords[i+1]) for i in range(len(A))),S.S.Zero)
    rhs=(U.T*R*U)[0]/2+(U.T*Sm*f)[0]
    residual=S.expand(lhs.xreplace(time_derivs)-rhs)
    return {
        "exact_local_balance_identity":bool(_zero(residual)),
        "energy_density":e,"energy_flux":tuple(flux),
        "coefficient_defect":R,
        "residual":S.simplify(residual),
        "global_coercivity_proven":False,
        "bounded_defect_proven":False,
        "boundary_flux_control_proven":False,
        "global_pde_uniqueness_proven":False}


def adm_constraint_matrices(coords,spatial_metric,lapse,shift):
    """Generate all principal and lower-order shifted-ADM constraint terms.

    U=(H,M_1,M_2,M_3), positive-K convention. Input coordinates
    are trusted SymPy objects; this function is not a public JSON parser.
    """
    coords=tuple(coords)
    if len(coords)!=4:
        raise ScopeError("Four spacetime coordinates required")
    spatial=coords[1:]
    h=S.Matrix(spatial_metric)
    if h.shape!=(3,3) or not _matrix_zero(h-h.T):
        raise ScopeError("Symmetric 3-metric required")
    N=S.sympify(lapse)
    beta=S.Matrix(shift)
    if beta.shape!=(3,1) or _zero(N) or _zero(h.det()):
        raise ScopeError("Nonsingular lapse, metric and 3-shift required")
    hi=h.inv().applyfunc(S.simplify)
    Gamma=[[[S.simplify(sum(
        hi[a,k]*(S.diff(h[k,b],spatial[c])+
                 S.diff(h[k,c],spatial[b])-
                 S.diff(h[b,c],spatial[k]))
        for k in range(3))/2)
        for c in range(3)] for b in range(3)] for a in range(3)]
    Lie=S.Matrix(3,3,lambda i,j:sum(
        beta[k]*S.diff(h[i,j],spatial[k])+
        h[i,k]*S.diff(beta[k],spatial[j])+
        h[j,k]*S.diff(beta[k],spatial[i]) for k in range(3)))
    K=(h.diff(coords[0])-Lie)/(2*N)
    Ktr=S.simplify(S.trace(hi*K))
    ai=S.Matrix([S.diff(N,x)/N for x in spatial])
    au=hi*ai
    Sm=S.zeros(4,4)
    Sm[0,0]=1
    for i in range(3):
        for j in range(3):
            Sm[i+1,j+1]=4*hi[i,j]
    As=[]
    for d in range(3):
        Ad=-S.eye(4)*beta[d]
        for i in range(3):
            Ad[0,i+1]=-2*N*hi[d,i]
            Ad[i+1,0]=-N*S.KroneckerDelta(i,d)/2
        As.append(Ad)
    B=S.zeros(4)
    B[0,0]=2*N*Ktr
    for j in range(3):
        B[0,j+1]=2*N*sum(
            hi[i,k]*Gamma[j][i][k]
            for i in range(3) for k in range(3))-4*N*au[j]
    for i in range(3):
        B[i+1,0]=-N*ai[i]
        for j in range(3):
            B[i+1,j+1]=(N*Ktr if i==j else 0)-S.diff(beta[j],spatial[i])
    return Sm,As,B
