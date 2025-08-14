import sys
import click
import questionary
from rich.console import Console
from rich.panel import Panel

from thanos.cli.runner import TestRunner

console = Console()

@click.group()
@click.version_option()
def main():
    """Thanos - A test framework for orchestrating stage workflows"""
    pass

@main.group()
def perf():
    """Performance testing commands"""
    pass

@main.group() 
def performance():
    """Performance testing commands (alias for perf)"""
    pass

@main.group()
def basic():
    """Basic testing commands"""
    pass

@perf.command()
@click.option('--engine', '-e', help='Engine type to use')
@click.option('--interactive/--no-interactive', '-i/-n', default=True, help='Interactive mode')
def run(engine, interactive):
    """Run performance tests"""
    console.print(Panel.fit("🚀 Thanos Performance Test Runner", style="bold blue"))
    
    if interactive:
        engine = _prompt_for_engine() if not engine else engine
    
    runner = TestRunner()
    runner.run_performance_tests(engine)

@performance.command()
@click.option('--engine', '-e', help='Engine type to use')
@click.option('--interactive/--no-interactive', '-i/-n', default=True, help='Interactive mode')
def run_perf(engine, interactive):
    """Run performance tests"""
    console.print(Panel.fit("🚀 Thanos Performance Test Runner", style="bold blue"))
    
    if interactive:
        engine = _prompt_for_engine() if not engine else engine
    
    runner = TestRunner()
    runner.run_performance_tests(engine)

@basic.command()
@click.option('--engine', '-e', help='Engine type to use') 
@click.option('--interactive/--no-interactive', '-i/-n', default=True, help='Interactive mode')
def run_basic(engine, interactive):
    """Run basic tests"""
    console.print(Panel.fit("🧪 Thanos Basic Test Runner", style="bold green"))
    
    if interactive:
        engine = _prompt_for_engine() if not engine else engine
    
    runner = TestRunner()
    runner.run_basic_tests(engine)

def _prompt_for_engine():
    """Interactive prompt for engine selection"""
    engines = ["eu.app_one", "us.app_two", "asia.app_three"]
    
    engine = questionary.select(
        "Select test engine:",
        choices=engines,
        default="eu.app_one"
    ).ask()
    
    return engine

if __name__ == '__main__':
    sys.exit(main())