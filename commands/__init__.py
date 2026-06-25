from commands.system import execute_system_command
from commands.git_helpers import execute_git_command
from commands.developer import execute_developer_command
from commands.general import execute_general_command

def execute_command(text: str) -> str | None:
    """
    Modular execution router. Parses transcribed text and forwards it sequentially 
    through system, git, developer, and general command engines.
    Returns the spoken feedback response, or None if no command matches (routing it to LLM).
    """
    clean_text = text.strip().lower()

    # 1. Check System and Hardware Commands
    response = execute_system_command(clean_text)
    if response is not None:
        return response

    # 2. Check Git Integrations
    response = execute_git_command(clean_text)
    if response is not None:
        return response

    # 3. Check Developer Utilities
    response = execute_developer_command(clean_text)
    if response is not None:
        return response

    # 4. Check General/Personal Assistant Helpers
    response = execute_general_command(clean_text, text)
    if response is not None:
        return response

    return None
