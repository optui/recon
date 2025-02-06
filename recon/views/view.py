import dearpygui.dearpygui as dpg
from views.menu import Menu
from views.parameters import Parameters
from views.objects.objects import Objects
from views.run import Run

class View:
    def __init__(self, simulation):
        self.simulation = simulation
        self._setup()

    def _setup(self):
        dpg.create_context()
        
        with dpg.font_registry():
            default_font = dpg.add_font("recon/assets/Roboto-Medium.ttf", 17)

        with dpg.window(tag="primary", label="Main Window"):
            Menu(self.simulation)
            with dpg.tab_bar():
                with dpg.tab(label="Simulation parameters"):
                    Parameters(self.simulation)
                with dpg.tab(label="Simulation objects"):
                    Objects(self.simulation)
                with dpg.tab(label="Simulation Run"):
                    Run(self.simulation)

            dpg.bind_font(default_font)
        
        dpg.create_viewport(title="Simulation Manager", width=950, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("primary", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
