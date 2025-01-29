# editor_view.py
import dearpygui.dearpygui as dpg


class EditorView:
    def __init__(self, controller, show):
        self.controller = controller
        self.simulation_list = controller.model.volume_manager.volume_tree().split()
        self.tag = "editor"
        self.setup(show)

    def setup(self, show):
        with dpg.child_window(border=False, tag=self.tag, show=show):
            with dpg.group(horizontal=True):
                dpg.add_button(label="Back", callback=self.back)
                dpg.add_text("Simulation Editor", color=[200, 200, 200])

            dpg.add_spacer(height=5)
            dpg.add_separator()
            dpg.add_spacer(height=5)

            with dpg.group(horizontal=True):
                # Left Side: Simulation Object List
                with dpg.child_window(width=400, height=400, border=False):
                    self.setup_objects_view()

                # Right Side: Tabbed Manager View
                with dpg.child_window(width=550, height=400, border=False):
                    with dpg.tab_bar():
                        with dpg.tab(label="Volume Manager"):
                            self.setup_volume_view()
                        with dpg.tab(label="Actor Manager"):
                            self.setup_actor_view()
                        with dpg.tab(label="Source Manager"):
                            self.setup_source_view()

            dpg.add_spacer(height=5)
            dpg.add_separator()
            dpg.add_spacer(height=5)

            with dpg.group(horizontal=True):
                dpg.add_button(label="View", width=400, height=100)
                dpg.add_button(label="Run", width=400, height=100)
            
    def back(self):
        dpg.hide_item("editor")
        dpg.show_item("simulation")

    def setup_actor_view(self):
        with dpg.child_window(label="Actor Manager", width=400, height=400, border=False):
            dpg.add_text("Actor Manager")

            # Actor Type Selection
            dpg.add_combo(
                label="Actor Type",
                items=["Fluence Actor", "Digitizer Hits Collection Actor", "Digitizer Projection Actor"],
                tag="Actor Type",
                width=300,
                callback=self.update_actor_inputs
            )

            # Common fields
            dpg.add_input_text(label="Actor Name", tag="Actor Name", width=300)
            dpg.add_input_text(label="Attached Volume", tag="Attached Volume", width=300)

            # Placeholder for dynamic inputs
            with dpg.group(tag="Dynamic Actor Inputs"):
                pass

            # Submit button
            dpg.add_button(label="Create Actor", callback=self.submit_actor, width=300)

    def update_actor_inputs(self, sender, app_data):
        actor_type = dpg.get_value("Actor Type")

        # Clear previous inputs
        dpg.delete_item("Dynamic Actor Inputs", children_only=True)

        if actor_type == "Fluence Actor":
            dpg.add_input_text(label="Output File", tag="Fluence Output", width=300, parent="Dynamic Actor Inputs")
            dpg.add_combo(label="Fluence Type", items=["All", "Primary", "Secondary"], tag="Fluence Type", width=300, parent="Dynamic Actor Inputs")
            dpg.add_input_floatx(label="Resolution (x, y)", tag="Fluence Resolution", size=2, width=300, parent="Dynamic Actor Inputs")

        elif actor_type == "Digitizer Hits Collection Actor":
            dpg.add_input_text(label="Hits Collection Name", tag="Hits Collection Name", width=300, parent="Dynamic Actor Inputs")
            dpg.add_input_text(label="Output File", tag="Hits Collection Output", width=300, parent="Dynamic Actor Inputs")

        elif actor_type == "Digitizer Projection Actor":
            dpg.add_input_text(label="Projection Name", tag="Projection Name", width=300, parent="Dynamic Actor Inputs")
            dpg.add_input_text(label="Output File", tag="Projection Output", width=300, parent="Dynamic Actor Inputs")
            dpg.add_input_floatx(label="Resolution (x, y)", tag="Projection Resolution", size=2, width=300, parent="Dynamic Actor Inputs")
            
    def setup_volume_view(self):
        with dpg.child_window(label="Volume Manager", width=400, height=400, border=False):
            dpg.add_text("Volume Manager")

            dpg.add_input_text(label="Volume Name", tag="Volume Name", width=300)
            dpg.add_input_text(label="Material", tag="Volume Material", width=300)

            dpg.add_combo(
                label="Volume Type",
                items=["CSG Volume", "Image Volume"],
                tag="Volume Type",
                width=300,
                callback=self.update_volume_inputs
            )

            # Placeholder for dynamic inputs
            with dpg.group(tag="Dynamic Volume Inputs"):
                pass

            # Submit button to create the volume
            dpg.add_button(label="Create Volume", callback=self.submit_volume, width=300)

    def update_volume_inputs(self, sender, app_data):
        volume_type = dpg.get_value("Volume Type")

        # Clear previous inputs
        dpg.delete_item("Dynamic Volume Inputs", children_only=True)

        if volume_type == "CSG Volume":
            # Shape Selection
            dpg.add_combo(
                label="Shape",
                items=["Box", "Sphere", "Cylinder", "Cone", "Ellipsoid"],
                tag="Volume Shape",
                width=300,
                parent="Dynamic Volume Inputs",
                callback=self.update_shape_inputs
            )
            
            # Default shape fields (will be updated based on shape)
            self.update_shape_inputs(None, "Box")  # Load Box inputs by default

        elif volume_type == "Image Volume":
            # Image Volume Specific Fields
            dpg.add_input_text(label="Image Path", tag="Image Path", width=300, parent="Dynamic Volume Inputs")
            dpg.add_input_floatx(label="Voxel Size (x, y, z)", tag="Voxel Size", size=3, width=300, parent="Dynamic Volume Inputs")

    def update_shape_inputs(self, sender, app_data):
        shape = app_data

        # Clear previous shape-specific inputs
        dpg.delete_item("Dynamic Volume Inputs", children_only=True)

        # Reload Shape Selection
        dpg.add_combo(
            label="Shape",
            items=["Box", "Sphere", "Cylinder", "Cone", "Ellipsoid"],
            tag="Volume Shape",
            width=300,
            parent="Dynamic Volume Inputs",
            callback=self.update_shape_inputs
        )

        # Shape-Specific Inputs
        if shape == "Box":
            dpg.add_input_floatx(label="Dimensions (x, y, z)", tag="Volume Dimensions", size=3, width=300, parent="Dynamic Volume Inputs")

        elif shape == "Sphere":
            dpg.add_input_float(label="Radius", tag="Volume Radius", width=300, parent="Dynamic Volume Inputs")

        elif shape == "Cylinder":
            dpg.add_input_float(label="Radius", tag="Cylinder Radius", width=300, parent="Dynamic Volume Inputs")
            dpg.add_input_float(label="Height", tag="Cylinder Height", width=300, parent="Dynamic Volume Inputs")

        elif shape == "Cone":
            dpg.add_input_float(label="Base Radius", tag="Cone Base Radius", width=300, parent="Dynamic Volume Inputs")
            dpg.add_input_float(label="Top Radius", tag="Cone Top Radius", width=300, parent="Dynamic Volume Inputs")
            dpg.add_input_float(label="Height", tag="Cone Height", width=300, parent="Dynamic Volume Inputs")

        elif shape == "Ellipsoid":
            dpg.add_input_floatx(label="Radii (x, y, z)", tag="Ellipsoid Radii", size=3, width=300, parent="Dynamic Volume Inputs")

        # Common Placement Field
        dpg.add_input_floatx(label="Placement (x, y, z)", tag="Volume Placement", size=3, width=300, parent="Dynamic Volume Inputs")

    def setup_source_view(self):
        with dpg.child_window(label="Source Manager", width=400, height=400, border=False):
            dpg.add_text("Source Manager")

            # Source Type Selection
            dpg.add_combo(
                label="Source Type",
                items=["Point Source", "Volume Source", "Surface Source"],
                tag="Source Type",
                width=300,
                callback=self.update_source_inputs
            )

            # Common fields
            dpg.add_input_text(label="Source Name", tag="Source Name", width=300)
            dpg.add_combo(
                label="Particle Type",
                items=["gamma", "e-", "e+"],  # Common choices
                tag="Particle Type",
                width=300
            )
            dpg.add_input_float(label="Energy (MeV)", tag="Source Energy", width=300)

            # Placeholder for dynamic inputs
            with dpg.group(tag="Dynamic Source Inputs"):
                pass

            # Submit button
            dpg.add_button(label="Create Source", callback=self.submit_source, width=300)

    def update_source_inputs(self, sender, app_data):
        source_type = dpg.get_value("Source Type")

        # Clear previous inputs
        dpg.delete_item("Dynamic Source Inputs", children_only=True)

        # Reload the Source Type Selection (keeps the dropdown visible)
        dpg.add_combo(
            label="Source Type",
            items=["Point Source", "Volume Source", "Surface Source"],
            tag="Source Type",
            width=300,
            parent="Dynamic Source Inputs",
            callback=self.update_source_inputs
        )

        if source_type == "Point Source":
            dpg.add_input_floatx(label="Position (x, y, z)", tag="Point Source Position", size=3, width=300, parent="Dynamic Source Inputs")

        elif source_type == "Volume Source":
            dpg.add_combo(
                label="Shape",
                items=["Box", "Sphere", "Cylinder"],
                tag="Volume Source Shape",
                width=300,
                parent="Dynamic Source Inputs",
                callback=self.update_volume_source_inputs
            )
            self.update_volume_source_inputs(None, "Box")  # Load Box inputs by default

        elif source_type == "Surface Source":
            dpg.add_input_floatx(label="Surface Position (x, y, z)", tag="Surface Source Position", size=3, width=300, parent="Dynamic Source Inputs")
            dpg.add_combo(
                label="Surface Type",
                items=["Plane", "Sphere", "Cylinder"],
                tag="Surface Source Type",
                width=300,
                parent="Dynamic Source Inputs"
            )

    def setup_objects_view(self):
        with dpg.child_window(label="Simulation Objects", width=400, height=400, border=False):
            dpg.add_text("Simulation Objects")
            
            dpg.add_listbox(
                items=self.simulation_list,
                tag="Simulation Listbox",
                width=300,
                num_items=8,
                callback=self.on_select_object
            )
            
            dpg.add_separator()
            dpg.add_text("Object Details:")
            dpg.add_text("", tag="Object Details", wrap=350)

    def on_select_object(self, sender, app_data):
        selected_object = app_data
        details = self.controller.model.volume_manager.get_volume(selected_object)
        
        dpg.set_value("Object Details", details)


    def submit_actor(self):
        pass
    
    def submit_volume(self):
        pass
    
    def submit_source(self):
        pass