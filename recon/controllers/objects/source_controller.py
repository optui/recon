from utils import Observable

class SourceController(Observable):
    def __init__(self, simulation):
        super().__init__()
        self.simulation = simulation

    def create(self, name, properties=None):
        """Create a new source with given properties."""
        if properties is None:
            properties = {}
            
        # Create source with the specified type
        source = self.simulation.add_source(name=name, source_type="GenericSource")
        
        # Set common properties
        if "particle" in properties:
            source.particle = properties["particle"]
        if "activity" in properties:
            source.activity = properties["activity"]
        if "energy" in properties:
            # Set energy properties as a Box object
            energy_props = properties["energy"]
            source.energy.type = "mono"  # Set the type first
            source.energy.mono = {"value": energy_props["mono"]["value"]}  # Set the mono energy value
        
        # Set position properties
        position = properties.get("position", {})
        source.position.type = position.get("type", "point")
        source.position.translation = position.get("translation", [0.0, 0.0, 0.0])
        
        if source.position.type == "box":
            source.position.size = position.get("size", [1.0, 1.0, 1.0])
        elif source.position.type == "sphere":
            source.position.radius = position.get("radius", 1.0)
        elif source.position.type == "disc":
            source.position.radius = position.get("radius", 1.0)
        
        # Set direction as a Box object
        if "direction" in properties:
            direction = properties["direction"]
            source.direction.type = "momentum"
            source.direction.momentum = direction
        
        # Notify observers of the change
        self.notify("source_created")
        return source

    def get_all(self):
        """Return list of source names."""
        return [src.name for src in self.simulation.source_manager.sources.values()]

    def get_details(self, name):
        """Return source details if exists."""
        source = self.simulation.source_manager.sources.get(name)
        if not source:
            return None
            
        details = {
            "name": source.name,
            "particle": source.particle if hasattr(source, "particle") else "gamma",
            "activity": source.activity if hasattr(source, "activity") else 1000.0,
            "position": source.position if hasattr(source, "position") else [0.0, 0.0, 0.0],
            "direction": source.direction if hasattr(source, "direction") else [0.0, 0.0, 1.0],
            "energy": {
                "spectrum_type": "mono",
                "mono": {
                    "value": source.energy.mono.value if hasattr(source, "energy") else 1.0
                }
            }
        }
        return details

    def delete(self, name):
        """Delete source if exists."""
        if name in self.simulation.source_manager.sources:
            del self.simulation.source_manager.sources[name]
            self.notify("source_deleted")
            return True
        return False

    def update(self, name, properties):
        """Update source properties."""
        source = self.simulation.source_manager.sources.get(name)
        if not source:
            return False
            
        # Update properties
        if "particle" in properties:
            source.particle = properties["particle"]
        if "activity" in properties:
            source.activity = properties["activity"]
        if "position" in properties:
            source.position = properties["position"]
        if "direction" in properties:
            source.direction = properties["direction"]
        if "energy" in properties:
            source.energy = properties["energy"]
            
        # Notify observers of the change
        self.notify("source_updated")
        return True 