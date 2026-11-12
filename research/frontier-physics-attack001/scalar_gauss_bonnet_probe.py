"""Known scalar--Gauss--Bonnet decoupling-limit Schwarzschild solution.

Action (matter-independent sector): S = integral sqrt(-g)[-1/2(grad phi)^2
+ eta*phi*GB]. Fixed Schwarzschild metric (no backreaction). Not a
singularity-resolution or full coupled gravitational solution.
"""
import sympy as s

def main():
    M,r,eta,phi_inf,C=s.symbols('M r eta phi_inf C', real=True, nonzero=True)
    A=1-2*M/r
    GB=48*M**2/r**6  # For Ricci-flat Schwarzschild, GB=K.
    # Integrate (r^2 A phi')' = -eta r^2 GB.
    radial_flux=C+16*eta*M**2/r**3
    assert s.simplify(s.diff(radial_flux,r)+eta*r**2*GB)==0
    # Regularity of derivative at r=2M requires C=-2eta/M.
    C_h=-2*eta/M
    assert s.simplify(radial_flux.subs({r:2*M,C:C_h}))==0
    phi_prime=s.factor(radial_flux.subs(C,C_h)/(r**2*A))
    phi=phi_inf+2*eta/(M*r)+2*eta/r**2+8*eta*M/(3*r**3)
    assert s.simplify(s.diff(phi,r)-phi_prime)==0
    scalar_eq=s.simplify(s.diff(r**2*A*s.diff(phi,r),r)/r**2+eta*GB)
    assert scalar_eq==0
    assert s.simplify(phi.subs(r,2*M)-phi_inf-11*eta/(6*M**2))==0
    assert s.simplify(phi_prime.subs(r,2*M)+3*eta/(2*M**3))==0
    assert s.limit(r*(phi-phi_inf),r,s.oo)==2*eta/M
    assert s.limit(r**3*(phi-phi_inf),r,0,dir='+')==8*eta*M/3
    print('PASS: Schwarzschild GB source =',GB)
    print('PASS: horizon regularity selects flux C =',C_h)
    print('PASS: exact scalar profile =',phi)
    print('PASS: scalar field equation residual =',scalar_eq)
    print('PASS: regular horizon; scalar still diverges ~ 8 eta M/(3r^3) at Schwarzschild center')
    print('SCOPE: prior-art fixed-background probe; backreaction and quantum dynamics omitted')

if __name__=='__main__':
    main()
