import numpy as np
import opengate as gate
from scipy.spatial.transform import Rotation
import os

# Units for convenience
m = gate.g4_units.m
cm = gate.g4_units.cm
mm = gate.g4_units.mm
keV = gate.g4_units.keV
deg = gate.g4_units.deg
Bq = gate.g4_units.Bq

def run_simulation(angle_deg, z_translation_cm, idx):
    sim = gate.Simulation()

    sim.visu = False
    sim.verbose_level = 'INFO'

    # Define world
    sim.world.size = [2 * m, 2 * m, 2 * m]

    # Add a water volume
    vol = sim.add_volume("Box", "vol")
    vol.size = [10 * cm, 10 * cm, 10 * cm]
    vol.material = "G4_WATER"
    vol.color = [0, 0.5, 1, 1]

    # Apply rotation and translation to the volume
    rotation_matrix = Rotation.from_euler('z', angle_deg, degrees=True).as_matrix()
    vol.rotation = rotation_matrix
    vol.translation = [0, 0, z_translation_cm * cm]

    # Add a detector volume
    detector = sim.add_volume("Box", "detector")
    detector.material = "G4_Si"
    detector.size = [20 * cm, 5 * mm, 20 * cm]
    detector.translation = [0, -0.5 * m, 0]

    # Add a gamma source
    source = sim.add_source("GenericSource", "parallel_source")
    source.particle = "gamma"
    source.activity = 1e5 * Bq
    source.energy.mono = 60 * keV
    source.position.type = "box"
    source.position.size = [20 * cm, 1 * mm, 1 * mm]
    source.position.translation = [0, 0.5 * m, z_translation_cm * cm]  # Align with object
    source.direction.type = "momentum"
    source.direction.momentum = [0, -1, 0]

    stats_actor = sim.add_actor("SimulationStatisticsActor", "Stats")
    stats_actor.output_filename = f"output/simulation_stats_{idx}.txt"

    # Add actors for digitization and projection
    hits_actor = sim.add_actor("DigitizerHitsCollectionActor", "Hits")
    hits_actor.attached_to = detector.name
    hits_actor.attributes = ['TotalEnergyDeposit', 'PostPosition', 'GlobalTime']
    hits_actor.output_filename = f'output/hits_{idx}.root'

    proj_actor = sim.add_actor("DigitizerProjectionActor", "Projection")
    proj_actor.attached_to = detector.name
    proj_actor.input_digi_collections = ["Hits"]
    proj_actor.spacing = [1 * mm, 1 * mm]
    proj_actor.size = [200, 200]
    proj_actor.origin_as_image_center = True
    proj_actor.output_filename = f'output/projections_{idx}.mhd'

    # Run the simulation
    print(f"Running simulation {idx}: Rotation {angle_deg} degrees, z-translation {z_translation_cm} cm")
    sim.run(start_new_process=True)

if __name__ == "__main__":
    # Ensure output directory exists
    if not os.path.exists('output'):
        os.makedirs('output')

    # Define rotations
    angular_step = 2  # degrees per step
    angles = np.arange(0, 180, angular_step)

    # Define helical translation
    pitch = 10  # cm (total translation over 360 degrees)
    num_steps = len(angles)
    z_step = pitch / (360 / angular_step)  # cm per step

    # Total translation distance
    start_z = -pitch / 2  # cm
    z_positions = [start_z + i * z_step for i in range(num_steps)]

    idx = 0
    for angle_deg, z_translation_cm in zip(angles, z_positions):
        run_simulation(angle_deg, z_translation_cm, idx)
        idx += 1

    print("All simulations completed.")
