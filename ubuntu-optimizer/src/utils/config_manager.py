class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = {}

    def load_config(self):
        import yaml
        with open(self.config_file, 'r') as file:
            self.config_data = yaml.safe_load(file)

    def save_config(self):
        import yaml
        with open(self.config_file, 'w') as file:
            yaml.safe_dump(self.config_data, file)