"""300 deterministic malformed-contract refusals; NOT an unrestricted security proof."""
import copy,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/'projects'/'physqed'
sys.path.insert(0,str(ROOT))
from conditional_claims import verify,ConditionalRefusal
from benchmarks.conditional_v08 import specimen
rng=random.Random(20261024)
values=[None,False,True,0,1,'',[],'bad',{},['x'],{'M':True},{'T':'x'},{'var':'missing'},{'const':'NaN'}]
keys=['schema','statement','variables','dimensions','premise','conclusion','witness','provenance']
refused=0;crashed=[];accepted=0
for j in range(300):
    z=copy.deepcopy(specimen(j%80));field=keys[j%len(keys)]
    before=copy.deepcopy(z)
    if field in ('premise','conclusion') and j%3:
        z[field]['rhs']=copy.deepcopy(rng.choice(values))
    elif field=='dimensions' and j%3:
        z[field][list(z[field])[0]]=copy.deepcopy(rng.choice(values))
    else:z[field]=copy.deepcopy(rng.choice(values))
    if z==before:
        z[field]=None
    try:verify(z)
    except ConditionalRefusal:refused+=1
    except Exception as e:crashed.append((j,type(e).__name__,str(e)))
    else:accepted+=1
summary={'fuzzed':300,'refused':refused,'accepted':accepted,'unhandled_errors':crashed[:10],
         'scope':'bounded malformed JSON-schema mutations of internally generated synthetic contracts'}
print(json.dumps(summary,indent=2))
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(summary,indent=2)+'\n')
if refused!=300 or crashed:raise SystemExit(2)
