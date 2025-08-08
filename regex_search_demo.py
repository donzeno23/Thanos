#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script showing advanced regex search functionality in Thanos test suite discovery.
"""

from pathlib import Path
from src.thanos.discovery.discovery import TestSuiteDiscovery
from src.thanos.discovery.discoverers import RegexFileDiscoverer

def main():
    """Demonstrate regex-based test suite discovery."""
    
    print("Thanos Advanced Regex Search Demo")
    print("=" * 50)
    
    # Initialize discovery service
    discovery = TestSuiteDiscovery()
    
    # Test directory
    test_dir = "src/thanos"
    
    print(f"\nSearching in: {test_dir}")
    print("-" * 30)
    
    # Example 1: Find all test files in app backend directories
    print("\n1. Backend test files:")
    backend_pattern = "app/.*/backend/.*test.*\\.py$"
    backend_suites = discovery.discover_with_regex(test_dir, backend_pattern)
    print(f"   Pattern: {backend_pattern}")
    print(f"   Found: {len(backend_suites)} suites")
    for suite in backend_suites:
        print(f"   - {suite.class_name} in {suite.file_path}")
    
    # Example 2: Find performance test suites
    print("\n2. Performance test suites:")
    perf_pattern = ".*/performance/.*\\.py$"
    perf_suites = discovery.discover_with_regex(test_dir, perf_pattern)
    print(f"   Pattern: {perf_pattern}")
    print(f"   Found: {len(perf_suites)} suites")
    for suite in perf_suites:
        print(f"   - {suite.class_name} in {suite.file_path}")
    
    # Example 3: Complex nested structure (like the requested example)
    print("\n3. Complex nested structure:")
    complex_pattern = "app/*/test_suite_.*\\.py$"
    complex_suites = discovery.discover_with_regex(test_dir, complex_pattern)
    print(f"   Pattern: {complex_pattern}")
    print(f"   Found: {len(complex_suites)} suites")
    for suite in complex_suites:
        print(f"   - {suite.class_name} in {suite.file_path}")
    
    # Example 4: Case-insensitive search
    print("\n4. Case-insensitive search:")
    case_pattern = ".*TEST.*\\.py$"
    case_suites = discovery.discover_with_regex(test_dir, case_pattern, case_sensitive=False)
    print(f"   Pattern: {case_pattern} (case-insensitive)")
    print(f"   Found: {len(case_suites)} suites")
    for suite in case_suites:
        print(f"   - {suite.class_name} in {suite.file_path}")
    
    # Example 5: Direct regex discoverer usage
    print("\n5. Direct RegexFileDiscoverer usage:")
    regex_discoverer = RegexFileDiscoverer(case_sensitive=True)
    files = regex_discoverer.discover_files(Path(test_dir), ".*suite.*\\.py$")
    print(f"   Pattern: .*suite.*\\.py$")
    print(f"   Found: {len(files)} files")
    for file_path in files:
        print(f"   - {file_path}")
    
    # Summary
    print("\nSummary:")
    print(f"   Total patterns tested: 5")
    print(f"   Backend tests: {len(backend_suites)}")
    print(f"   Performance tests: {len(perf_suites)}")
    print(f"   Complex pattern matches: {len(complex_suites)}")
    print(f"   Case-insensitive matches: {len(case_suites)}")
    print(f"   Direct discoverer files: {len(files)}")
    
    print("\nDemo completed!")

if __name__ == "__main__":
    main()