from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QGroupBox, QGridLayout
)

class VisualizationTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Visualization Settings Group
        vis_group = QGroupBox("Visualization Settings")
        vis_layout = QGridLayout()
        
        vis_layout.addWidget(QLabel("View Mode:"), 0, 0)
        self.view_mode = QComboBox()
        self.view_mode.addItems(["2D", "3D"])
        vis_layout.addWidget(self.view_mode, 0, 1)

        vis_layout.addWidget(QLabel("Color Map:"), 1, 0)
        self.color_map = QComboBox()
        self.color_map.addItems(["Gray", "Hot", "Jet"])
        vis_layout.addWidget(self.color_map, 1, 1)

        vis_group.setLayout(vis_layout)
        layout.addWidget(vis_group)

        # View Button
        self.view_button = QPushButton("View Results")
        layout.addWidget(self.view_button)

        # Set layout
        self.setLayout(layout)
