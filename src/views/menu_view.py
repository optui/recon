# menu_view.py
import dearpygui.dearpygui as dpg


class MenuView:
    def __init__(self, controller):
        self.controller = controller
        self.setup()
    
    def setup(self):
        with dpg.menu_bar():
            with dpg.menu(label="Simulation"):
                dpg.add_menu_item(label="New Simulation", callback=self.new_simulation)
                dpg.add_menu_item(label="Load Simulation", callback=self.open_load_dialog)
                dpg.add_menu_item(label="Save Simulation", callback=self.open_save_dialog, tag="save", enabled=False)

    def enable_save(self):
        dpg.configure_item("save", enabled=True)
        
    def new_simulation(self):
        if dpg.does_item_exist("editor") and dpg.is_item_shown("editor"):
            dpg.hide_item("editor")
            dpg.show_item("simulation")

    def open_load_dialog(self):
        with dpg.file_dialog(
            label="Load Simulation", directory_selector=False,
            callback=lambda s, d: self.on_load(d["file_path_name"]),
            width=600, height=400, show=True):
            dpg.add_file_extension(".json")

    def open_save_dialog(self):
        with dpg.file_dialog(
            label="Save Simulation", directory_selector=False,
            callback=lambda s, d: self.on_save(d["current_path"], d["file_name"]),
            width=600, height=400, show=True, default_filename="simulation"):
            dpg.add_file_extension(".json")