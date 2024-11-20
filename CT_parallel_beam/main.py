import numpy as np
import opengate as gate
from scipy.spatial.transform import Rotation

# Units
m = gate.g4_units.m
cm = gate.g4_units.cm
mm = gate.g4_units.mm
keV = gate.g4_units.keV
sec = gate.g4_units.second
deg = gate.g4_units.deg
Bq = gate.g4_units.Bq

# Number of angles
n = 180

if __name__ == "__main__":
    sim = gate.Simulation()

    # Simulation parameters
    sim.visu = False
    sim.verbose_level = 'INFO'
    sim.run_timing_intervals = [[i * sec, (i + 1) * sec] for i in range(n)]
    sim.number_of_threads = 1
    sim.progress_bar = True

    # World
    world = sim.world
    world.size = [2 * m] * 3

    # Volume
    vol = sim.add_volume("Box", "vol")
    vol.size = [10 * cm] * 3
    vol.material = "G4_WATER"
    vol.color = [0, 0.5, 1, 1]

    # Detector
    detector = sim.add_volume("Box", "detector")
    detector.material = "G4_Si"
    detector.size = [20 * cm, 5 * mm, 20 * cm]
    detector.translation = [0, -0.5 * m, 0]

    # Source
    source = sim.add_source("GenericSource", "parallel_source")
    source.particle = "gamma"
    source.activity = 1e6 * Bq
    source.energy.mono = 80 * keV
    source.position.type = "box"
    source.position.size = [20 * cm, 1 * mm, 1 * mm]
    source.position.translation = [0, 0.5 * m, 0]
    source.direction.type = "momentum"
    source.direction.momentum = [0, -1, 0]

    # Simulation Statistics
    stats_actor = sim.add_actor("SimulationStatisticsActor", "Stats")
    stats_actor.output_filename = "output/simulation_stats.txt"

    # Hits Collection
    hits_actor = sim.add_actor("DigitizerHitsCollectionActor", "Hits")
    hits_actor.attached_to = detector.name
    hits_actor.attributes = ['TotalEnergyDeposit', 'PostPosition', 'GlobalTime']
    hits_actor.output_filename = 'output/hits.root'

    # Projection
    proj_actor = sim.add_actor("DigitizerProjectionActor", "Projection")
    proj_actor.attached_to = detector.name
    proj_actor.input_digi_collections = ["Hits"]
    proj_actor.spacing = [1 * mm, 1 * mm]
    proj_actor.size = [256, 256]
    proj_actor.origin_as_image_center = True
    proj_actor.output_filename = 'output/projection.mhd'

    angles = np.linspace(0, 180, n)  # Rotate from 0° to 180° over n runs
    rotations = [Rotation.from_euler('z', angle, degrees=True).as_matrix() for angle in angles]

    # Apply dynamic rotation to the "vol" volume
    vol.add_dynamic_parametrisation(rotation=rotations)

    # Run the simulation
    sim.run()
