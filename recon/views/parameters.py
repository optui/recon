import dearpygui.dearpygui as dpg
from utils import Observer
import os

class Parameters(Observer):
    def __init__(self, simulation):
        self.tag = "parameters"
        self.simulation = simulation
        self.simulation.attach(self)
        self._create_parameter_form()

    def _create_parameter_form(self):
        """Creates parameter inputs for simulation name and output directory."""
        if dpg.does_item_exist(self.tag):
            dpg.delete_item(self.tag)

        with dpg.child_window(tag=self.tag, border=False):
            dpg.add_input_text(
                label="Simulation Name",
                tag="name",
                default_value=self.simulation.name,
                on_enter=True,
                callback=self._update_name,
                width=300
            )
            dpg.add_button(
                label="Select Output Directory",
                callback=self.open_output_dialog,
                width=300
            )
            dpg.add_input_text(
                label="Output Directory",
                tag="output_dir",
                default_value=self.simulation.output_dir if hasattr(self.simulation, 'output_dir') else "",
                readonly=True,
                width=300
            )
            
            dpg.add_button(
                label="Update",
                callback=self._update_parameters,
                width=300
            )

    def _update_parameters(self, sender=None, app_data=None):
        """Updates all simulation parameters."""
        self.simulation.name = dpg.get_value("name")
        output_dir = dpg.get_value("output_dir")
        if output_dir:
            self.simulation.output_dir = output_dir
            os.makedirs(output_dir, exist_ok=True)

    def _update_name(self, sender, app_data):
        """Updates the simulation name."""
        if sender == "name":
            self.simulation.name = app_data
        else:
            self.simulation.name = dpg.get_value("name")

    def update(self, event, *args, **kwargs):
        """Handles simulation changes (reset and load)."""
        if event in ["simulation_reset", "simulation_loaded"]:
            self._create_parameter_form()

    def open_output_dialog(self):
        """Opens a file dialog to select the output directory."""
        with dpg.file_dialog(
            directory_selector=True,
            label="Select Output Directory",
            callback=self._output_dir_selected,
            width=700,
            height=400
        ):
            pass

    def _output_dir_selected(self, sender, app_data):
        """Handles output directory selection."""
        selected_dir = app_data["file_path_name"]
        dpg.set_value("output_dir", selected_dir)
        self._update_parameters()