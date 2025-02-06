from utils import Observable

class VolumeController(Observable):
    def __init__(self, simulation):
        super().__init__()
        self.simulation = simulation

    def create(self, name, properties=None):
        """Create a new volume with given properties."""
        if properties is None:
            properties = {}
        
        volume_type = properties.get("type", "Box")  # Note: GATE uses "Box" not "BoxVolume"
        
        # Create volume using GATE's add_volume method
        volume = self.simulation.add_volume(
            volume_type,
            name=name
        )
        
        # Set common properties
        volume.material = properties.get("material", "G4_AIR")
        volume.mother = "world"  # Default to world as parent
        
        # Set type-specific properties
        if volume_type == "Box":
            volume.size = properties.get("size", [10.0, 10.0, 10.0])
        elif volume_type == "Sphere":
            volume.rmax = properties.get("rmax", 1.0)
            volume.rmin = properties.get("rmin", 0.0)
            volume.sphi = properties.get("sphi", 0.0)
            volume.dphi = properties.get("dphi", 6.283185307179586)
            volume.stheta = properties.get("stheta", 0.0)
            volume.dtheta = properties.get("dtheta", 3.141592653589793)
            
        # Set position and rotation
        if "translation" in properties:
            volume.translation = properties["translation"]
        if "rotation" in properties:
            volume.rotation = properties["rotation"]
            
        # Notify observers of the change
        self.notify("volume_created")
        return volume

    def get_all(self):
        """Return list of volume names."""
        return [vol.name for vol in self.simulation.volume_manager.volumes.values()]

    def get_details(self, name):
        """Return volume details if exists."""
        volume = self.simulation.volume_manager.volumes.get(name)
        if not volume:
            return None
            
        details = {
            "name": volume.name,
            "type": volume.volume_type.replace("Volume", ""),  # Convert BoxVolume to Box
            "material": volume.material,
        }
        
        # Get common properties
        if hasattr(volume, "size"):
            details["size"] = volume.size
        if hasattr(volume, "translation"):
            details["translation"] = volume.translation
        if hasattr(volume, "rotation"):
            details["rotation"] = volume.rotation
            
        # Get sphere specific properties
        if volume.volume_type == "SphereVolume":
            for prop in ["rmax", "rmin", "sphi", "dphi", "stheta", "dtheta"]:
                if hasattr(volume, prop):
                    details[prop] = getattr(volume, prop)
                    
        return details

    def delete(self, name):
        """Delete volume if exists."""
        if name in self.simulation.volume_manager.volumes:
            del self.simulation.volume_manager.volumes[name]
            # Notify observers of the change
            self.notify("volume_deleted")
            return True
        return False

    def update(self, name, properties):
        """Update volume properties."""
        volume = self.simulation.volume_manager.volumes.get(name)
        if not volume:
            return False
            
        # Update common properties
        if "material" in properties:
            volume.material = properties["material"]
        if "translation" in properties:
            volume.translation = properties["translation"]
        if "rotation" in properties:
            volume.rotation = properties["rotation"]
            
        # Update type-specific properties
        if volume.volume_type == "SphereVolume":
            for prop in ["rmax", "rmin", "sphi", "dphi", "stheta", "dtheta"]:
                if prop in properties:
                    setattr(volume, prop, properties[prop])
        else:  # BoxVolume
            if "size" in properties:
                volume.size = properties["size"]
                    
        # Notify observers of the change
        self.notify("volume_updated")
        return True 