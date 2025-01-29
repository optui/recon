# models/simulation.py
import opengate as gate


class Simulation:
    def __init__(self, name="simulation", **kwargs):
        self.simulation = gate.Simulation(name, **kwargs)
        self.volume_manager = VolumeManager(self.simulation)
        self.source_manager = SourceManager(self.simulation)
        self.actor_manager = ActorManager(self.simulation)

    def save(self, directory, filename="simulation"):
        self.simulation.to_json_file(directory, filename)

    def load(self, path):
        self.simulation.from_json_file(path)

    def add_volume(self, volume_type, name):
        return self.simulation.add_volume(volume_type, name)

    def add_source(self, source_type, name):
        return self.simulation.add_source(source_type, name)

    def add_actor(self, actor_type, name):
        return self.simulation.add_actor(actor_type, name)

    def run(self, start_new_process: bool = False):
        self.simulation.run(start_new_process)


class VolumeManager:
    def __init__(self, simulation: gate.Simulation):
        self.manager = simulation.volume_manager

    def volumes(self):
        return self.manager.dump_volumes()
    
    def get_volume(self, volume_name):
        return self.manager.get_volume(volume_name)

    def volume_types(self):
        return self.manager.dump_volume_types()

    def volume_tree(self):
        return self.manager.dump_volume_tree()


class SourceManager:
    def __init__(self, simulation: gate.Simulation):
        self.manager = simulation.source_manager

    def sources(self):
        return self.manager.dump_sources()
    
    def get_source(self, source_name):
        return self.manager.get_source(source_name)
    
    def source_types(self):
        return self.manager.dump_source_types()


class ActorManager:
    def __init__(self, simulation: gate.Simulation):
        self.manager = simulation.actor_manager

    def actors(self):
        return self.manager.dump_actors()
    
    def get_actor(self, actor_name):
        return self.manager.get_actor(actor_name)

    def actor_types(self):
        return self.manager.dump_actor_types()

