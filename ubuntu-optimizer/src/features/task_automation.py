import os
import json
import time
import threading
import schedule
import psutil

class TaskAutomation:
    def __init__(self):
        self.tasks_dir = os.path.expanduser("~/.config/ubuntu-optimizer/tasks")
        os.makedirs(self.tasks_dir, exist_ok=True)
        self.tasks_file = os.path.join(self.tasks_dir, "tasks.json")
        self.running_tasks = {}
        
        # Initialize tasks file if it doesn't exist
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w') as f:
                json.dump({}, f)
        
        # Load existing tasks at startup
        self._load_and_schedule_tasks()
    
    def create_task(self, name, command, schedule_time, condition=None):
        """
        Create a new automated task
        
        Parameters:
        - name: Task name
        - command: Command to execute
        - schedule_time: When to run (e.g. "daily at 10:00", "every 2 hours")
        - condition: Optional condition function (as string) that should return True to run
        """
        tasks = self._load_tasks()
        
        # Add new task
        tasks[name] = {
            "command": command,
            "schedule": schedule_time,
            "condition": condition,
            "enabled": True,
            "last_run": None
        }
        
        # Save tasks
        self._save_tasks(tasks)
        
        # Schedule the new task
        self._schedule_task(name, tasks[name])
        
        return f"Task '{name}' created with schedule '{schedule_time}'"
    
    def list_tasks(self):
        """List all registered tasks"""
        tasks = self._load_tasks()
        if not tasks:
            return "No tasks found"
            
        result = "Registered tasks:\n"
        for name, details in tasks.items():
            status = "enabled" if details.get("enabled", True) else "disabled"
            last_run = details.get("last_run", "never")
            result += f"- {name}: {details['command']} ({details['schedule']}) - {status}, last run: {last_run}\n"
            
        return result
    
    def remove_task(self, name):
        """Remove an automated task"""
        tasks = self._load_tasks()
        
        if name not in tasks:
            return f"Task '{name}' not found"
            
        # Stop task if it's scheduled
        if name in self.running_tasks:
            schedule.cancel_job(self.running_tasks[name])
            del self.running_tasks[name]
            
        # Remove from our json file
        del tasks[name]
        self._save_tasks(tasks)
        
        return f"Task '{name}' removed successfully"
    
    def enable_task(self, name, enable=True):
        """Enable or disable a task"""
        tasks = self._load_tasks()
        
        if name not in tasks:
            return f"Task '{name}' not found"
            
        tasks[name]["enabled"] = enable
        self._save_tasks(tasks)
        
        if enable:
            # Schedule the task
            self._schedule_task(name, tasks[name])
            return f"Task '{name}' enabled"
        else:
            # Cancel the job if it's running
            if name in self.running_tasks:
                schedule.cancel_job(self.running_tasks[name])
                del self.running_tasks[name]
            return f"Task '{name}' disabled"
    
    def _load_tasks(self):
        """Load tasks from file"""
        try:
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        except:
            return {}
            
    def _save_tasks(self, tasks):
        """Save tasks to file"""
        with open(self.tasks_file, 'w') as f:
            json.dump(tasks, f, indent=2)
    
    def _load_and_schedule_tasks(self):
        """Load tasks from file and schedule them"""
        tasks = self._load_tasks()
        
        for name, task in tasks.items():
            if task.get("enabled", True):
                self._schedule_task(name, task)
    
    def _schedule_task(self, name, task):
        """Schedule a task using the schedule library"""
        schedule_str = task["schedule"]
        command = task["command"]
        condition = task.get("condition")
        
        def job():
            should_run = True
            
            # Check condition if provided
            if condition:
                try:
                    # This is potentially dangerous - evaluating a string as code
                    # In a real implementation, use a safer approach
                    should_run = eval(condition)
                except:
                    print(f"Error evaluating condition for task {name}")
            
            if should_run:
                try:
                    os.system(command)
                    tasks = self._load_tasks()
                    if name in tasks:
                        tasks[name]["last_run"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        self._save_tasks(tasks)
                except Exception as e:
                    print(f"Error running task {name}: {str(e)}")
        
        # Parse the schedule string and set up the job
        schedule_parts = schedule_str.split()
        
        if schedule_str.startswith("every"):
            interval = int(schedule_parts[1])
            unit = schedule_parts[2]
            
            if unit.startswith("minute"):
                self.running_tasks[name] = schedule.every(interval).minutes.do(job)
            elif unit.startswith("hour"):
                self.running_tasks[name] = schedule.every(interval).hours.do(job)
            elif unit.startswith("day"):
                self.running_tasks[name] = schedule.every(interval).days.do(job)
        elif "at" in schedule_str:
            time_str = schedule_parts[-1]
            
            if "daily" in schedule_str:
                self.running_tasks[name] = schedule.every().day.at(time_str).do(job)
            elif "monday" in schedule_str:
                self.running_tasks[name] = schedule.every().monday.at(time_str).do(job)
            elif "tuesday" in schedule_str:
                self.running_tasks[name] = schedule.every().tuesday.at(time_str).do(job)
            elif "wednesday" in schedule_str:
                self.running_tasks[name] = schedule.every().wednesday.at(time_str).do(job)
            elif "thursday" in schedule_str:
                self.running_tasks[name] = schedule.every().thursday.at(time_str).do(job)
            elif "friday" in schedule_str:
                self.running_tasks[name] = schedule.every().friday.at(time_str).do(job)
            elif "saturday" in schedule_str:
                self.running_tasks[name] = schedule.every().saturday.at(time_str).do(job)
            elif "sunday" in schedule_str:
                self.running_tasks[name] = schedule.every().sunday.at(time_str).do(job)
        
        # Start the scheduler in a background thread if not already running
        if not hasattr(self, '_scheduler_running') or not self._scheduler_running:
            self._scheduler_running = True
            
            def run_scheduler():
                while self._scheduler_running:
                    schedule.run_pending()
                    time.sleep(1)
            
            thread = threading.Thread(target=run_scheduler, daemon=True)
            thread.start()

    def create_cpu_optimization_task(self, threshold=80, name="auto_cpu_optimizer"):
        """Create a task that automatically optimizes when CPU usage is too high"""
        condition = f"psutil.cpu_percent() > {threshold}"
        command = "killall -STOP $(ps aux | sort -nrk 3,3 | grep -v PID | head -n 5 | awk '{print $2}')"
        
        return self.create_task(
            name=name,
            command=command,
            schedule_time="every 5 minutes",
            condition=condition
        )