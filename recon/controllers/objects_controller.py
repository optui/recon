from models import Simulation
from utils import Observable
from controllers.objects.volume_controller import VolumeController
from controllers.objects.actor_controller import ActorController
from controllers.objects.source_controller import SourceController

class ObjectsController(Observable):
    def __init__(self, simulation: Simulation):
        super().__init__()
        self.simulation = simulation
        self.volume_controller = VolumeController(simulation)
        self.actor_controller = ActorController(simulation)
        self.source_controller = SourceController(simulation)

    def get_objects(self):
        """Fetch and return object data in formatted lists."""
        volumes = list(self.simulation.simulation.volume_manager.volumes.keys())
        sources = list(self.simulation.simulation.source_manager.sources.keys())
        actors = list(self.simulation.simulation.actor_manager.actors.keys())

        return {
            "volumes": volumes,
            "sources": sources,
            "actors": actors
        }

    def get_object_details(self, object_name):
        """Retrieve details for a selected object."""
        if object_name in self.simulation.simulation.volume_manager.volumes:
            volume = self.simulation.simulation.volume_manager.volumes[object_name]
            return f"Volume Name: {object_name}\nMaterial: {volume.material}\nSize: {volume.size}\nTranslation: {volume.translation}\nRotation: {volume.rotation}"
        
        if object_name in self.simulation.simulation.source_manager.sources:
            source = self.simulation.simulation.source_manager.sources[object_name]
            return f"Source Name: {object_name}\nParticle: {source.particle}\nEnergy: {source.energy} MeV"
        
        if object_name in self.simulation.simulation.actor_manager.actors:
            actor = self.simulation.simulation.actor_manager.actors[object_name]
            return f"Actor Name: {object_name}\nType: {actor.actor_type}"
        
        return "No details available."

    def delete_object(self, object_name):
        """Delete an object based on its type."""
        if object_name in self.simulation.simulation.volume_manager.volumes:
            self.volume_controller.delete(object_name)
        elif object_name in self.simulation.simulation.source_manager.sources:
            self.source_controller.delete(object_name)
        elif object_name in self.simulation.simulation.actor_manager.actors:
            self.actor_controller.delete(object_name)
        self.notify("object_deleted")
