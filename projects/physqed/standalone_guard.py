"""Reject accidental inclusion of project-specific audit files in engine source."""
from pathlib import Path

ROOT=Path(__file__).resolve().parent
# Never ship a former audited manuscript, a bespoke solver, event data or
# project-specific result directory inside the general-purpose engine.
BANNED_PARTS={'paper-audits','external_case_audits','case_studies',
              'cases','datasets','manuscripts','observations','raw_data'}
BANNED_FILENAME_TOKENS=('event_specific_','paper_specific_','case_dataset_')
for p in ROOT.rglob('*'):
    if not p.is_file():
        continue
    rel=p.relative_to(ROOT)
    if any(part.lower() in BANNED_PARTS for part in rel.parts):
        raise SystemExit('REFUSED: project-specific directory: '+str(rel))
    if any(token in rel.name.lower() for token in BANNED_FILENAME_TOKENS) or p.suffix.lower() in ('.pdf','.tex','.h5','.hdf5','.fits'):
        raise SystemExit('REFUSED: project-specific file: '+str(rel))
print('STANDALONE_RELEASE_GUARD_PASS: no project-specific audit files')
