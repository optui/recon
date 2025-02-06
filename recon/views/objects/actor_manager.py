import dearpygui.dearpygui as dpg
from utils import Observer

class ActorManager(Observer):
    def __init__(self, controller):
        self.controller = controller
        self.current_type = "SimulationStatisticsActor"  # Default type
        self.selected_actor = None  # Add this to track the selected actor
        controller.attach(self)  # Attach to controller
        self._setup()

    def _setup(self):
        with dpg.child_window(label="Actor Manager", width=450, height=600, border=False):
            # Basic Properties
            with dpg.collapsing_header(label="Basic Properties", default_open=True):
                dpg.add_input_text(label="Actor Name", tag="Actor Name", width=300)
                
                # Actor type selection (using simplified names)
                actor_types = ["SimulationStatisticsActor", "HitsCollectionActor", "ProjectionActor"]
                dpg.add_combo(
                    label="Actor Type",
                    items=actor_types,
                    default_value=self.current_type,
                    tag="Actor Type",
                    width=300,
                    callback=self.on_type_change
                )
                
                # Common properties - convert volume keys to list
                volume_list = list(self.controller.simulation.volume_manager.volumes.keys())
                dpg.add_combo(
                    label="Attached Volume",
                    items=volume_list if volume_list else [""],  # Ensure non-empty list
                    default_value=volume_list[0] if volume_list else "",
                    tag="Actor Attached Volume",
                    width=300
                )

            # Type-specific parameters
            with dpg.collapsing_header(label="Actor Parameters", default_open=True):
                # Hits Collection parameters
                with dpg.group(tag="hits_collection_params", show=False):
                    dpg.add_input_text(
                        label="Output File",
                        tag="Actor Output File",
                        default_value="hits.root",
                        width=300
                    )
                    dpg.add_input_text(
                        label="Collection Name",
                        tag="Actor Collection Name",
                        default_value="Hits",
                        width=300
                    )

                # Projection parameters
                with dpg.group(tag="projection_params", show=False):
                    dpg.add_input_text(
                        label="Output File",
                        tag="Projection Output File",
                        default_value="projections.root",
                        width=300
                    )
                    dpg.add_input_text(
                        label="Collection Name",
                        tag="Projection Collection Name",
                        default_value="Projections",
                        width=300
                    )
                    dpg.add_checkbox(
                        label="Store Uncertainty",
                        tag="Store Uncertainty",
                        default_value=True
                    )

            # Buttons
            with dpg.group(horizontal=True):
                dpg.add_button(label="Create/Update", callback=self.submit_actor, width=145)
                dpg.add_button(label="Clear", callback=self.clear_fields, width=145)

    def on_type_change(self, sender, app_data):
        """Handle actor type change."""
        self.current_type = app_data
        
        # Show/hide parameters based on type
        dpg.configure_item("hits_collection_params", 
                          show=(app_data == "HitsCollectionActor"))
        dpg.configure_item("projection_params", 
                          show=(app_data == "ProjectionActor"))

    def get_actor_properties(self):
        """Get properties based on current actor type."""
        properties = {
            "type": self.current_type,
            "attached_volume": dpg.get_value("Actor Attached Volume")
        }

        if self.current_type == "HitsCollectionActor":
            properties.update({
                "output": dpg.get_value("Actor Output File"),
                "collection_name": dpg.get_value("Actor Collection Name")
            })
        elif self.current_type == "ProjectionActor":
            properties.update({
                "output": dpg.get_value("Projection Output File"),
                "collection_name": dpg.get_value("Projection Collection Name"),
                "store_uncertainty": dpg.get_value("Store Uncertainty")
            })

        return properties

    def set_actor_properties(self, actor_data):
        """Set all fields based on actor data."""
        if not actor_data:
            self.clear_fields()
            return

        # Store the original name of the selected actor
        self.selected_actor = actor_data.get("name", "")
        
        # Set basic properties
        dpg.set_value("Actor Name", self.selected_actor)
        dpg.set_value("Actor Type", actor_data.get("type", "SimulationStatisticsActor"))
        dpg.set_value("Actor Attached Volume", actor_data.get("attached_volume", ""))
        
        # Set type-specific properties based on actor type
        actor_type = actor_data.get("type", "SimulationStatisticsActor")
        if actor_type in ["HitsCollectionActor", "ProjectionActor"]:
            dpg.set_value("Actor Output File", actor_data.get("output", "hits.root"))
            dpg.set_value("Actor Collection Name", actor_data.get("collection_name", "Hits"))
            
            if actor_type == "ProjectionActor":
                dpg.set_value("Store Uncertainty", actor_data.get("store_uncertainty", True))

    def submit_actor(self):
        name = dpg.get_value("Actor Name")
        if not name:
            return
            
        properties = self.get_actor_properties()
        
        # If we're editing an existing actor
        if self.selected_actor:
            # If name hasn't changed, just update properties
            if name == self.selected_actor:
                self.controller.update(name, properties)
            # If name has changed, handle rename
            else:
                # First delete the old actor
                self.controller.delete(self.selected_actor)
                # Then create new actor with new name
                self.controller.create(name, properties)
        else:
            # Creating a new actor
            self.controller.create(name, properties)
        
        # Clear selection and fields
        self.selected_actor = None
        self.clear_fields()

    def clear_fields(self):
        """Reset all fields to defaults."""
        self.selected_actor = None  # Clear selected actor
        dpg.set_value("Actor Name", "")
        dpg.set_value("Actor Type", "SimulationStatisticsActor")
        dpg.set_value("Actor Attached Volume", "")
        dpg.set_value("Actor Output File", "hits.root")
        dpg.set_value("Actor Collection Name", "Hits")
        dpg.set_value("Projection Output File", "projections.root")
        dpg.set_value("Projection Collection Name", "Projections")
        dpg.set_value("Store Uncertainty", True)
        
        self.on_type_change(None, "SimulationStatisticsActor")

    def update_volume_list(self):
        """Update the list of available volumes in the combo box."""
        volume_list = list(self.controller.simulation.volume_manager.volumes.keys())
        dpg.configure_item(
            "Actor Attached Volume",
            items=volume_list if volume_list else [""],
            default_value=volume_list[0] if volume_list else ""
        )

    def update(self, event, *args, **kwargs):
        """Handle updates from controller."""
        if event in ["actor_created", "actor_updated", "actor_deleted"]:
            self.clear_fields()