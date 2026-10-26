"""Periodic finite four-dimensional SU(2) Wilson lattice.

No continuum limit, QFT reconstruction, or physical mass-gap claim is made.
"""

from __future__ import annotations

import itertools
import math

from .su2 import Quaternion, dagger, mul, norm2

Site = tuple[int, int, int, int]
LinkKey = tuple[Site, int]
IDENTITY: Quaternion = (1.0, 0.0, 0.0, 0.0)


class Lattice4D:
    def __init__(
        self,
        extents: tuple[int, int, int, int],
        links: dict[LinkKey, Quaternion] | None = None,
    ) -> None:
        if (len(extents) != 4 or any(type(n) is not int or n < 2 for n in extents)):
            raise ValueError("four integer lattice extents of at least 2 required")
        self.extents = tuple(extents)
        self.sites: tuple[Site, ...] = tuple(itertools.product(*(range(n) for n in extents)))
        self.plaquette_count = 6 * len(self.sites)
        self.links: dict[LinkKey, Quaternion] = {
            (site, direction): IDENTITY for site in self.sites for direction in range(4)
        }
        if links is not None:
            if set(links) != set(self.links):
                raise ValueError("link mapping must cover exactly every oriented positive link")
            for (site, direction), value in links.items():
                self.set_link(site, direction, value)

    def _check_site(self, site: Site) -> None:
        if (not isinstance(site, tuple) or len(site) != 4 or
            any(type(i) is not int or i < 0 or i >= n for i, n in zip(site, self.extents))):
            raise ValueError("site outside periodic 4D lattice")

    @staticmethod
    def _check_direction(direction: int) -> None:
        if type(direction) is not int or not 0 <= direction < 4:
            raise ValueError("invalid link direction")

    def shifted(self, site: Site, direction: int, step: int = 1) -> Site:
        self._check_site(site)
        self._check_direction(direction)
        if type(step) is not int:
            raise ValueError("integer lattice step required")
        coords = list(site)
        coords[direction] = (coords[direction] + step) % self.extents[direction]
        return tuple(coords)  # type: ignore[return-value]

    def link(self, site: Site, direction: int) -> Quaternion:
        self._check_site(site)
        self._check_direction(direction)
        return self.links[(site, direction)]

    def set_link(self, site: Site, direction: int, value: Quaternion) -> None:
        self._check_site(site)
        self._check_direction(direction)
        squared = norm2(value)
        if not math.isfinite(squared) or abs(squared - 1.0) > 1e-9:
            raise ValueError("SU(2) link requires a unit quaternion")
        self.links[(site, direction)] = tuple(float(x) for x in value)  # type: ignore[assignment]

    def plaquette(self, site: Site, mu: int, nu: int) -> Quaternion:
        self._check_site(site)
        self._check_direction(mu)
        self._check_direction(nu)
        if mu == nu:
            raise ValueError("plaquette directions must differ")
        first = mul(self.link(site, mu), self.link(self.shifted(site, mu), nu))
        second = mul(first, dagger(self.link(self.shifted(site, nu), mu)))
        return mul(second, dagger(self.link(site, nu)))

    def wilson_action(self, beta: float) -> float:
        if not isinstance(beta, (int, float)) or not math.isfinite(beta) or beta < 0:
            raise ValueError("finite nonnegative beta required")
        return float(beta) * math.fsum(
            1.0 - self.plaquette(site, mu, nu)[0]
            for site in self.sites for mu in range(4) for nu in range(mu+1, 4)
        )

    def gauge_transformed(self, site_gauge: dict[Site, Quaternion]) -> Lattice4D:
        if set(site_gauge) != set(self.sites):
            raise ValueError("gauge transformation requires one SU(2) element per site")
        for value in site_gauge.values():
            if abs(norm2(value) - 1) > 1e-9:
                raise ValueError("site gauge elements must be unit quaternions")
        transformed = {}
        for site in self.sites:
            for mu in range(4):
                endpoint = self.shifted(site, mu)
                transformed[(site, mu)] = mul(
                    mul(site_gauge[site], self.link(site, mu)),
                    dagger(site_gauge[endpoint]),
                )
        return Lattice4D(self.extents, transformed)
