"""Research Attack 002: exact scalar--Gauss--Bonnet flux obstruction.

Assumptions: 4D static spherically symmetric spacetime, areal radius r,
 ds^2=-N(r)^2 F(r) dt^2 + dr^2/F(r)+r^2 dOmega^2,
N(r)>0 finite nonzero at center and horizon.  Static phi=phi(r),
canonical scalar kinetic term and linear eta*phi*Gauss-Bonnet coupling,
without scalar potentials or other phi terms.  This derives a necessary
scalar equation in a fully coupled theory; it does not solve the gravity EOM.
"""
import sympy as s
r,eta,M,ell,a,b,c=s.symbols('r eta M ell a b c', positive=True)
F=s.Function('F')(r)
N=s.Function('N')(r)
phi=s.Function('phi')(r)
u=s.diff(N,r)/N
# Orthonormal curvature sections for diagonal static spherical metric.
X=s.diff(F,r,2)/2+s.Rational(3,2)*u*s.diff(F,r)+F*s.diff(N,r,2)/N
Y=(s.diff(F,r)/2+F*u)/r
Z=-s.diff(F,r)/(2*r)
W=(1-F)/r**2
GB_sections=s.expand(-8*(X*W+2*Y*Z))
Q=N*(F-1)*(s.diff(F,r)+2*F*u)
GB_div=4*s.diff(Q,r)/(N*r**2)
assert s.simplify(GB_sections-GB_div)==0
# Action: kinetic -1/2 (nabla phi)^2 + eta phi GB => box phi = - eta GB
scalar_eom=s.diff(N*r**2*F*s.diff(phi,r),r)+eta*N*r**2*GB_sections
flux=N*r**2*F*s.diff(phi,r)+4*eta*Q
assert s.simplify(scalar_eom-s.diff(flux,r))==0
# Regular center F=1-c r^2 + ..., N=1+a r^2+...; phi' derived with C=0.
Fc=1-c*r**2+b*r**4
Nc=1+a*r**2
phipr_center=s.factor(-4*eta*(Fc-1)*(s.diff(Fc,r)+2*Fc*s.diff(Nc,r)/Nc)/(r**2*Fc))
assert s.simplify(s.limit(phipr_center/r,r,0)+8*eta*c*(c-2*a))==0
# Generic horizon of order p: F=f_p x^p, N=N_h (1+kx) => divergence 4eta*p/rh^2/x.
x,rh,fp,nh,k=s.symbols('x rh fp nh k',positive=True)
for p in (1,2,3,4):
    Fh=fp*x**p
    Nh=nh*(1+k*x)
    R=rh+x
    u_h=s.diff(Nh,x)/Nh
    phipr_h=-4*eta*(Fh-1)*(s.diff(Fh,x)+2*Fh*u_h)/(R**2*Fh)
    assert s.simplify(s.limit(x*phipr_h,x,0)-4*eta*p/rh**2)==0
# Hayward exact radial flux, two horizon threshold, values at horizon.
D=r**3+2*M*ell**2
Fh=1-2*M*r**2/D
Nh=s.S.One
GB_h=s.factor(4*s.diff((Fh-1)*s.diff(Fh,r),r)/r**2)
Jphi=s.factor(-4*eta*(Fh-1)*s.diff(Fh,r)/(r**2*Fh))
assert s.simplify(s.limit(Jphi/r,r,0)+8*eta/ell**4)==0
poly=s.factor(D*Fh)
assert s.factor(poly-(r**3-2*M*r**2+2*M*ell**2))==0
r_ext=4*M/3
assert s.solve(poly.subs(r,r_ext),ell**2)==[s.Rational(16,27)*M**2]
rhor=s.symbols('r_h',positive=True)
# Under F(r_h)=0, ell^2 = r_h^2*(2M-r_h)/(2M):
ell2_on_horizon=rhor**2*(2*M-rhor)/(2*M)
Fprimeh=s.simplify(s.diff(Fh,r).subs({r:rhor,ell**2:ell2_on_horizon}))
assert s.simplify(Fprimeh-(3*rhor-4*M)/(2*M*rhor))==0
# Special exactly factorable two-horizon Hayward case M=1, ell^2=1/2.
example_poly=s.factor(poly.subs({M:1,ell**2:s.Rational(1,2)}))
assert example_poly==(r-1)*(r**2-r-1)
r_inner=s.S.One
r_outer=(1+s.sqrt(5))/2
assert s.simplify(example_poly.subs(r,r_outer))==0
Fi=s.simplify(Fprimeh.subs({M:1,rhor:r_inner}))
Fo=s.simplify(Fprimeh.subs({M:1,rhor:r_outer}))
assert Fi==-s.Rational(1,2)
assert s.simplify(Fo-(s.Rational(5,2)-s.sqrt(5)))==0
assert Fi<0 and Fo>0
# Horizon regularity would require C=-4eta*N_h*F'_h, which has
# opposite signs at two simple horizons, thus cannot hold at both.
C_inner=-4*eta*Fi
C_outer=s.simplify(-4*eta*Fo)
assert s.simplify(C_inner-C_outer)!=0
# Potential integration balance: integral_0^rh N r^2 V'(phi) = -4eta N_h F'_h
print('PASS: generic N(r),F(r) Gauss-Bonnet exact divergence identity')
print('PASS: scalar equation equals radial derivative of conserved topological flux')
print('CENTER: phi-prime leading coefficient:',s.simplify(s.limit(phipr_center/r,r,0)))
print('PASS: 4 horizon orders p=1,2,3,4 require logarithmic scalar divergence for center-regular flux')
print('HAYWARD: extremal ell^2 = 16M^2/27, horizon derivative:',Fprimeh)
print('HAYWARD: exact two horizons r=1 and (1+sqrt(5))/2; required fluxes:',C_inner,C_outer)
print('HAYWARD: center-regular scalar derivative:',Jphi)
print('HAYWARD: GB =',GB_h)
print('POTENTIAL SUM RULE: integral_0^rh N*r^2*Vprime(phi) dr = -4*eta*N(rh)*Fprime(rh)')
print('SCOPE: exact scalar EOM obstruction, no Einstein equation or nonlinear collapse solved; prior-art-sensitive')
