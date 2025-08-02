from thanos.stage import TestStage
from thanos.workflow import WorkflowRunner
from rich import print as rprint

from thanos.stages.login import login_to_service
from thanos.stages.user import create_user, check_user_profile
from thanos.stages.cleanup import cleanup_data

# --- Main Test Scenario ---
if __name__ == "__main__":
    runner = WorkflowRunner()

    # Define the stages and their dependencies
    stage_login = TestStage(
        name="login_to_service",
        action=login_to_service,
        dependencies=[]
    )

    stage_create = TestStage(
        name="create_user",
        action=create_user,
        dependencies=["login_to_service"]
    )

    stage_check = TestStage(
        name="check_user_profile",
        action=check_user_profile,
        dependencies=["create_user"]
    )

    stage_cleanup = TestStage(
        name="cleanup_data",
        action=cleanup_data,
        dependencies=["create_user"] # Can be dependent on create_user to know which user to delete
    )

    # Add stages to the runner
    runner.add_stage(stage_login)
    runner.add_stage(stage_create)
    runner.add_stage(stage_check)
    runner.add_stage(stage_cleanup)

    # Run the tests
    runner.execute_workflow()
    
    # Enhanced final reporting
    rprint("\n[bold cyan]📊 === FINAL RESULTS ===[/bold cyan]")
    rprint(f"[bold green]🎆 Test run completed successfully![/bold green]")
    
    rprint("\n[bold yellow]📝 Final context:[/bold yellow]")
    rprint(f"[dim]{runner.context}[/dim]")
    
    rprint("\n[bold magenta]📈 Stage results:[/bold magenta]")
    for stage_name, stage in runner.stages.items():
        status_icon = "✅" if stage.status == "PASSED" else "❌" if stage.status == "FAILED" else "⏭️"
        status_color = "green" if stage.status == "PASSED" else "red" if stage.status == "FAILED" else "yellow"
        rprint(f"  {status_icon} [cyan]{stage_name}[/cyan]: [{status_color}]{stage.status}[/{status_color}] [dim](Result: {stage.result})[/dim]")
    
    rprint("\n[bold cyan]========================[/bold cyan]\n")
        
