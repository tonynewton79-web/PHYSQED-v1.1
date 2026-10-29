"""PHYSQED v1.2: fail-closed proof-carrying symbolic component receipts.

Hashes attest reproducibility, not independent proof, authenticity, or physics.
Programs are trusted; never evaluate user-supplied Python/expression strings.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as S
from .geometry import ScopeError


def _components(expr):
    if isinstance(expr,S.MatrixBase):
        return list(expr)
    if isinstance(expr,(list,tuple)):
        out=[]
        for e in expr:
            out.extend(_components(e))
        return out
    if isinstance(expr,S.NDimArray):
        return list(expr)
    return [S.sympify(expr)]


def _counterexample(difference):
    syms=sorted(difference.free_symbols,key=str)
    if not syms or len(syms)>5:
        return None
    for j in range(1,8):
        env={s:S.Rational(((j*(i+2)) % 11)-5, i+1) for i,s in enumerate(syms)}
        try:
            v=S.simplify(difference.subs(env))
            if v.is_finite is True and v.is_zero is False:
                return {"assignment":{str(k):str(val) for k,val in env.items()},
                        "residual":str(v)}
        except (TypeError,ValueError,ZeroDivisionError,NotImplementedError):
            pass
    return None


def certify(claim_id, domain, equations, assumptions=(), source=""):
    """Check exact component equations; each item is (lhs,rhs).

    Controlled programmatic SymPy objects only, not arbitrary text input.
    Secondary route expands/together/cancels independently of simplify, but
    shares SymPy and must NOT be described as an independent proof engine.
    """
    if not isinstance(claim_id,str) or not claim_id or not isinstance(source,str) or not source:
        raise ScopeError("claim identifier and source required")
    if domain not in ("tensor","einstein","gauge","quantum","field","canonical"):
        raise ScopeError("unsupported physics domain")
    if not isinstance(equations,(tuple,list)) or not 1<=len(equations)<=128:
        raise ScopeError("1..128 component relations required")
    rows=[]
    for k,relation in enumerate(equations):
        if not isinstance(relation,(list,tuple)) or len(relation)!=2:
            raise ScopeError("each relation must have lhs and rhs")
        a,b=map(_components,relation)
        if len(a)!=len(b) or not 1<=len(a)<=4096:
            raise ScopeError("component count mismatch or over limit")
        for i,(x,y) in enumerate(zip(a,b)):
            delta=x-y
            primary=S.simplify(delta)
            secondary=S.cancel(S.together(S.expand(delta)))
            passed=primary==0 and secondary==0
            rows.append({"relation":k,"component":i,
                         "passed":bool(passed),
                         "exact_primary_zero":bool(primary==0),
                         "exact_secondary_zero":bool(secondary==0),
                         "counterexample":None if passed else _counterexample(delta),
                         "lhs":S.srepr(x),"rhs":S.srepr(y)})
    status=("EXACT_SYMBOLIC_COMPONENTS_PASSED__PHYSICS_UNVERIFIED"
            if all(r["passed"] for r in rows) else "REJECTED")
    engine=Path(__file__)
    payload={"schema":"physqed-v1.2-symbolic-components",
             "claim_id":claim_id,"domain":domain,"source":source,
             "assumptions":list(assumptions),
             "status":status,
             "checks":rows,"check_count":len(rows),
             "backend_sha256":hashlib.sha256(engine.read_bytes()).hexdigest(),
             "symbolic_backend":"sympy-"+S.__version__,
             "physical_law_proven":False,"lean_kernel_verified":False,
             "global_geometric_validity_proven":False,
             "continuum_qft_validity_proven":False,
             "independent_engine_verified":False,
             "limitations":"chart-local/finite symbolic SymPy components; no natural-language semantic or empirical certification"}
    payload["certificate_sha256"]=hashlib.sha256(json.dumps(
        payload,sort_keys=True,ensure_ascii=True,
        separators=(",",":")).encode()).hexdigest()
    return payload


def save_certificate(receipt, path):
    target=Path(path)
    target.write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n",
                      encoding="utf-8")
    return target
