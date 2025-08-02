import time
from rich import print as rprint

def create_user(context):
    """Simulates creating a new user, requires a session."""
    rprint(f"[green]👤 Executing create user action with session: [bold]{context['login_to_service']['session_id']}[/bold][/green]")
    time.sleep(1)
    # Simulate a failure if the session is invalid
    if not context['login_to_service']['session_id']:
        raise ValueError("Invalid session ID.")
    # Return user details
    return {"user_id": "test_user_1", "username": "test_user"}

def check_user_profile(context):
    """Simulates checking a user profile, requires a user to exist."""
    rprint(f"[blue]🔍 Executing check profile action for user: [bold]{context['create_user']['user_id']}[/bold][/blue]")
    time.sleep(0.5)
    # Assert some condition
    assert context['create_user']['username'] == "test_user"
    return "Profile check successful."
