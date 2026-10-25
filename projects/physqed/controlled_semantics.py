"""PHYSQED v0.7: a narrow controlled-language algebra-to-claim verifier.
No LLM/NLP semantic verification, domain interpretation, experiments, or Lean proof.
Accepts exactly one unconditional real-polynomial identity and its controlled
English template. The user-supplied math must match each side of that identity
individually under exact rational polynomial normalization.
"""
from __future__ import annotations
import ast
from fractions import Fraction
import re
from typing import Any
from engine import certify, polynomial

PREFIX = "For all real scalars {names}, the polynomial identity "
SUFFIX = " holds. This checks only the algebraic identity; no physical law is established."
MAX_TERMS = 512
MAX_POWER = 8
MAX_DEPTH = 30
MAX_BITS = 2048

class ControlledLanguageRefusal(ValueError):
    pass

def _verify_size(value: Fraction):
    if value.numerator.bit_length() > MAX_BITS or value.denominator.bit_length() > MAX_BITS:
        raise ControlledLanguageRefusal("rational size limit")
    return value

def _plus(p, q):
    r = p.copy()
    for powers, value in q.items():
        a = _verify_size(r.get(powers, Fraction(0)) + value)
        if a: r[powers] = a
        else: r.pop(powers, None)
    if len(r) > MAX_TERMS: raise ControlledLanguageRefusal("term limit")
    return r

def _mult(p, q):
    r = {}
    for n,a in p.items():
        for m,b in q.items():
            idx = tuple(x+y for x,y in zip(n,m))
            new = _verify_size(r.get(idx, Fraction(0)) + a*b)
            if new: r[idx] = new
            else: r.pop(idx, None)
            if len(r) > MAX_TERMS: raise ControlledLanguageRefusal("term limit")
    return r

def _scale(p, c):
    return {k:_verify_size(c*v) for k,v in p.items() if c*v}

def _num(node):
    if isinstance(node, ast.Constant) and type(node.value) is int and abs(node.value) <= 10**14:
        return Fraction(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd,ast.USub)):
        v = _num(node.operand)
        return v if isinstance(node.op, ast.UAdd) else -v
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        numerator,denominator = _num(node.left),_num(node.right)
        if not denominator: raise ControlledLanguageRefusal("division by zero")
        return _verify_size(numerator/denominator)
    raise ControlledLanguageRefusal("only exact integer/rational constants allowed")

def _poly(node, variables, depth=0):
    if depth > MAX_DEPTH: raise ControlledLanguageRefusal("expression too deep")
    zero=(0,)*len(variables)
    if isinstance(node,ast.Name):
        if node.id not in variables: raise ControlledLanguageRefusal("undeclared identifier")
        return {tuple(int(node.id == k) for k in variables):Fraction(1)}
    if isinstance(node,(ast.Constant,ast.UnaryOp)):
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
            p=_poly(node.operand,variables,depth+1)
            return _scale(p, 1 if isinstance(node.op,ast.UAdd) else -1)
        value=_num(node)
        return {zero:value} if value else {}
    if not isinstance(node,ast.BinOp):raise ControlledLanguageRefusal("unsupported expression syntax")
    if isinstance(node.op,ast.Pow):
        if not isinstance(node.right,ast.Constant) or type(node.right.value) is not int or not 0<=node.right.value<=MAX_POWER:
            raise ControlledLanguageRefusal("invalid exponent")
        p=_poly(node.left,variables,depth+1)
        result={zero:Fraction(1)}
        for _ in range(node.right.value):result=_mult(result,p)
        return result
    if isinstance(node.op,ast.Div):
        return _scale(_poly(node.left,variables,depth+1), Fraction(1)/_num(node.right))
    a,b=_poly(node.left,variables,depth+1),_poly(node.right,variables,depth+1)
    if isinstance(node.op,ast.Add):return _plus(a,b)
    if isinstance(node.op,ast.Sub):return _plus(a,_scale(b,-1))
    if isinstance(node.op,ast.Mult):return _mult(a,b)
    raise ControlledLanguageRefusal("only polynomial arithmetic is permitted")

def _parse_expression(src, variables):
    if not (0 < len(src) <= 1700) or re.search(r"[^A-Za-z0-9_+*/(). \t-]", src):
        raise ControlledLanguageRefusal("invalid expression characters")
    try: tree=ast.parse(src,mode="eval")
    except (SyntaxError,ValueError,RecursionError) as exc:
        raise ControlledLanguageRefusal("malformed polynomial expression") from exc
    try:return _poly(tree.body,variables)
    except (RecursionError,OverflowError,ZeroDivisionError) as exc:
        raise ControlledLanguageRefusal("unsupported or too-large expression") from exc

def verify_controlled_claim(claim: dict):
    if not isinstance(claim,dict) or claim.get("schema_version") != "physqed-0.1":
        raise ControlledLanguageRefusal("wrong contract version")
    checks=claim.get("checks")
    if not isinstance(checks,list) or len(checks)!=1 or not isinstance(checks[0],dict):
        raise ControlledLanguageRefusal("exactly one declared check is supported")
    spec=checks[0]
    if set(spec)!={"kind","variables","lhs","rhs"} or spec["kind"]!="algebra_identity":
        raise ControlledLanguageRefusal("only unconditional exact polynomial identities supported")
    variables=spec["variables"]
    if (not isinstance(variables,list) or not 1 <= len(variables) <= 6 or
        any(not isinstance(v,str) or
        not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,24}",v) for v in variables) or
        len(set(variables))!=len(variables)):
        raise ControlledLanguageRefusal("invalid variable domain")
    if claim.get("assumptions")!=[]:raise ControlledLanguageRefusal("nonempty or implicit assumptions unsupported")
    if not isinstance(claim.get("statement"),str) or len(claim["statement"])>4096:
        raise ControlledLanguageRefusal("no controlled statement supplied")
    start=PREFIX.format(names=", ".join(variables))
    text=claim["statement"]
    if not text.startswith(start) or not text.endswith(SUFFIX):
        raise ControlledLanguageRefusal("uncontrolled quantifier, domain, scope or physical prose")
    equation=text[len(start):-len(SUFFIX)]
    if equation.count(" == ")!=1:raise ControlledLanguageRefusal("expected one exact equality operator")
    left,right=equation.split(" == ")
    got_left=_parse_expression(left,variables)
    got_right=_parse_expression(right,variables)
    try:
        expected_left=polynomial(spec["lhs"],variables)
        expected_right=polynomial(spec["rhs"],variables)
    except (ValueError,TypeError,KeyError,RecursionError,OverflowError) as exc:
        raise ControlledLanguageRefusal("invalid submitted formal expression") from exc
    if got_left!=expected_left or got_right!=expected_right:
        raise ControlledLanguageRefusal("CONTROLLED_TEXT_FORMAL_EQUATION_MISMATCH")
    result=certify(claim)
    if result["status"]!="MATHEMATICAL_COMPONENTS_VERIFIED":
        raise ControlledLanguageRefusal("algebraic identity was not established")
    return {"status":"CONTROLLED_TEXT_AND_EXACT_ALGEBRA_MATCH__PHYSICS_UNVERIFIED",
            "controlled_language_scope":"unconditional real-scalar polynomial equality only",
            "controlled_statement_alignment_verified":True,
            "unrestricted_semantic_correctness_verified":False,
            "real_world_model_assumptions_verified":False,
            "lean_kernel_verified":False,
            "physical_law_proven":False,
            "algebraic_engine_status":result["status"]}
