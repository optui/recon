import dearpygui.dearpygui as dpg
from utils import Observer

class ObjectsList(Observer):
    def __init__(self, controller):
        self.controller = controller
        self.volume_view = None  # Will be set by Objects class
        self.actor_view = None  # Add reference to actor view
        self.source_view = None  # Add reference to source view
        self._setup()
        self.refresh_objects()

    def update(self, event, *args, **kwargs):
        """Handle updates from controllers."""
        if event.endswith(("_created", "_updated", "_deleted")):
            self.refresh_objects()

    def _setup(self):
        with dpg.child_window(width=400, height=400, border=False):
            dpg.add_text("Simulation Objects")
            
            dpg.add_listbox(
                items=[],
                tag="Simulation Listbox",
                width=350,
                num_items=10,
                callback=self.on_select_object,
                default_value=""
            )
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Edit", callback=self.edit_selected)
                dpg.add_button(label="Delete", callback=self.delete_selected)

    def set_volume_view(self, volume_view):
        """Set reference to volume view."""
        self.volume_view = volume_view

    def set_actor_view(self, actor_view):
        """Set reference to actor view."""
        self.actor_view = actor_view

    def set_source_view(self, source_view):
        """Set reference to source view."""
        self.source_view = source_view

    def get_flat_objects(self):
        """Get all objects as a flat list."""
        objects = self.controller.get_objects()
        return (
            objects.get("volumes", []) + 
            objects.get("actors", []) + 
            objects.get("sources", [])
        )

    def refresh_objects(self):
        """Update the listbox with current objects."""
        items = self.get_flat_objects()
        dpg.configure_item("Simulation Listbox", items=items)
        dpg.set_value("Simulation Listbox", "")  # Clear selection

    def on_select_object(self, sender, app_data):
        """Handle object selection."""
        selected_object = app_data
        if not selected_object:
            return
            
        # Update volume manager if a volume is selected
        if selected_object in self.controller.get_objects()["volumes"] and self.volume_view:
            volume = self.controller.volume_controller.get_details(selected_object)
            if volume:
                self.volume_view.set_volume_properties(volume)
                
        # Update actor manager if an actor is selected
        elif selected_object in self.controller.get_objects()["actors"] and self.actor_view:
            actor = self.controller.actor_controller.get_details(selected_object)
            if actor:
                self.actor_view.set_actor_properties(actor)

        # Update source manager if a source is selected
        elif selected_object in self.controller.get_objects()["sources"] and self.source_view:
            source = self.controller.source_controller.get_details(selected_object)
            if source:
                self.source_view.set_source_properties(source)

    def edit_selected(self):
        selected_object = dpg.get_value("Simulation Listbox")
        if not selected_object:
            return
            
        if selected_object in self.controller.get_objects()["volumes"] and self.volume_view:
            volume = self.controller.volume_controller.get_details(selected_object)
            if volume:
                self.volume_view.set_volume_properties(volume)
        elif selected_object in self.controller.get_objects()["actors"] and self.actor_view:
            actor = self.controller.actor_controller.get_details(selected_object)
            if actor:
                self.actor_view.set_actor_properties(actor)

    def delete_selected(self):
        selected_object = dpg.get_value("Simulation Listbox")
        if selected_object:
            self.controller.delete_object(selected_object)
            self.refresh_objects()
