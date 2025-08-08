# Thanos Test Suite Discovery - Usage Examples

This document provides comprehensive usage examples for the Thanos test suite discovery system.

## Quick Start

The simplest way to discover test suites:

```python
from thanos.discovery.discovery import TestSuiteDiscovery

# Discover all test suites in project
discovery = TestSuiteDiscovery()
suites = discovery.discover("src/thanos")

for suite in suites:
    print(f"{suite.class_name}: {len(suite.methods)} methods")
```

## Core Components

### 1. ASTTestSuiteParser

Parses Python files using AST to find decorated test suite classes:

```python
from thanos.discovery.parsers import ASTTestSuiteParser

# Default parser looks for @testsuite decorator
parser = ASTTestSuiteParser()
suites = parser.parse(Path("test_file.py"))

# Custom decorators
parser = ASTTestSuiteParser(target_decorators={'testsuite', 'performance_suite'})
```

### 2. File Discoverers

Find files matching patterns:

```python
from thanos.discovery.discoverers import GlobFileDiscoverer, FilteredFileDiscoverer

# Basic glob pattern matching
discoverer = GlobFileDiscoverer()
files = discoverer.discover_files(Path("src"), "*.py")

# Advanced filtering
discoverer = FilteredFileDiscoverer(
    extensions={'.py'},
    exclude_patterns={'__pycache__', '.pyc'}
)
```

### 3. Filters

Filter discovered test suites:

```python
from thanos.discovery.filters import DecoratorFilter, MethodCountFilter

# Filter by decorator
decorator_filter = DecoratorFilter({'testsuite'})

# Filter by minimum method count
method_filter = MethodCountFilter(min_methods=2)

# Check if suite matches
if decorator_filter.matches(suite_info):
    print("Suite has @testsuite decorator")
```

### 4. Main Discovery Service

The primary interface for test suite discovery:

```python
from thanos.discovery.discovery import TestSuiteDiscovery

# Default configuration
discovery = TestSuiteDiscovery()

# Custom configuration
discovery = TestSuiteDiscovery(
    parser=custom_parser,
    discoverer=custom_discoverer,
    filters=[custom_filter1, custom_filter2]
)

# Discover suites
suites = discovery.discover("src/thanos")

# Get summary statistics
summary = discovery.get_summary(suites)
print(f"Total suites: {summary['total']}")
```

## Common Use Cases

### Find All Test Suites

```python
discovery = TestSuiteDiscovery()
suites = discovery.discover("src/thanos")

for suite in suites:
    print(f"Suite: {suite.class_name}")
    print(f"File: {suite.file_path}")
    print(f"Methods: {suite.methods}")
```

### Find Suites by Decorator

```python
# Find only @testsuite decorated classes
testsuite_classes = discovery.discover_by_decorator("src/thanos", "testsuite")

# Find performance test suites
perf_suites = discovery.discover_by_decorator("src/thanos", "performance_suite")
```

### Scan Specific Directories

```python
directories = ["src/thanos/tests", "src/thanos/app/backend"]

for directory in directories:
    suites = discovery.discover(directory)
    print(f"{directory}: {len(suites)} suites")
```

### Custom Pattern Matching

```python
# Find files matching specific patterns
patterns = ["*test*.py", "*suite*.py", "test_*.py"]

for pattern in patterns:
    suites = discovery.discover("src/thanos", pattern)


### Advanced Regex Path Search

```python
# Use regex patterns for complex path matching
discovery = TestSuiteDiscovery()

# Find performance tests in specific directory structure
perf_suites = discovery.discover_with_regex(
    "src/thanos", 
    "ets/*/project*/py3/test/*/performance/*.py"
)

# Find all test files in app backend directories
backend_tests = discovery.discover_with_regex(
    "src/thanos",
    "app/.*/backend/.*test.*\.py$"
)

# Case-insensitive search for test suites
all_tests = discovery.discover_with_regex(
    "src/thanos",
    ".*test.*\.py$",
    case_sensitive=False
)

print(f"Performance suites: {len(perf_suites)}")
print(f"Backend tests: {len(backend_tests)}")
print(f"All tests (case-insensitive): {len(all_tests)}")
```

## Advanced Examples

### Custom Parser Configuration

```python
# Look for multiple decorator types
parser = ASTTestSuiteParser(
    target_decorators={'testsuite', 'integration_test', 'performance_test'}
)

discovery = TestSuiteDiscovery(parser=parser)
```

### Composite Filtering

```python
from thanos.discovery.filters import CompositeFilter

# Combine multiple filters
composite_filter = CompositeFilter([
    DecoratorFilter({'testsuite'}),
    MethodCountFilter(min_methods=1)
])

discovery = TestSuiteDiscovery(filters=[composite_filter])
```

### Custom File Discovery

```python
# Only scan Python files, exclude certain patterns
discoverer = FilteredFileDiscoverer(
    extensions={'.py'},
    exclude_patterns={'__init__.py', '__pycache__', 'venv'}
)



### Advanced Regex File Discovery

```python
from thanos.discovery.discoverers import RegexFileDiscoverer

# Use regex discoverer for complex path patterns
regex_discoverer = RegexFileDiscoverer(case_sensitive=True)
discovery = TestSuiteDiscovery(discoverer=regex_discoverer)

# Complex pattern examples
patterns = [
    "ets/*/project*/py3/test/*/performance/*.py",  # Specific nested structure
    "app/(backend|frontend)/.*/test_.*\.py$",       # Backend or frontend tests
    "tests/.*/(unit|integration)/.*\.py$",          # Unit or integration tests
    ".*/(test_|.*_test)\.py$"                       # Files starting with test_ or ending with _test
]

for pattern in patterns:
    suites = discovery.discover("src/thanos", pattern)
    print(f"Regex pattern '{pattern}': {len(suites)} suites")
```

## Running the Examples

1. **Comprehensive Examples**: Run `python usage_examples.py` for detailed examples
2. **Quick Examples**: Run `python quick_examples.py` for basic usage patterns

## Example Output

```
Found 4 test suites:
  SuiteOne in test_suite_one.py
  SuiteTwo in test_suite_two.py
  BasicSuite in test_suite_basic.py
  PerformanceSuite in test_suite_performance.py

Summary: {
  'total': 4, 
  'files': 4, 
  'decorators': {'testsuite': 4}, 
  'avg_methods_per_suite': 2.5
}
```

## Integration with Test Execution

The discovered test suites can be integrated with test execution frameworks:

```python
# Discover suites
suites = discovery.discover("src/thanos")

# Execute each suite
for suite in suites:
    print(f"Executing {suite.class_name} from {suite.file_path}")
    # Integration with testplan or other test runners
```