import time
from rich import print as rprint

def cleanup_data(context):
    """Cleanup action, can be run at the end."""
    rprint(f"[magenta]🧹 Cleaning up data for user: [bold]{context['create_user']['user_id']}[/bold][/magenta]")
    time.sleep(0.5)
    return "Cleanup successful."
