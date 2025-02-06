import dearpygui.dearpygui as dpg
import numpy as np
from scipy.spatial.transform import Rotation
from utils import Observer

class VolumeManager(Observer):
    def __init__(self, controller):
        self.controller = controller
        self.current_type = "Box"
        self.selected_volume = None
        controller.attach(self)
        self._setup()

    def _setup(self):
        with dpg.child_window(label="Volume Manager", width=450, height=600, border=False):
          
            with dpg.collapsing_header(label="Basic Properties", default_open=True):
                dpg.add_input_text(label="Volume Name", tag="Volume Name", width=300)
                
              
                volume_types = ["Box", "Sphere"]
                dpg.add_combo(
                    label="Volume Type",
                    items=volume_types,
                    default_value="Box",
                    tag="Volume Type",
                    width=300,
                    callback=self.on_type_change
                )
                
              
                materials = ["G4_AIR", "G4_WATER", "G4_BONE_COMPACT_ICRU"]
                dpg.add_combo(
                    label="Material",
                    items=materials,
                    default_value="G4_AIR",
                    tag="Volume Material",
                    width=300
                )

          
            with dpg.collapsing_header(label="Shape Parameters", default_open=True):
              
                with dpg.group(tag="box_params"):
                    dpg.add_input_floatx(
                        label="Size (mm)",
                        tag="Box Size",
                        size=3,
                        default_value=[10.0, 10.0, 10.0],
                        width=300
                    )

              
                with dpg.group(tag="sphere_params", show=False):
                    dpg.add_input_float(
                        label="Outer Radius (mm)",
                        tag="Sphere Rmax",
                        default_value=1.0,
                        width=300
                    )
                    dpg.add_input_float(
                        label="Inner Radius (mm)",
                        tag="Sphere Rmin",
                        default_value=0.0,
                        width=300
                    )
                    dpg.add_input_float(
                        label="Phi Start (rad)",
                        tag="Sphere Sphi",
                        default_value=0.0,
                        width=300
                    )
                    dpg.add_input_float(
                        label="Delta Phi (rad)",
                        tag="Sphere Dphi",
                        default_value=6.283185307179586,
                        width=300
                    )
                    dpg.add_input_float(
                        label="Theta Start (rad)",
                        tag="Sphere Stheta",
                        default_value=0.0,
                        width=300
                    )
                    dpg.add_input_float(
                        label="Delta Theta (rad)",
                        tag="Sphere Dtheta",
                        default_value=3.141592653589793,
                        width=300
                    )

          
            with dpg.collapsing_header(label="Position", default_open=True):
                dpg.add_input_floatx(
                    label="Translation (mm)",
                    tag="Volume Translation",
                    size=3,
                    default_value=[0.0, 0.0, 0.0],
                    width=300
                )

            with dpg.collapsing_header(label="Rotation", default_open=True):
                dpg.add_input_floatx(
                    label="Rotation (degrees)",
                    tag="Volume Rotation Euler",
                    size=3,
                    default_value=[0.0, 0.0, 0.0],
                    callback=self.update_rotation_matrix,
                    width=300
                )
                
                with dpg.group(horizontal=False):
                    dpg.add_text("Rotation Matrix (read-only):")
                    dpg.add_text("", tag="Rotation Matrix Display")
            
          
            with dpg.group(horizontal=True):
                dpg.add_button(label="Create/Update", callback=self.submit_volume, width=145)
                dpg.add_button(label="Clear", callback=self.clear_fields, width=145)

    def on_type_change(self, sender, app_data):
        """Handle volume type change."""
        self.current_type = app_data
        
      
        if self.current_type == "Box":
            dpg.configure_item("box_params", show=True)
            dpg.configure_item("sphere_params", show=False)
        elif self.current_type == "Sphere":
            dpg.configure_item("box_params", show=False)
            dpg.configure_item("sphere_params", show=True)

    def get_volume_properties(self):
        """Get properties based on current volume type."""
        properties = {
            "type": self.current_type,
            "material": dpg.get_value("Volume Material"),
            "translation": list(dpg.get_value("Volume Translation"))[:3],
            "rotation": Rotation.from_euler('xyz', 
                list(dpg.get_value("Volume Rotation Euler"))[:3], 
                degrees=True).as_matrix()
        }

      
        if self.current_type == "Box":
            properties["size"] = list(dpg.get_value("Box Size"))[:3]
        elif self.current_type == "Sphere":
            properties.update({
                "rmax": dpg.get_value("Sphere Rmax"),
                "rmin": dpg.get_value("Sphere Rmin"),
                "sphi": dpg.get_value("Sphere Sphi"),
                "dphi": dpg.get_value("Sphere Dphi"),
                "stheta": dpg.get_value("Sphere Stheta"),
                "dtheta": dpg.get_value("Sphere Dtheta")
            })

        return properties

    def submit_volume(self):
        name = dpg.get_value("Volume Name")
        if not name:
            return
            
        properties = self.get_volume_properties()
        
        # If we're editing an existing volume
        if self.selected_volume:
            # If name hasn't changed, just update properties
            if name == self.selected_volume:
                self.controller.update(name, properties)
            # If name has changed, handle rename
            else:
                # First delete the old volume
                self.controller.delete(self.selected_volume)
                # Then create new volume with new name
                self.controller.create(name, properties)
        else:
            # Creating a new volume
            self.controller.create(name, properties)
        
        # Clear selection and fields
        self.selected_volume = None
        self.clear_fields()

    def clear_fields(self):
        """Reset all fields to defaults."""
        self.selected_volume = None
        dpg.set_value("Volume Name", "")
        dpg.set_value("Volume Type", "Box")
        dpg.set_value("Volume Material", "G4_AIR")
        dpg.set_value("Volume Translation", [0.0, 0.0, 0.0])
        dpg.set_value("Volume Rotation Euler", [0.0, 0.0, 0.0])
        
      
        dpg.set_value("Box Size", [10.0, 10.0, 10.0])
        dpg.set_value("Sphere Rmax", 1.0)
        dpg.set_value("Sphere Rmin", 0.0)
        dpg.set_value("Sphere Sphi", 0.0)
        dpg.set_value("Sphere Dphi", 6.283185307179586)
        dpg.set_value("Sphere Stheta", 0.0)
        dpg.set_value("Sphere Dtheta", 3.141592653589793)
        
        self.update_rotation_matrix(None, None)
        self.on_type_change(None, "Box")

    def update_rotation_matrix(self, sender, app_data):
        """Update rotation matrix when Euler angles change."""
        try:
          
            euler_angles = list(dpg.get_value("Volume Rotation Euler"))[:3]
            rotation_matrix = Rotation.from_euler('xyz', euler_angles, degrees=True).as_matrix()
            
          
            matrix_text = f"[{rotation_matrix[0,0]:.3f} {rotation_matrix[0,1]:.3f} {rotation_matrix[0,2]:.3f}]\n"
            matrix_text += f"[{rotation_matrix[1,0]:.3f} {rotation_matrix[1,1]:.3f} {rotation_matrix[1,2]:.3f}]\n"
            matrix_text += f"[{rotation_matrix[2,0]:.3f} {rotation_matrix[2,1]:.3f} {rotation_matrix[2,2]:.3f}]"
            
            dpg.set_value("Rotation Matrix Display", matrix_text)
        except Exception as e:
            dpg.set_value("Rotation Matrix Display", "Error calculating rotation matrix")
            print(f"Rotation error: {e}")

    def set_volume_properties(self, volume_data):
        """Set all fields based on volume data."""
        if not volume_data:
            self.clear_fields()
            return

      
        self.selected_volume = volume_data.get("name", "")
        
      
        dpg.set_value("Volume Name", self.selected_volume)
        dpg.set_value("Volume Material", volume_data.get("material", "G4_AIR"))
        
      
        volume_type = volume_data.get("type", "Box")
        dpg.set_value("Volume Type", volume_type)
        self.on_type_change(None, volume_type)
        
      
        translation = volume_data.get("translation", [0.0, 0.0, 0.0])
        dpg.set_value("Volume Translation", translation[:3])
        
      
        try:
            rotation_matrix = volume_data.get("rotation", np.eye(3))
            euler_angles = Rotation.from_matrix(rotation_matrix).as_euler('xyz', degrees=True)
            dpg.set_value("Volume Rotation Euler", euler_angles.tolist()[:3])
            self.update_rotation_matrix(None, None)
        except Exception as e:
            print(f"Error setting rotation: {e}")
            dpg.set_value("Volume Rotation Euler", [0.0, 0.0, 0.0])
        
      
        if volume_type == "Box":
            size = volume_data.get("size", [10.0, 10.0, 10.0])
            dpg.set_value("Box Size", size[:3])
        elif volume_type == "Sphere":
            dpg.set_value("Sphere Rmax", volume_data.get("rmax", 1.0))
            dpg.set_value("Sphere Rmin", volume_data.get("rmin", 0.0))
            dpg.set_value("Sphere Sphi", volume_data.get("sphi", 0.0))
            dpg.set_value("Sphere Dphi", volume_data.get("dphi", 6.283185307179586))
            dpg.set_value("Sphere Stheta", volume_data.get("stheta", 0.0))
            dpg.set_value("Sphere Dtheta", volume_data.get("dtheta", 3.141592653589793))

    def update(self, event, *args, **kwargs):
        """Handle updates from controller."""
        if event in ["volume_created", "volume_updated", "volume_deleted"]:
            self.clear_fields()
