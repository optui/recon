import numpy as np
import opengate as gate
from scipy.spatial.transform import Rotation
from pathlib import Path

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

    n = 10  # Number of projections

    # Simulation settings
    sim.g4_verbose = False
    sim.g4_verbose_level = 1
    sim.visu = False
    sim.random_engine = "MersenneTwister"
    sim.random_seed = "auto"
    sim.number_of_threads = 1  # Single thread for consistency
    sim.progress_bar = True
    sim.output_dir = "./output"
    sim.run_timing_intervals = [[0 * sec, 1 * sec]]

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
    source.energy.mono = 60 * keV
    source.position.type = "box"
    source.position.size = [1 * nm, 2 * 8 * mm, 2 * 8 * mm]
    source.position.translation = [1000 * mm, 0, 0]
    source.direction.type = "focused"
    source.direction.focus_point = [950 * mm, 0, 0]
    source.activity = 1e6 * Bq

    # Physics
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option1"
    sim.physics_manager.set_production_cut("world", "all", 10 * mm)

    # Define rotation angles for the volume
    angles = np.linspace(0, 360, n, endpoint=False)

    for i, angle in enumerate(angles):
        rotation_matrix = Rotation.from_euler("z", angle, degrees=True).as_matrix()
        vol.rotation = rotation_matrix
        # Set a unique filename for each projection
        filename = f"fluence_projection_{i:03d}.mhd"

        # Add FluenceActor for this projection
        detector_actor = sim.add_actor("FluenceActor", f"detector_actor_{i}")
        detector_actor.attached_to = detector_plane
        detector_actor.output_filename = filename
        detector_actor.spacing = [1 * cm, 0.5 * cm, 0.5 * cm]
        detector_actor.size = [1, 100, 100]
        detector_actor.output_coordinate_system = "global"

        # Run the simulation for this projection
        sim.run(start_new_process=True)
