"""Independent SymPy/SI oracle; imports ONLY the generator, not PHYSQED verifier."""
import ast,json,sys
from pathlib import Path
from sympy import Symbol, Rational, Poly, expand
ROOT=Path(__file__).resolve().parents[2]/'projects'/'physqed'
sys.path.insert(0,str(ROOT))
from benchmarks.two_premise_v09 import cases

def formal(n,sym):
    if set(n)=={'var'}:return sym[n['var']]
    if set(n)=={'const'}:return Rational(n['const'])
    if n.get('op')=='pow':return formal(n['arg'],sym)**n['exp']
    if n.get('op')=='add':return sum(formal(x,sym) for x in n['args'])
    if n.get('op')=='mul':
        r=1
        for x in n['args']:r*=formal(x,sym)
        return r
    raise ValueError('unsupported formal')

def controlled(x,sym):
    def rec(n):
        if isinstance(n,ast.Name):return sym[n.id]
        if isinstance(n,ast.Constant) and type(n.value) is int:return Rational(n.value)
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -rec(n.operand)
        if isinstance(n,ast.BinOp):
            a=rec(n.left)
            if isinstance(n.op,ast.Pow):
                if not isinstance(n.right,ast.Constant) or type(n.right.value) is not int:return ValueError()
                return a**n.right.value
            b=rec(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
        raise ValueError('bad grammar')
    return rec(ast.parse(x,mode='eval').body)

BASE=('M','L','T','I','Theta','N','J')
def dim(n,dims):
    if set(n)=={'var'}:return tuple(dims[n['var']].get(b,0) for b in BASE)
    if set(n)=={'const'}:return (0,)*7
    if n.get('op')=='pow':return tuple(v*n['exp'] for v in dim(n['arg'],dims))
    if n.get('op')=='mul':
        ds=[dim(x,dims) for x in n['args']]
        return tuple(sum(y) for y in zip(*ds))
    if n.get('op')=='add':
        ds=[dim(x,dims) for x in n['args']]
        if len(set(ds))!=1:raise ValueError('sum dimensions')
        return ds[0]
    raise ValueError('bad dimensions')

def equality_dim(p,syms,units):
    l,r=p['lhs'],p['rhs'];ld,rd=dim(l,units),dim(r,units)
    if expand(formal(l,syms))==0:ld=rd
    if expand(formal(r,syms))==0:rd=ld
    if ld!=rd:raise ValueError('incompatible dimensions')
    return ld

def valid(c):
    syms={n:Symbol(n) for n in c['variables']};sym_vars=list(syms.values())
    prefix='For all real scalars '+', '.join(c['variables'])+', if '
    tail=' This checks only a conditional polynomial consequence; no physical law is established.'
    s=c['statement']
    if not s.startswith(prefix) or not s.endswith(tail):return False
    payload=s[len(prefix):-len(tail)]
    if payload.count(', then ')!=1:return False
    lhs,rhs=payload.split(', then ')
    if lhs.count(' and ')!=1 or not rhs.endswith(' holds.'):return False
    antecedents=lhs.split(' and ');texts=antecedents+[rhs[:-7]]
    eqs=c['premises']+[c['conclusion']]
    if len(eqs)!=3 or len(c['witnesses'])!=2:return False
    for text,p in zip(texts,eqs):
        if text.count(' == ')!=1:return False
        l,r=text.split(' == ')
        if expand(controlled(l,syms)-formal(p['lhs'],syms))!=0:return False
        if expand(controlled(r,syms)-formal(p['rhs'],syms))!=0:return False
    p1=expand(formal(c['premises'][0]['lhs'],syms)-formal(c['premises'][0]['rhs'],syms))
    p2=expand(formal(c['premises'][1]['lhs'],syms)-formal(c['premises'][1]['rhs'],syms))
    if any(Poly(p,sym_vars).total_degree()>1 for p in (p1,p2)):return False
    g1=[p1.diff(v) for v in sym_vars];g2=[p2.diff(v) for v in sym_vars]
    if not any(expand(g1[i]*g2[j]-g1[j]*g2[i])!=0 for i in range(len(sym_vars)) for j in range(i+1,len(sym_vars))):return False
    w1,w2=(formal(w,syms) for w in c['witnesses'])
    lhs=expand(formal(c['conclusion']['lhs'],syms)-formal(c['conclusion']['rhs'],syms))
    if expand(lhs-w1*p1-w2*p2)!=0:return False
    d1,d2=(equality_dim(p,syms,c['dimensions']) for p in c['premises'])
    dc=equality_dim(c['conclusion'],syms,c['dimensions'])
    for d,w in zip((d1,d2),c['witnesses']):
        if tuple(a+b for a,b in zip(d,dim(w,c['dimensions'])))!=dc:return False
    return True

def run():
    rows=[]
    for i,(label,c) in enumerate(cases()):
        try: verdict=valid(c)
        except (ValueError,TypeError,KeyError,IndexError,AttributeError,OverflowError,ZeroDivisionError):verdict=False
        expected=label=='ACCEPT_EXACT'
        rows.append({'case':i,'label':label,'oracle_accept':verdict,'expected':expected,'agrees':verdict==expected})
    return {'total':len(rows),'agreements':sum(x['agrees'] for x in rows),
            'oracle':'SymPy expansion/gradients plus independent AST and SI exponent implementation',
            'physical_truth_certified':False,'independently_annotated_external_source':False,'rows':rows}
if __name__=='__main__':
    r=run()
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='rows'},indent=2))
    raise SystemExit(0 if r['total']==r['agreements']==540 else 2)
