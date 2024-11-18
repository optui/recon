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

if __name__ == "__main__":
    sim = gate.Simulation()

    # Simulation parameters
    sim.visu = False
    sim.verbose_level = 'DEBUG'

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
    source.activity = 1e5 * Bq
    source.energy.mono = 60 * keV
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
    proj_actor.size = [200, 200]
    proj_actor.origin_as_image_center = True

    # Dynamic Rotation
    angular_step = 5
    angles = np.arange(0, 180, angular_step)

    # Compute rotation matrices
    rotations = [Rotation.from_euler('z', angle, degrees=True).as_matrix() for angle in angles]

    # Simulation timing intervals parameter
    sim.run_timing_intervals = [[i * sec, (i + 1) * sec] for i in range(len(rotations))]

    for idx, rotation in enumerate(rotations):
        # Rotate the volume
        vol.rotation = rotation

        proj_actor.output_filename = f'output/projections{idx}.mhd'

        # Run for current interval
        sim.run_timing_intervals = [[idx * sec, (idx + 1) * sec]]
        sim.run(start_new_process=True)
