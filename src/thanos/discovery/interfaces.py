"""Interfaces for test suite discovery components."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pathlib import Path
from dataclasses import dataclass


@dataclass
class TestSuiteInfo:
    """Information about a discovered test suite."""
    file_path: Path
    class_name: str
    decorator_name: str
    methods: List[str]
    imports: List[str]


class FileParser(ABC):
    """Abstract interface for parsing files to extract test suite information."""
    
    @abstractmethod
    def parse(self, file_path: Path) -> List[TestSuiteInfo]:
        """Parse a file and return test suite information."""
        pass


class TestSuiteFilter(ABC):
    """Abstract interface for filtering test suites."""
    
    @abstractmethod
    def matches(self, test_suite_info: TestSuiteInfo) -> bool:
        """Check if test suite matches filter criteria."""
        pass


class FileDiscoverer(ABC):
    """Abstract interface for discovering files."""
    
    @abstractmethod
    def discover_files(self, directory: Path, pattern: str) -> List[Path]:
        """Discover files matching pattern in directory."""
        pass