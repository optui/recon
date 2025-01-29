import dearpygui.dearpygui as dpg
from views.factory import create_views


class View:
    def __init__(self, controller):
        self.controller = controller
        self.views = None
        self.setup()

    def setup(self) -> None:
        dpg.create_context()

        with dpg.font_registry():
            default_font = dpg.add_font("src/assets/Roboto-Medium.ttf", 17)

        with dpg.window(tag="primary"):
            self.views = create_views(self.controller)
            dpg.bind_font(default_font)
        
        dpg.create_viewport(title="Simulation View", width=1000, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("primary", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

