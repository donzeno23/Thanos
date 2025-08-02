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
- rprint (>=0.0.8,<0.0.9)

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