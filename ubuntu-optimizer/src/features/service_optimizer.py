import os
import subprocess
import json
import psutil

class ServiceOptimizer:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/ubuntu-optimizer/services")
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, "services.json")
        
        # Initialize config file if it doesn't exist
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                json.dump({
                    "monitored_services": [],
                    "auto_restart": True,
                    "services_to_disable": []
                }, f)
    
    def list_all_services(self):
        """List all system services"""
        try:
            output = subprocess.check_output(["systemctl", "list-units", "--type=service", "--all"], 
                                           universal_newlines=True)
            return output
        except subprocess.CalledProcessError:
            return "Failed to list services"
    
    def optimize_service(self, service_name):
        """Optimize a specific service"""
        try:
            # Check if service exists
            status = subprocess.run(["systemctl", "status", service_name], 
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
            if status.returncode != 0 and status.returncode != 3:  # 3 means inactive service
                return f"Service '{service_name}' not found"
            
            # Get current memory and CPU usage
            before_stats = self._get_service_stats(service_name)
            if not before_stats:
                return f"Failed to get statistics for service '{service_name}'"
            
            # Apply optimization based on the service
            # This is where you'd implement custom optimizations per service type
            # For now, we'll just try some common optimizations:
            
            # 1. Try to reduce service priority (nice)
            try:
                pids = self._get_service_pids(service_name)
                for pid in pids:
                    subprocess.run(["renice", "+10", str(pid)], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
            except:
                pass
            
            # 2. Restart service to free memory
            subprocess.run(["systemctl", "restart", service_name], 
                         stdout=subprocess.DEVNULL)
            
            # Get stats after optimization
            after_stats = self._get_service_stats(service_name)
            
            # Add to monitored services
            config = self._load_config()
            if service_name not in config["monitored_services"]:
                config["monitored_services"].append(service_name)
                self._save_config(config)
            
            # Return result
            if before_stats and after_stats:
                memory_change = before_stats["memory"] - after_stats["memory"]
                cpu_change = before_stats["cpu"] - after_stats["cpu"]
                
                return (f"Service '{service_name}' optimized.\n"
                        f"Memory usage: {before_stats['memory']:.1f}MB -> {after_stats['memory']:.1f}MB "
                        f"({memory_change:.1f}MB {'saved' if memory_change >= 0 else 'increased'})\n"
                        f"CPU usage: {before_stats['cpu']:.1f}% -> {after_stats['cpu']:.1f}% "
                        f"({cpu_change:.1f}% {'reduced' if cpu_change >= 0 else 'increased'})")
            else:
                return f"Service '{service_name}' optimized, but couldn't measure impact"
        except Exception as e:
            return f"Error optimizing service: {str(e)}"
    
    def auto_optimize_services(self):
        """Automatically optimize all monitored services"""
        config = self._load_config()
        results = []
        
        for service in config["monitored_services"]:
            result = self.optimize_service(service)
            results.append(result)
        
        return "\n".join(results)
    
    def disable_unwanted_services(self):
        """Disable services configured as unwanted"""
        config = self._load_config()
        results = []
        
        for service in config["services_to_disable"]:
            try:
                subprocess.run(["systemctl", "stop", service], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
                subprocess.run(["systemctl", "disable", service], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
                results.append(f"Disabled service: {service}")
            except:
                results.append(f"Failed to disable service: {service}")
        
        return "\n".join(results)
    
    def add_service_to_disable(self, service_name):
        """Add a service to the disable list"""
        config = self._load_config()
        
        if service_name not in config["services_to_disable"]:
            config["services_to_disable"].append(service_name)
            self._save_config(config)
            return f"Added '{service_name}' to services to disable"
        else:
            return f"Service '{service_name}' is already in the disable list"
    
    def remove_service_from_disable(self, service_name):
        """Remove a service from the disable list"""
        config = self._load_config()
        
        if service_name in config["services_to_disable"]:
            config["services_to_disable"].remove(service_name)
            self._save_config(config)
            return f"Removed '{service_name}' from services to disable"
        else:
            return f"Service '{service_name}' is not in the disable list"
    
    def _get_service_stats(self, service_name):
        """Get memory and CPU usage of a service"""
        try:
            pids = self._get_service_pids(service_name)
            if not pids:
                return None
            
            total_memory = 0
            total_cpu = 0
            
            for pid in pids:
                try:
                    process = psutil.Process(int(pid))
                    mem_info = process.memory_info()
                    total_memory += mem_info.rss / 1024 / 1024  # Convert to MB
                    total_cpu += process.cpu_percent()
                except:
                    continue
            
            return {"memory": total_memory, "cpu": total_cpu}
        except:
            return None
    
    def _get_service_pids(self, service_name):
        """Get PIDs associated with a service"""
        try:
            output = subprocess.check_output(
                ["systemctl", "status", service_name], 
                universal_newlines=True
            )
            
            pids = []
            for line in output.split("\n"):
                if "Main PID:" in line:
                    pid = line.split("Main PID:")[1].split()[0]
                    pids.append(pid)
                    break
            
            # Get child processes
            if pids:
                children = self._get_child_pids(pids[0])
                pids.extend(children)
            
            return pids
        except:
            return []
    
    def _get_child_pids(self, parent_pid):
        """Get child PIDs of a process"""
        try:
            output = subprocess.check_output(
                ["pgrep", "-P", parent_pid], 
                universal_newlines=True
            )
            return output.strip().split("\n")
        except:
            return []
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return {"monitored_services": [], "auto_restart": True, "services_to_disable": []}
    
    def _save_config(self, config):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)