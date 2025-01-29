# controllers/simulation_controller.py
from models import Simulation


class SimulationController:
    def __init__(self, model: Simulation) -> None:
        self.model = model

    def new_sim(self, name, params: dict) -> None:
        self.model = Simulation(name, **params)

    def save_sim(self, directory: str, filename: str) -> None:
        if self.model:
            self.model.save(directory, filename)
    
    def load_sim(self, filepath: str) -> None:
        self.model.load(filepath)

    def run_sim(self, start_new_process: bool = False) -> None:
        if self.model:
            self.model.run(start_new_process)

