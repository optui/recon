from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QGroupBox, QGridLayout, QSpinBox, QDoubleSpinBox
)

class ReconstructionTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Geometry Settings Group
        geom_group = QGroupBox("Geometry Settings")
        geom_layout = QGridLayout()

        geom_layout.addWidget(QLabel("Detector Size (mm):"), 0, 0)
        self.detector_size = QLineEdit("500, 500")
        geom_layout.addWidget(self.detector_size, 0, 1)

        geom_layout.addWidget(QLabel("Source-to-Detector Distance (mm):"), 1, 0)
        self.source_detector_distance = QDoubleSpinBox()
        self.source_detector_distance.setRange(0, 2000)
        self.source_detector_distance.setValue(1000)
        geom_layout.addWidget(self.source_detector_distance, 1, 1)

        geom_layout.addWidget(QLabel("Number of Projections:"), 2, 0)
        self.num_projections = QSpinBox()
        self.num_projections.setRange(1, 360)
        self.num_projections.setValue(180)
        geom_layout.addWidget(self.num_projections, 2, 1)

        geom_group.setLayout(geom_layout)
        layout.addWidget(geom_group)

        # FBP Settings Group
        fbp_group = QGroupBox("FBP Settings")
        fbp_layout = QGridLayout()

        fbp_layout.addWidget(QLabel("Filter Type:"), 0, 0)
        self.filter_type = QComboBox()
        self.filter_type.addItems(["Ram-Lak", "Shepp-Logan", "Hann"])
        fbp_layout.addWidget(self.filter_type, 0, 1)

        fbp_layout.addWidget(QLabel("Cutoff Frequency:"), 1, 0)
        self.cutoff_frequency = QDoubleSpinBox()
        self.cutoff_frequency.setRange(0, 1)
        self.cutoff_frequency.setSingleStep(0.01)
        self.cutoff_frequency.setValue(0.5)
        fbp_layout.addWidget(self.cutoff_frequency, 1, 1)

        fbp_group.setLayout(fbp_layout)
        layout.addWidget(fbp_group)

        # Preprocessing Settings Group
        preprocess_group = QGroupBox("Preprocessing Settings")
        preprocess_layout = QGridLayout()

        preprocess_layout.addWidget(QLabel("Gain Correction Factor:"), 0, 0)
        self.gain_correction = QDoubleSpinBox()
        self.gain_correction.setRange(0, 10)
        self.gain_correction.setValue(1.0)
        preprocess_layout.addWidget(self.gain_correction, 0, 1)

        preprocess_layout.addWidget(QLabel("Bad Pixel Threshold:"), 1, 0)
        self.bad_pixel_threshold = QSpinBox()
        self.bad_pixel_threshold.setRange(0, 255)
        self.bad_pixel_threshold.setValue(50)
        preprocess_layout.addWidget(self.bad_pixel_threshold, 1, 1)

        preprocess_layout.addWidget(QLabel("Deblurring Kernel Size:"), 2, 0)
        self.deblurring_kernel_size = QSpinBox()
        self.deblurring_kernel_size.setRange(1, 10)
        self.deblurring_kernel_size.setValue(3)
        preprocess_layout.addWidget(self.deblurring_kernel_size, 2, 1)

        preprocess_group.setLayout(preprocess_layout)
        layout.addWidget(preprocess_group)

        # Run Button
        self.run_button = QPushButton("Run Reconstruction")
        layout.addWidget(self.run_button)

        # Set layout
        self.setLayout(layout)
