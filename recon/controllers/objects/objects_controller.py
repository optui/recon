from .volume_controller import VolumeController
from .actor_controller import ActorController
from .source_controller import SourceController

class ObjectsController:
    def __init__(self, simulation):
        self.simulation = simulation
        self.volume_controller = VolumeController(simulation)
        self.actor_controller = ActorController(simulation)
        self.source_controller = SourceController(simulation)

    def get_objects(self):
        return {
            "volumes": self.volume_controller.get_all(),
            "actors": self.actor_controller.get_all(),
            "sources": self.source_controller.get_all()
        }

    def get_object_details(self, name):
        # Try each controller to find the object
        for controller in [self.volume_controller, 
                         self.actor_controller, 
                         self.source_controller]:
            details = controller.get_details(name)
            if details:
                return details
        return None

    def delete_object(self, name):
        # Try each controller to delete the object
        for controller in [self.volume_controller, 
                         self.actor_controller, 
                         self.source_controller]:
            if controller.delete(name):
                return True
        return False