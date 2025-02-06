import dearpygui.dearpygui as dpg
from controllers.objects import ObjectsController
from views.objects import ObjectsList, VolumeManager, ActorManager, SourceManager
from utils import Observer

class Objects(Observer):
    def __init__(self, simulation):
        self.tag = "objects"
        self.controller = ObjectsController(simulation)
        self.controller.volume_controller.attach(self)
        self.controller.actor_controller.attach(self)
        self.controller.source_controller.attach(self)
        
        self._setup()

    def _setup(self):
        with dpg.child_window(tag=self.tag, border=False):
            with dpg.group(horizontal=True):
                self.objects_list = ObjectsList(self.controller)
                dpg.set_item_user_data("Simulation Listbox", self.objects_list)
                
                with dpg.tab_bar():
                    with dpg.tab(label="Volume Manager"):
                        self.volume_view = VolumeManager(self.controller.volume_controller)
                        self.objects_list.set_volume_view(self.volume_view)
                    with dpg.tab(label="Actor Manager"):
                        self.actor_view = ActorManager(self.controller.actor_controller)
                        self.objects_list.set_actor_view(self.actor_view)
                    with dpg.tab(label="Source Manager"):
                        self.source_view = SourceManager(self.controller.source_controller)
                        self.objects_list.set_source_view(self.source_view)

    def update(self, event, *args, **kwargs):
        """Handle updates from simulation and controllers."""
        if event in ["simulation_reset", "simulation_loaded"] or \
           event.endswith(("_created", "_updated", "_deleted")):
            self.refresh_objects()

    def refresh_objects(self):
        """Refresh the objects list"""
        self.objects_list.refresh_objects()