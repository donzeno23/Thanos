"""Main test suite discovery implementation."""

from pathlib import Path
from typing import List, Optional

from .interfaces import FileParser, TestSuiteFilter, FileDiscoverer, TestSuiteInfo
from .parsers import ASTTestSuiteParser
from .filters import DecoratorFilter
from .discoverers import GlobFileDiscoverer, RegexFileDiscoverer


class TestSuiteDiscovery:
    """Main test suite discovery service following dependency injection pattern."""
    
    def __init__(
        self,
        parser: Optional[FileParser] = None,
        discoverer: Optional[FileDiscoverer] = None,
        filters: Optional[List[TestSuiteFilter]] = None
    ):
        self.parser = parser or ASTTestSuiteParser()
        self.discoverer = discoverer or GlobFileDiscoverer()
        self.filters = filters or [DecoratorFilter({'testsuite'})]
    
    def discover(self, directory: str | Path, pattern: str = "*.py") -> List[TestSuiteInfo]:
        """Discover test suites in directory matching pattern and filters."""
        directory = Path(directory)
        
        # Discover files
        files = self.discoverer.discover_files(directory, pattern)
        
        # Parse files for test suites
        all_test_suites = []
        for file_path in files:
            test_suites = self.parser.parse(file_path)
            all_test_suites.extend(test_suites)
        
        # Apply filters
        filtered_suites = []
        for suite in all_test_suites:
            if all(f.matches(suite) for f in self.filters):
                filtered_suites.append(suite)
        
        return filtered_suites
    
    def discover_by_decorator(self, directory: str | Path, decorator: str) -> List[TestSuiteInfo]:
        """Convenience method to discover by specific decorator."""
        discovery = TestSuiteDiscovery(
            parser=self.parser,
            discoverer=self.discoverer,
            filters=[DecoratorFilter({decorator})]
        )

    
    def discover_with_regex(self, directory: str | Path, regex_pattern: str, case_sensitive: bool = True) -> List[TestSuiteInfo]:
        """Discover test suites using advanced regex path matching.
        
        Args:
            directory: Root directory to search
            regex_pattern: Regex pattern for path matching
                          Examples:
                          - 'ets/*/project*/py3/test/*/performance/*.py'
                          - 'app/.*/test.*\.py$'
                          - '.*test.*\.py$'
            case_sensitive: Whether pattern matching is case sensitive
            
        Returns:
            List of discovered test suites matching the regex pattern
        """
        regex_discoverer = RegexFileDiscoverer(case_sensitive=case_sensitive)
        discovery = TestSuiteDiscovery(
            parser=self.parser,
            discoverer=regex_discoverer,
            filters=self.filters
        )
        return discovery.discover(directory, regex_pattern)
    
    def get_summary(self, test_suites: List[TestSuiteInfo]) -> dict:
        """Get summary statistics of discovered test suites."""
        if not test_suites:
            return {"total": 0, "files": 0, "decorators": {}}
        
        files = set(suite.file_path for suite in test_suites)
        decorators = {}
        
        for suite in test_suites:
            decorator = suite.decorator_name
            decorators[decorator] = decorators.get(decorator, 0) + 1
        
        return {
            "total": len(test_suites),
            "files": len(files),
            "decorators": decorators,
            "avg_methods_per_suite": sum(len(suite.methods) for suite in test_suites) / len(test_suites)
        }