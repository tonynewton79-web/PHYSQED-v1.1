"""Independent stdlib-only replay of the v0.5 synthetic numerical baseline.

Deliberately does not import the PHYSQED method gate or read a 'PASS' report.
This checks only a controlled toy fixture, not physical verification.
"""
from __future__ import annotations
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
j=json.loads((ROOT/'fixtures'/'generic_method_fixture.json').read_text())
assert j['schema']=='physqed-method-gate-v0.5'
assert len(j['methods'])==2
for field in ('input','context'):
    src=ROOT/j[field+'_path']
    assert src.is_file()
    assert hashlib.sha256(src.read_bytes()).hexdigest()==j[field+'_sha256']


# Reconstruct a numeric check independently of method_gate's pairwise code.
source_lines=[]
values=[]
for m in j['methods']:
    source=(ROOT/m['source_path']).read_bytes()
    h=hashlib.sha256(source).hexdigest()
    assert h==m['source_sha256'], 'method source hash mismatch'
    # A controlled fixture, never evaluate arbitrary filenames from user manifests.
    assert m['source_path'] in ('fixtures/toy_method_a.py','fixtures/toy_method_b.py')
    proc=subprocess.run([sys.executable,str(ROOT/m['source_path'])],
                        check=True,capture_output=True,text=True,timeout=5)
    v=Decimal(proc.stdout.strip())
    assert v==Decimal(m['result']['re'])
    values.append(v)
    source_lines.append((m['method_id'],h))
assert values[0]==Decimal(Fraction(8,4).numerator)
assert values[1]-values[0]==Decimal('0.0001')
assert values[1]-values[0] < Decimal(j['comparison']['absolute_tolerance'])
for x in j['negative_controls']:
    assert Decimal(x['baseline_residual'])<Decimal(x['baseline_maximum'])
    assert Decimal(x['corrupted_residual'])>Decimal(x['corruption_minimum'])
for s in j['stability_samples']:
    assert abs(Decimal(s['result']['re'])-values[0])<Decimal(s['declared_maximum_deviation'])
print('INDEPENDENT_V05_TOY_AUDIT_PASS: source hashes, two executed toy algorithms, arithmetic, controls and stability')
for name,h in source_lines:
    print(name+' source sha256='+h)
print('NOT proof, independent provenance attestation, or physical validation')
