"""Task D: show that greedy-by-decreasing-profit is not optimal.

Value of delivery j in slot T:  P_j / (1 + (T - R_j)).
"""

from fractions import Fraction
from itertools import permutations

# (name, ready time R, profit P)
JOBS = [("A", 0, 10), ("B", 0, 9), ("C", 1, 8)]


def value(schedule: dict[str, int]) -> Fraction:
    jobs = {name: (r, p) for name, r, p in JOBS}
    return sum(Fraction(jobs[n][1], 1 + t - jobs[n][0]) for n, t in schedule.items())


def greedy_schedule() -> dict[str, int]:
    """Strategy G: decreasing profit, earliest free slot at or after R."""
    used: set[int] = set()
    schedule = {}
    for name, r, _ in sorted(JOBS, key=lambda j: -j[2]):
        t = r
        while t in used:
            t += 1
        used.add(t)
        schedule[name] = t
    return schedule


def brute_force_best() -> tuple[dict[str, int], Fraction]:
    """Try every assignment of jobs to slots 0..n+max(R) to find the optimum."""
    horizon = len(JOBS) + max(r for _, r, _ in JOBS)
    best, best_val = None, Fraction(-1)
    for slots in permutations(range(horizon), len(JOBS)):
        if all(t >= r for t, (_, r, _) in zip(slots, JOBS)):
            s = {name: t for t, (name, _, _) in zip(slots, JOBS)}
            v = value(s)
            if v > best_val:
                best, best_val = s, v
    return best, best_val


def fmt(schedule: dict[str, int]) -> str:
    return ", ".join(f"{n}@t={t}" for n, t in sorted(schedule.items(), key=lambda x: x[1]))


def main() -> None:
    print("Jobs (name, R, P):", JOBS)
    g = greedy_schedule()
    print(f"Greedy G : {fmt(g)}  ->  V = {float(value(g)):g}")
    s, v = brute_force_best()
    print(f"Optimal S: {fmt(s)}  ->  V = {float(v):g}")
    print("Greedy is NOT optimal." if v > value(g) else "Greedy matched optimum.")


if __name__ == "__main__":
    main()
