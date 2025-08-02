import time
from rich import print as rprint

# --- Test Action Functions ---
def login_to_service(context):
    """Simulates a login action."""
    rprint("[yellow]🔑 Executing login action...[/yellow]")
    time.sleep(0.5)
    # Return a token or session ID
    return {"session_id": "12345-abcde"}
