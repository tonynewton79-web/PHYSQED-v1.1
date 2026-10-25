"""Independent v0.8 oracle: SymPy algebra and separate AST parsing.
Does NOT import PHYSQED's conditional_claims or controlled_semantics.
The 560 cases remain internally generated, not external blind tasks.
"""
import ast,json,sys
from pathlib import Path
from sympy import Symbol,expand,sympify
ROOT=Path(__file__).resolve().parents[2]/'projects'/'physqed'
sys.path.insert(0,str(ROOT))
from benchmarks.conditional_v08 import cases,specimen

def formal(n,names):
    if 'var' in n:return names[n['var']]
    if 'const' in n:return sympify(n['const'],rational=True)
    if n.get('op')=='pow':return formal(n['arg'],names)**n['exp']
    if n.get('op')=='mul':
        r=1
        for x in n['args']:r*=formal(x,names)
        return r
    if n.get('op')=='add':return sum(formal(x,names) for x in n['args'])
    raise ValueError('unsupported formal expression')

def controlled(n,names):
    if isinstance(n,ast.Name):return names[n.id]
    if isinstance(n,ast.Constant) and type(n.value) is int:return sympify(n.value)
    if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -controlled(n.operand,names)
    if isinstance(n,ast.BinOp):
        l,r=controlled(n.left,names),controlled(n.right,names)
        if isinstance(n.op,ast.Add):return l+r
        if isinstance(n.op,ast.Sub):return l-r
        if isinstance(n.op,ast.Mult):return l*r
        if isinstance(n.op,ast.Pow) and n.right.value>=0:return l**r
    raise ValueError('invalid controlled math')

def evaluate(r):
    vs=r['variables']; sym={v:Symbol(v,real=True) for v in vs}
    a,b=r['premise']['lhs'],r['premise']['rhs']
    c,d=r['conclusion']['lhs'],r['conclusion']['rhs']
    mathematical=expand(formal(c,sym)-formal(d,sym)-
                        formal(r['witness'],sym)*(formal(a,sym)-formal(b,sym)))==0
    text=r['statement'];first=f'For all real scalars {", ".join(vs)}, if '
    last=' This checks only the conditional polynomial consequence; no physical law is established.'
    exact=False
    if text.startswith(first) and text.endswith(last):
        segment=text[len(first):-len(last)]
        if segment.count(', then ')==1 and segment.endswith(' holds.'):
            left,right=segment[:-7].split(', then ')
            if left.count(' == ')==right.count(' == ')==1:
                la,lb=left.split(' == '); lc,ld=right.split(' == ')
                try:
                    checks=[(la,a),(lb,b),(lc,c),(ld,d)]
                    exact=all(expand(controlled(ast.parse(t,mode='eval').body,sym)-formal(q,sym))==0
                              for t,q in checks)
                except Exception:exact=False
    return mathematical,exact

def run():
    data=cases();records=[]
    for i,(category,r) in enumerate(data):
        algebra_ok,text_ok=evaluate(r)
        base=specimen(i//7)
        dims_unchanged=r['dimensions']==base['dimensions']
        provenance_supported=r['provenance']=='SYNTHETIC_SCOPED'
        accepted=algebra_ok and text_ok and dims_unchanged and provenance_supported
        expected=(category=='ACCEPT_CONDITIONAL_EXACT')
        records.append({'i':i,'category':category,'oracle_accept':accepted,
                        'expected_accept':expected,'agrees':accepted==expected})
    return {'oracle':'independently written SymPy algebra + AST controlled text check + frozen dimensional contract',
            'total':len(records),'agreement':sum(x['agrees'] for x in records),
            'standalone_external_dataset':False,
            'formal_lean_compilation':False,'records':records}
if __name__=='__main__':
    r=run()
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='records'},indent=2))
    raise SystemExit(0 if r['total']==r['agreement']==560 else 1)
