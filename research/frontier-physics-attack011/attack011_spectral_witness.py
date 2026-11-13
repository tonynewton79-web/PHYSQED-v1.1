"""Attack 011: exact H² compact-support negative Rayleigh witness.

Applies to the FULLY CONSTRAINED FLAT scalar operator
H=(Delta²/mu+Delta)/(2/eps+3). For a curved exterior it implies
a negative essential band only IF the full physical constraint-reduced
operator approaches this H in the requisite local quadratic-form sense.
"""
import sympy as s

def main():
    t=s.symbols("t",real=True)
    f=(1-t*t)**3
    fp=s.diff(f,t)
    lap=s.simplify(s.diff(f,t,2)+2*fp/t)
    I0=s.integrate(t*t*f*f,(t,0,1))
    I1=s.integrate(t*t*fp*fp,(t,0,1))
    I2=s.integrate(t*t*lap*lap,(t,0,1))
    assert (I0,I1,I2)==(s.Rational(1024,45045),s.Rational(1536,5005),s.Rational(512,77))
    assert I1/I0==s.Rational(27,2)
    assert I2/I0==s.Rational(585,2)
    mu,eps=s.symbols("mu eps",positive=True);D=2/eps+3
    L=6/s.sqrt(mu)
    expectation=s.factor((I2/(I0*mu*L**4)-I1/(I0*L**2))/D)
    assert s.simplify(expectation+43*mu/(288*D))==0
    assert expectation.subs({mu:1,eps:s.Rational(1,1000)})==-s.Rational(43,288*2003)
    z=s.symbols("z",nonnegative=True)
    symbol=(z*z/mu-z)/D
    assert s.solve(s.diff(symbol,z),z)==[mu/2]
    assert s.simplify(symbol.subs(z,mu/2)+mu/(4*D))==0
    print("PASS explicit compact-support test f=(1-|x-x0|²/L²)_+³, L=6/sqrt(mu)")
    print("PASS exact negative Rayleigh quotient -43*mu/[288*(2/eps+3)]")
    print("PASS flat scalar continuous spectral band [-mu/(4D),infinity) via Fourier/Weyl")
    print("WARNING curved physical spectrum requires independently reduced operator")

if __name__=="__main__":main()
