#!/usr/bin/env python3
"""
Usage Examples for Thanos Test Suite Discovery System

This file demonstrates various ways to use the test suite discovery components
including parsers, discoverers, filters, and the main discovery service.
"""

from pathlib import Path
from thanos.discovery.parsers import ASTTestSuiteParser
from thanos.discovery.discoverers import GlobFileDiscoverer, FilteredFileDiscoverer
from thanos.discovery.filters import DecoratorFilter, MethodCountFilter, CompositeFilter
from thanos.discovery.discovery import TestSuiteDiscovery


def example_basic_parser():
    """Example 1: Basic AST parser usage"""
    print("=== Example 1: Basic AST Parser ===")
    
    parser = ASTTestSuiteParser()
    test_file = Path("src/thanos/tests/test_suite_basic.py")
    
    if test_file.exists():
        suites = parser.parse(test_file)
        for suite in suites:
            print(f"Found suite: {suite.class_name}")
            print(f"  Decorator: {suite.decorator_name}")
            print(f"  Methods: {suite.methods}")
            print(f"  File: {suite.file_path}")
    else:
        print(f"File not found: {test_file}")


def example_custom_decorators():
    """Example 2: Parser with custom decorators"""
    print("\n=== Example 2: Custom Decorators ===")
    
    # Look for multiple decorator types
    parser = ASTTestSuiteParser(target_decorators={'testsuite', 'performance_suite', 'integration_suite'})
    
    test_files = [
        Path("src/thanos/tests/test_suite_basic.py"),
        Path("src/thanos/app/backend/bapp_one/test_suite_one.py")
    ]
    
    for test_file in test_files:
        if test_file.exists():
            suites = parser.parse(test_file)
            print(f"\nFile: {test_file}")
            for suite in suites:
                print(f"  Suite: {suite.class_name} (@{suite.decorator_name})")


def example_file_discovery():
    """Example 3: File discovery patterns"""
    print("\n=== Example 3: File Discovery ===")
    
    # Basic glob discoverer
    discoverer = GlobFileDiscoverer()
    base_dir = Path("src/thanos")
    
    # Find all Python files
    py_files = discoverer.discover_files(base_dir, "*.py")
    print(f"Found {len(py_files)} Python files")
    
    # Find test suite files specifically
    test_files = discoverer.discover_files(base_dir, "*test_suite*.py")
    print(f"Found {len(test_files)} test suite files:")
    for file in test_files:
        print(f"  {file}")


def example_filtered_discovery():
    """Example 4: Filtered file discovery"""
    print("\n=== Example 4: Filtered Discovery ===")
    
    # Custom filtered discoverer
    discoverer = FilteredFileDiscoverer(
        extensions={'.py'},
        exclude_patterns={'__pycache__', '.pyc', 'venv'}
    )
    
    base_dir = Path("src/thanos")
    files = discoverer.discover_files(base_dir, "*test*")
    print(f"Found {len(files)} test-related files:")
    for file in files:
        print(f"  {file}")


def example_filters():
    """Example 5: Using filters"""
    print("\n=== Example 5: Filters ===")
    
    parser = ASTTestSuiteParser()
    test_file = Path("src/thanos/app/backend/bapp_one/test_suite_one.py")
    
    if test_file.exists():
        suites = parser.parse(test_file)
        
        # Decorator filter
        decorator_filter = DecoratorFilter({'testsuite'})
        filtered_suites = [s for s in suites if decorator_filter.matches(s)]
        print(f"Suites with @testsuite: {len(filtered_suites)}")
        
        # Method count filter
        method_filter = MethodCountFilter(min_methods=1)
        method_filtered = [s for s in suites if method_filter.matches(s)]
        print(f"Suites with 1+ methods: {len(method_filtered)}")
        
        # Composite filter
        composite = CompositeFilter([decorator_filter, method_filter])
        composite_filtered = [s for s in suites if composite.matches(s)]
        print(f"Suites matching both filters: {len(composite_filtered)}")


def example_main_discovery():
    """Example 6: Main discovery service"""
    print("\n=== Example 6: Main Discovery Service ===")
    
    # Default discovery
    discovery = TestSuiteDiscovery()
    base_dir = Path("src/thanos")
    
    suites = discovery.discover(base_dir)
    print(f"Discovered {len(suites)} test suites")
    
    # Get summary
    summary = discovery.get_summary(suites)
    print(f"Summary: {summary}")
    
    # Show details
    for suite in suites:
        print(f"\nSuite: {suite.class_name}")
        print(f"  File: {suite.file_path}")
        print(f"  Decorator: @{suite.decorator_name}")
        print(f"  Methods: {len(suite.methods)} - {suite.methods}")


def example_custom_discovery():
    """Example 7: Custom discovery configuration"""
    print("\n=== Example 7: Custom Discovery ===")
    
    # Custom parser for specific decorators
    parser = ASTTestSuiteParser(target_decorators={'testsuite'})
    
    # Custom discoverer with filtering
    discoverer = FilteredFileDiscoverer(
        extensions={'.py'},
        exclude_patterns={'__init__.py', '__pycache__'}
    )
    
    # Custom filters
    filters = [
        DecoratorFilter({'testsuite'}),
        MethodCountFilter(min_methods=1)
    ]
    
    # Create discovery service
    discovery = TestSuiteDiscovery(
        parser=parser,
        discoverer=discoverer,
        filters=filters
    )
    
    suites = discovery.discover("src/thanos/app")
    print(f"Custom discovery found {len(suites)} suites in app directory")
    
    for suite in suites:
        print(f"  {suite.class_name} in {suite.file_path.name}")


def example_decorator_specific():
    """Example 8: Discover by specific decorator"""
    print("\n=== Example 8: Decorator-Specific Discovery ===")
    
    discovery = TestSuiteDiscovery()
    
    # Find only @testsuite decorated classes
    testsuite_classes = discovery.discover_by_decorator("src/thanos", "testsuite")
    print(f"Found {len(testsuite_classes)} @testsuite classes")
    
    for suite in testsuite_classes:
        print(f"  {suite.class_name}: {len(suite.methods)} methods")


def example_directory_scanning():
    """Example 9: Scanning different directories"""
    print("\n=== Example 9: Directory Scanning ===")
    
    discovery = TestSuiteDiscovery()
    
    directories = [
        "src/thanos/tests",
        "src/thanos/app/backend",
        "src/thanos/app/frontend"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if dir_path.exists():
            suites = discovery.discover(directory)
            print(f"\n{directory}: {len(suites)} suites")
            for suite in suites:
                print(f"  {suite.class_name} ({len(suite.methods)} methods)")


def example_pattern_matching():
    """Example 10: Pattern matching for files"""
    print("\n=== Example 10: Pattern Matching ===")
    
    discovery = TestSuiteDiscovery()
    base_dir = "src/thanos"
    
    patterns = ["*test*.py", "*suite*.py", "test_*.py"]
    
    for pattern in patterns:
        suites = discovery.discover(base_dir, pattern)
        print(f"\nPattern '{pattern}': {len(suites)} suites")


if __name__ == "__main__":
    print("Thanos Test Suite Discovery - Usage Examples")
    print("=" * 50)
    
    # Run all examples
    example_basic_parser()
    example_custom_decorators()
    example_file_discovery()
    example_filtered_discovery()
    example_filters()
    example_main_discovery()
    example_custom_discovery()
    example_decorator_specific()
    example_directory_scanning()
    example_pattern_matching()
    
    print("\n" + "=" * 50)
    print("All examples completed!")