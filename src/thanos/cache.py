from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List
from rich import print as rprint


@dataclass
class StageResult:
    name: str
    status: str
    result_data: Any
    start_time: datetime
    end_time: datetime
    duration_ms: float

@dataclass
class TestRunResult:
    run_id: str
    timestamp: datetime
    overall_status: str
    stage_results: List[StageResult] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
class TestCache:
    """
    A simple in-memory cache to store test run results.
    """
    def __init__(self):
        self._cache: Dict[str, TestRunResult] = {}
    
    def add_run_result(self, run_result: TestRunResult):
        """Adds a complete test run result to the cache."""
        self._cache[run_result.run_id] = run_result
        rprint(f"Test run '{run_result.run_id}' added to cache with status '{run_result.overall_status}'.") 
        print(f"Test run '{run_result.run_id}' stored in cache.")

    def get_run_result(self, run_id: str) -> TestRunResult | None:
        """Retrieves a test run result from the cache."""
        return self._cache.get(run_id)

    def get_all_results(self) -> List[TestRunResult]:
        """Returns all cached results."""
        return list(self._cache.values())

    def clear(self):
        """Clears the cache."""
        self._cache = {}
