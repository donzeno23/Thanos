from rich import print as rprint


def report_workflow_results(runner):
    """Helper function to generate enhanced final reporting for workflow results."""
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