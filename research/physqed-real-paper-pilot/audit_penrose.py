#!/usr/bin/env python3
"""Scoped external 56-page Penrose paper pilot: number replay, not a new Kerr solve."""
import argparse,hashlib,json,subprocess
from decimal import Decimal,localcontext
from pathlib import Path
C220=("1.1011615657606169","2.130059996355615")
C221=("1.2418259874347639","-0.4191586512340580")
PRINTED=("0.082546385292784","-0.540327071785322")
LEAVER=("0.082546385844219","-0.540327072615269")
def ratio(a,b):
    ar,ai=map(Decimal,a);br,bi=map(Decimal,b);d=br*br+bi*bi
    return ((ar*br+ai*bi)/d,(ai*br-ar*bi)/d)
def distance(a,b):
    br,bi=map(Decimal,b)
    return ((a[0]-br)**2+(a[1]-bi)**2).sqrt()
def audit(pdf):
    raw=pdf.read_bytes()
    text=subprocess.run(["pdftotext","-layout",str(pdf),"-"],check=True,text=True,capture_output=True).stdout
    assert "Independently Reproduced Kerr 221/220 Radial" in text
    assert "synthetic" in text.lower() and "physical" in text.lower()
    with localcontext() as ctx:
        ctx.prec=75
        z=ratio(C221,C220)
        e=distance(z,LEAVER)
        checks={"GSN_quotient":distance(z,PRINTED)<Decimal("3e-15"),
                "Leaver_discrepancy":abs(e-Decimal("9.9644e-10"))<Decimal("3e-13"),
                "denominator_nonzero":z[0]*z[0]+z[1]*z[1]>0,
                "reversed_221_phase_refused":distance(ratio((C221[0],str(-Decimal(C221[1]))),C220),PRINTED)>Decimal("0.1"),
                "swapped_modes_refused":distance(ratio(C220,C221),PRINTED)>Decimal("1"),
                "discarded_phase_refused":abs((z[0]*z[0]+z[1]*z[1]).sqrt()-Decimal(PRINTED[0]))>Decimal("0.01"),
                "wrong_220_sign_refused":distance(ratio(C221,(str(-Decimal(C220[0])),C220[1])),PRINTED)>Decimal("0.1"),
                "missing_NR_gate_recognized":"no independently" in text.lower() and "horizon" in text.lower()}
        return {"pdf_sha256":hashlib.sha256(raw).hexdigest(),"scope":"external paper printed decimal arithmetic only",
                "checks":checks,"passed":sum(checks.values()),"total":len(checks),
                "gsn_ratio":[str(t) for t in z],"absolute_GSN_vs_Leaver":str(e),
                "numerical_physics_recomputed":False,"lean_kernel_verified":False,
                "empirical_horizon_shear_verified":False,
                "limitations":"GSN coefficients transcribed from paper; no independent raw solver, NR data, or rigorous enclosure"}
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("pdf",type=Path);parser.add_argument("--output",type=Path)
    args=parser.parse_args();r=audit(args.pdf)
    if args.output:args.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"passed":r["passed"],"total":r["total"],"scope":r["scope"]},indent=2))
    raise SystemExit(0 if r["passed"]==r["total"] else 2)
