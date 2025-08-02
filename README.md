# Thanos

A test framework for orchestrating stage workflows

## Description

Thanos is a Python test framework designed to orchestrate complex stage workflows with dependencies. It allows you to define test stages, manage their dependencies, and execute them in the correct order while maintaining context between stages.

## Installation

### Prerequisites

- Python 3.11.9 or higher
- Poetry (for dependency management)

### Install Poetry

If you don't have Poetry installed, install it first:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Install Dependencies

1. Clone the repository and navigate to the project directory:

```bash
cd Thanos
```

1. Install the project dependencies using Poetry:

```bash
poetry install
```

This will create a virtual environment and install all dependencies specified in `pyproject.toml`:

- polars (>=1.32.0,<2.0.0)
- click (>=8.2.2,<9.0.0)
- pydantic (>=2.11.7,<3.0.0)
- rich (>=14.1.0,<15.0.0)

## Usage

### Activate the Poetry Environment

```bash
poetry shell
```

### Run the Test Workflow

Execute the main test plan:

```bash
python src/thanos/test_runner.py
```

Or using Poetry:

```bash
poetry run python src/thanos/test_runner.py
```

### Run Test Plan with TestPlan Framework

Execute the comprehensive test plan that includes both basic and performance tests:

```bash
poetry run python src/thanos/test_plan.py
```

**Example Output:**
```
Running Testplan[StageWorkflow Test Plan]

Testplan[StageWorkflow Test Plan] has runpath: /var/tmp/racheldaloia/testplan/stageworkflow-test-plan and pid 36014

Running MultiTest[StageWorkflow Tests]

Setting up BasicSuite...

      [BasicMultiplyTest <numA=2, numB=3, product=6>] -> Passed
      [BasicMultiplyTest <numA=4, numB=5, product=20>] -> Passed
    [BasicSuite] -> Passed
  [StageWorkflow Tests] -> Passed

Running MultiTest[Performance Tests]

Setting up Performance Test Suite: PerformanceTestSuite

🚀 === THANOS TEST FRAMEWORK ===

--- Starting Test Run ---

📋 Execution order: ['login_to_service', 'create_user', 'check_user_profile', 'cleanup_data']

🚀 Running stage: login_to_service
🔑 Executing login action...
✅ Stage 'login_to_service' PASSED.

🚀 Running stage: create_user
👤 Executing create user action with session: 12345-abcde
✅ Stage 'create_user' PASSED.

🚀 Running stage: check_user_profile
🔍 Executing check profile action for user: test_user_1
✅ Stage 'check_user_profile' PASSED.

🚀 Running stage: cleanup_data
🧹 Cleaning up data for user: test_user_1
✅ Stage 'cleanup_data' PASSED.

🎉 --- Test Run Complete ---

📊 === TEST SUMMARY ===
  ✅ Stage: login_to_service     Status: PASSED
  ✅ Stage: create_user          Status: PASSED
  ✅ Stage: check_user_profile   Status: PASSED
  ✅ Stage: cleanup_data         Status: PASSED

PDF generated at /Users/racheldaloia/sandbox/Thanos/src/thanos/report.pdf
```

### Run Individual Test Suites

The test plan includes two main test suites:

#### Basic Test Suite
Contains basic functionality tests including mathematical operations:
- Located in: `src/thanos/tests/test_suite_basic.py`
- Tests basic multiply function with parameterized inputs
- Tags: `["math", "basic"]`

#### Performance Test Suite
Contains workflow performance tests that execute the full stage pipeline:
- Located in: `src/thanos/tests/test_suite_performance.py`
- Tests the complete workflow: login → create user → check profile → cleanup
- Tags: `["performance", "workflow"]`
- Demonstrates stage dependencies and context passing

**Test Suite Features:**
- **Parameterized Testing**: Both suites support multiple parameter combinations
- **Rich Output**: Colorized console output with emojis for better readability
- **PDF Reports**: Automatic generation of detailed PDF test reports
- **Stage Dependencies**: Performance suite demonstrates proper stage ordering
- **Context Sharing**: Shows how data flows between dependent stages

## Project Structure

```text
Thanos/
├── src/
│   └── thanos/
│       ├── stages/          # Individual test stages
│       │   ├── cleanup.py   # Cleanup operations
│       │   ├── login.py     # Login functionality
│       │   └── user.py      # User management
│       ├── __init__.py
│       ├── _version.py      # Version information
│       ├── stage.py         # Stage definition and management
│       ├── test_runner.py   # Main test execution runner
│       └── workflow.py      # Workflow runner and orchestration
├── .gitignore
├── LICENSE
├── poetry.lock             # Locked dependency versions
├── pyproject.toml          # Project configuration and dependencies
└── README.md
```

## Development

### Creating New Stage Files

Stages are the core building blocks of the Thanos framework. Each stage represents a discrete test action that can depend on other stages.

#### Step 1: Create a Stage File

Create a new Python file in the `src/thanos/stages/` directory:

```python
# src/thanos/stages/my_new_stage.py
import time
from rich import print as rprint

def my_action(context):
    """Description of what this stage does."""
    rprint("[cyan]🔧 Executing my custom action...[/cyan]")
    time.sleep(0.5)
    
    # Access data from dependent stages
    # session_id = context['login_to_service']['session_id']
    
    # Your stage logic here
    result = {"custom_data": "example_value"}
    return result
```

#### Step 2: Import and Use in Test Suite

Add your stage to a test suite (e.g., `src/thanos/tests/test_suite_performance.py`):

```python
from thanos.stages.my_new_stage import my_action

# In your test method:
stage_custom = TestStage(
    name="my_custom_stage",
    action=my_action,
    dependencies=["login_to_service"]  # List dependent stages
)

self.runner.add_stage(stage_custom)
```

### Setting Stage Dependencies

Dependencies ensure stages execute in the correct order and have access to required data.

#### Dependency Rules

1. **No Dependencies**: `dependencies=[]`
2. **Single Dependency**: `dependencies=["stage_name"]`
3. **Multiple Dependencies**: `dependencies=["stage1", "stage2"]`
4. **Context Access**: Use `context['dependency_stage_name']['key']`

#### Example Dependency Chain

```python
# Stage 1: No dependencies
stage_init = TestStage(
    name="initialize",
    action=initialize_system,
    dependencies=[]
)

# Stage 2: Depends on initialize
stage_login = TestStage(
    name="login",
    action=login_to_service,
    dependencies=["initialize"]
)

# Stage 3: Depends on login
stage_user = TestStage(
    name="create_user",
    action=create_user,
    dependencies=["login"]
)

# Stage 4: Depends on both login and create_user
stage_verify = TestStage(
    name="verify_user",
    action=verify_user_creation,
    dependencies=["login", "create_user"]
)
```

#### Context Data Flow

Data flows between stages through the `context` parameter:

```python
def dependent_action(context):
    # Access data from 'login_to_service' stage
    session = context['login_to_service']['session_id']
    
    # Access data from 'create_user' stage
    user_id = context['create_user']['user_id']
    
    # Use the data in your logic
    result = process_user(session, user_id)
    return result
```

### Adding New Dependencies

To add new dependencies to the project:

```bash
poetry add <package-name>
```

For development dependencies:

```bash
poetry add --group dev <package-name>
```

### Running Tests

Currently, the main test workflow can be executed with:

```bash
poetry run python src/thanos/test_runner.py
```

### Building the Project

To build the project for distribution:

```bash
poetry build
```

## Configuration

The project configuration is managed through `pyproject.toml`. Key configurations include:

- **Project metadata**: name, version, description, authors
- **Python version requirement**: >=3.11.9
- **Dependencies**: Core packages required for the framework
- **Build system**: Uses poetry-core for building

## Contributing

1. Ensure you have Poetry installed
2. Clone the repository
3. Run `poetry install` to set up the development environment
4. Make your changes
5. Test your changes by running the test workflow
6. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Author

donzeno23 ([donzeno23@yahoo.com](mailto:donzeno23@yahoo.com))