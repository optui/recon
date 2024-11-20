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
    sim.run_timing_intervals = [[i * sec, (i + 1) * sec] for i in range(n)]

    # World
    world = sim.world
    world.size = [2 * m] * 3

    # Volume
    vol = sim.add_volume("Box", "vol")
    vol.size = [10 * cm] * 3
    vol.material = "G4_WATER"
    vol.color = [0, 0.5, 1, 1]

    # Detector Plane
    detector_plane = sim.add_volume("Box", "detector_plane")
    detector_plane.size = [30 * cm, 1 * cm, 30 * cm]
    detector_plane.material = "G4_Si"
    detector_plane.translation = [0, -50 * cm, 0]

    # Source
    source = sim.add_source("GenericSource", "source")
    source.particle = "gamma"
    source.energy.mono = 60 * keV
    source.position.type = "box"
    source.position.size = [16 * mm, 16 * mm, 16 * mm]
    source.position.translation = [0, 50 * cm, 0]  # Positioned opposite the detector
    source.direction.type = "focused"
    source.direction.focus_point = [0, 45 * cm, 0]  # Center of the volume
    source.activity = 1e6 * Bq

    hc = sim.add_actor('DigitizerHitsCollectionActor', 'Hits')
    hc.attached_to = detector_plane.name
    hc.output_filename = 'hits.root'
    hc.attributes = ['TotalEnergyDeposit', 'KineticEnergy', 'PostPosition', 'RunID', 'ThreadID', 'TrackID']

    # Projections Actor
    projections_actor = sim.add_actor("DigitizerProjectionActor", "projections_actor")
    projections_actor.attached_to = detector_plane.name
    projections_actor.input_digi_collections = ["Hits"]
    projections_actor.spacing = [1 * mm, 1 * mm]
    projections_actor.size = [128, 128]
    projections_actor.output_filename = "projections.mhd"

    # Physics
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option1"

    # Define rotation angles for the volume
    angles = np.linspace(0, 360, n, endpoint=False)

    # Create rotation matrices for dynamic parameterization
    rotations = [
        Rotation.from_euler("z", angle, degrees=True).as_matrix() for angle in angles
    ]

    # Add dynamic parameterization to the volume
    vol.add_dynamic_parametrisation(rotation=rotations)


    # Run the simulation
    sim.run()

    print("All projections completed.")
