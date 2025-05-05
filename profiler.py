import threading
from collections import defaultdict
from typing import Dict, List, Any

class Profiler:
    def __init__(self):
        # Thread-safe storage for profiling data
        self._lock = threading.Lock()
        self._records = []  # List of dicts: {segment_name, start, end, duration, iteration}
        self._segment_counts = defaultdict(int)
        self._iteration_map = defaultdict(list)  # iteration_num -> list of records
        self._current_iteration = 0

    def start_iteration(self):
        """Start a new iteration scope. Returns the iteration number."""
        with self._lock:
            self._current_iteration += 1
            return self._current_iteration

    def record(self, segment_name: str, start_ms: float, end_ms: float):
        """Record a segment's execution time in milliseconds."""
        duration = end_ms - start_ms
        with self._lock:
            # Always use the current iteration
            iteration = self._current_iteration
            record = {
                'segment_name': segment_name,
                'start': start_ms,
                'end': end_ms,
                'duration': duration,
                'iteration': iteration
            }
            self._records.append(record)
            self._segment_counts[segment_name] += 1
            self._iteration_map[iteration].append(record)

    def numberOfExecutions(self) -> int:
        """Return the total number of recorded executions."""
        with self._lock:
            return len(self._records)

    def listSegments(self) -> List[str]:
        """Return a list of unique segment names."""
        with self._lock:
            return list(self._segment_counts.keys())

    def iterationData(self, iteration: int) -> List[Dict[str, Any]]:
        """Return all records for a given iteration."""
        with self._lock:
            return list(self._iteration_map.get(iteration, []))

    def averageDuration(self, segment_name: str, parent_iteration: int = None) -> float:
        """Compute average duration for a segment, optionally within a parent iteration scope."""
        with self._lock:
            if parent_iteration is not None:
                records = [r for r in self._iteration_map[parent_iteration] if r['segment_name'] == segment_name]
            else:
                records = [r for r in self._records if r['segment_name'] == segment_name]
            if not records:
                return 0.0
            return sum(r['duration'] for r in records) / len(records)

# Example usage:
# profiler = Profiler()
# iter1 = profiler.start_iteration()
# profiler.record("segment A", 1000, 1200)
# profiler.record("segment B", 1200, 1300)
# profiler.numberOfExecutions()
# profiler.listSegments()
# profiler.iterationData(iter1)
# profiler.averageDuration("segment A")
