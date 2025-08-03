# test_framework/runner.py

import uuid

from datetime import datetime
from typing import Dict, Any, List
from graphlib import TopologicalSorter
from thanos.stage import TestStage
from thanos.cache import TestCache, StageResult, TestRunResult
from rich import print as rprint


class WorkflowRunner:
    def __init__(self, cache: TestCache):
        self.stages: Dict[str, TestStage] = {}
        self.dag: Dict[str, List[str]] = {}
        self.context: Dict[str, Any] = {}
        self.cache = cache

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

        run_id = str(uuid.uuid4())
        overall_status = "PASSED"
        test_run_result = TestRunResult(
            run_id=run_id,
            timestamp=datetime.now(),
            overall_status="IN_PROGRESS"
        )        
        try:
            # Use Python's built-in TopologicalSorter
            sorter = TopologicalSorter(self.dag)
            sorted_stages = list(sorter.static_order())
            
            rprint(f"[bold blue]📋 Execution order:[/bold blue] [cyan]{sorted_stages}[/cyan]")

            for stage_name in sorted_stages:
                stage = self.stages[stage_name]
                start_time = datetime.now()
                
                # Check for failed dependencies
                # In a real-world scenario, you might add more sophisticated dependency checks
                # here. For simplicity, we just check if any dependent stage failed.
                is_dependency_failed = False
                for dep_name in stage.dependencies:
                    if self.stages[dep_name].status == "FAILED":
                        rprint(f"[yellow]⚠️  Stage '{stage.name}' skipped due to failed dependency: '{dep_name}'.[/yellow]")
                        stage.status = "SKIPPED"
                        is_dependency_failed = True
                        break
                
                if is_dependency_failed:
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds() * 1000
                    stage_result = StageResult(
                        name=stage.name,
                        status="SKIPPED",
                        result_data=None,
                        start_time=start_time,
                        end_time=end_time,
                        duration_ms=duration
                    )
                    test_run_result.stage_results.append(stage_result)
                    continue

                if stage.status != "SKIPPED":
                    try:
                        stage.run(self.context)
                        # Store the result in the global context if needed for other stages
                        self.context[stage.name] = stage.result
                    except Exception:
                        rprint(f"[bold red]❌ Test run aborted due to failure in stage: {stage.name}[/bold red]")
                        overall_status = "FAILED"
                        # Capture the result of the failed stage
                        stage.status = "FAILED"
                        stage.result = self.stages[stage_name].result
                        self._report_summary()
                        return
                    
                    # Record the result of the executed stage
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds() * 1000
                    stage_result = StageResult(
                        name=stage.name,
                        status=stage.status,
                        result_data=stage.result,
                        start_time=start_time,
                        end_time=end_time,
                        duration_ms=duration
                    )
                    test_run_result.stage_results.append(stage_result)
                
                    # If the stage failed, we break the loop and prevent further execution
                    if stage.status == "FAILED":
                        break
            
        except Exception as e:
            rprint(f"[bold red]💥 Error during test setup or execution: {e}[/bold red]")
            overall_status = "ERROR"

        # Update final status and store in cache
        test_run_result.overall_status = overall_status
        self.cache.add_run_result(test_run_result)
        
        rprint("\n[bold green]🎉 --- Test Run Complete ---[/bold green]")
        self._report_summary()
        return run_id
    

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


    def upload_to_db(self):
        """Simulates uploading all cached results to a database."""
        print("\n--- Uploading Results to DB ---")
        cached_results = self.cache.get_all_results()
        if not cached_results:
            print("No results to upload.")
            return

        for run_result in cached_results:
            # Here, you would implement the actual database interaction code
            # e.g., using SQLAlchemy, Django ORM, or a simple `requests` call
            # to a backend API.
            print(f"  Uploading run_id: {run_result.run_id} (Status: {run_result.overall_status})")
            
            # For demonstration, we'll just print the data
            # print(f"    Data: {run_result}")
            # Simulate a successful upload
            print("  ...Upload successful.")

        print("--- Upload Complete ---")
        # Optional: Clear the cache after a successful upload
        # self.cache.clear()
        rprint("\n[bold green]✅ All results uploaded successfully![/bold green]")
