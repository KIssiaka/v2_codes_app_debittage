class StartupManager:
    def manage_startup_apps(self, app_name, action):
        """
        Manage applications that run on startup.
        
        :param app_name: Name of the application to manage.
        :param action: Action to perform ('add' or 'remove').
        """
        if action == 'add':
            # Code to add the application to startup
            pass
        elif action == 'remove':
            # Code to remove the application from startup
            pass
        else:
            raise ValueError("Action must be 'add' or 'remove'.")

    def list_startup_apps(self):
        """
        List all applications that are set to run on startup.
        
        :return: List of startup applications.
        """
        # Code to list startup applications
        return []  # Placeholder for the actual list of startup applications.