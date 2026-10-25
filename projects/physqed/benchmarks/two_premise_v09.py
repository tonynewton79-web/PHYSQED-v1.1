"""Deterministic two-premise synthetic labels: 60 positive and 480 negative."""
import ast,copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from two_premise_claims import VERSION,TAIL,verify,MultiPremiseRefusal

def to_json(n):
    if isinstance(n,ast.Name):return {'var':n.id}
    if isinstance(n,ast.Constant) and type(n.value) is int:return {'const':str(n.value)}
    if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return {'op':'mul','args':[{'const':'-1'},to_json(n.operand)]}
    if isinstance(n,ast.BinOp):
        if isinstance(n.op,ast.Pow) and type(n.right.value) is int:
            return {'op':'pow','arg':to_json(n.left),'exp':n.right.value}
        a,b=to_json(n.left),to_json(n.right)
        if isinstance(n.op,ast.Add):return {'op':'add','args':[a,b]}
        if isinstance(n.op,ast.Sub):return {'op':'add','args':[a,{'op':'mul','args':[{'const':'-1'},b]}]}
        if isinstance(n.op,ast.Mult):return {'op':'mul','args':[a,b]}
    raise ValueError('restricted benchmark expression')

def expr(s):return to_json(ast.parse(s,mode='eval').body)

def specimen(i):
    t=i//2+1
    if i%2==0:
        vs=['x','y','z','w'];ds={name:{} for name in vs}
        first=('x+y','z');second=('x-y','w')
        conclusion=(f'{t}*(x**2-y**2)',f'{t}*z*w')
        witnesses=(f'{t}*(x-y)',f'{t}*z')
    else:
        vs=['v','u','a','b'];ds={'v':{'L':1,'T':-1},'u':{'L':1,'T':-1},
                                 'a':{'L':1,'T':-2},'b':{'L':1,'T':-2}}
        first=('v','u');second=('a','b')
        conclusion=(f'{t}*v*a',f'{t}*u*b')
        witnesses=(f'{t}*a',f'{t}*u')
    text=(f'For all real scalars {", ".join(vs)}, if {first[0]} == {first[1]} and '
          f'{second[0]} == {second[1]}, then {conclusion[0]} == {conclusion[1]} holds.'+TAIL)
    return {'schema':VERSION,'statement':text,'variables':vs,'dimensions':ds,
            'premises':[{'lhs':expr(a),'rhs':expr(b)} for a,b in (first,second)],
            'conclusion':{'lhs':expr(conclusion[0]),'rhs':expr(conclusion[1])},
            'witnesses':[expr(w) for w in witnesses], 'provenance':'SYNTHETIC_SCOPED'}

def cases():
    rows=[]
    for i in range(60):
        good=specimen(i);rows.append(('ACCEPT_EXACT',good))
        edits=[]
        a=copy.deepcopy(good);a['witnesses'][0]={'const':'0'};edits.append(('WRONG_WITNESS_ONE',a))
        a=copy.deepcopy(good);a['witnesses'][1]={'const':'0'};edits.append(('WRONG_WITNESS_TWO',a))
        a=copy.deepcopy(good);a['statement']=a['statement'].replace(' == ', ' + 1 == ',1);edits.append(('TEXT_PREMISE_MISMATCH',a))
        a=copy.deepcopy(good);a['conclusion']['rhs']={'const':'0'};edits.append(('FORMAL_CONCLUSION_MISMATCH',a))
        a=copy.deepcopy(good);a['premises'][1]=copy.deepcopy(a['premises'][0]);edits.append(('DEPENDENT_PREMISES',a))
        a=copy.deepcopy(good);a['dimensions'][good['variables'][0]]={'T':9};edits.append(('INCORRECT_UNITS',a))
        a=copy.deepcopy(good);a['statement']+=' All physical phenomena have been proven.';edits.append(('PHYSICS_OVERCLAIM',a))
        a=copy.deepcopy(good);a['statement']=a['statement'].replace('For all real','There exist real',1);edits.append(('QUANTIFIER_DRIFT',a))
        rows.extend(edits)
    assert len(rows)==540
    return rows

def run():
    rows=[]
    for i,(label,c) in enumerate(cases()):
        try:
            r=verify(c);accepted=True
            assert r['physical_law_proven'] is False and r['lean_kernel_verified'] is False
        except MultiPremiseRefusal:accepted=False
        expected=label=='ACCEPT_EXACT'
        rows.append({'id':i,'label':label,'accepted':accepted,'expected':expected,'correct':expected==accepted})
    return {'suite':'two independent affine premises, synthetic v0.9',
            'total':len(rows),'correct':sum(r['correct'] for r in rows),
            'accepts':sum(r['accepted'] for r in rows),
            'false_accepts':sum(r['accepted'] and not r['expected'] for r in rows),
            'false_refusals':sum(not r['accepted'] and r['expected'] for r in rows),
            'gold_labels':'internally generated synthetic cases; no external blind review',
            'lean_compilation_confirmed':False,'external_competitor_comparison':False,
            'rows':rows,'rows_sha256':hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()}
if __name__=='__main__':
    r=run()
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='rows'},indent=2))
    raise SystemExit(0 if r['total']==r['correct']==540 else 2)
