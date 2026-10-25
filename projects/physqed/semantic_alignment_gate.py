"""PHYSQED v0.6 restricted semantic-alignment firewall.
This binds candidate text and formal mathematics to an EXTERNALLY reviewed exact
reference using a reviewer-held key. It never proves semantic or physical truth.
"""
from __future__ import annotations
import hashlib
import hmac
import json
from typing import Any

VERSION = "physqed-semantic-alignment-v0.6"
SCOPE = "MATHEMATICAL_COMPONENT_ONLY"
ALLOWED_CLAIM_KEYS = frozenset({"schema_version", "id", "statement", "source", "assumptions", "checks"})

class SemanticGateRefusal(ValueError):
    pass

def _canonical(obj: Any) -> bytes:
    try:
        return json.dumps(obj, ensure_ascii=False, allow_nan=False, sort_keys=True,
                          separators=(",", ":")).encode("utf-8")
    except (ValueError, TypeError, OverflowError) as exc:
        raise SemanticGateRefusal("not canonical JSON") from exc

def _digest(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()

def _validated_claim(claim: Any) -> dict:
    if not isinstance(claim, dict) or set(claim) != ALLOWED_CLAIM_KEYS:
        raise SemanticGateRefusal("invalid claim schema")
    if not isinstance(claim["statement"], str) or not claim["statement"].strip():
        raise SemanticGateRefusal("missing statement")
    if not isinstance(claim["id"], str) or not claim["id"].strip():
        raise SemanticGateRefusal("missing claim id")
    if not isinstance(claim["assumptions"], list) or not isinstance(claim["checks"], list):
        raise SemanticGateRefusal("missing assumptions or formal claims")
    if not claim["checks"]:
        raise SemanticGateRefusal("empty check set")
    if len(_canonical(claim)) > (1 << 20):
        raise SemanticGateRefusal("claim too large")
    return claim

def _validated_key(key: bytes) -> bytes:
    if not isinstance(key, bytes) or len(key) < 32:
        raise SemanticGateRefusal("external reviewer HMAC key must be >= 256 bits")
    return key

def issue_reference(claim: dict, key: bytes, reviewer_label: str,
                    reviewed_scope: str = SCOPE) -> dict:
    """Only a reviewer holding an independent key should approve a baseline.

    Not a semantic proof. NEVER call automatically on an incoming claim.
    """
    _validated_claim(claim)
    _validated_key(key)
    if reviewed_scope != SCOPE:
        raise SemanticGateRefusal("only scoped mathematics authorization supported")
    if not isinstance(reviewer_label, str) or not reviewer_label.strip() or len(reviewer_label) > 100:
        raise SemanticGateRefusal("reviewer label required")
    payload = {"version": VERSION, "claim": claim,
               "reviewed_scope": SCOPE, "reviewer_label_unverified": reviewer_label}
    return {"payload": payload, "hmac_sha256": hmac.new(key, _canonical(payload), hashlib.sha256).hexdigest()}

def verify_alignment(candidate: dict, reference: dict, key: bytes) -> dict:
    """Only match exact natural-language and formal claim to signed reference."""
    _validated_claim(candidate)
    _validated_key(key)
    if not isinstance(reference, dict) or set(reference) != {"payload", "hmac_sha256"}:
        raise SemanticGateRefusal("untrusted or incomplete review record")
    payload = reference["payload"]
    if (not isinstance(payload, dict) or
        set(payload) != {"version", "claim", "reviewed_scope", "reviewer_label_unverified"} or
        payload["version"] != VERSION or payload["reviewed_scope"] != SCOPE):
        raise SemanticGateRefusal("malformed or escalated review record")
    _validated_claim(payload["claim"])
    sig = reference["hmac_sha256"]
    if not isinstance(sig, str) or len(sig) != 64:
        raise SemanticGateRefusal("invalid HMAC signature")
    expected = hmac.new(key, _canonical(payload), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        raise SemanticGateRefusal("review integrity/authentication failed")
    checked = payload["claim"]
    if candidate["id"] != checked["id"]:
        raise SemanticGateRefusal("claim id not in reviewed scope")
    if candidate["statement"] != checked["statement"]:
        raise SemanticGateRefusal("UNREVIEWED_NATURAL_LANGUAGE_STATEMENT")
    if any(candidate[k] != checked[k] for k in ("assumptions", "checks", "schema_version", "source")):
        raise SemanticGateRefusal("UNREVIEWED_FORMAL_CLAIM_OR_CONTEXT")
    if _canonical(candidate) != _canonical(checked):
        raise SemanticGateRefusal("claim differs from approved reference")
    return {"status": "REVIEWED_CLAIM_BYTES_MATCH__SEMANTIC_TRUTH_UNVERIFIED",
            "claim_sha256": _digest(candidate),
            "review_record_sha256": _digest(reference),
            "binding_to_reviewed_statement": True,
            "reviewer_identity_authenticated": False,
            "semantic_correctness_verified": False,
            "physical_law_proven": False,
            "lean_kernel_verified": False,
            "review_scope": SCOPE,
            "warning": "Signature binds previously reviewed text/formalization only; reviewer identity and physics are not certified."}
