"""PHYSQED v0.5 -- reusable, fail-closed multi-method scientific audit gate.

This gate consumes a method-neutral result manifest from ANY research project.
It DOES NOT validate the asserted provenance, mathematical correctness, method
independence, empirical truth, or the claim's semantics. It treats method
metadata as untrusted declarations. A pass is only a *local consistency*
result, NEVER a formal proof receipt. Formal CI/Lean receipts remain separate.

Design: no research manuscript, particular physical model, solver, or measured
source material is imported into the PHYSQED package.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any

SCHEMA = "physqed-method-gate-v0.5"
SHA256 = re.compile(r"^[a-f0-9]{64}$")
ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]{0,95}$")
MAX_INPUT_BYTES = 1024 * 1024
MAX_METHODS = 12
MAX_NEGATIVE_CONTROLS = 30
MAX_STABILITY_SAMPLES = 30
WARNING = ("Method identities, provenance, error budgets and equation families "
           "are self-declared, not authenticated. Numerical consistency is "
           "not Lean verification, rigorous error certification, semantic "
           "equivalence, or physical validation.")


class MethodGateError(ValueError):
    """The supplied audit cannot be trusted or is outside the declared scope."""


def _fields(value: Any, keys: set[str], label: str) -> dict:
    if not isinstance(value, dict) or set(value) != keys:
        raise MethodGateError(f"{label}: invalid or incomplete schema")
    return value


def _identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise MethodGateError(f"{label}: invalid identifier")
    return value


def _hash(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA256.fullmatch(value) or value == "0"*64:
        raise MethodGateError(f"{label}: full nonzero sha256 hex required")
    return value


def _description(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value)>600:
        raise MethodGateError(f"{label}: nonblank bounded explanation required")
    return value


def _decimal(value: Any, label: str, nonnegative=False) -> Decimal:
    # JSON numbers are not allowed: require explicit decimal text, without
    # implicit float conversion or accidental rounding during JSON parsing.
    if not isinstance(value, str) or len(value)>90 or not value.strip():
        raise MethodGateError(f"{label}: numeric value must be decimal text")
    try:
        x=Decimal(value)
    except InvalidOperation as exc:
        raise MethodGateError(f"{label}: invalid decimal") from exc
    if not x.is_finite() or (nonnegative and x<0):
        raise MethodGateError(f"{label}: finite/nonnegative value required")
    if x.adjusted()>120 or (x!=0 and x.adjusted() < -120):
        raise MethodGateError(f"{label}: exponent outside safe range")
    return x


def _complex(value: Any, label: str) -> tuple[Decimal,Decimal]:
    _fields(value,{'re','im'},label)
    return _decimal(value['re'],label+'.re'), _decimal(value['im'],label+'.im')


def _sqdiff(a,b) -> Decimal:
    with localcontext() as ctx:
        ctx.prec=1024
        return (a[0]-b[0])**2+(a[1]-b[1])**2


def _within(a,b,bound:Decimal) -> bool:
    with localcontext() as ctx:
        ctx.prec=1024
        return _sqdiff(a,b)<=bound**2


def _read_json_strict(path:Path) -> dict:
    if not path.is_file() or path.is_symlink() or path.stat().st_size>MAX_INPUT_BYTES:
        raise MethodGateError('manifest missing, symlinked or too large')
    def unique_pairs(pairs):
        ret={}
        for key,value in pairs:
            if key in ret:
                raise MethodGateError('duplicate JSON key: '+key)
            ret[key]=value
        return ret
    def refuse_constant(token):
        raise MethodGateError('non-finite JSON literal: '+token)
    try:
        return json.loads(path.read_text(encoding='utf-8'),
                          object_pairs_hook=unique_pairs,parse_constant=refuse_constant)
    except (OSError,UnicodeError,json.JSONDecodeError) as exc:
        raise MethodGateError('invalid manifest JSON') from exc


def _checked_source_bytes(root:Path,relative:str) -> bytes:
    if not isinstance(relative,str) or len(relative)>250 or '\\' in relative or ':' in relative:
        raise MethodGateError('unsafe method source path')
    pp=PurePosixPath(relative)
    if pp.is_absolute() or '..' in pp.parts or '.' in pp.parts or not pp.parts or str(pp)!=relative:
        raise MethodGateError('noncanonical method source path')
    root=Path(root).resolve(strict=True)
    p=root
    for component in pp.parts:
        p=p/component
        if p.is_symlink():
            raise MethodGateError('symlink in method source path')
    if not p.is_file() or p.stat().st_size>MAX_INPUT_BYTES:
        raise MethodGateError('method source not a regular, bounded file')
    if not p.resolve().is_relative_to(root):
        raise MethodGateError('method source outside audit root')
    return p.read_bytes()


def evaluate(manifest:dict, source_root:Path|None=None) -> dict:
    """Evaluate locally checked declarations; intentionally never award proof credit.

    Malformed or incomplete evidence raises MethodGateError and returns no PASS.
    A completed report states only local arithmetic/metadata consistency.
    """
    _fields(manifest,{'schema','claim_id','claim_text','input_path','context_path','input_sha256',
                      'context_sha256','comparison','methods','negative_controls',
                      'stability_samples'},'manifest')
    if manifest['schema']!=SCHEMA:
        raise MethodGateError('unsupported manifest schema')
    _identifier(manifest['claim_id'],'claim_id')
    _description(manifest['claim_text'],'claim_text')
    _hash(manifest['input_sha256'],'input_sha256')
    _hash(manifest['context_sha256'],'context_sha256')
    for path_key,sha_key in (('input_path','input_sha256'),('context_path','context_sha256')):
        rel=manifest[path_key]
        if not isinstance(rel,str) or not rel or len(rel)>250:
            raise MethodGateError('missing/noncanonical '+path_key)
        if source_root is not None:
            if hashlib.sha256(_checked_source_bytes(source_root,rel)).hexdigest()!=manifest[sha_key]:
                raise MethodGateError('frozen input or context source mismatch: '+path_key)
    policy=_fields(manifest['comparison'],{'absolute_tolerance','require_distinct_equation_families',
                                          'require_distinct_implementations'},'comparison')
    tolerance=_decimal(policy['absolute_tolerance'],'absolute_tolerance',True)
    if not isinstance(policy['require_distinct_equation_families'],bool) or not isinstance(policy['require_distinct_implementations'],bool):
        raise MethodGateError('comparison flags must be booleans')
    methods=manifest['methods']
    if not isinstance(methods,list) or not 2<=len(methods)<=MAX_METHODS:
        raise MethodGateError('2 to 12 independently described methods required')
    seen=set(); families=set(); equations=set(); implementations=set(); sources=set()
    parsed=[]
    for i,m in enumerate(methods):
        tag=f'methods[{i}]'
        _fields(m,{'method_id','method_family','equation_family','implementation_id',
                   'source_sha256','source_path','input_sha256','context_sha256','status',
                   'result','absolute_error_budget','error_budget_class','provenance'},tag)
        mid=_identifier(m['method_id'],tag+'.method_id')
        if mid in seen: raise MethodGateError('duplicate method ID')
        seen.add(mid)
        for k in ('method_family','equation_family','implementation_id'):
            _identifier(m[k],tag+'.'+k)
        src=_hash(m['source_sha256'],tag+'.source_sha256')
        rel=m['source_path']
        if not isinstance(rel,str) or not rel or len(rel)>250:
            raise MethodGateError(tag+'.source_path missing')
        if source_root is not None:
            actual=hashlib.sha256(_checked_source_bytes(source_root,rel)).hexdigest()
            if actual!=src:
                raise MethodGateError('source SHA256 mismatch: '+mid)
        if m['input_sha256']!=manifest['input_sha256'] or m['context_sha256']!=manifest['context_sha256']:
            raise MethodGateError('methods do not share frozen input and physical context')
        if m['status']!='completed':
            raise MethodGateError('method not completed')
        _description(m['provenance'],tag+'.provenance')
        if m['error_budget_class'] not in ('self_declared_numerical','verified_interval','exact_symbolic'):
            raise MethodGateError('unknown error-budget declaration')
        value=_complex(m['result'],tag+'.result')
        budget=_decimal(m['absolute_error_budget'],tag+'.absolute_error_budget',True)
        parsed.append((mid,value,budget))
        families.add(m['method_family']); equations.add(m['equation_family']); implementations.add(m['implementation_id']); sources.add(src)
    if len(families)<2 or len(sources)<2:
        raise MethodGateError('same declared method family/source cannot establish cross-method comparison')
    if policy['require_distinct_equation_families'] and len(equations)<2:
        raise MethodGateError('distinct equation families required but not present')
    if policy['require_distinct_implementations'] and len(implementations)<2:
        raise MethodGateError('distinct implementations required but not present')
    disagreements=[]
    for i in range(len(parsed)):
        for j in range(i+1,len(parsed)):
            mi,vi,ei=parsed[i]; mj,vj,ej=parsed[j]
            with localcontext() as ctx:
                ctx.prec=1024
                effective=ei+ej+tolerance
            if not _within(vi,vj,effective):
                raise MethodGateError(f'incompatible methods: {mi} vs {mj}')
            disagreements.append(f'{mi} / {mj}: compatible under declared budgets')
    controls=manifest['negative_controls']
    if not isinstance(controls,list) or not 1<=len(controls)<=MAX_NEGATIVE_CONTROLS:
        raise MethodGateError('at least one negative control is mandatory')
    ctl_names=set()
    for i,c in enumerate(controls):
        tag=f'negative_controls[{i}]'
        _fields(c,{'name','perturbation','baseline_residual','corrupted_residual',
                   'baseline_maximum','corruption_minimum'},tag)
        name=_identifier(c['name'],tag+'.name')
        if name in ctl_names: raise MethodGateError('duplicate negative-control name')
        ctl_names.add(name)
        _description(c['perturbation'],tag+'.perturbation')
        good=_decimal(c['baseline_residual'],tag+'.baseline_residual',True)
        bad=_decimal(c['corrupted_residual'],tag+'.corrupted_residual',True)
        goodmax=_decimal(c['baseline_maximum'],tag+'.baseline_maximum',True)
        badmin=_decimal(c['corruption_minimum'],tag+'.corruption_minimum',True)
        if good>goodmax or bad<=badmin or badmin<=goodmax:
            raise MethodGateError(f'negative control not discriminating: {name}')
    stability=manifest['stability_samples']
    if not isinstance(stability,list) or not 3<=len(stability)<=MAX_STABILITY_SAMPLES:
        raise MethodGateError('minimum three stability settings required')
    setting_names=set()
    for i,s in enumerate(stability):
        tag=f'stability_samples[{i}]'
        _fields(s,{'setting','result','reference_method_id','declared_maximum_deviation'},tag)
        name=_identifier(s['setting'],tag+'.setting')
        if name in setting_names: raise MethodGateError('duplicate stability setting')
        setting_names.add(name)
        ref=_identifier(s['reference_method_id'],tag+'.reference_method_id')
        matching=[v for n,v,e in parsed if n==ref]
        if len(matching)!=1: raise MethodGateError('unknown stability reference method')
        value=_complex(s['result'],tag+'.result')
        bound=_decimal(s['declared_maximum_deviation'],tag+'.declared_maximum_deviation',True)
        if not _within(value,matching[0],bound):
            raise MethodGateError(f'instability at setting: {name}')
    canonical=json.dumps(manifest,sort_keys=True,ensure_ascii=False,
                         separators=(',',':'),allow_nan=False).encode('utf-8')
    return {
       'schema':'physqed-method-report-v0.5',
       'claim_id':manifest['claim_id'],
       'input_sha256':manifest['input_sha256'],
       'context_sha256':manifest['context_sha256'],
       'manifest_sha256':hashlib.sha256(canonical).hexdigest(),
       'status':('LOCAL_METHOD_AND_SOURCE_INTEGRITY_PASSED__PROOF_UNVERIFIED' if source_root is not None else 'LOCAL_METHOD_CONSISTENCY_PASSED__SOURCE_UNVERIFIED__PROOF_UNVERIFIED'),
       'method_source_hashes_verified':source_root is not None,
       'methods_compared':len(methods),
       'pairwise_comparisons':len(disagreements),
       'negative_controls_passed':len(controls),
       'stability_settings_checked':len(stability),
       'different_equation_families_declared':len(equations)>1,
       'independent_method_provenance_authenticated':False,
       'rigorous_error_bounds_independently_verified':False,
       'lean_kernel_verified':False,
       'semantic_alignment_verified':False,
       'empirical_validation_verified':False,
       'physical_law_proven':False,
       'warning':WARNING,
    }


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--source-root',type=Path,help='verify actual source bytes for each declared method')
    p.add_argument('--output',type=Path)
    args=p.parse_args(argv)
    try:
        result=evaluate(_read_json_strict(args.manifest),source_root=args.source_root)
        raw=json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+'\n'
        if args.output:
            if args.output.is_symlink(): raise MethodGateError('output path cannot be symlink')
            args.output.write_text(raw,encoding='utf-8')
        else:
            print(raw,end='')
    except (MethodGateError,ValueError,TypeError,OSError) as exc:
        p.exit(2,'PHYSQED method gate REFUSED: '+str(exc)+'\n')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
