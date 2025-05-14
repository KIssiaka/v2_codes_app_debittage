def execute_command(command):
    if command == "list":
        return list_commands()
    else:
        return f"Unknown command: {command}"

def list_commands():
    return [
        "optimize_memory - Optimize memory usage",
        "clean_disk - Clean up disk space",
        "manage_startup - Manage startup applications",
        "apply_tweaks - Apply system tweaks",
        "reset_tweaks - Reset system tweaks"
    ]