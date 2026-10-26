"""SU(2) link matrices represented by real unit Hamilton quaternions.

The map to matrices uses q = a I - i(b sigma_x + c sigma_y + d sigma_z)
with standard Pauli generators. Hamilton multiplication then matches
ordinary matrix multiplication exactly.
Only unit quaternions are group elements; norm2 also accepts general inputs.
"""

from __future__ import annotations

import math
from typing import TypeAlias

Quaternion: TypeAlias = tuple[float, float, float, float]


def _checked(q, dimension: int) -> tuple[float, ...]:
    try:
        result = tuple(float(value) for value in q)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("invalid quaternion/vector") from exc
    if len(result) != dimension or not all(math.isfinite(x) for x in result):
        raise ValueError("wrong dimension or nonfinite quaternion/vector")
    return result


def norm2(q: Quaternion) -> float:
    return sum(x*x for x in _checked(q, 4))


def normalized(q: Quaternion) -> Quaternion:
    values = _checked(q, 4)
    length = math.sqrt(sum(x*x for x in values))
    if not (length > 0 and math.isfinite(length)):
        raise ValueError("nonzero finite norm required")
    return tuple(x / length for x in values)  # type: ignore[return-value]


def dagger(q: Quaternion) -> Quaternion:
    a, b, c, d = _checked(q, 4)
    return (a, -b, -c, -d)


def mul(q: Quaternion, p: Quaternion) -> Quaternion:
    a, b, c, d = _checked(q, 4)
    e, f, g, h = _checked(p, 4)
    return (
        a*e - b*f - c*g - d*h,
        a*f + b*e + c*h - d*g,
        a*g - b*h + c*e + d*f,
        a*h + b*g - c*f + d*e,
    )


def scalar_trace(q: Quaternion) -> float:
    return 2.0 * _checked(q, 4)[0]


def axis_angle(axis: tuple[float, float, float], theta: float) -> Quaternion:
    x, y, z = _checked(axis, 3)
    if not math.isfinite(theta):
        raise ValueError("angle must be finite")
    length = math.hypot(x, y, z)
    if not length:
        raise ValueError("nonzero axis required")
    s = math.sin(theta)/length
    return (math.cos(theta), x*s, y*s, z*s)
