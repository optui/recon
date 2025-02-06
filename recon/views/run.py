import dearpygui.dearpygui as dpg

class Run:
    def __init__(self, simulation):
        self.simulation = simulation
        self._setup()

    def _setup(self):
        with dpg.child_window(label="Simulation Control", border=False):
            # Simulation Info
            with dpg.collapsing_header(label="Simulation Information", default_open=True):
                dpg.add_text("Number of events: 0")
                dpg.add_text("Status: Not running")
                dpg.add_separator()
                
            # Visualization Options
            with dpg.collapsing_header(label="Visualization", default_open=True):
                dpg.add_checkbox(label="Show geometry", default_value=True)
                dpg.add_checkbox(label="Show trajectories", default_value=True)
                dpg.add_separator()
                
                with dpg.group(horizontal=True):
                    dpg.add_button(label="View Geometry", callback=self.view_geometry)
                    dpg.add_button(label="Reset View", callback=self.reset_view)
            
            # Run Controls
            with dpg.collapsing_header(label="Run Control", default_open=True):
                with dpg.group():
                    dpg.add_input_int(
                        label="Number of events",
                        default_value=1000,
                        tag="num_events"
                    )
                    dpg.add_input_int(
                        label="Number of threads",
                        default_value=1,
                        min_value=1,
                        max_value=64,
                        tag="num_threads"
                    )
                    dpg.add_separator()
                    
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label="Run Simulation",
                            callback=self.simulation.run,
                            width=300,
                            height=50
                        )
                        dpg.add_button(
                            label="View Simulation",
                            callback=self.simulation.view,
                            width=300,
                            height=50
                        )
                    
                    dpg.add_progress_bar(
                        label="Progress",
                        default_value=0.0,
                        overlay="0%",
                        tag="sim_progress"
                    )

    def view_geometry(self):
        """Display the simulation geometry."""
        try:
            self.simulation.view()
        except Exception as e:
            print(f"Error viewing geometry: {e}")

    def reset_view(self):
        """Reset the geometry view."""
        try:
            # Add reset view functionality
            pass
        except Exception as e:
            print(f"Error resetting view: {e}")

    def run_simulation(self):
        """Run the simulation with current settings."""
        try:
            num_events = dpg.get_value("num_events")
            num_threads = dpg.get_value("num_threads")
            
            # Configure simulation
            self.simulation.number_of_threads = num_threads
            
            # Run simulation
            self.simulation.run(num_events)
            
        except Exception as e:
            print(f"Error running simulation: {e}")

    def stop_simulation(self):
        """Stop the current simulation."""
        try:
            # Add stop functionality
            pass
        except Exception as e:
            print(f"Error stopping simulation: {e}")