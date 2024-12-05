from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QGroupBox, QGridLayout, QSpinBox, QDoubleSpinBox
)

class SimulationTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Simulation Settings Group
        sim_group = QGroupBox("Simulation Settings")
        sim_layout = QGridLayout()
        
        # Basic settings
        sim_layout.addWidget(QLabel("Simulation Name:"), 0, 0)
        self.name_input = QLineEdit("simulation")
        sim_layout.addWidget(self.name_input, 0, 1)

        sim_layout.addWidget(QLabel("Verbose Level:"), 1, 0)
        self.verbose_level = QComboBox()
        self.verbose_level.addItems(["0", "1", "2"])
        sim_layout.addWidget(self.verbose_level, 1, 1)

        sim_layout.addWidget(QLabel("Visualization:"), 2, 0)
        self.visu = QComboBox()
        self.visu.addItems(["False", "True"])
        sim_layout.addWidget(self.visu, 2, 1)

        sim_layout.addWidget(QLabel("Random Engine:"), 3, 0)
        self.random_engine = QComboBox()
        self.random_engine.addItems(["MersenneTwister", "Ranlux64"])
        sim_layout.addWidget(self.random_engine, 3, 1)

        sim_layout.addWidget(QLabel("Random Seed:"), 4, 0)
        self.random_seed = QLineEdit("auto")
        sim_layout.addWidget(self.random_seed, 4, 1)

        sim_layout.addWidget(QLabel("Number of Threads:"), 5, 0)
        self.threads = QSpinBox()
        self.threads.setRange(1, 16)
        self.threads.setValue(1)
        sim_layout.addWidget(self.threads, 5, 1)

        sim_group.setLayout(sim_layout)
        layout.addWidget(sim_group)

        # World Configuration Group
        world_group = QGroupBox("World Configuration")
        world_layout = QGridLayout()

        world_layout.addWidget(QLabel("World Size (m):"), 0, 0)
        self.world_size = QDoubleSpinBox()
        self.world_size.setRange(0, 10)
        self.world_size.setValue(2)
        world_layout.addWidget(self.world_size, 0, 1)

        world_layout.addWidget(QLabel("World Material:"), 1, 0)
        self.world_material = QLineEdit("G4_AIR")
        world_layout.addWidget(self.world_material, 1, 1)

        world_group.setLayout(world_layout)
        layout.addWidget(world_group)

        # Volume Configuration Group
        volume_group = QGroupBox("Volume Configuration")
        volume_layout = QGridLayout()

        volume_layout.addWidget(QLabel("Volume Size (cm):"), 0, 0)
        self.volume_size = QDoubleSpinBox()
        self.volume_size.setRange(0, 100)
        self.volume_size.setValue(20)
        volume_layout.addWidget(self.volume_size, 0, 1)

        volume_layout.addWidget(QLabel("Volume Material:"), 1, 0)
        self.volume_material = QLineEdit("G4_WATER")
        volume_layout.addWidget(self.volume_material, 1, 1)

        volume_group.setLayout(volume_layout)
        layout.addWidget(volume_group)

        # Detector Group
        detector_group = QGroupBox("Detector Configuration")
        detector_layout = QGridLayout()

        detector_layout.addWidget(QLabel("Detector Size (mm):"), 0, 0)
        self.detector_size = QLineEdit("10, 500, 500")
        detector_layout.addWidget(self.detector_size, 0, 1)

        detector_layout.addWidget(QLabel("Detector Translation (mm):"), 1, 0)
        self.detector_translation = QLineEdit("-536, 0, 0")
        detector_layout.addWidget(self.detector_translation, 1, 1)

        detector_layout.addWidget(QLabel("Detector Material:"), 2, 0)
        self.detector_material = QLineEdit("G4_AIR")
        detector_layout.addWidget(self.detector_material, 2, 1)

        detector_group.setLayout(detector_layout)
        layout.addWidget(detector_group)

        # Source Group
        source_group = QGroupBox("Source Configuration")
        source_layout = QGridLayout()

        source_layout.addWidget(QLabel("Particle Type:"), 0, 0)
        self.particle_type = QLineEdit("gamma")
        source_layout.addWidget(self.particle_type, 0, 1)

        source_layout.addWidget(QLabel("Energy (keV):"), 1, 0)
        self.source_energy = QDoubleSpinBox()
        self.source_energy.setRange(0, 1000)
        self.source_energy.setValue(80)
        source_layout.addWidget(self.source_energy, 1, 1)

        source_layout.addWidget(QLabel("Position Size (nm, mm):"), 2, 0)
        self.position_size = QLineEdit("1, 16, 16")
        source_layout.addWidget(self.position_size, 2, 1)

        source_layout.addWidget(QLabel("Position Translation (mm):"), 3, 0)
        self.position_translation = QLineEdit("1000, 0, 0")
        source_layout.addWidget(self.position_translation, 3, 1)

        source_layout.addWidget(QLabel("Direction Focus Point (mm):"), 4, 0)
        self.focus_point = QLineEdit("950, 0, 0")
        source_layout.addWidget(self.focus_point, 4, 1)

        source_layout.addWidget(QLabel("Activity (Bq):"), 5, 0)
        self.activity = QDoubleSpinBox()
        self.activity.setRange(0, 1e6)
        self.activity.setValue(1e2)
        source_layout.addWidget(self.activity, 5, 1)

        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        # View Simulation Button
        self.view_button = QPushButton("View Simulation")
        layout.addWidget(self.view_button)

        # Run Simulation Button
        self.run_button = QPushButton("Run Simulation")
        layout.addWidget(self.run_button)

        # Set layout
        self.setLayout(layout)
