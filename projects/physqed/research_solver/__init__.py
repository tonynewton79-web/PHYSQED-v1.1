"""PHYSQED research solver (scoped orchestration, not universal certification)."""
from .problem import SCHEMA, solve_research_problem, replay_research_problem
__all__ = ("SCHEMA","solve_research_problem","replay_research_problem")
