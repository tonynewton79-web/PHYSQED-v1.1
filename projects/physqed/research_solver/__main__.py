"""CLI entrypoint. From repo root: PYTHONPATH=projects/physqed python -m research_solver ..."""
from .problem import main
if __name__ == "__main__":
    raise SystemExit(main())
