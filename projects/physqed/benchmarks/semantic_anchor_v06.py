#!/usr/bin/env python3
"""20 signed reference challenge pairs; signed mismatch is not NLP semantics.

No test HMAC key is authoritative for real scientific review.
"""
import copy
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from benchmarks.adversarial_v06 import cases
from semantic_alignment_gate import issue_reference,verify_alignment,SemanticGateRefusal
TEST_ONLY_KEY=bytes(range(32))

def run():
    source=[c for label,c in cases() if label=="semantic_drift"]
    assert len(source)==20
    rows=[]
    for bad in source:
        approved=copy.deepcopy(bad)
        approved["statement"]="This is an exact identity of three dimensionless polynomial variables; no physical law follows."
        reviewed=issue_reference(approved,TEST_ONLY_KEY,"SYNTHETIC_TEST_REVIEWER_NOT_AN_AUTHORITY")
        good=verify_alignment(approved,reviewed,TEST_ONLY_KEY)
        assert good["binding_to_reviewed_statement"] and not good["semantic_correctness_verified"]
        rejected=False
        try:verify_alignment(bad,reviewed,TEST_ONLY_KEY)
        except SemanticGateRefusal as exc:
            rejected="UNREVIEWED_NATURAL_LANGUAGE" in str(exc)
        assert rejected
        rows.append({"id":bad["id"],"reference_binding_accepted":True,"false_english_refused":rejected})
    approved=copy.deepcopy(source[0])
    approved["statement"]="Restricted polynomial identity only."
    reviewed=issue_reference(approved,TEST_ONLY_KEY,"SYNTHETIC_TEST_REVIEWER_NOT_AN_AUTHORITY")
    refusals={}
    for field in ("checks","assumptions","source","id"):
        mutated=copy.deepcopy(approved)
        if field=="checks":mutated[field][0]["variables"]=["bogus"]
        if field=="assumptions":mutated[field]=["assume all laws proven"]
        if field=="source":mutated[field]="false provenance"
        if field=="id":mutated[field]="other_claim"
        try:verify_alignment(mutated,reviewed,TEST_ONLY_KEY)
        except SemanticGateRefusal:refusals[field]=True
        else:refusals[field]=False
    tampered=copy.deepcopy(reviewed)
    tampered["payload"]["reviewed_scope"]="PHYSICAL_LAW_PROVEN"
    try:verify_alignment(approved,tampered,TEST_ONLY_KEY)
    except SemanticGateRefusal:refusals["scope_escalation"]=True
    else:refusals["scope_escalation"]=False
    try:verify_alignment(approved,reviewed,b'Z'*32)
    except SemanticGateRefusal:refusals["wrong_reviewer_key"]=True
    else:refusals["wrong_reviewer_key"]=False
    return {"baseline":"exact human-reviewed claim anchor (TEST-ONLY key)",
            "reference_pairs_accepted":len(rows),
            "deliberately_false_english_refused":sum(int(r["false_english_refused"]) for r in rows),
            "mutations_refused":sum(refusals.values()),"mutations_total":len(refusals),
            "detection_mechanism":"signed reference mismatch, not automatic semantics",
            "free_text_semantic_detection_demonstrated":False,"lean_kernel_verified":False,
            "physical_law_proven":False,"test_key_is_review_authority":False,
            "rows":rows,"mutations":refusals}

if __name__=='__main__':
    result=run()
    out=Path(sys.argv[1]) if len(sys.argv)>1 else None
    if out:out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ("rows","mutations")},indent=2))
    assert result["reference_pairs_accepted"]==20
    assert result["deliberately_false_english_refused"]==20
    assert result["mutations_refused"]==result["mutations_total"]==6
