from utils import Observable

class ActorController(Observable):
    def __init__(self, simulation):
        super().__init__()  # Initialize Observable
        self.simulation = simulation

    def create(self, name, properties=None):
        """Create a new actor with given properties."""
        if properties is None:
            properties = {}
            
        # Map our simplified names to GATE's actual actor types
        actor_type_map = {
            "SimulationStatisticsActor": "SimulationStatisticsActor",
            "HitsCollectionActor": "DigitizerHitsCollectionActor",
            "ProjectionActor": "DigitizerProjectionActor"
        }
            
        actor_type = properties.get("type", "SimulationStatisticsActor")
        gate_actor_type = actor_type_map.get(actor_type, actor_type)
        
        # Create actor using GATE's add_actor method
        actor = self.simulation.add_actor(
            gate_actor_type,
            name=name
        )
        
        # Set common properties - using attached_to instead of attached_volume
        if "attached_volume" in properties:
            actor.attached_to = properties["attached_volume"]
            
        # Set type-specific properties
        if actor_type == "HitsCollectionActor":
            actor.output = properties.get("output", "hits.root")
            actor.collection_name = properties.get("collection_name", "Hits")
        elif actor_type == "ProjectionActor":
            actor.output = properties.get("output", "projections.root")
            actor.collection_name = properties.get("collection_name", "Projections")
            actor.store_uncertainty = properties.get("store_uncertainty", True)
            
        # Notify observers of the change
        self.notify("actor_created")  # More specific events
        return actor

    def get_all(self):
        """Return list of actor names."""
        return [actor.name for actor in self.simulation.actor_manager.actors.values()]

    def get_details(self, name):
        """Return actor details if exists."""
        actor = self.simulation.actor_manager.actors.get(name)
        if not actor:
            return None
            
        # Get actor type from class name
        actor_type = actor.__class__.__name__.replace("Digitizer", "")
        
        details = {
            "name": actor.name,
            "type": actor_type,
            "attached_volume": actor.attached_to if hasattr(actor, "attached_to") else None
        }
        
        # Get type-specific properties
        if actor_type == "HitsCollectionActor":
            details.update({
                "output": actor.output if hasattr(actor, "output") else "hits.root",
                "collection_name": actor.collection_name if hasattr(actor, "collection_name") else "Hits"
            })
        elif actor_type == "ProjectionActor":
            details.update({
                "output": actor.output if hasattr(actor, "output") else "projections.root",
                "collection_name": actor.collection_name if hasattr(actor, "collection_name") else "Projections",
                "store_uncertainty": actor.store_uncertainty if hasattr(actor, "store_uncertainty") else True
            })
            
        return details

    def delete(self, name):
        """Delete actor if exists."""
        if name in self.simulation.actor_manager.actors:
            del self.simulation.actor_manager.actors[name]
            # Notify observers of the change
            self.notify("actor_deleted")
            return True
        return False

    def update(self, name, properties):
        """Update actor properties."""
        actor = self.simulation.actor_manager.actors.get(name)
        if not actor:
            return False
            
        # Update common properties
        if "attached_volume" in properties:
            actor.attached_to = properties["attached_volume"]
            
        # Get actor type from class name
        actor_type = actor.__class__.__name__.replace("Digitizer", "")
        
        # Update type-specific properties
        if actor_type == "HitsCollectionActor":
            if "output" in properties:
                actor.output = properties["output"]
            if "collection_name" in properties:
                actor.collection_name = properties["collection_name"]
        elif actor_type == "ProjectionActor":
            if "output" in properties:
                actor.output = properties["output"]
            if "collection_name" in properties:
                actor.collection_name = properties["collection_name"]
            if "store_uncertainty" in properties:
                actor.store_uncertainty = properties["store_uncertainty"]
            
        # Notify observers of the change
        self.notify("actor_updated")
        return True 