# thanos/stage.py

from dataclasses import dataclass
from typing import Any, Callable, Dict
from rich import print as rprint

@dataclass
class TestStage:
    name: str
    action: Callable[..., Any]
    dependencies: list[str]
    result: Any = None
    status: str = "PENDING"
    
    def run(self, context: Dict[str, Any]):
        """
        Executes the action of the test stage and updates its status and result.
        """
        rprint(f"\n[bold blue]🚀 Running stage:[/bold blue] [bold cyan]{self.name}[/bold cyan]")
        try:
            self.result = self.action(context)
            self.status = "PASSED"
            rprint(f"[bold green]✅ Stage '{self.name}' PASSED.[/bold green]")
        except Exception as e:
            self.result = str(e)
            self.status = "FAILED"
            rprint(f"[bold red]❌ Stage '{self.name}' FAILED: {e}[/bold red]")
            raise  # Re-raise to stop further dependent stages
