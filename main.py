"""Command-line entry point: run Tasks A, B and C on a delivery file.

Usage:  python main.py deliveries.txt
"""

import sys

from delivery import load_deliveries
from scheduling import max_deliveries_one_driver, min_drivers, min_rejections


def report_task_a(deliveries) -> None:
    print("=== Task A: Maximum deliveries for one driver ===")
    selected = max_deliveries_one_driver(deliveries)
    for d in selected:
        print(f"  {d.id:<6} start={d.start:<4} finish={d.finish}")
    print(f"Total deliveries completed: {len(selected)}\n")


def report_task_b(deliveries) -> None:
    print("=== Task B: Minimum number of drivers ===")
    schedules = min_drivers(deliveries)
    for i, sched in enumerate(schedules, start=1):
        print(f"  Driver {i}: " + " ".join(d.id for d in sched))
    print(f"Minimum drivers required: {len(schedules)}\n")


def report_task_c(deliveries) -> None:
    print("=== Task C: Minimum rejections (one driver) ===")
    count, rejected = min_rejections(deliveries)
    print("  Rejected: " + (" ".join(d.id for d in rejected) or "(none)"))
    print(f"Minimum deliveries rejected: {count}\n")


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    deliveries = load_deliveries(sys.argv[1])
    print(f"Loaded {len(deliveries)} deliveries from {sys.argv[1]}\n")
    report_task_a(deliveries)
    report_task_b(deliveries)
    report_task_c(deliveries)


if __name__ == "__main__":
    main()
