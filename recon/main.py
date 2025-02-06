from models import Simulation
from views import View

def main():
    simulation = Simulation()
    View(simulation)

if __name__ == "__main__":
    main()
