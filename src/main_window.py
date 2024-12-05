from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QMenuBar, QStatusBar, QMessageBox, QApplication
)
from PySide6.QtCore import Qt
from simulation_tab import SimulationTab
from reconstruction_tab import ReconstructionTab
from visualization_tab import VisualizationTab
from home_tab import HomeTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CT Simulation & Reconstruction")
        self.resize(1200, 800)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Add tabs
        self.home_tab = HomeTab()
        self.simulation_tab = SimulationTab()
        self.reconstruction_tab = ReconstructionTab()
        self.visualization_tab = VisualizationTab()
        
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.simulation_tab, "Simulation Setup")
        self.tabs.addTab(self.reconstruction_tab, "Reconstruction")
        self.tabs.addTab(self.visualization_tab, "Visualization")
        
        # Connect signals
        self.tabs.currentChanged.connect(self.on_tab_change)
        if hasattr(self.simulation_tab, 'run_button'):
            self.simulation_tab.run_button.clicked.connect(self.on_simulation_run)

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New", self.new_project)
        file_menu.addAction("Open", self.open_project)
        file_menu.addAction("Save", self.save_project)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)

    def on_tab_change(self, index):
        tab_name = self.tabs.tabText(index)
        self.statusBar.showMessage(f"Switched to {tab_name}")

    def on_simulation_run(self):
        self.statusBar.showMessage("Running simulation...")
        # Add simulation logic here

    def new_project(self):
        self.statusBar.showMessage("Creating new project...")
        # Add new project logic

    def open_project(self):
        self.statusBar.showMessage("Opening project...")
        # Add open project logic

    def save_project(self):
        self.statusBar.showMessage("Saving project...")
        # Add save project logic

    def show_about(self):
        QMessageBox.about(
            self,
            "About CT Simulation & Reconstruction",
            "A graphical interface for:\n\n"
            "1. Setting up and running OpenGATE CT simulations\n"
            "2. Performing CT reconstruction using LEAP\n"
            "3. Visualizing results"
        )
