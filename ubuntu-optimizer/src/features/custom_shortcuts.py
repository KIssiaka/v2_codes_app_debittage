import os
import subprocess
import json

class ShortcutManager:
    def __init__(self):
        self.shortcuts_dir = os.path.expanduser("~/.config/custom-shortcuts")
        os.makedirs(self.shortcuts_dir, exist_ok=True)
        self.shortcuts_file = os.path.join(self.shortcuts_dir, "shortcuts.json")
        
        # Initialize shortcuts file if it doesn't exist
        if not os.path.exists(self.shortcuts_file):
            with open(self.shortcuts_file, 'w') as f:
                json.dump({}, f)
                
    def create_shortcut(self, name, command, key_combo):
        """Create a custom keyboard shortcut"""
        # Load existing shortcuts
        shortcuts = self._load_shortcuts()
        
        # Add new shortcut
        shortcuts[name] = {
            "command": command,
            "key_combo": key_combo
        }
        
        # Save shortcuts
        self._save_shortcuts(shortcuts)
        
        # Configure the keyboard shortcut using gsettings
        try:
            # Create a unique path for this shortcut
            path_name = f"custom{len(shortcuts)}"
            base_path = "org.gnome.settings-daemon.plugins.media-keys"
            full_path = f"{base_path}.custom-keybinding:/{base_path}/custom-keybindings/{path_name}/"
            
            subprocess.run(["gsettings", "set", full_path, "binding", key_combo])
            subprocess.run(["gsettings", "set", full_path, "command", command])
            subprocess.run(["gsettings", "set", full_path, "name", name])
            
            # Update the list of custom keybindings
            paths = []
            for i in range(len(shortcuts)):
                paths.append(f"/{base_path}/custom-keybindings/custom{i}/")
                
            subprocess.run(["gsettings", "set", base_path, "custom-keybindings", str(paths)])
            
            return f"Shortcut '{name}' created with key combination '{key_combo}'"
        except Exception as e:
            return f"Error creating shortcut: {str(e)}"
    
    def list_shortcuts(self):
        """List all registered shortcuts"""
        shortcuts = self._load_shortcuts()
        if not shortcuts:
            return "No shortcuts found"
            
        result = "Registered shortcuts:\n"
        for name, details in shortcuts.items():
            result += f"- {name}: {details['command']} ({details['key_combo']})\n"
            
        return result
        
    def remove_shortcut(self, name):
        """Remove a custom keyboard shortcut"""
        shortcuts = self._load_shortcuts()
        
        if name not in shortcuts:
            return f"Shortcut '{name}' not found"
            
        # Remove from our json file
        del shortcuts[name]
        self._save_shortcuts(shortcuts)
        
        # Reconfigure gsettings
        try:
            base_path = "org.gnome.settings-daemon.plugins.media-keys"
            paths = []
            for i, shortcut_name in enumerate(shortcuts.keys()):
                path_name = f"custom{i}"
                full_path = f"{base_path}.custom-keybinding:/{base_path}/custom-keybindings/{path_name}/"
                details = shortcuts[shortcut_name]
                
                subprocess.run(["gsettings", "set", full_path, "binding", details["key_combo"]])
                subprocess.run(["gsettings", "set", full_path, "command", details["command"]])
                subprocess.run(["gsettings", "set", full_path, "name", shortcut_name])
                
                paths.append(f"/{base_path}/custom-keybindings/{path_name}/")
                
            subprocess.run(["gsettings", "set", base_path, "custom-keybindings", str(paths)])
            
            return f"Shortcut '{name}' removed successfully"
        except Exception as e:
            return f"Error removing shortcut: {str(e)}"
    
    def _load_shortcuts(self):
        """Load shortcuts from file"""
        try:
            with open(self.shortcuts_file, 'r') as f:
                return json.load(f)
        except:
            return {}
            
    def _save_shortcuts(self, shortcuts):
        """Save shortcuts to file"""
        with open(self.shortcuts_file, 'w') as f:
            json.dump(shortcuts, f, indent=2)