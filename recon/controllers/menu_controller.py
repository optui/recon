import os

class MenuController:
    def __init__(self, simulation):
        self.simulation = simulation
    
    def new(self):
        """Resets the simulation without breaking observers."""
        self.simulation.new()

    def load(self, sender, app_data):
        """Loads simulation from a JSON file."""
        path = app_data["file_path_name"]
        if path:
            self.simulation.load(path)
    
    def save(self, sender, app_data):
        """Saves simulation to a JSON file."""
        path = app_data["file_path_name"]
        if path:
            directory, filename = os.path.split(path)
            self.simulation.save(directory=directory, filename=filename)