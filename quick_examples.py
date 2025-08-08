#!/usr/bin/env python3
"""Quick Usage Examples for Thanos Test Suite Discovery"""

from pathlib import Path
from thanos.discovery.parsers import ASTTestSuiteParser
from thanos.discovery.discovery import TestSuiteDiscovery


def quick_parse_example():
    """Parse a single test file"""
    parser = ASTTestSuiteParser()
    suites = parser.parse(Path("src/thanos/tests/test_suite_basic.py"))
    
    for suite in suites:
        print(f"Suite: {suite.class_name}")
        print(f"Methods: {suite.methods}")


def quick_discovery_example():
    """Discover all test suites in project"""
    discovery = TestSuiteDiscovery()
    suites = discovery.discover("src/thanos")
    
    print(f"Found {len(suites)} test suites:")
    for suite in suites:
        print(f"  {suite.class_name} in {suite.file_path.name}")


def quick_filter_example():
    """Find suites by decorator"""
    discovery = TestSuiteDiscovery()
    suites = discovery.discover_by_decorator("src/thanos", "testsuite")
    
    for suite in suites:
        print(f"{suite.class_name}: {len(suite.methods)} test methods")


if __name__ == "__main__":
    print("=== Quick Examples ===")
    quick_parse_example()
    print()
    quick_discovery_example()
    print()
    quick_filter_example()