"""Filters for test suite discovery."""

from typing import Set
from .interfaces import TestSuiteFilter, TestSuiteInfo


class DecoratorFilter(TestSuiteFilter):
    """Filter test suites by decorator name."""
    
    def __init__(self, decorators: Set[str]):
        self.decorators = decorators
    
    def matches(self, test_suite_info: TestSuiteInfo) -> bool:
        """Check if test suite has matching decorator."""
        return test_suite_info.decorator_name in self.decorators


class MethodCountFilter(TestSuiteFilter):
    """Filter test suites by minimum method count."""
    
    def __init__(self, min_methods: int):
        self.min_methods = min_methods
    
    def matches(self, test_suite_info: TestSuiteInfo) -> bool:
        """Check if test suite has minimum number of methods."""
        return len(test_suite_info.methods) >= self.min_methods


class CompositeFilter(TestSuiteFilter):
    """Composite filter that combines multiple filters with AND logic."""
    
    def __init__(self, filters: list[TestSuiteFilter]):
        self.filters = filters
    
    def matches(self, test_suite_info: TestSuiteInfo) -> bool:
        """Check if test suite matches all filters."""
        return all(f.matches(test_suite_info) for f in self.filters)