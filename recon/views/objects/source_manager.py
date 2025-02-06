import dearpygui.dearpygui as dpg
from utils import Observer

class SourceManager(Observer):
    def __init__(self, controller):
        self.controller = controller
        self.selected_source = None
        controller.attach(self)
        self._setup()

    def _setup(self):
        with dpg.child_window(label="Source Manager", width=450, height=600, border=False):
            with dpg.collapsing_header(label="Basic Properties", default_open=True):
                dpg.add_input_text(label="Source Name", tag="Source Name", width=300)
                
                particles = ["gamma", "e+", "e-", "proton", "neutron"]
                dpg.add_combo(
                    label="Particle Type",
                    items=particles,
                    default_value="gamma",
                    tag="Source Particle",
                    width=300
                )
                
                dpg.add_input_float(
                    label="Activity (Bq)",
                    tag="Source Activity",
                    default_value=1000.0,
                    width=300
                )
                
                dpg.add_input_float(
                    label="Energy (MeV)",
                    tag="Source Energy",
                    default_value=1.0,
                    width=300
                )
                
            with dpg.collapsing_header(label="Position & Direction", default_open=True):
                dpg.add_combo(
                    items=["point", "box", "sphere", "disc"],
                    label="Source Position Type",
                    tag="Source Position Type",
                    default_value="point"
                )
                
                dpg.add_input_floatx(label="Source Position", tag="Source Position", size=3, default_value=[0.0, 0.0, 0.0])
                dpg.add_input_floatx(label="Source Box Size", tag="Source Box Size", size=3, default_value=[1.0, 1.0, 1.0], show=False)
                dpg.add_input_float(label="Source Sphere Radius", tag="Source Sphere Radius", default_value=1.0, show=False)
                dpg.add_input_float(label="Source Disc Radius", tag="Source Disc Radius", default_value=1.0, show=False)

                dpg.add_input_floatx(
                    label="Direction",
                    tag="Source Direction",
                    size=3,
                    default_value=[0.0, 0.0, 1.0],
                    width=300
                )
            
            dpg.add_button(
                label="Create/Update Source",
                callback=self.submit_source,
                width=300
            )

            # Add a callback to update visible fields based on position type
            dpg.set_item_callback("Source Position Type", self._update_position_fields)

    def _update_position_fields(self, sender, app_data):
        """Update visible fields based on selected position type."""
        position_type = dpg.get_value("Source Position Type")
        dpg.configure_item("Source Box Size", show=(position_type == "box"))
        dpg.configure_item("Source Sphere Radius", show=(position_type == "sphere"))
        dpg.configure_item("Source Disc Radius", show=(position_type == "disc"))

    def get_source_properties(self):
        """Get all source properties from UI."""
        position_type = dpg.get_value("Source Position Type")
        position_properties = {
            "type": position_type,
            "translation": list(dpg.get_value("Source Position"))[:3]
        }
        
        if position_type == "box":
            position_properties["size"] = list(dpg.get_value("Source Box Size"))[:3]
        elif position_type == "sphere":
            position_properties["radius"] = dpg.get_value("Source Sphere Radius")
        elif position_type == "disc":
            position_properties["radius"] = dpg.get_value("Source Disc Radius")
        
        # Configure energy with spectrum_type
        energy_value = dpg.get_value("Source Energy")
        energy_distribution = {
            "spectrum_type": "mono",  # Required by OpenGATE
            "mono": {
                "value": energy_value  # Energy value in MeV
            }
        }
        
        return {
            "particle": dpg.get_value("Source Particle"),
            "activity": dpg.get_value("Source Activity"),
            "energy": energy_distribution,
            "position": position_properties,
            "direction": list(dpg.get_value("Source Direction"))[:3]
        }

    def set_source_properties(self, source_data):
        """Set all fields based on source data."""
        if not source_data:
            self.clear_fields()
            return

        self.selected_source = source_data.get("name", "")
        
        # Extract position as a list of floats
        position = source_data.get("position", {}).get("translation", [0.0, 0.0, 0.0])
        if not isinstance(position, list) or not all(isinstance(i, (float, int)) for i in position):
            print("Error: Position must be a list of floats.")
            position = [0.0, 0.0, 0.0]  # Default to a valid position
        
        dpg.set_value("Source Name", self.selected_source)
        dpg.set_value("Source Particle", source_data.get("particle", "gamma"))
        dpg.set_value("Source Activity", source_data.get("activity", 1000.0))
        dpg.set_value("Source Energy", source_data.get("energy", {}).get("value", 1.0))
        dpg.set_value("Source Position", position)
        dpg.set_value("Source Direction", source_data.get("direction", [0.0, 0.0, 1.0]))

    def submit_source(self):
        name = dpg.get_value("Source Name")
        if not name:
            return
            
        properties = self.get_source_properties()
        
        # If we're editing an existing source
        if self.selected_source:
            # If name hasn't changed, just update properties
            if name == self.selected_source:
                self.controller.update(name, properties)
            # If name has changed, handle rename
            else:
                # First delete the old source
                self.controller.delete(self.selected_source)
                # Then create new source with new name
                self.controller.create(name, properties)
        else:
            # Creating a new source
            self.controller.create(name, properties)
        
        # Clear selection and fields
        self.selected_source = None
        self.clear_fields()

    def clear_fields(self):
        """Reset all fields to defaults."""
        self.selected_source = None
        dpg.set_value("Source Name", "")
        dpg.set_value("Source Particle", "gamma")
        dpg.set_value("Source Activity", 1000.0)
        dpg.set_value("Source Energy", 1.0)
        dpg.set_value("Source Position", [0.0, 0.0, 0.0])
        dpg.set_value("Source Direction", [0.0, 0.0, 1.0])

    def update(self, event, *args, **kwargs):
        """Handle updates from controller."""
        if event in ["source_created", "source_updated", "source_deleted"]:
            self.clear_fields()

    def on_select_source(self, sender, app_data):
        """Handle source selection."""
        selected_source = app_data
        if not selected_source:
            return

        source = self.controller.get_details(selected_source)
        if source:
            self.set_source_properties(source)

    def edit_selected(self):
        selected_source = dpg.get_value("Source Listbox")
        if not selected_source:
            return

        source = self.controller.get_details(selected_source)
        if source:
            self.set_source_properties(source)

    def refresh_sources(self):
        """Update the listbox with current sources."""
        items = self.controller.get_all()
        dpg.configure_item("Source Listbox", items=items)
        dpg.set_value("Source Listbox", "")  # Clear selection