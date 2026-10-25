"""Deterministic 250-case test; intentionally synthetic and limited in scope."""
import copy
import hashlib
import json
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from controlled_semantics import verify_controlled_claim,ControlledLanguageRefusal,PREFIX,SUFFIX
from benchmarks.adversarial_v06 import algebra,claim

def statements(k,p):
    if p==0:return f'{k}*(x+y)**2', f'{k}*x**2 + {2*k}*x*y + {k}*y**2'
    if p==1:return f'{k}*(x-y)**2', f'{k}*x**2 - {2*k}*x*y + {k}*y**2'
    if p==2:return f'{k}*x*(y+z)', f'{k}*x*y + {k}*x*z'
    if p==3:return f'{k}*(x+y)*(x-y)', f'{k}*x**2 - {k}*y**2'
    raise ValueError

def examples():
    tests=[]
    for i in range(50):
        k=i+1;p=i%4
        lhs,rhs=algebra(k,p,False)
        raw=claim(f'controlled_{i}','placeholder','algebra_identity',lhs,rhs,['x','y','z'])
        raw['assumptions']=[]
        left,right=statements(k,p)
        start=PREFIX.format(names='x, y, z')
        original=start+left+' == '+right+SUFFIX
        raw['statement']=original
        tests.append(('VALID_EXACT_ALIGNMENT',raw))
        z=copy.deepcopy(raw)
        z['statement']=start+left+' == '+right+' + 1'+SUFFIX
        tests.append(('REJECT_WRONG_MATH_IN_ENGLISH',z))
        z=copy.deepcopy(raw)
        z['statement']=start+'x == x'+SUFFIX
        tests.append(('REJECT_UNRELATED_TRUE_THEOREM',z))
        z=copy.deepcopy(raw)
        z['statement']=original+' Therefore all black holes evaporate instantly.'
        tests.append(('REJECT_PHYSICS_OVERCLAIM',z))
        z=copy.deepcopy(raw)
        z['statement']=original.replace('For all real scalars', 'There exist real scalars',1)
        tests.append(('REJECT_CHANGED_QUANTIFIER',z))
    return tests

def run():
    rows=[]
    for i,(klass,example) in enumerate(examples()):
        expect=klass=='VALID_EXACT_ALIGNMENT'
        try:
            result=verify_controlled_claim(example)
            actual=True
            assert not result['physical_law_proven'] and not result['lean_kernel_verified']
        except ControlledLanguageRefusal:
            actual=False
        rows.append({'id':i,'category':klass,'expected_accepted':expect,'accepted':actual,'right':expect==actual})
    counts={c:{'tested':sum(x['category']==c for x in rows),'correct':sum(x['category']==c and x['right'] for x in rows)} for c in sorted(set(x['category'] for x in rows))}
    return {'benchmark':'PHYSQED v0.7 controlled real-polynomial claims',
            'claims':len(rows),'correct_classifications':sum(x['right'] for x in rows),
            'correctly_accepted':sum(x['accepted'] and x['expected_accepted'] for x in rows),
            'false_acceptances':sum(x['accepted'] and not x['expected_accepted'] for x in rows),
            'false_refusals':sum(not x['accepted'] and x['expected_accepted'] for x in rows),
            'categories':counts,'gold_label_provenance':'deterministic synthetic construction, not published externally labeled claims',
            'unrestricted_scientific_semantics_solved':False,'competitor_comparison_performed':False,
            'rows_sha256':hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),'rows':rows}

if __name__=='__main__':
    result=run();path=Path(sys.argv[1]) if len(sys.argv)>1 else None
    if path:path.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},sort_keys=True,indent=2))
    raise SystemExit(0 if result['claims']==250 and result['correct_classifications']==250 else 2)
