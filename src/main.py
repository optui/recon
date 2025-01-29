# main.py
from controllers import SimulationController
from views import View
from models import Simulation


def main():
    simulation_model = Simulation()
    simulation_controller = SimulationController(simulation_model)
    view = View(simulation_controller)
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)

