import dearpygui.dearpygui as dpg
from controllers.menu_controller import MenuController

class Menu:
    def __init__(self, simulation):
        self.controller = MenuController(simulation)
        self._setup()

    def _setup(self):
        with dpg.menu_bar():
            with dpg.menu(label="Simulation"):
                dpg.add_menu_item(label="New Simulation", callback=self.controller.new)
                dpg.add_menu_item(label="Load Simulation", callback=lambda: dpg.show_item("load_dialog"))
                dpg.add_menu_item(label="Save Simulation", callback=lambda: dpg.show_item("save_dialog"))

        self._create_file_dialogs()
        
    def _create_file_dialogs(self):
        """Creates save and load file dialogs only once."""
        with dpg.file_dialog(directory_selector=False, show=False, tag="load_dialog",
                             width=600, height=400, modal=True, callback=self.controller.load):
            dpg.add_file_extension(".json", color=(255, 255, 0, 255))

        with dpg.file_dialog(directory_selector=False, show=False, tag="save_dialog",
                             width=600, height=400, modal=True, callback=self.controller.save):
            dpg.add_file_extension(".json", color=(0, 255, 0, 255))