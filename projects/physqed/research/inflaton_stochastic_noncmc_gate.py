"""Scoped numerical gate: stochastic phase-space momentum versus non-CMC geometry.
Two grid-derivative-null modes are projected; this is not a quantum state
construction or a Hamiltonian-constraint/Einstein evolution proof.
"""
import json,math
from pathlib import Path
import numpy as np
MU=10.05;KAPPA=10000.;a=(4+.016202803686105016)/2;yc=.81
v=3-a*a/2;beta=v/((a-yc)**2+2*v);lam=KAPPA**2/(4*beta)
B=lam-KAPPA**2/2;zv=math.sqrt(KAPPA*(a-yc)/B)
xv=math.sqrt(a+KAPPA*zv*zv/2);width=math.sqrt(2/lam)/zv;L=.4
def D(f,dx):return (np.roll(f,-1)-np.roll(f,1))/(2*dx)
def sample(xi):
    rng=np.random.default_rng(20261109)
    f=[];mom=[]
    for _ in range(2):
        F=np.zeros_like(xi);P=np.zeros_like(xi)
        for j in range(1,9):
            k=2*math.pi*j/L;om=math.sqrt(k*k+60**2)
            fs,fc,ps,pc=rng.normal(size=4)
            F+=(fs*np.sin(k*xi)+fc*np.cos(k*xi))/math.sqrt(om)
            P+=math.sqrt(om)*(ps*np.sin(k*xi)+pc*np.cos(k*xi))
        F-=np.mean(F);fac=3.8e-7/np.std(F)
        f.append(fac*F);mom.append(fac*P)
    return np.array(f),np.array(mom)
def case(n):
    xi=L*np.arange(n)/n;dx=L/n
    f,mom=sample(xi)
    z0=zv*np.tanh((xi-L/4)/width)*np.tanh((3*L/4-xi)/width)
    f=np.array([xv+f[0],z0+f[1]])
    g=np.array([D(f[0],dx),D(f[1],dx)])
    j=np.sum(g*mom,axis=0)
    W=np.array([np.ones(n),(-1.)**np.arange(n)])
    gram=np.einsum('ai,bi,i->ab',W,W,np.sum(g*g,axis=0))
    c=np.linalg.solve(gram,W@j)
    new=mom-np.sum(c[:,None]*W,axis=0)[None,:]*g
    jnew=np.sum(new*g,axis=0)
    freq=np.arange(n);sym=1j*np.sin(2*math.pi*freq/n)/dx
    Kh=np.zeros(n,dtype=complex)
    mask=(freq!=0)&(freq!=n//2)
    Kh[mask]=np.fft.fft(.5*MU**2*jnew)[mask]/sym[mask]
    k=np.fft.ifft(Kh).real
    residual=float(np.max(abs(-2*D(k,dx)+MU**2*jnew)))
    lost=float(1-np.sum(new*new)/np.sum(mom*mom))
    assert residual<2e-12 and 0<=lost<.001
    assert np.max(abs(jnew))>1e-7
    return dict(n=n,initial_momentum_residual=residual,
                kinetic_fraction_removed=lost,
                original_momentum_source_max=float(np.max(abs(MU**2*j))),
                retained_momentum_source_max=float(np.max(abs(MU**2*jnew))),
                local_curvature_offset_max=float(np.max(abs(k))))
if __name__=='__main__':
    cases=[case(n) for n in (128,256,512)]
    r=dict(schema="physqed.stochastic-noncmc-momentum-gate.v1",
      status="PASS_SCOPED_DISCRETE_MOMENTUM_ONLY__NOT_QUANTUM_STATE",
      cases=cases,hamiltonian_constraint_solved=False,
      physical_stochastic_state_derived=False,full_einstein_evolved=False)
    Path("inflaton_noncmc_momentum_receipt.json").write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(json.dumps(r,indent=2,sort_keys=True))
