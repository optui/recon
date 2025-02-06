import opengate as gate
from utils import Observable

class Simulation(Observable):
    def __init__(self):
        super().__init__()
        self.simulation = gate.Simulation()
        
    def new(self):
        self.simulation = gate.Simulation()
        self.notify("simulation_reset")
        
    def load(self, path):
        """Loads simulation from a JSON file and notifies observers."""
        self.simulation.from_json_file(path)
        self.notify("simulation_loaded")
        
    def save(self, directory, filename):
        """Saves simulation to a JSON file and notifies observers."""
        self.simulation.to_json_file(directory, filename)
        self.notify("simulation_saved")

    def view(self):
        """View the simulation and notifies observers."""
        self.simulation.visu = True
        self.simulation.run(start_new_process=True)
        self.notify("simulation_viewed")

    def run(self):
        """Run the simulation and notifies observers."""
        self.simulation.visu = False
        self.simulation.run(start_new_process=True)
        self.notify("simulation_run")
    
    def __getattr__(self, item):
        return getattr(self.simulation, item)
    
    def __setattr__(self, key, value):
        if key in {"simulation", "_observers"}:
            object.__setattr__(self, key, value)
        else:
            setattr(self.simulation, key, value)
            self.notify(f"{key}_updated", value=value)