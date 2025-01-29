# simulation_view.py
import dearpygui.dearpygui as dpg


class CreatorView:
    def __init__(self, controller, show):
        self.controller = controller
        self.tag = "simulation"
        self.setup(show)
        
    def setup(self, show):   
        with dpg.child_window(border=False, tag=self.tag, show=show):
            
            dpg.add_text("Simulation Creator", color=[200, 200, 200])
            
            dpg.add_spacer(height=5)
            dpg.add_separator()
            dpg.add_spacer(height=5)
            
            dpg.add_text("Simulation parameters")            
            dpg.add_input_text(label="Simulation Name", tag="name", default_value="simulation", hint="Enter simulation name", width=300)

            dpg.add_spacer(height=5)

            dpg.add_combo(label="Random Engine", tag="random_engine", items=["MersenneTwister", "Ranlux", "MixMaxRng"], default_value="MersenneTwister", width=300)
            dpg.add_input_text(label="Random Seed", tag="random_seed", default_value="auto", hint="Enter 'auto' or a number", width=300)

            dpg.add_spacer(height=5)

            dpg.add_button(label="Select Output Directory", callback=self.open_output_dialog, width=300)
            dpg.add_input_text(label="Output Directory", tag="output_dir", readonly=True, width=300)
            
            dpg.add_spacer(height=5)
            
            dpg.add_input_int(label="Number of Intervals", tag="num_intervals", default_value=10, min_value=1, width=300)
            dpg.add_input_int(label="Interval Duration (seconds)", tag="interval_duration", default_value=1, min_value=1, width=300)
            
            dpg.add_spacer(height=5)
            dpg.add_separator()
            dpg.add_spacer(height=5)
            
            dpg.add_button(label="Submit", callback=self.submit, width=300)

    def open_output_dialog(self):
        with dpg.file_dialog(
            directory_selector=True, label="Select Output Directory",
            callback=lambda sender, data: dpg.set_value("output_dir", data["file_path_name"]),
            width=600, height=250):
            pass

    def submit(self):
        params = self.get_sim_params()
        name = params.pop("name")
        self.controller.new_sim(name, params)
        dpg.hide_item("simulation")
        dpg.show_item("editor")

    def get_sim_params(self):
        num_intervals = dpg.get_value("num_intervals")
        interval_duration = dpg.get_value("interval_duration")
        run_timing_intervals = [
            [i * interval_duration, (i + 1) * interval_duration] for i in range(num_intervals)
        ]
        
        random_seed_value = dpg.get_value("random_seed")
        try:
            random_seed = int(random_seed_value) if random_seed_value != "auto" else "auto"
        except ValueError:
            random_seed = "auto"
        
        return {
            "name": dpg.get_value("name"),
            "random_engine": dpg.get_value("random_engine"),
            "random_seed": random_seed,
            "run_timing_intervals": run_timing_intervals,
            "output_dir": dpg.get_value("output_dir"),
        }