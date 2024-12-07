import numpy as np
import opengate as gate
from scipy.spatial.transform import Rotation

# Units
m = gate.g4_units.m
cm = gate.g4_units.cm
mm = gate.g4_units.mm
nm = gate.g4_units.nm
keV = gate.g4_units.keV
sec = gate.g4_units.second
deg = gate.g4_units.deg
Bq = gate.g4_units.Bq

if __name__ == "__main__":
    # Initialize the simulation
    sim = gate.Simulation()

    # Simulation settings
    sim.g4_verbose = False
    sim.g4_verbose_level = 1
    sim.visu = False
    sim.random_engine = "MersenneTwister"
    sim.random_seed = "auto"
    sim.number_of_threads = 1
    sim.progress_bar = True
    sim.output_dir = "./output"

    # World
    world = sim.world
    world.size = [2 * m] * 3

    # Volume
    vol = sim.add_volume("Box", "vol")
    vol.size = [20 * cm] * 3
    vol.translation = [0 * cm, 0 * cm, 0 * cm]
    vol.material = "G4_WATER"

    # Detector Plane
    detector_plane = sim.add_volume("Box", "CBCT_detector_plane")
    detector_plane.size = [10 * mm, 500 * mm, 500 * mm]
    detector_plane.translation = [-536 * mm, 0, 0]
    detector_plane.material = "G4_AIR"
    detector_plane.color = [1, 0, 0, 1]

    # Source
    source = sim.add_source("GenericSource", "source")
    source.particle = "gamma"
    source.energy.mono = 80 * keV
    source.position.type = "box"
    source.position.size = [1 * nm, 2 * 8 * mm, 2 * 8 * mm]
    source.position.translation = [1000 * mm, 0, 0]
    source.direction.type = "focused"
    source.direction.focus_point = [950 * mm, 0, 0]
    source.activity = 1e2 * Bq

    # Physics
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option1"
    sim.physics_manager.set_production_cut("world", "all", 10 * mm)

    # Dynamic rotation parameters
    n = 180  # Number of rotation steps
    total_time = 10 * sec  # Total simulation time
    angles = np.linspace(0, 360, n, endpoint=False)  # Full rotation (360°)
    interval = total_time / n  # Time per step

    for i, angle in enumerate(angles):
        # Update rotation
        rotation_matrix = Rotation.from_euler('z', angle, degrees=True).as_matrix()
        vol.rotation = rotation_matrix

        # Remove the previous actor (if it exists)
        actor_name = f"fluence_{i-1}" if i > 0 else None
        if actor_name in sim.actor_manager.actors:
            sim.actor_manager.actors.pop(actor_name)

        # Add a new fluence actor for this step
        fluence = sim.add_actor("FluenceActor", f"fluence_{i}")
        fluence.attached_to = detector_plane
        fluence.spacing = [10 * cm, 0.5 * cm, 0.5 * cm]
        fluence.size = [1, 256, 256]
        fluence.output_filename = f"fluence_{i}.mhd"

        # Run the simulation for this configuration
        sim.run(start_new_process=True)
