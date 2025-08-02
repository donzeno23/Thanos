# test_framework/runner.py

from typing import Dict, Any, List
from graphlib import TopologicalSorter
from thanos.stage import TestStage
from rich import print as rprint

class WorkflowRunner:
    def __init__(self):
        self.stages: Dict[str, TestStage] = {}
        self.dag: Dict[str, List[str]] = {}
        self.context: Dict[str, Any] = {}

    def add_stage(self, stage: TestStage):
        """Adds a stage to the runner and builds the dependency graph."""
        if stage.name in self.stages:
            raise ValueError(f"Stage with name '{stage.name}' already exists.")
        
        self.stages[stage.name] = stage
        self.dag[stage.name] = stage.dependencies

    def execute_workflow(self):
        """
        Executes all test stages in a topologically sorted order.
        """
        rprint("\n[bold cyan]🚀 === THANOS TEST FRAMEWORK ===[/bold cyan]")
        rprint("[bold yellow]--- Starting Test Run ---[/bold yellow]\n")
        try:
            # Use Python's built-in TopologicalSorter
            sorter = TopologicalSorter(self.dag)
            sorted_stages = list(sorter.static_order())
            
            rprint(f"[bold blue]📋 Execution order:[/bold blue] [cyan]{sorted_stages}[/cyan]")

            for stage_name in sorted_stages:
                stage = self.stages[stage_name]
                
                # Check for failed dependencies
                # In a real-world scenario, you might add more sophisticated dependency checks
                # here. For simplicity, we just check if any dependent stage failed.
                for dep_name in stage.dependencies:
                    if self.stages[dep_name].status == "FAILED":
                        rprint(f"[yellow]⚠️  Stage '{stage.name}' skipped due to failed dependency: '{dep_name}'.[/yellow]")
                        stage.status = "SKIPPED"
                        break
                
                if stage.status != "SKIPPED":
                    try:
                        stage.run(self.context)
                        # Store the result in the global context if needed for other stages
                        self.context[stage.name] = stage.result
                    except Exception:
                        rprint(f"[bold red]❌ Test run aborted due to failure in stage: {stage.name}[/bold red]")
                        self._report_summary()
                        return
                        
        except Exception as e:
            rprint(f"[bold red]💥 Error during test setup or execution: {e}[/bold red]")
        
        rprint("\n[bold green]🎉 --- Test Run Complete ---[/bold green]")
        self._report_summary()

    def _report_summary(self):
        """Prints a summary of the test results."""
        rprint("\n[bold magenta]📊 === TEST SUMMARY ===[/bold magenta]")
        for stage_name, stage in self.stages.items():
            status_icon = "✅" if stage.status == "PASSED" else "❌" if stage.status == "FAILED" else "⏭️"
            status_color = "green" if stage.status == "PASSED" else "red" if stage.status == "FAILED" else "yellow"
            rprint(f"  {status_icon} [bold]Stage:[/bold] [cyan]{stage_name:<20}[/cyan] [bold]Status:[/bold] [{status_color}]{stage.status:<10}[/{status_color}]")
            if stage.status == "FAILED":
                rprint(f"    [red]💀 Error: {stage.result}[/red]")
        rprint("[bold magenta]========================[/bold magenta]")
