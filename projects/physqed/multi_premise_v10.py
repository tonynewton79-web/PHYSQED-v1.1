"""PHYSQED v1.0: bounded 2–4 independent affine-premise polynomial certificate.

The exact check C-D = SUM_j W_j (A_j-B_j) proves only a conditional
rational-polynomial implication. RREF also checks rank k and that each premise
is essential to the SPECIFIC conclusion (a stronger property than rank alone).

Controlled algebra language and SI typing are inherited from v0.9; there is
no unrestricted natural-language, physical-model or Lean certification.
"""
from __future__ import annotations
from fractions import Fraction
import hashlib
import json
import re

from engine import BASES
from two_premise_claims import (
    _add, _neg, _mul, _read_formal, _controlled, _equality_dim, _typed,
    TAIL, MultiPremiseRefusal,
)

VERSION = "physqed-multi-premise-v1.0"
MAX_PREMISES = 4
MAX_TERMS = 512

def _rref_affine(premises, n):
    """Exact Q-RREF of a system p_j(x)=0; returns pivot substitutions.

    Full row rank implies solvability over R for any affine offsets.
    No floating-point tolerance or empirical rank heuristic is used.
    """
    rows = []
    zero = (0,) * n
    for p in premises:
        if any(sum(m) > 1 for m in p):
            raise MultiPremiseRefusal("nonlinear premise independence unsupported")
        normal = [p.get(tuple(int(i == j) for i in range(n)), Fraction(0))
                  for j in range(n)]
        if not any(normal):
            raise MultiPremiseRefusal("constant or tautological premise unsupported")
        rows.append(normal + [-p.get(zero, Fraction(0))])
    pivots = []
    lead = 0
    for col in range(n):
        pivot = next((i for i in range(lead, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[lead], rows[pivot] = rows[pivot], rows[lead]
        fac = rows[lead][col]
        rows[lead] = [v / fac for v in rows[lead]]
        for i in range(len(rows)):
            if i != lead and rows[i][col]:
                fac = rows[i][col]
                rows[i] = [x - fac * y for x, y in zip(rows[i], rows[lead])]
        pivots.append(col)
        lead += 1
        if lead == len(rows):
            break
    if lead != len(rows):
        raise MultiPremiseRefusal("affine premise gradients are linearly dependent")
    return rows, pivots

def _substitute_vanish(target, constraints, n):
    """Exact restriction to the affine variety of a proper premise subset."""
    rows, pivots = _rref_affine(constraints, n)
    free = set(range(n)) - set(pivots)
    zero = (0,) * n
    identities = [{tuple(int(i == j) for i in range(n)): Fraction(1)}
                  for j in range(n)]
    for row, col in zip(rows, pivots):
        subst = {zero: row[-1]} if row[-1] else {}
        for j in free:
            if row[j]:
                subst = _add(subst, {tuple(int(i == j) for i in range(n)): -row[j]})
        identities[col] = subst
    reduced = {}
    for mon, coefficient in target.items():
        term = {zero: coefficient}
        for i, power in enumerate(mon):
            for _ in range(power):
                term = _mul(term, identities[i], MAX_TERMS)
        reduced = _add(reduced, term)
        if len(reduced) > MAX_TERMS:
            raise MultiPremiseRefusal("essentiality reduction over budget")
    return not reduced

def verify(contract, *, require_essential=True):
    """Check controlled text, dimensions, exact identity and premise rank.

    By default, refuse an assumption which can be omitted without changing
    the conclusion. 'Essential' is exact ideal non-membership relative to
    the remaining independent affine equations.
    """
    required = {"schema", "statement", "variables", "dimensions", "premises",
                "conclusion", "witnesses", "provenance"}
    if not isinstance(contract, dict) or set(contract) != required:
        raise MultiPremiseRefusal("incorrect bounded multi-premise schema")
    if contract["schema"] != VERSION or contract["provenance"] != "SYNTHETIC_SCOPED":
        raise MultiPremiseRefusal("unsupported version or unreviewed provenance")
    names = contract["variables"]
    premises, witnesses = contract["premises"], contract["witnesses"]
    conclusion = contract["conclusion"]
    if (not isinstance(premises, list) or not 2 <= len(premises) <= MAX_PREMISES or
        not isinstance(witnesses, list) or len(witnesses) != len(premises) or
        any(not isinstance(p, dict) or set(p) != {"lhs", "rhs"} for p in premises) or
        not isinstance(conclusion, dict) or set(conclusion) != {"lhs", "rhs"}):
        raise MultiPremiseRefusal("2–4 premises, matching witnesses, one conclusion required")
    k = len(premises)
    if (not isinstance(names, list) or not k <= len(names) <= 8 or
        len(set(names)) != len(names) or
        any(not isinstance(s, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,18}", s)
                for s in names)):
        raise MultiPremiseRefusal("invalid controlled variable names")
    types = contract["dimensions"]
    if not isinstance(types, dict) or set(types) != set(names):
        raise MultiPremiseRefusal("incomplete dimensional declarations")
    for dim in types.values():
        if (not isinstance(dim, dict) or any(b not in BASES for b in dim) or
            any(type(v) is not int or abs(v) > 16 for v in dim.values())):
            raise MultiPremiseRefusal("invalid declared SI dimensions")
    statement = contract["statement"]
    prefix = "For all real scalars " + ", ".join(names) + ", if "
    if (not isinstance(statement, str) or len(statement) > 4096 or
        not statement.startswith(prefix) or not statement.endswith(TAIL)):
        raise MultiPremiseRefusal("uncontrolled quantifier or scientific language")
    body = statement[len(prefix):-len(TAIL)]
    if body.count(", then ") != 1:
        raise MultiPremiseRefusal("invalid premise-to-conclusion boundary")
    antecedent, consequent = body.split(", then ")
    if not consequent.endswith(" holds."):
        raise MultiPremiseRefusal("uncontrolled conclusion grammar")
    statements = antecedent.split(" and ") + [consequent[:-len(" holds.")]]
    if len(statements) != k + 1:
        raise MultiPremiseRefusal("wrong number of controlled premise clauses")
    for text, formal in zip(statements, premises + [conclusion]):
        if text.count(" == ") != 1:
            raise MultiPremiseRefusal("invalid controlled equality")
        left, right = text.split(" == ")
        if (_controlled(left, names) != _read_formal(formal["lhs"], names) or
            _controlled(right, names) != _read_formal(formal["rhs"], names)):
            raise MultiPremiseRefusal("controlled text-to-formal SIDE MISMATCH")
    premise_dimensions = [_equality_dim(p["lhs"], p["rhs"], names, types)
                          for p in premises]
    conclusion_dim = _equality_dim(conclusion["lhs"], conclusion["rhs"], names, types)
    generators = [_add(_read_formal(p["lhs"], names),
                       _neg(_read_formal(p["rhs"], names))) for p in premises]
    _rref_affine(generators, len(names))
    target = _add(_read_formal(conclusion["lhs"], names),
                  _neg(_read_formal(conclusion["rhs"], names)))
    parsed_witnesses = [_read_formal(w, names) for w in witnesses]
    total = {}
    for i, (w, p) in enumerate(zip(parsed_witnesses, generators)):
        wd = _typed(witnesses[i], types)
        if tuple(a + b for a, b in zip(premise_dimensions[i], wd)) != conclusion_dim:
            raise MultiPremiseRefusal("witness product has inconsistent dimensions")
        total = _add(total, _mul(w, p, MAX_TERMS))
        if len(total) > MAX_TERMS:
            raise MultiPremiseRefusal("certificate term budget exceeded")
    if total != target:
        raise MultiPremiseRefusal("incorrect exact multi-premise ideal membership")
    if require_essential:
        for i in range(k):
            other = generators[:i] + generators[i+1:]
            if _substitute_vanish(target, other, len(names)):
                raise MultiPremiseRefusal("premise not essential to stated conclusion")
    digest = hashlib.sha256(json.dumps(contract, sort_keys=True,
                   separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()
    return {"status": "INDEPENDENT_AFFINE_MULTI_PREMISE_CERTIFICATE_VALID__PHYSICS_UNVERIFIED",
            "contract_sha256": digest, "premise_count": k,
            "affine_gradient_rank": k, "all_premises_essential_to_conclusion": require_essential,
            "exact_polynomial_identity": True, "controlled_text_formal_alignment_verified": True,
            "declared_dimensions_consistent": True, "physical_law_proven": False,
            "lean_kernel_verified": False, "empirical_validation_verified": False,
            "unrestricted_semantic_correctness": False,
            "scope": "Exact rational affine premises, polynomial witnesses, controlled text, declared SI dimensions"}
