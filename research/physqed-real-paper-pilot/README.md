# External real-paper pilot: Penrose Kerr 221/220 numerical claim

The user-supplied 56-page Penrose research PDF is intentionally NOT committed into PHYSQED's generic engine or the public repository. The separate external audit is executable as:

```sh
python research/physqed-real-paper-pilot/audit_penrose.py \
    /path/to/Penrose_GW250114_Cumulative_NR_Validated-1.pdf \
    --output penrose-scoped-arithmetic-report.json
```

Input PDF SHA256: `603f0e8833f9adef1f3c8bd262c1499c73b5483d0c994b24132f582e8882b215`

**Local independent audit of printed paper numbers (24 Oct 2026): 8/8** scoped checks passed, including ratio division with 75-digit Decimal arithmetic, quoted Leaver discrepancy and four negative controls. These are NOT 8 physical tests or mathematical proof certificates; the inputs are numbers quoted in the user's paper, not fresh GSN solver outputs. The paper's proposed independent horizon-shear measurement is explicitly still missing.

External auditor code lives outside `projects/physqed/` so that the reusable PHYSQED engine is manuscript-independent. CI does not test this external paper unless the exact user-provided source PDF is supplied; no remote PDF build or actual Kerr solver certification is asserted.
