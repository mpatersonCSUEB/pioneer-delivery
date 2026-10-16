"""Greedy scheduling algorithms for Tasks A, B and C."""

import heapq

from delivery import Delivery


def max_deliveries_one_driver(deliveries: list[Delivery]) -> list[Delivery]:
    """Task A: interval scheduling by earliest finish time.

    Greedy choice: among the deliveries compatible with what has already been
    chosen, take the one that finishes first.  O(n log n) for the sort, O(n) scan.
    """
    selected: list[Delivery] = []
    last_finish = float("-inf")
    for d in sorted(deliveries, key=lambda d: d.finish):
        if d.start >= last_finish:  # touching endpoints are allowed
            selected.append(d)
            last_finish = d.finish
    return selected


def min_drivers(deliveries: list[Delivery]) -> list[list[Delivery]]:
    """Task B: interval partitioning with a min-heap.

    Deliveries are processed by start time.  The heap holds one entry per
    driver: (time that driver becomes free, driver index).  If the driver who
    frees up earliest is free by the new delivery's start, reuse that driver;
    otherwise hire a new one.  O(n log n).

    Returns a list of schedules, one per driver.
    """
    schedules: list[list[Delivery]] = []
    heap: list[tuple[int, int]] = []  # (free_at, driver_index)

    for d in sorted(deliveries, key=lambda d: d.start):
        if heap and heap[0][0] <= d.start:
            _, idx = heapq.heappop(heap)
        else:
            idx = len(schedules)
            schedules.append([])
        schedules[idx].append(d)
        heapq.heappush(heap, (d.finish, idx))

    return schedules


def min_rejections(deliveries: list[Delivery]) -> tuple[int, list[Delivery]]:
    """Task C: fewest deliveries to reject so the rest are compatible.

    Keeping the most deliveries means rejecting the fewest, so this is
    n - (Task A answer).  O(n log n).

    Returns (number rejected, the rejected deliveries).
    """
    kept = set(max_deliveries_one_driver(deliveries))
    rejected = [d for d in deliveries if d not in kept]
    return len(rejected), rejected


def is_compatible(schedule: list[Delivery]) -> bool:
    """True if no two deliveries in the schedule overlap."""
    ordered = sorted(schedule, key=lambda d: d.start)
    return all(a.finish <= b.start for a, b in zip(ordered, ordered[1:]))
