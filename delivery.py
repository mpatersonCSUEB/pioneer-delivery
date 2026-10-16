"""Delivery data model and file loading for the Pioneer Delivery scheduler."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Delivery:
    id: str
    start: int
    finish: int

    def __str__(self) -> str:
        return f"{self.id} [{self.start}, {self.finish})"


def load_deliveries(path: str) -> list[Delivery]:
    """Read deliveries from a whitespace-separated file: `id start finish` per line.

    Blank lines and lines starting with '#' are ignored.
    """
    deliveries = []
    with open(path) as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(f"Line {line_no}: expected 'id start finish', got {raw!r}")
            did, start, finish = parts[0], int(parts[1]), int(parts[2])
            if start >= finish:
                raise ValueError(f"Line {line_no}: start must be < finish ({start} >= {finish})")
            deliveries.append(Delivery(did, start, finish))
    return deliveries


def from_pairs(pairs: list[tuple[int, int]]) -> list[Delivery]:
    """Build deliveries from (start, finish) pairs, auto-naming them D1, D2, ..."""
    return [Delivery(f"D{i}", s, f) for i, (s, f) in enumerate(pairs, start=1)]
