"""PHYSQED v0.8, deterministic 560 synthetic conditional/algebra/dimension challenges."""
import ast,copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from conditional_claims import verify,ConditionalRefusal,VERSION,TAIL

def to_json(n):
    if isinstance(n,ast.Name):return {'var':n.id}
    if isinstance(n,ast.Constant) and type(n.value) is int:return {'const':str(n.value)}
    if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):
        return {'op':'mul','args':[{'const':'-1'},to_json(n.operand)]}
    if isinstance(n,ast.BinOp):
        op=n.op
        if isinstance(op,ast.Pow):
            if type(n.right.value) is not int:raise ValueError
            return {'op':'pow','arg':to_json(n.left),'exp':n.right.value}
        if isinstance(op,ast.Sub):
            return {'op':'add','args':[to_json(n.left),{'op':'mul','args':[{'const':'-1'},to_json(n.right)]}]}
        if isinstance(op,(ast.Mult,ast.Add)):
            return {'op':'mul' if isinstance(op,ast.Mult) else 'add','args':[to_json(n.left),to_json(n.right)]}
    raise ValueError('benchmark source only uses supported ops')

def expr(s):return to_json(ast.parse(s,mode='eval').body)

def specimen(i):
    t=i//2+1
    if i%2==0:
        vs=['m','c','k','x','v','a']
        ds={'m':{'M':1},'c':{'M':1,'T':-1},'k':{'M':1,'T':-2},
            'x':{'L':1},'v':{'L':1,'T':-1},'a':{'L':1,'T':-2}}
        al,ar='m*a + c*v + k*x','0'
        cl,cr=f'{t}*(m*a*v+k*x*v)',f'-{t}*c*v**2'
        wit=f'{t}*v'
    else:
        vs=['x','y','z']
        ds={x:{} for x in vs}
        al,ar='x+y','z'
        cl,cr=f'{t}*(x**2-z**2)',f'-{t}*y*(x+z)'
        wit=f'{t}*(x+z)'
    text=(f'For all real scalars {", ".join(vs)}, if {al} == {ar}, then '
          f'{cl} == {cr} holds.'+TAIL)
    return {'schema':VERSION,'statement':text,'variables':vs,
            'dimensions':ds,'premise':{'lhs':expr(al),'rhs':expr(ar)},
            'conclusion':{'lhs':expr(cl),'rhs':expr(cr)},
            'witness':expr(wit),'provenance':'SYNTHETIC_SCOPED'}

def cases():
    rows=[]
    for i in range(80):
        good=specimen(i)
        rows.append(('ACCEPT_CONDITIONAL_EXACT',good))
        variants=[]
        m=copy.deepcopy(good);m['statement']=m['statement'].replace(' == ', ' + 1 == ',1)
        variants.append(('REJECT_TEXT_PREMISE_MISMATCH',m))
        m=copy.deepcopy(good);m['statement']=m['statement'].replace(' holds.', ' + 1 holds.')
        variants.append(('REJECT_TEXT_CONCLUSION_MISMATCH',m))
        m=copy.deepcopy(good);m['statement']+=' Therefore every black hole is singular.'
        variants.append(('REJECT_PHYSICAL_OVERCLAIM',m))
        m=copy.deepcopy(good);m['statement']=m['statement'].replace('For all real scalars','There exist real scalars',1)
        variants.append(('REJECT_CHANGED_QUANTIFIER',m))
        m=copy.deepcopy(good);m['witness']={'const':'0'}
        variants.append(('REJECT_INVALID_IMPLICATION_WITNESS',m))
        m=copy.deepcopy(good);m['dimensions'][good['variables'][0]]={'T':2}
        variants.append(('REJECT_INCONSISTENT_UNITS',m))
        rows.extend(variants)
    assert len(rows)==560
    return rows

def run():
    result=[]
    for i,(kind,c) in enumerate(cases()):
        try:report=verify(c);yes=True;assert not report['physical_law_proven']
        except ConditionalRefusal:yes=False
        expect=kind=='ACCEPT_CONDITIONAL_EXACT'
        result.append({'case':i,'type':kind,'accepted':yes,'expected':expect,'correct':yes==expect})
    categories={name:{'total':sum(x['type']==name for x in result),
                      'correct':sum(x['type']==name and x['correct'] for x in result)}
                for name in sorted(set(x['type'] for x in result))}
    return {'label':'v0.8 conditional polynomial claim',
            'cases':len(result),'correct':sum(r['correct'] for r in result),
            'false_accepted':sum(r['accepted'] and not r['expected'] for r in result),
            'false_refused':sum(not r['accepted'] and r['expected'] for r in result),
            'gold_origin':'synthetic controlled generator; not external blind scientific benchmark',
            'categories':categories,'competitor_tests_run':False,
            'physical_truth_verified':False,
            'results_digest':hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest(),
            'rows':result}

if __name__=='__main__':
    d=run();print(json.dumps({k:v for k,v in d.items() if k!='rows'},indent=2))
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
    raise SystemExit(0 if d['correct']==d['cases']==560 else 1)
