# This file serves as the entry point for the application. It initializes the application and handles command-line arguments.

import sys
from features.memory_optimization import MemoryOptimizer
from features.disk_cleanup import DiskCleaner
from features.startup_manager import StartupManager
from features.system_tweaks import SystemTweaks
from features.custom_shortcuts import ShortcutManager
from features.task_automation import TaskAutomation
from features.service_optimizer import ServiceOptimizer

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [arguments]")
        print("\nAvailable commands:")
        print("  optimize_memory               - Optimize memory usage")
        print("  clean_disk                    - Clean up disk space")
        print("  manage_startup                - Manage startup applications")
        print("  apply_tweaks                  - Apply system tweaks")
        print("  create_shortcut <name> <cmd> <keys> - Create keyboard shortcut")
        print("  list_shortcuts                - List all keyboard shortcuts")
        print("  remove_shortcut <name>        - Remove keyboard shortcut")
        print("  create_task <name> <cmd> <schedule> - Create automated task")
        print("  list_tasks                    - List all automated tasks")
        print("  remove_task <name>            - Remove automated task")
        print("  list_services                 - List all system services")
        print("  optimize_service <name>       - Optimize specific service")
        print("  auto_optimize_services        - Optimize all monitored services")
        print("  disable_service <name>        - Add service to disable list")
        return

    command = sys.argv[1]

    if command == "optimize_memory":
        optimizer = MemoryOptimizer()
        optimizer.optimize_memory()
    elif command == "clean_disk":
        cleaner = DiskCleaner()
        cleaner.clean_disk()
    elif command == "manage_startup":
        manager = StartupManager()
        manager.manage_startup_apps()
    elif command == "apply_tweaks":
        tweaks = SystemTweaks()
        tweaks.apply_tweaks()
    # Keyboard Shortcuts commands
    elif command == "create_shortcut":
        if len(sys.argv) < 5:
            print("Usage: python main.py create_shortcut <name> <command> <key_combo>")
            return
        shortcut_mgr = ShortcutManager()
        result = shortcut_mgr.create_shortcut(sys.argv[2], sys.argv[3], sys.argv[4])
        print(result)
    elif command == "list_shortcuts":
        shortcut_mgr = ShortcutManager()
        print(shortcut_mgr.list_shortcuts())
    elif command == "remove_shortcut":
        if len(sys.argv) < 3:
            print("Usage: python main.py remove_shortcut <name>")
            return
        shortcut_mgr = ShortcutManager()
        result = shortcut_mgr.remove_shortcut(sys.argv[2])
        print(result)
    # Task Automation commands
    elif command == "create_task":
        if len(sys.argv) < 5:
            print("Usage: python main.py create_task <name> <command> <schedule>")
            return
        task_auto = TaskAutomation()
        result = task_auto.create_task(sys.argv[2], sys.argv[3], sys.argv[4])
        print(result)
    elif command == "list_tasks":
        task_auto = TaskAutomation()
        print(task_auto.list_tasks())
    elif command == "remove_task":
        if len(sys.argv) < 3:
            print("Usage: python main.py remove_task <name>")
            return
        task_auto = TaskAutomation()
        result = task_auto.remove_task(sys.argv[2])
        print(result)
    # Service Optimizer commands
    elif command == "list_services":
        service_opt = ServiceOptimizer()
        print(service_opt.list_all_services())
    elif command == "optimize_service":
        if len(sys.argv) < 3:
            print("Usage: python main.py optimize_service <service_name>")
            return
        service_opt = ServiceOptimizer()
        result = service_opt.optimize_service(sys.argv[2])
        print(result)
    elif command == "auto_optimize_services":
        service_opt = ServiceOptimizer()
        result = service_opt.auto_optimize_services()
        print(result)
    elif command == "disable_service":
        if len(sys.argv) < 3:
            print("Usage: python main.py disable_service <service_name>")
            return
        service_opt = ServiceOptimizer()
        result = service_opt.add_service_to_disable(sys.argv[2])
        print(result)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()