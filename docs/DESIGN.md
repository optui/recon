# Design

## Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Components](#components)
  - [Simulation Setup](#simulation-setup)
  - [Reconstruction Setup](#reconstruction-setup)
  - [Visualization](#visualization)
- [Data Flow](#data-flow)
- [Technologies](#technologies)

## Overview

A graphical interface for:

1. Setting up and running OpenGATE CT simulations
2. Performing CT reconstruction using LEAP
3. Visualizing results

## Architecture

Three-tier architecture:

1. Frontend: GUI implementation
2. Middle layer: Simulation/reconstruction controller
3. Backend: OpenGATE and LEAP integration

## Components

### Simulation Setup

1. Geometry Configuration
   - Parallel beam setup
   - Cone beam setup
   - Source parameters
   - Detector configuration

2. Material Properties
   - Predefined materials
   - Custom material definition

3. Simulation Parameters
   - Number of projections
   - Energy settings
   - Time settings

### Reconstruction Setup

1. LEAP Configuration
   - Geometry selection
   - Volume parameters
   - Reconstruction algorithm selection

2. Processing Pipeline
   - Data conversion
   - Filtering options
   - Reconstruction parameters

### Visualization

1. 3D Scene View
   - Geometry preview
   - Interactive manipulation

2. Results Display
   - Sinogram visualization
   - Reconstruction preview
   - Slice viewers

## Data Flow

1. User Input → GUI
2. GUI → Simulation Configuration
3. Simulation → Raw Data
4. Raw Data → Reconstruction
5. Results → Visualization

## Technologies

1. GUI Framework Options:
   - PyQt/PySide6
   - Tkinter
   - Dear PyGui

2. Backend:
   - OpenGATE Python API
   - LEAP/leapctype
   - NumPy/SciPy for data processing
   - MayaVi for visualization
