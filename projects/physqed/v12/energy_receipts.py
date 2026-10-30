"""Recomputed component certificates for variable-coefficient energy checks.

No supplied certificate is trusted solely on its own checksum; the
typed mathematical inputs are recomputed by the current verifier.
"""
from hashlib import sha256
from pathlib import Path
import json
import sympy as S
from .variable_energy import audit_matrix_energy


def issue_energy_receipt(coords,symmetrizer,principal,lower_order,source=None):
    result=audit_matrix_energy(
        coords,symmetrizer,principal,lower_order,source)
    raw={
        "schema":"physqed.variable-energy-receipt.v1",
        "status":("PASS_LOCAL_ENERGY_IDENTITY__DOMAIN_UNVERIFIED"
                  if result["exact_local_balance_identity"] else
                  "REJECTED_LOCAL_ENERGY_IDENTITY"),
        "coords":[str(x) for x in coords],
        "symmetrizer":S.srepr(S.Matrix(symmetrizer)),
        "principal":[S.srepr(S.Matrix(x)) for x in principal],
        "lower_order":S.srepr(S.Matrix(lower_order)),
        "source":S.srepr(S.zeros(S.Matrix(symmetrizer).rows,1)
                         if source is None else S.Matrix(source)),
        "energy_density":S.srepr(result["energy_density"]),
        "energy_flux":[S.srepr(x) for x in result["energy_flux"]],
        "coefficient_defect":S.srepr(result["coefficient_defect"]),
        "residual":S.srepr(result["residual"]),
        "global_coercivity_proven":False,
        "domain_derivative_bounds_proven":False,
        "boundary_flux_control_proven":False,
        "global_pde_uniqueness_proven":False,
        "backend_sha256":sha256(
            Path(__file__).with_name("variable_energy.py").read_bytes()).hexdigest(),
    }
    raw["receipt_sha256"]=sha256(json.dumps(
        raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return raw


def replay_energy_receipt(coords,symmetrizer,principal,lower_order,stored,source=None):
    if not isinstance(stored,dict):
        return False
    fresh=issue_energy_receipt(coords,symmetrizer,principal,lower_order,source)
    return (json.dumps(fresh,sort_keys=True,separators=(",",":")) ==
            json.dumps(stored,sort_keys=True,separators=(",",":")))
