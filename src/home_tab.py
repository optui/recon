from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QGroupBox, QPushButton

class HomeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        
        welcome_label = QLabel("Welcome to the CT Simulation & Reconstruction Tool!")
        layout.addWidget(welcome_label, 0, 0, 1, 2)  # Span across two columns
        
        # Create a group box for quick actions
        quick_actions_group = QGroupBox("Quick Actions")
        quick_actions_layout = QGridLayout()
        
        new_project_button = QPushButton("New Project")
        open_project_button = QPushButton("Open Project")
        
        quick_actions_layout.addWidget(new_project_button, 0, 0)
        quick_actions_layout.addWidget(open_project_button, 0, 1)
        
        quick_actions_group.setLayout(quick_actions_layout)
        layout.addWidget(quick_actions_group, 1, 0, 1, 2)
        
        self.setLayout(layout)