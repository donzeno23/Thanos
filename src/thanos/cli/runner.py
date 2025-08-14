import sys
import os
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from testplan import test_plan, Testplan
from testplan.testing.multitest import MultiTest
from testplan.report.testing.styles import Style

console = Console()

class TestRunner:
    """Test runner for executing different test types"""
    
    def __init__(self):
        self.console = console
    
    def run_performance_tests(self, engine: Optional[str] = None):
        """Run performance tests with optional engine selection"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Loading performance tests...", total=None)
            
            # Import test suites
            from thanos.tests.test_suite_performance import PerformanceTestSuite
            from thanos.engine.eu.app_one.test_suite_one import PerfTestSuite
            
            progress.update(task, description="Executing performance tests...")
            
            # Create and run test plan
            self._run_test_plan(
                name="Performance Test Plan",
                suites=[
                    PerformanceTestSuite(name='PerformanceTestSuite'),
                    PerfTestSuite(name='PerfTestSuite')
                ],
                engine=engine
            )
    
    def run_basic_tests(self, engine: Optional[str] = None):
        """Run basic tests with optional engine selection"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Loading basic tests...", total=None)
            
            # Import test suites
            from thanos.tests.test_suite_basic import BasicSuite
            
            progress.update(task, description="Executing basic tests...")
            
            # Create and run test plan
            self._run_test_plan(
                name="Basic Test Plan",
                suites=[BasicSuite(name='BasicSuite')],
                engine=engine
            )
    
    def _run_test_plan(self, name: str, suites: list, engine: Optional[str] = None):
        """Execute test plan with given suites"""
        
        @test_plan(
            name=name,
            stdout_style=Style(passing="testcase", failing="assertion-detail"),
            pdf_path=os.path.join(os.path.dirname(__file__), f"{name.lower().replace(' ', '_')}_report.pdf"),
            pdf_style=Style(passing="testcase", failing="assertion-detail"),
        )
        def plan(testplan: Testplan):
            test = MultiTest(
                name=f'{name} - {engine or "default"}',
                suites=suites
            )
            testplan.add(test)
        
        console.print(f"\n[bold green]Starting {name}[/bold green]")
        if engine:
            console.print(f"[dim]Engine: {engine}[/dim]")
        
        try:
            result = plan()
            if result:
                console.print(Panel.fit("✅ Tests completed successfully!", style="bold green"))
            else:
                console.print(Panel.fit("❌ Tests failed!", style="bold red"))
                sys.exit(1)
        except Exception as e:
            console.print(Panel.fit(f"💥 Error running tests: {str(e)}", style="bold red"))
            sys.exit(1)